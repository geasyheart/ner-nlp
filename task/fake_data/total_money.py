# -*- coding: utf8 -*-
import random
import re


class project_parm(object):

    def IIf(self, b, s1, s2):
        if b:
            return s1
        else:
            return s2

    def num2chn(self, nin=None):
        """小写金额转大写"""
        cs = (
            '零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '◇', '分', '角', '圆', '拾', '佰', '仟', '万', '拾', '佰', '仟',
            '亿',
            '拾', '佰', '仟', '万')
        st = ''
        st1 = ''
        s = '%0.2f' % (nin)
        sln = len(s)
        if sln > 15:
            return None
        fg = (nin < 1)
        for i in range(0, sln - 3):
            ns = ord(s[sln - i - 4]) - ord('0')
            st = self.IIf((ns == 0) and (fg or (i == 8) or (i == 4) or (i == 0)), '', cs[ns]) + self.IIf(
                (ns == 0) and ((i != 8) and (i != 4) and (i != 0) or fg and (i == 0)), '', cs[i + 13]) + st
            fg = (ns == 0)
        fg = False
        for i in [1, 2]:
            ns = ord(s[sln - i]) - ord('0')
            st1 = self.IIf((ns == 0) and ((i == 1) or (i == 2) and (fg or (nin < 1))), '', cs[ns]) + self.IIf((ns > 0),
                                                                                                              cs[
                                                                                                                  i + 10],
                                                                                                              self.IIf((
                                                                                                                               i == 2) or fg,
                                                                                                                       '',
                                                                                                                       '整')) + st1
            fg = (ns == 0)
        st.replace('亿万', '万')
        return self.IIf(nin == 0, '零', st + st1)


def fake_sequence():
    return random.choice(
        ('一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))


def fake_name():
    return random.choice(
        ['价款', '项目合同金额', '项目预算金额', '此次设备产品供货总价格',
         '合同价', '合同价格', '合同价款', '暂估价', '金额', '暂列金额', '报价金额', '合同价价款',
         '本合同项下合同价款暂定为',
         '服务费用', '人民币合计金额', '租金', '合同总价', '工程中标总价', '合同金额',
         '合同总金额', '合同总价款', '总金额'
         ]

    )


def fake1_1():
    # 6、报价金额:合同的金额为(大写)捌佰肆拾伍万叁仟肆佰肆拾圆整(￥8453440)人民币
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_sequence()}、{fake_name()}:合同的金额为(大写){money}(￥{lower_money})人民币", f"￥{lower_money}"


def fake1_2():
    # 3、租金:合同的金额为(大写)贰佰柒拾柒万零柒佰零玖圆整(￥2770709)人民币。
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_sequence()}、{fake_name()}:合同的金额为(大写){money}(￥{lower_money})人民币。", f"￥{lower_money}"


def fake2_1():
    # 六、报价金额:本合同费用含税价共计人民币:￥300000元(大写:人民币叁拾万元整。)
    lower_money = random.choice(range(1, 100))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_sequence()}、{fake_name()}:本合同费用含税价共计人民币:￥{lower_money * 10000}元(大写:人民币{money[:-2]}万元整。)", f"￥{lower_money * 10000}元"


def fake2_2():
    # 六、报价金额:本合同费用含税价共计人民币:￥300000元(大写:人民币叁拾万元整)。
    lower_money = random.choice(range(1, 100))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_sequence()}、{fake_name()}:本合同费用含税价共计人民币:￥{lower_money * 10000}元(大写:人民币{money[:-2]}万元整)。", f"￥{lower_money * 10000}元"


def fake2_3():
    lower_money = random.choice(range(1, 100))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}(小写){lower_money}万元，(大写:{money[:-2]}万元整);', f"{lower_money}万元"


def fake3_1():
    # 人民币合计金额(大写)壹佰零伍万叁仟玖佰柒拾柒圆整(小写)1053977
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_name()}(大写){money}(小写){lower_money}", f"{lower_money}"


def fake3_4():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_name()}(大写){money}(小写){lower_money}元", f"{lower_money}元"


def fake3_2():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"{fake_name()}(大写){money}(小写){lower_money}。", f"{lower_money}"


