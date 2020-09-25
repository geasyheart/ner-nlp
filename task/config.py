# -*- coding: utf8 -*-
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TRAIN_DATA_PATH = os.path.join(DATA_DIR, "时间空间指向训练数据总表-0425.xlsx")

BERT_PRETRAIN_PATH: str = os.path.join(DATA_DIR, "chinese_L-12_H-768_A-12")
