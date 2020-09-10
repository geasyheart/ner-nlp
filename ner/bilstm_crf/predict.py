# -*- coding: utf8 -*-
import os

import numpy as np
from keras.engine.saving import load_model
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from sklearn.metrics import f1_score

from ner.bilstm_crf.data_preprocess import DataProcess
from ner.config import DATA_DIR


class Predict(object):
    def __init__(self):
        self.dp = DataProcess(max_len=100)
        self.abs_path = os.path.join(
            DATA_DIR,
            "bilstm_crf.h5")
        custom_objects = {
            "CRF": CRF,
            'crf_loss': crf_loss,
            'crf_viterbi_accuracy': crf_viterbi_accuracy
        }
        self.model = load_model(self.abs_path, custom_objects=custom_objects)

    def predict(self, word):

        num2tag = self.dp.i2tag()
        i2w = self.dp.i2w()

        sentence_index = self.dp.sentence(word)
        y = self.model.predict(sentence_index)

        x_line = sentence_index[0]
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
        return chars, tags

    def score(self):
        num2tag = self.dp.i2tag()
        i2w = self.dp.i2w()

        train_data, train_label, test_data, test_label = self.dp.get_data()
        y = self.model.predict(test_data)
        label_indexs, predict_indexs = [], []
        for i, x_line in enumerate(test_data):
            for j, index in enumerate(x_line):
                char = i2w.get(index, " ")
                t_line = y[i]
                t_index = np.argmax(t_line[j])
                tag = num2tag.get(t_index, "O")

                predict_indexs.append(t_index)

                t_line = test_label[i]
                t_index = np.argmax(t_line[j])
                ori_tag = num2tag.get(t_index, "O")
                label_indexs.append(t_index)
        f1score = f1_score(label_indexs, predict_indexs, average='macro')
        print(f"f1score:{f1score}")


if __name__ == '__main__':
    predict = Predict()
    predict.score()
    #chars, tags = predict.predict("我在缅甸")
    #print(chars, tags)

