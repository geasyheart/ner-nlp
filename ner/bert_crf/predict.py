# -*- coding: utf8 -*-
from keras.backend import backend
from keras.engine.saving import load_model
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy, crf_accuracy

from ner.bert_crf.data_preprocess import DataProcess
from ner.config import DATA_DIR
import os
from keras_bert import get_custom_objects
import tensorflow as tf
import ipdb

path = os.path.join(DATA_DIR, "bert_crf.h5")

bert_custom = get_custom_objects()
custom_objects = {
    "tf": tf, "backend": backend,
    'CRF': CRF,
    'crf_loss': crf_loss,
    'crf_accuracy': crf_accuracy
}
custom_objects.update(bert_custom)

ner_model = load_model(path, custom_objects=custom_objects)

dp = DataProcess()
train_data, train_label, test_data, test_label = dp.get_data(one_hot=True)
ipdb.set_trace()
print("here")
