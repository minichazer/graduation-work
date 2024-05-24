import numpy as np
import pandas as pd
import os
import warnings
from utils import format_output, one_hot_encode, embed_bert_cls
from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
from transformers import BertTokenizer, BertModel
import argparse


parser = argparse.ArgumentParser(description='Process input data')
parser.add_argument('--data', type=str, required=True, help='Input data')
parser.add_argument('--type', type=str, required=True, help='Input data type')

args = parser.parse_args()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
warnings.simplefilter(action='ignore', category=FutureWarning)

tokenizer = BertTokenizer.from_pretrained(
    'google-bert/bert-base-uncased', 
    return_attention_mask=False,
    return_token_type_ids=False
)
model_bert = BertModel.from_pretrained('google-bert/bert-base-uncased')
model = load_model('models\\128_nadam_2drop.h5')
lb = LabelEncoder()

target_df = pd.DataFrame(columns=['type', 'data'])

# TODO: тип данных позже сделать текстовым представлением, а не векторным
target_df = target_df.append({
    'data': args.data,
    'type': args.type,
}, ignore_index=True)
# TODO: поменять временное решение на нормальное
source_df = target_df.copy()

# TODO: вынести предобработку в отдельную функцию
target_df['type'] = lb.fit_transform(target_df['type'])
target_df['type'] = target_df['type'].apply(one_hot_encode)
target_df['data'] = target_df['data'].apply(lambda x: embed_bert_cls(x, model_bert, tokenizer))

data_eval = np.stack(target_df['data'].values)
type_eval = np.stack(target_df['type'].values)
type_eval = np.zeros((type_eval.shape[0], 255), dtype=np.float32)
type_eval[:, :type_eval.shape[1]] = type_eval

predictions = model.predict(
    {
        'i_type': type_eval,
        'i_data': data_eval
    })
predictions_df = pd.DataFrame(columns=['type', 'data', 'prediction'])
result = format_output(source_df, predictions, predictions_df)

print(result)