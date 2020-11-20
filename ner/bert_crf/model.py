"""
采用 BERT + BILSTM + CRF 网络进行处理
"""

import os

import keras_bert
from keras.layers import Bidirectional, LSTM, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras_contrib.layers import CRF

from ner.bert_crf.data_preprocess import DataProcess
from ner.config import BERT_PRE_TRAIN_PATH, DATA_DIR


class BERTBILSTMCRF(object):
    def __init__(self,
                 vocab_size: int,
                 n_class: int,
                 max_len: int = 100,
                 embedding_dim: int = 128,
                 rnn_units: int = 128,
                 drop_rate: float = 0.5,
                 ):
        self.vocab_size = vocab_size
        self.n_class = n_class
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        self.rnn_units = rnn_units
        self.drop_rate = drop_rate
        self.config_path = os.path.join(BERT_PRE_TRAIN_PATH, 'bert_config.json')
        self.check_point_path = os.path.join(BERT_PRE_TRAIN_PATH, 'bert_model.ckpt')
        self.dict_path = os.path.join(BERT_PRE_TRAIN_PATH, 'vocab.txt')

    def creat_model(self):
        print('load bert Model start!')
        model = keras_bert.load_trained_model_from_checkpoint(self.config_path,
                                                              checkpoint_file=self.check_point_path,
                                                              seq_len=self.max_len,
                                                              trainable=True)
        print('load bert Model end!')
        inputs = model.inputs
        embedding = model.output
        x = Bidirectional(LSTM(units=self.rnn_units, return_sequences=True))(embedding)
        x = Dropout(self.drop_rate)(x)
        x = Dense(self.n_class)(x)
        self.crf = CRF(self.n_class, sparse_target=False)
        x = self.crf(x)
        self.model = Model(inputs=inputs, outputs=x)
        self.model.summary()
        self.compile()

        return self.model

    def compile(self):
        self.model.compile(optimizer=Adam(1e-5),
                           loss=self.crf.loss_function,
                           metrics=[self.crf.accuracy])


if __name__ == '__main__':
    dp = DataProcess()
    train_data, train_label, test_data, test_label = dp.get_data(one_hot=True)
    
    md = BERTBILSTMCRF(vocab_size=dp.vocab_size, n_class=dp.tag_size)
    md.creat_model()
    
    model = md.model
    model.summary()

    # plot_model(model, to_file='picture/BERT_BILSTM_CRF.png', show_shapes=True)
    #
    # exit()

    model.fit(train_data, train_label, batch_size=32, epochs=25,
              validation_data=[test_data, test_label])
    model.save(os.path.join(DATA_DIR, "bert_ner.h5"))
    model.save_weights(os.path.join(DATA_DIR, "bert_ner_weight.h5"))

