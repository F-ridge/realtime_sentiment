# import os, sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time
import os
import sys
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json

from models.src.rnn.data.dataset_readers.reader import TwiReader
from models.src.rnn.model.model import RnnClassifier

from allennlp.predictors import Predictor
import models.src.rnn.predictor.predictor

from realtime_sentiment.src.streaming.streaming import input
from realtime_sentiment.src.output.output import output

model_path = 'models/serials/xxlarge-bin/model.tar.gz'
input_path = 'data/input.jsonl'
output_path = 'data/predict.jsonl'

predictor = Predictor.from_path(archive_path=model_path, predictor_name='sentiment', cuda_device=-1)

def main():
    # start = time.time()
    new_massage = input()
    if new_massage:
        with open(input_path, 'r') as f:
            json_lines = f.readlines()
        json_dicts = []
        for line in json_lines:
            json_dicts.append(predictor.load_line(line))
        output_dicts = predictor.batch_json_to_labeled_instances(json_dicts)
        for i in range(len(output_dicts)):
            del output_dicts[i]["text"]
        outputs = [repr(json.dumps(d).encode().decode('unicode-escape')).strip('\'') + '\n' for d in output_dicts]
        with open(output_path, 'w') as f:
            f.writelines(outputs)
        output()
        # elapsed_time = time.time() - start
        # print ("elapsed_time:{:.3f}".format(elapsed_time) + "[sec]")
    else:
        print("No new messages!")
        # elapsed_time = time.time() - start
        # print ("elapsed_time:{:.3f}".format(elapsed_time) + "[sec]")

if __name__ == '__main__':
    count = 0
    while True:
        print(count)
        main()
        count+=1
        time.sleep(5)
        if count == 3:
            break