# coding:utf-8
"""
采用 BERT + BILSTM + CRF 网络进行处理
"""

import os

import keras_bert
from keras.layers import Bidirectional, LSTM, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras_contrib.layers import CRF

from task.config import BERT_PRETRAIN_PATH
from task.date_task.data_preprocess import DataProcess


class BERTBILSTMCRF(object):
    def __init__(
            self,

    ):
        self.dp = DataProcess()
        self.n_class = self.dp.tag_size

    def get_model(self):
        """
        bert+crf 和 bert+softmax模型 按理说crf效果会更好，但是对比结果基本没有太大区别，这篇文章给出来一个比较合理的解释：
        https://zhuanlan.zhihu.com/p/106654565
        :return:
        """
        bert_model = keras_bert.load_trained_model_from_checkpoint(
            os.path.join(BERT_PRETRAIN_PATH, 'bert_config.json'),
            checkpoint_file=os.path.join(BERT_PRETRAIN_PATH, 'bert_model.ckpt'),
            seq_len=128,
            trainable=True
        )

        # x = Bidirectional(LSTM(units=128, return_sequences=True))(bert_model.output)
        x = Dropout(0.3)(bert_model.output)
        # x = Dense(self.n_class)(x)
        crf = CRF(self.n_class, sparse_target=False)
        x = crf(x)
        model = Model(inputs=bert_model.inputs, outputs=x)
        model.summary()

        self.model = model
        self.crf = crf
        return model

    def compile(self):
        self.model.compile(
            optimizer=Adam(1e-5),
            loss=self.crf.loss_function,
            metrics=[self.crf.accuracy]
        )
