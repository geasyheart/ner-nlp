# -*- coding: utf8 -*-
import os

from keras.callbacks import ModelCheckpoint

from config import DATA_DIR
from task.date_task.model import BERTBILSTMCRF


def train():
    bert_ner = BERTBILSTMCRF()
    train_data, train_label = bert_ner.dp.get_data()

    md = BERTBILSTMCRF()
    model = md.get_model()
    md.compile()

    checkpoint = ModelCheckpoint(
        filepath=os.path.join(DATA_DIR, "model_{epoch:02d}.hdf5"),
        # monitor='val_acc',
        verbose=1,
        # save_best_only=True,
        # mode='max'
        save_weights_only=True,
        period=1
    )
    callbacks = [
        checkpoint,

    ]

    model.fit(
        train_data, train_label, batch_size=32, epochs=10,
        callbacks=callbacks,
        validation_split=0.2,
        shuffle=True
    )
    model.save(os.path.join(DATA_DIR, "bert_ner_md1.h5"))
    model.save_weights(os.path.join(DATA_DIR, "bert_ner_md2.h5"))
