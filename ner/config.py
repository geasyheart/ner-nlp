# -*- coding: utf8 -*-
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

VOCAB_PATH = os.path.join(CUR_DIR, "data/vocab.txt")

DATA_DIR = os.path.join(CUR_DIR, "data")

MSRA_DIR = os.path.join(CUR_DIR, "data/MSRA/")
MSRA_PATH = os.path.join(MSRA_DIR, "train1.txt")


BERT_PRE_TRAIN_PATH = os.path.join(CUR_DIR, "data/chinese_L-12_H-768_A-12")
