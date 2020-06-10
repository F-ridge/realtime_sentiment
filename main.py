import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import time

from realtime_sentiment.src.streaming import streaming
from realtime_sentiment.src.output import output


from realtime_sentiment.models.src.rnn.data.dataset_readers.reader import TwiReader
from realtime_sentiment.models.src.rnn.model.model import RnnClassifier
from allennlp.predictors import Predictor

model_path = 'realtime_sentiment/models/serials/xxlarge-bin/model.tar.gz'
input_path = 'realtime_sentiment/data/input.jsonl'
output_path = 'realtime_sentiment/data/predict.jsonl'

predictor = Predictor.from_path(archive_path=model_path, predictor_name='sentiment', cuda_device=-1)

def main():
    # start = time.time()
    new_massage = streaming()
    if new_massage:
        with open(input_path, 'r') as f:
            json_lines = f.readlines()
        json_dicts = []
        for line in json_lines:
            json_dicts.append(predictor.load_line(line))
        output_dicts = predictor.batch_json_to_labeled_instances(json_dicts)
        outputs = [repr(json.dumps(d).encode().decode('unicode-escape')).strip('\'') + '\n' for d in output_dicts]
        with open(output_path, 'w') as f:
            f.writelines(outputs)
        # output()
        # elapsed_time = time.time() - start
        # print ("elapsed_time:{:.3f}".format(elapsed_time) + "[sec]")
    else:
        print("No new messages!")
        # elapsed_time = time.time() - start
        # print ("elapsed_time:{:.3f}".format(elapsed_time) + "[sec]")

if __name__ == '__main__':
    main()