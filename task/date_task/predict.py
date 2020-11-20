# -*- coding: utf8 -*-
import os

import numpy as np

from task.config import DATA_DIR
from task.date_task.model import BERTBILSTMCRF


class Predict(object):
    def __init__(self):
        self.bert_ner = BERTBILSTMCRF()

        self.abs_path = os.path.join(
            DATA_DIR,
            "time_bert_ner.h5"
        )

        self.model = self.bert_ner.get_model()
        self.model.load_weights(filepath='/home/yuzhang/PycharmProjects/ner-nlp/task/data/model_02.hdf5')

        self.num2tag = self.bert_ner.dp.i2tag()
        self.i2w = self.bert_ner.dp.i2w()

    def predict_sentence(self, sentence):
        data = self.bert_ner.dp.to_index(sentence)
        y = self.model.predict(data)

        x_line = data[0][0]
        t_line = y[0]
        chars, tags = [], []
        for i, index in enumerate(x_line):
            if index == self.bert_ner.dp.pad_index:
                continue
            char = self.i2w.get(index, " ")
            t_index = np.argmax(t_line[i])
            tag = self.num2tag.get(t_index, " ")
            chars.append(char)
            tags.append(tag)

        print(chars)
        print(tags)


if __name__ == '__main__':
    p = Predict()
    # p.score()
    # p.predict_sentence("南京联著创建于1990年2月")
    # p.predict_sentence("每月8日为发薪日")
    p.predict_sentence('2020年11月1日我在南京看电影')
    p.predict_sentence('今天2020年11月1日')
    p.predict_sentence('我在南京看电影')
