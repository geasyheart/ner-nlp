# -*- coding: utf8 -*-
import os

from task.config import BERT_PRETRAIN_PATH


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
