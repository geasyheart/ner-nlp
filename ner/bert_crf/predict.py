# -*- coding: utf8 -*-
import os
import numpy as np

from keras.engine.saving import load_model
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy

from ner.bert_crf.data_preprocess import DataProcess
from ner.config import DATA_DIR
from keras_bert import get_custom_objects

import ipdb


class Predict(object):
    def __init__(self):
        self.dp = DataProcess()
        self.abs_path = os.path.join(
            DATA_DIR,
            "bert_ner.h5"
        )
        c = get_custom_objects()
        c.update({
            "CRF": CRF,
            'crf_loss': crf_loss,
            'crf_viterbi_accuracy': crf_accuracy
        })
        self.model = load_model(self.abs_path, custom_objects=c)

    def predict(self):
        train_data, train_label, test_data, test_label = self.dp.get_data(one_hot=True)
        ipdb.set_trace()
        #result = self.model.predict(test_data)
        #print("here")
        
    def predict_sentence(self, sentence):
        num2tag = self.dp.i2tag()
        i2w = self.dp.i2w()
        data = self.dp.to_index(sentence)
        y = self.model.predict(data)

        x_line = data[0][0]
        t_line = y[0]
        chars, tags = [], []
        for i, index in enumerate(x_line):
            if index == self.dp.pad_index:
                continue
            char = i2w.get(index, " ")
            t_index = np.argmax(t_line[i])
            tag = num2tag.get(t_index, " ")
            chars.append(char)
            tags.append(tag)

        ipdb.set_trace()

if __name__ == '__main__':
    p = Predict()
    #p.predict()
    p.predict_sentence("我在马来西亚")

