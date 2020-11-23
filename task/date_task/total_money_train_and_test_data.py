# -*- coding: utf8 -*-

import os

import pandas as pd

from task.config import DATA_DIR
from task.utils import word2index


class TotalMoneyDataProcess(object):
    def __init__(self, max_len: int = 128):
        self.proportion()
        self.word2index = word2index()
        self.max_len = max_len

        self.cls_char = '[CLS]'
        self.sep_char = '[SEP]'
        self.pad_char = '[PAD]'
        self.unk_char = '[UNK]'
        self.cls_index = self.word2index[self.cls_char]
        self.sep_index = self.word2index[self.sep_char]
        self.pad_index = self.word2index[self.pad_char]
        self.unk_index = self.word2index[self.unk_char]

    def proportion(self):
        """
        查看一下数据的长度分布情况

        75%       81.000000
        :return:
        """
        p = {}
        with open(os.path.join(DATA_DIR, 'total_money.txt'), 'r') as f:
            for line in f:
                data, mark = line.strip().split('^$$^')
                data_len = len(data)
                p[data] = data_len

        df = pd.DataFrame(p.items(), columns=("text", "text_len"))
        print(df.describe())

    def to_file(self):
        final_data_as_np, final_labels_as_np = [], []
        with open(os.path.join(DATA_DIR, 'total_money.txt'), 'r') as f:
            for line in f:
                data, label = line.strip().split('^$$^')
                if not isinstance(data, str):
                    continue
                data = data.replace(" ", "")

                start_index = data.find(label)
                if start_index == -1:
                    continue
                end_index = start_index + len(label)

                tmp_label = []
                for _index, _label in enumerate(data):
                    if _index == start_index:
                        tmp_label.append('B-MONEY')
                    elif start_index < _index < end_index:
                        tmp_label.append('I-MONEY')
                    else:
                        tmp_label.append('O')
                final_data_as_np.append(list(data))
                final_labels_as_np.append(tmp_label)

            to_file = zip(final_data_as_np, final_labels_as_np)

            for index, (d, l) in enumerate(to_file):
                with open(os.path.join(DATA_DIR, "all_total_money.txt"), "a+") as f:
                    newline = "\n".join([" ".join(line) for line in zip(d, l)])
                    f.write(newline)
                    f.write("\n\n")


if __name__ == '__main__':
    t = TotalMoneyDataProcess()
    t.to_file()
