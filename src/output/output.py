import os
import yaml
import pandas as pd
from realtime_sentiment.lib.auth import google_spreadsheet_auth
from realtime_sentiment.lib.spread_sheet import update_values_by_range


def output(service):
    # service = google_spreadsheet_auth()
    service = service
    predict_path = os.path.join(os.path.dirname(__file__),'../../data/predict.jsonl')
    with open(predict_path) as jsonl:
        predict_jsonl = jsonl.read()
    post_labels(service, predict_jsonl)


def post_labels(
        service, predict_jsonl,
        config_path=os.path.join(os.path.dirname(__file__),'../../config.yml'),
        sheet_name='シート1'):
    with open(config_path, 'r', encoding='UTF-8') as yml:
        config = yaml.safe_load(yml)
    sheet_id = config['sheet_id']
    predict_df = pd.read_json(predict_jsonl, orient='records', lines=True)
    row_start = predict_df['id'].min() + 2
    row_end = predict_df['id'].max() + 2
    labels = predict_df.label.values.reshape(-1, 1).tolist()
    update_values_by_range(
        service, sheet_id, labels,
        'C', row_start, 'C', row_end,
        majorDimension=None, sheet_name='シート1')

