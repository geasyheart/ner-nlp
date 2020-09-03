# -*- coding: utf8 -*-
from ner.config import VOCAB_PATH


def get_w2i():
    """
    获取word to index词典
    :return:
    """
    w2i = {}

    with open(VOCAB_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            w2i[line] = len(w2i) + 1

    return w2i


def get_tag2index():
    """
    获取 tag
    :return:
    """
    return {
        "O": 0,
        "B-PER": 1, "I-PER": 2,
        "B-LOC": 3, "I-LOC": 4,
        "B-ORG": 5, "I-ORG": 6
    }


if __name__ == '__main__':
    get_w2i()
