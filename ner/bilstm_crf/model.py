# -*- coding: utf8 -*-
from keras import Input, Model
from keras.layers import Bidirectional, LSTM, Dropout, TimeDistributed, Dense, Embedding
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from sklearn.metrics import f1_score

from ner.bilstm_crf.data_preprocess import DataProcess
import numpy as np


class BILSTMCRF(object):
    def __init__(self):
        self.dp = DataProcess(max_len=100)
        self.train_data, self.onehot_train_label, self.test_data, self.onehot_test_label = self.dp.get_data()

        self.model = self.create_model()

    def create_model(self):
        inputs = Input(shape=(None,))
        x = Embedding(input_dim=self.dp.vocab_size, output_dim=128)(inputs)
        x = Bidirectional(LSTM(units=128, return_sequences=True))(x)
        x = Dropout(0.5)(x)
        x = TimeDistributed(Dense(self.dp.tag_size,  activation="softmax"))(x)
        crf = CRF(self.dp.tag_size)
        x = crf(x)
        model = Model(inputs=inputs, outputs=x)
        model.summary()
        model.compile('adam',
                      loss=crf_loss,
                      metrics=[crf_viterbi_accuracy])

        return model

    def train(self):

        self.model.fit(
            self.train_data,
            self.onehot_train_label,
            batch_size=64,
            epochs=15,
            validation_data=[self.test_data, self.onehot_test_label]
        )
        self.model.save("bilstm_crf.h5")
        self.model.save("bilstm_crf_weight.h5")


if __name__ == '__main__':
    bilstm_crf = BILSTMCRF()
    bilstm_crf.train()
