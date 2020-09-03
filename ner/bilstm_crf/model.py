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

    def predict(self):
        y = self.model.predict(self.test_data)

        label_indexs = []
        pridict_indexs = []

        num2tag = self.dp.i2tag()
        i2w = self.dp.i2w()
        texts = []
        texts.append(f"字符\t预测tag\t原tag\n")
        for i, x_line in enumerate(self.test_data):
            # x_line: [0, 0, 2769, 1762, 704, 1744]
            for j, index in enumerate(x_line):
                # 这里不会有index为0的情况
                if index != 0:
                    char = i2w.get(index, ' ')
                    t_line = y[i]  # 获取这一行的one hot编码
                    # t_line[j] 对应那一个index对应的one hot编码
                    # t_line[j] [0, 0, 0, 0, 0, 0, 1]
                    t_index = np.argmax(t_line[j])
                    tag = num2tag.get(t_index, 'O')
                    pridict_indexs.append(t_index)

                    t_line = self.onehot_test_label[i]
                    t_index = np.argmax(t_line[j])
                    org_tag = num2tag.get(t_index, 'O')
                    label_indexs.append(t_index)

                    texts.append(f"{char}\t{tag}\t{org_tag}\n")
            texts.append('\n')

        f1score = f1_score(label_indexs, pridict_indexs, average='macro')
        print(f"f1score:{f1score}")


if __name__ == '__main__':
    bilstm_crf = BILSTMCRF()
    bilstm_crf.train()
    bilstm_crf.predict()
