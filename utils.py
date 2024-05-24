import pandas as pd
import torch
from keras.utils import to_categorical
from mappings import mappings, mappings_label, mappings_types

def format_output(target_df, predictions, predictions_df) -> pd.DataFrame:
    for i in range(len(predictions)):
        col1, col2 = target_df['type'][i], target_df['data'][i]
        sorted_indices = sorted(range(len(predictions[i])), key=lambda k: predictions[i][k], reverse=True)
        filtered_indices = [idx for idx in sorted_indices if predictions[i][idx] >= 0.3]
        predictions_str = ', '.join([f'{list(mappings_label.keys())[list(mappings_label.values()).index(idx+1)]} - {predictions[i][idx]:.4f}' for idx in filtered_indices])
        predictions_df = predictions_df.append({
            'type': col1,
            'data': col2,
            'prediction': predictions_str
        }, ignore_index=True)
        return predictions_df

def one_hot_encode(text, num_classes=15):
    one_hot = to_categorical(text, num_classes=num_classes)
    return one_hot

def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()
