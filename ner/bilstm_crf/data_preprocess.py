# -*- coding: utf8 -*-
import os

import numpy as np
from keras.utils import to_categorical

from ner.config import MSRA_DIR
from ner.msra_preprocessing import msra_preprocessing
from ner.vocab import get_w2i, get_tag2index


class DataProcess(object):
    def __init__(
            self,
            max_len: int = 100,
    ):
        """
        句子最长的长度，默认为100
        :param max_len:
        """
        self.w2i = get_w2i()  # vocab to index
        self.tag2i = get_tag2index()  # tag to index
        self.vocab_size = len(self.w2i)
        self.tag_size = len(self.tag2i)
        self.max_len = max_len
        self.unk_flag = '[UNK]'
        self.pad_flag = '[PAD]'
        self.cls_flag = '[CLS]'
        self.sep_flag = '[SEP]'
        self.unk_index = self.w2i[self.unk_flag]
        self.pad_index = self.w2i[self.pad_flag]
        self.cls_index = self.w2i[self.cls_flag]
        self.sep_index = self.w2i[self.sep_flag]

        msra_preprocessing()

    def get_data(self):
        train_path = os.path.join(MSRA_DIR, "train.txt")
        test_path = os.path.join(MSRA_DIR, "test.txt")

        train_data, train_label = self.text_to_indexes(train_path)
        test_data, test_label = self.text_to_indexes(test_path)

        # 转成one-hot
        def to_one_hot(label):
            y = np.empty(
                shape=(
                    len(label),
                    self.max_len,
                    self.tag_size
                )
            )
            for i, seq in enumerate(label):
                y[i, :, :] = to_categorical(seq, num_classes=self.tag_size)
            return y

        onehot_train_label = to_one_hot(train_label)
        onehot_test_label = to_one_hot(test_label)
        return train_data, onehot_train_label, test_data, onehot_test_label

    def text_to_indexes(self, file_path: str):
        """
        1. 转成index
        2. 补齐
        :param file_path:
        :return:
        """
        data, label = [], []
        with open(file_path, 'r') as f:
            line_data, line_label = [], []
            for line in f:
                if line != '\n':
                    w, t = line.split()
                    char_index = self.w2i.get(w, self.unk_index)
                    tag_index = self.tag2i.get(t, 0)
                    line_data.append(char_index)
                    line_label.append(tag_index)
                else:
                    if len(line_data) < self.max_len:
                        pad_num = self.max_len - len(line_data)
                        line_data = [self.pad_index] * pad_num + line_data
                        line_label = [0] * pad_num + line_label
                    else:
                        line_data = line_data[:self.max_len]
                        line_label = line_label[:self.max_len]
                    data.append(line_data)
                    label.append(line_label)
                    line_data, line_label = [], []
        return np.array(data), np.array(label)

    def i2tag(self):
        return {
            value: key for key, value in self.tag2i.items()
        }

    def i2w(self):
        return {
            value: key for key, value in self.w2i.items()
        }

    def sentence(self, word):
        line_data = []
        for char in word:
            char_index = self.w2i.get(char, self.unk_index)
            line_data.append(char_index)
        if len(line_data) < self.max_len:
            pad_num = self.max_len - len(line_data)
            line_data = [self.pad_index] * pad_num + line_data
        else:
            line_data = line_data[:self.max_len]
        line_data = np.array([line_data])
        return line_data


if __name__ == '__main__':
    d = DataProcess()

