import base64
import uuid
import pandas as pd
import typing
import random
import datetime
import os
from faker import Faker
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding


class AESCipher(object):

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        # print(f'Шифруем {raw} с помощью своего ключа {self.key}...')
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(
            Padding.pad(raw.encode(), AES.block_size)
        )
        result = base64.b64encode(cipher.nonce + tag + ciphertext)
        # print(f'Зашифрованные данные (имя) с использование GCM режима AES шифрования: {result}\n')
        return result

    def decrypt(self, enc):
        # print(f'Расшифровываем {enc} с помощью своего ключа {self.key}...')
        enc = base64.b64decode(enc)
        nonce = enc[:16]
        tag = enc[16:32]
        ciphertext = enc[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        decrypted_data = Padding.unpad(
            cipher.decrypt_and_verify(ciphertext, tag), AES.block_size
        )
        result = decrypted_data.decode("utf-8")
        # print(f'Расшифрованные данные (имя) с использование GCM режима AES шифрования: {result}\n')
        return result


class DataAnonymizer:

    def __init__(self, key):
        self.key = key
        self.cipher = AESCipher(self.key)
        self.db = pd.DataFrame(columns=["uuid", "source_encrypted", "data"])
        self.fake = Faker(locale="ru_RU")

    def anonymize(self, data):
        seed = os.urandom(16)
        Faker.seed(seed)
        new_data = self.fake.name_male()
        # print(f'Генерируем новое ФИО, используя случайный seed ({seed})...\nНовое имя: {new_data}')
        source_encrypted = self.cipher.encrypt(data)
        uuid_ = uuid.uuid4()
        new_row = pd.DataFrame(
            [[uuid_, source_encrypted, new_data]],
            columns=["uuid", "source_encrypted", "data"],
        )
        self.db = pd.concat([self.db, new_row], ignore_index=True)
        # print(f'В БД добавляется новая запись: {uuid_} | {source_encrypted} | {new_data}\n')
        return new_data

    def deanonymize(self, data, uuid_=None):
        if uuid_ is None:
            res = self.db[self.db["data"] == data]
            if len(res) == 0:
                return None
            uuid_ = res.iloc[0]["uuid"]

        # print(f'Делаю запрос в БД, пытаюсь найти исходные данные по ключу uuid ({uuid_})...')

        res = self.db[self.db["uuid"] == uuid_]
        if len(res) == 0:
            return None
        source_encrypted = res.iloc[0]["source_encrypted"]

        # print(f'По значениям ключей нашёл зашифрованные данные: {source_encrypted}\n')

        decrypted_data = self.cipher.decrypt(source_encrypted)
        return decrypted_data


key = Random.new().read(16)
anonymizer = DataAnonymizer(key)

target = "Даничкин Антон Сергеевич"
print(f"Исходное имя: {target}")

anonymized_name = anonymizer.anonymize(target)
# print(f"Обезличенное имя: {anonymized_name}")

deanonymized_name = anonymizer.deanonymize(anonymized_name)
# print(f"Деобезличенное имя: {deanonymized_name}")


def gen_FIO(target: str, fake: Faker) -> str:
    Faker.seed(os.urandom(16))
    return fake.name_male()


def mask_phone(target: str) -> typing.Union[str, int]:
    return target[:2] + "*" * (len(target) - 2)


def obfuscate_address(address: str) -> str:
    address_parts = address.split(",")
    num_parts_to_obfuscate = random.randint(1, len(address_parts))
    address_parts = address_parts[:num_parts_to_obfuscate]
    return address_parts


def anonymize_date(dt: str) -> str:
    parts = dt.split("-")
    parts[0], parts[1], parts[2] = int(parts[0]), int(parts[1]), int(parts[2])
    ssd = datetime.datetime(parts[2], parts[1], parts[0])
    start_date = datetime.datetime(
        parts[2], abs(parts[1] - 1 % 12), abs(parts[0] - 28 % 12)
    )
    end_date = datetime.datetime(
        parts[2], abs(parts[1] + 1 % 12), abs(parts[0] - 28 % 12)
    )
    time_between_dates = end_date - start_date
    days_between = random.randint(0, time_between_dates.days)

    rdt = ssd + datetime.timedelta(days=days_between)
    return rdt.strftime("%d-%m-%Y")


fake = Faker(locale="ru_RU")


target_name = "Даничкин Антон Сергеевич"
print(
    f"Анонимизация имени\nИсходные данные: {target}\nПолученные данные: {gen_FIO(target_name, fake)}\n"
)

target_address = "клх Диксон, ш. Толстого, д. 4/6 к. 6/9, 324855"
print(
    f'Обобщение адреса\nИсходные данные: {target_address}\nПолученные данные: {", ".join(obfuscate_address(target_address))}\n'
)

target_date = "22-11-1999"
print(
    f"Анонимизация даты\nИсходные данные: {target_date}\nПолученные данные: {anonymize_date(target_date)}\n"
)
