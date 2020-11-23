# -*- coding: utf8 -*-
import os
from typing import Iterable, List

import numpy as np

from task.config import DATA_DIR
from task.date_task.model import BERTBILSTMCRF


class Predict(object):
    def __init__(self):
        self.bert_ner = BERTBILSTMCRF()

        self.abs_path = os.path.join(
            DATA_DIR,
            "model_02.hdf5"
        )

        self.model = self.bert_ner.get_model()
        self.model.load_weights(filepath=self.abs_path)

        self.num2tag = self.bert_ner.dp.i2tag()
        self.i2w = self.bert_ner.dp.i2w()

    def predict_sentence(self, sentence):
        data = self.bert_ner.dp.to_index(sentence)
        y = self.model.predict(data)

        x_line = data[0][0]
        t_line = y[0]
        chars, tags = [], []
        for i, index in enumerate(x_line):
            if index == self.bert_ner.dp.pad_index:
                continue
            char = self.i2w.get(index, " ")
            t_index = np.argmax(t_line[i])
            tag = self.num2tag.get(t_index, " ")
            chars.append(char)
            tags.append(tag)
        # print(chars)
        # print(tags)
        return self.get_marked(chars, tags)

    @staticmethod
    def get_marked(chars: List[str], tags: List[str]):
        assert len(chars) == len(tags)

        result, tmp_result = [], []
        for index, tag in enumerate(tags):
            if tag.startswith('B') and not tmp_result:
                tmp_result.append(chars[index])
            elif tag.startswith('I'):
                tmp_result.append(chars[index])
            elif tag.startswith('O'):
                if not tmp_result:
                    continue
                else:
                    result.append("".join(tmp_result))
                    tmp_result = []
        return result


if __name__ == '__main__':
    p = Predict()
    print(p.predict_sentence('三、合同金额:合同的金额为(大写)壹佰万圆整(￥1000000)人民币'))
    print(p.predict_sentence('1、合同金额:本合同费用含税价共计人民币:￥1000000元(大写:人民币100万元整)'))
    print(p.predict_sentence('人民币合计金额(大写)壹佰万圆整元(小写)1900000元'))
    print(p.predict_sentence('人民币合计金额(大写)壹佰万圆整元(小写1900000元)'))
    print(p.predict_sentence('检测合同价=中标价。'))
    print(p.predict_sentence('金额(大写): 100000元(人民币)'))
    print(p.predict_sentence('(小写)￥: 10000元'))
    print(p.predict_sentence('月租金总计人民币199445.481元, 其中不含税合同额为[91234.391元,'))
    print(p.predict_sentence('1、合同金额:本合同费用含税价共计人民币:￥1200000元(大写:人民币一2百万元整)'))
    print(p.predict_sentence('月租金总计人民币[99445.48]元，其中不含税合同额为[91234.39]元，税金为[8211.09]元。'))
    print(p.predict_sentence('本合同总金额为人民币一百元(￥100)。本项目的一切税费均已由乙方计入本合同总金额中。'))
    print(p.predict_sentence('合同总价为人民币(大写)壹佰万圆整整。'))
    print(p.predict_sentence('合同总价款(大小写，含税价格): ￥100000元(大写:壹佰万圆整元整)'))
    print(p.predict_sentence('合同总价为人民币大写:10000万元,即RMB￥壹佰万圆整元;'))
    print(p.predict_sentence('签约合同价为：人民币（大写） 壹佰万 （¥ 1000000 元）；'))
    print(p.predict_sentence('三、合同金额:合同的金额为(大写)叁拾肆万伍仟(￥345000元)人民币。'))
    print(p.predict_sentence('合同金额为￥105000.00元(大写:壹拾万伍仟元整)。'))
    print(p.predict_sentence("人民币合计金额(大写)壹佰万(小写)1000000"))
    print(p.predict_sentence('本项目合同金额(大写)人民币拾万(￥100000元)。'))