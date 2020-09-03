# -*- coding: utf8 -*-
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(CUR_DIR, "data")
VOCAB_PATH = os.path.join(DATA_DIR, "vocab.txt")

MSRA_DIR = os.path.join(DATA_DIR, "MSRA/")
MSRA_PATH = os.path.join(MSRA_DIR, "train1.txt")


BERT_PRE_TRAIN_PATH = os.path.join(DATA_DIR, "chinese_L-12_H-768_A-12")