def fake3_5():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"人民币合计金额(大写){money}(小写){lower_money}元。", f"{lower_money}元"


def fake3_3():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"人民币合计金额(大写){money}(小写){lower_money}元。", f"{lower_money}元"


def fake3_6():
    # ￥
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f"人民币合计金额(大写){money}(小写)￥{lower_money}元。", f"￥{lower_money}元"


def fake3_7():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}(大写){money}(小写:{lower_money}元)。', f'{lower_money}元'


def fake4():
    # 检测此次设备产品供货总价格=中标价。
    return f'检测{fake_name()}=中标价。', '中标价'


def fake5():
    # '项目预算金额为(大写): 捌拾玖万零伍拾柒圆整(￥890057元)。
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}为(大写):{money}(￥{lower_money}元)。', f'￥{lower_money}元'


def fake5_1():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}为(大写):{money}元(￥{lower_money}元)人民币。', f'￥{lower_money}元'


def fake5_2():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}为(大写):{money}人民币(￥{lower_money}元)', f'￥{lower_money}元'


def fake6():
    # 金额(大写):捌佰肆拾壹万玖仟叁佰贰拾贰圆整元(人民币)
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'金额(大写):{money}元(人民币)', f'{money}'


def fake6_1():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'金额(大写):{money}(人民币)', f'{money}'


def fake7():
    # (大写):伍拾万叁仟柒佰玖拾玖圆整元(人民币)
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'(大写):{money}元(人民币)', f'{money}'


def fake7_1():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'(大写):{money}(人民币)', f'{money}'


def fake8():
    # (小写)￥:4923972元
    lower_money = random.choice(range(1, 10000000))
    # p = project_parm()
    # money = p.num2chn(lower_money)
    return f'(小写)￥:{lower_money}元', f'{lower_money}元'


def fake9():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'人民币(大写){money}元整;人民币(小写){lower_money}元整。', f'{lower_money}元整'


def fake10():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'人民币(大写){money}元整;人民币(小写)￥{lower_money}元整。', f'￥{lower_money}元整'


def fake11():
    lower_money = random.choice(range(1, 10000000))

    return f'本合同总价为{lower_money}元人民币。', f'{lower_money}元人民币'


def fake12():
    lower_money = random.choice(range(1, 10000000))
    return f'月租金总计人民币[{lower_money}]元', f'[{lower_money}]元'


def fake13():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'合计大写金额:{money}', money


def fake14():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    money = money[:-2] + "元"
    return f'合计大写金额:{money}', money


def fake15():
    lower_money = random.choice(range(1, 10000000))
    return f'{fake_name()}:{lower_money}元，', f'{lower_money}元'


def fake16():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}(大写)人民币{money}(￥{lower_money}元)', f'￥{lower_money}元'


def fake17():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}为人民币大写:{money}元(￥{lower_money})', f'￥{lower_money}'


def fake18():
    lower_money = random.choice(range(1, 10000000))
    p = project_parm()
    money = p.num2chn(lower_money)
    return f'{fake_name()}为人民币{money}元(￥{lower_money}元)。', f'￥{lower_money}元'


def fake_money():
    for func in (
            fake1_1, fake1_2, fake2_1, fake2_2,
            fake2_3,
            fake3_1, fake3_2, fake3_3, fake3_4,
            fake3_5, fake3_6, fake3_7,
            fake4, fake5,
            fake5_1,
            fake5_2,
            fake6,
            fake6_1,
            fake7,
            fake7_1,
            fake8,
            fake9,
            fake10,
            fake11,
            fake12,
            fake13,
            fake14,
            fake15,
            fake16,
            fake17,
            fake18,
    ):
        text, mark = func()
        # print(func.__name__, ':', text, mark)
        # assert text.find(mark) != -1
        yield text, mark
    # return text, mark


def fake_to_excel():
    # with open('../data/total_money.txt', 'a+') as f:
    #     for i in range(5000):
            for text, make in fake_money():
                print(text, make)
                # f.write(f'{text}^$$^{make}\n')


if __name__ == '__main__':
    fake_to_excel()
    # fake_money()
