# -*- coding: utf8 -*-
import os

import numpy as np

from task.config import BERT_PRETRAIN_PATH


def train_test_split(data, label, size=0.75):
    """
    train_data, test_data, train_label, test_label
    :param data:
    :param label:
    :param size:
    :return:
    """
    np.random.seed(321)
    train_size = int(size * data.shape[0])

    indices = np.random.permutation(data.shape[0])
    train_idx, test_idx = indices[:train_size], indices[train_size:]
    result = []
    result += [data.take(train_idx, axis=0), data.take(test_idx, axis=0)]
    result += [label.take(train_idx, axis=0), label.take(test_idx, axis=0)]
    return tuple(result)


def word2index():
    d = dict()
    vocab_path = os.path.join(BERT_PRETRAIN_PATH, "vocab.txt")
    with open(vocab_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d[line] = len(d) + 1  # escape 0

    return d


if __name__ == '__main__':
    word2index()

