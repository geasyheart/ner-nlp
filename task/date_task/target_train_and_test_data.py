# -*- coding: utf8 -*-
# 指向
# -*- coding: utf8 -*-


import os
import random
import time
from datetime import datetime

import pandas as pd

from task.config import TRAIN_DATA_PATH, DATA_DIR
from task.utils import word2index


class TargetDataProcess(object):
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

    @property
    def target_df(self):
        return pd.read_excel(TRAIN_DATA_PATH, sheet_name="指向").fillna("")

    def proportion(self):
        """
        查看一下数据的长度分布情况

        75%       90.000000
        :return:
        """
        p = {}
        for index, row in self.target_df.iterrows():
            data = str(row['原文'])
            data_len = len(data)
            p[data] = data_len

        df = pd.DataFrame(p.items(), columns=("text", "text_len"))
        print(df.describe())

    def to_file(self):
        final_data_as_np, final_labels_as_np = [], []

        for index, row in self.target_df.iterrows():
            data = row['原文']
            if not isinstance(data, str):
                continue
            data = data.replace(" ", "")
            labels = [str(value).strip() for key, value in row.items() if
                      key not in ("编号", "原文") and str(value).strip()]

            for label in labels:
                start_index = data.find(label)
                if start_index == -1:
                    continue
                end_index = start_index + len(label)

                tmp_label = []
                for _index, _label in enumerate(data):
                    if _index == start_index:
                        tmp_label.append('B-TGT')
                    elif start_index < _index < end_index:
                        tmp_label.append('I-TGT')
                    else:
                        tmp_label.append('O')
                final_data_as_np.append(list(data))
                final_labels_as_np.append(tmp_label)

        to_file = zip(final_data_as_np, final_labels_as_np)
        length = len(final_data_as_np)
        train_length = int(length * 0.8)
        for index, (d, l) in enumerate(to_file):
            with open(os.path.join(DATA_DIR, "union_train_data.txt"), "a+") as f:
                newline = "\n".join([" ".join(line) for line in zip(d, l)])
                f.write(newline)
                f.write("\n\n")
        # for index, (d, l) in enumerate(to_file):
        #     if index <= train_length:
        #         with open(os.path.join(DATA_DIR, "tgt_train_data.txt"), "a+") as f:
        #             newline = "\n".join([" ".join(line) for line in zip(d, l)])
        #             f.write(newline)
        #             f.write("\n\n")
        #     else:
        #         with open(os.path.join(DATA_DIR, "tgt_test_data.txt"), "a+") as f:
        #             newline = "\n".join([" ".join(line) for line in zip(d, l)])
        #             f.write(newline)
        #             f.write("\n\n")


if __name__ == '__main__':
    s = TargetDataProcess()
    s.to_file()
