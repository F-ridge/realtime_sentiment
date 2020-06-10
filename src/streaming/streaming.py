import os
import yaml
from realtime_sentiment.lib.converters import save_dir
from realtime_sentiment.lib.auth import google_spreadsheet_auth
from realtime_sentiment.lib.spread_sheet import (
    get_sheet_as_df, update_values_by_range)


def streaming():
    service = google_spreadsheet_auth()
    target_jsonl = get_new_comments(service)
    # with open(f"{save_dir('streaming/example')}/output.jsonl", mode='w') as j:
    #     j.write(target_jsonl)
    if target_jsonl is None:
        return 0
    with open(os.path.join(os.path.dirname(__file__),'../../data/input.jsonl'), "w") as f:
        for _, row in target_jsonl.iterrows():
            f.write(f'{{"id":{int(row[0])},"text":"{row[1]}"}}\n')
    return 1

def get_new_comments(
        service,
        config_path=os.path.join(os.path.dirname(__file__),'../../config.yml'), 
        sheet_name='シート1'):
    with open(config_path, 'r', encoding='UTF-8') as yml:
        config = yaml.safe_load(yml)
    sheet_id = config['sheet_id']
    target_sheet = get_sheet_as_df(service, sheet_id, sheet_name)
    target_records = target_sheet[
        target_sheet.is_taken.astype(str, errors='ignore') != '1']
    if len(target_records) == 0:
        return None
    else:
        target_ids = target_records.id.astype(int)
        mark_taken_records(service, target_ids, sheet_id, sheet_name)
        # target_jsonl = target_records[['id', 'text']].to_json(
        #     orient='records', force_ascii=False, lines=True)
        # return target_jsonl
        target_df = target_records[['id', 'text']]
        return target_df


def mark_taken_records(
        service, target_ids, sheet_id, sheet_name='シート1'):
    range_start = min(target_ids) + 2
    range_end = max(target_ids) + 2
    values = [[1]] * (range_end - range_start + 1)
    update_values_by_range(
        service, sheet_id, values,
        'D', range_start, 'D', range_end)