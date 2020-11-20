# -*- coding: utf8 -*-
import os
import random
import time
from datetime import datetime

import pandas as pd

from task.config import TRAIN_DATA_PATH, DATA_DIR
from task.utils import word2index


class DateDataProcess(object):
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
    def date_df(self):
        return pd.read_excel(TRAIN_DATA_PATH, sheet_name="时间").fillna("")

    def proportion(self):
        """
        查看一下数据的长度分布情况
        :return:
        """
        p = {}
        for index, row in self.date_df.iterrows():
            data = str(row['原文'])
            data_len = len(data)
            p[data] = data_len

        df = pd.DataFrame(p.items(), columns=("text", "text_len"))
        print(df.describe())
        # 82个长度的大致占了75%，所以此处max_len直接设置成128

    def to_file(self):
        final_data_as_np, final_labels_as_np = [], []
        for index, row in self.date_df.iterrows():
            data = row['原文']
            if not isinstance(data, str):
                continue
            data = data.replace(" ", "")
            labels = [value.strip() for key, value in row.items() if
                      key not in ("Unamed", "编号", "原文") and value.strip()]

            rd = self.random_date()

            fmt_data = data.replace(
                "##年", f"{rd.year}年"
            ).replace(
                "##月", f"{rd.month}月"
            ).replace(
                "##日", f"{rd.day}日"
            ).replace(" ", "")

            fmt_labels = [
                data.replace(
                    "#n#年", f"{rd.year}年"
                ).replace(
                    "#y#月", f"{rd.month}月"
                ).replace(
                    "#r#日",
                    f"{rd.day}日"
                ).replace(
                    "#t#年", f"{rd.year}年"
                )
                for data in labels
            ]
            for fmt_label in fmt_labels:
                start_index = fmt_data.find(fmt_label)
                if start_index == -1:
                    continue
                end_index = start_index + len(fmt_label)

                tmp_label = []
                for _index, _label in enumerate(fmt_data):
                    if _index == start_index:
                        tmp_label.append('B-TIME')
                    elif start_index < _index < end_index:
                        tmp_label.append('I-TIME')
                    else:
                        tmp_label.append('O')

                final_data_as_np.append(list(fmt_data))
                final_labels_as_np.append(tmp_label)

        to_file = zip(final_data_as_np, final_labels_as_np)
        length = len(final_data_as_np)
        train_length = int(length * 0.8)
        for index, (d, l) in enumerate(to_file):
            with open(os.path.join(DATA_DIR, "union_train_data.txt"), "a+") as f:
                newline = "\n".join([" ".join(line) for line in zip(d, l)])
                f.write(newline)
                f.write("\n\n")

            # if index <= train_length:
            #     with open(os.path.join(DATA_DIR, "time_train_data.txt"), "a+") as f:
            #         newline = "\n".join([" ".join(line) for line in zip(d, l)])
            #         f.write(newline)
            #         f.write("\n\n")
            # else:
            #     with open(os.path.join(DATA_DIR, "time_test_data.txt"), "a+") as f:
            #         newline = "\n".join([" ".join(line) for line in zip(d, l)])
            #         f.write(newline)
            #         f.write("\n\n")

    def random_date(self):
        d = random.randint(1, int(time.time()))
        return datetime.fromtimestamp(d)


if __name__ == '__main__':
    p = DateDataProcess()
    p.to_file()
