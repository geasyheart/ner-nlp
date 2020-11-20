# -*- coding: utf8 -*-
import random

import pandas as pd

from config import TRAIN_DATA_PATH
import faker

# df = pd.read_excel(TRAIN_DATA_PATH, sheet_name="合同主体").fillna("")

fake = faker.Faker("zh_CN")

jiafang = (
    "甲方", '发包单位', '采购方', '采购人', '采购单位', '委托人', '发包人', '买方', '出租方',
)
yifang = ('乙方',
          '成交供应商', '供 应 商', '供货单位', '卖方名称', '承接方', '卖方', '服务方', '监理人', '承包人', '(承包人)',
          '承包方', '本合同卖方系指',
          '受托方', '供方', '乙方单位', '受托方', '承担单位', '承包单位', '供应商', '承租方'
          )
jiafang_suffixes = ('(甲方)', '(买方)', '(全称)', '(公章)', '(采购人)', '(委托方)', '(发包单位)', '(采购人)', '系指', '(简称甲方)', '(以下称甲方)',
                    '(需方)', '即',
                    '(C3卖方)', '(供应商)', '(盖章)', '(采购人)', '(采购人名称)', '(以下简称甲方)', '(章)')

yifang_suffixes = (
    '(乙方)', '(卖方)', '(全称)', '(公章)', '(供应商)', '(受托方)', '(承包单位)', '(供应商)', '系指', '(简称乙方)', '(中标人)',
    '(以下称乙方)', '(供方)', '即', '(章)', '(以下简称乙方)',
)

others = set([
    '人民币合计金额', '合同金额', '签约合同价', '合同总价款', '产品的价格', '本合同总金额', '保险金额、保险费', '活动经费', '合同总金额', '合同的总金额', '本合同总价款', '合同总额',
    '总金额', '合同价', '本合同价款', '项目合同金额', '项目预算金额', '此次设备产品供货总价格', '合同价格', '合同价款', '暂估价', '金额', ' 暂列金额', '报价金额', '合同价价款',
    '本合同项下合同价款暂定为', '服务费用', '人民币合计金额', '一次总付', '租金',
    '付款', '付款条件和方式', '付款条款及合同期限', '付款措施', '保费结算', '费用支付', '项目付款方式', '保费支付', '结算方式', '支付方式', '合同款支付 ', '付款方法和条件', '付款条件',
    '付款 ', '支付', '竣工结算', ' 工程进度款支付', '进度款支付方式', '工程进度付款', '本合同的付款方式为', '合同价款支付', '支付途径', '项目费用', '甲方按下表约定支付工程款', '支付方法'
])

end = ['机关', '集团', '设计院', '工作室', '公司', '研究所', '办事处', '公署', '事务所', '部门', '中心', '厂', '血站', '网络有限公司', '科技有限公司', '信息有限公司',
       '传媒有限公司']


def company():
    _suffixes = []
    _aa = {
        '机构', '办公室', '酒店', '监狱', '基地', '旅游局', '责任公司', '税务局', '建设局', '政府', '国土局', '办公厅', '信息部', '事业部',
        '科委', '省委', '殡仪馆', '养生馆', '管理公司', '电视台', '卫生局', '水利局', '药房', '电影院', '有限公司', '法院', '公安局', '报社',
        '集团', '红十字会', '居委会', '基金会', '疗养院', '企业', '党委', '门诊部', '纠察队', '书馆', '财团', '药监局','歌舞团',

    }
    _suffixes.extend(_aa)

    def is_same(name: str):
        if name.endswith('店') or name.endswith('厂'):
            return True
        if name[-4:] in _suffixes:
            return True
        elif name[-3:] in _suffixes:
            return True
        elif name[-2:] in _suffixes:
            return True
        else:
            _suffixes.extend([name[-4:], name[-3:], name[-2:], ])

            return False

    path1 = "/home/yuzhang/桌面/公司名/company_name_480w.txt"
    path2 = "/home/yuzhang/桌面/公司名/Organization-Names-Corpus-110w.txt"
    for path in (path1, path2):
        with open(path, 'r') as f:
            for line in f:
                is_same(line.strip())
    print(_suffixes)


print(company())


def fake1():
    """
    采购人(甲方):____________
    成交供应商(乙方):________
    """

    result = []

    define_words, suffixes = random.choice(((jiafang, jiafang_suffixes), (yifang, yifang_suffixes)))

    for define_word in define_words:
        for suffix in suffixes:
            _company = company()
            result.append((define_word + suffix + ":" + _company, _company))
            result.append(define_word + suffix + "：" + company())
            result.append(define_word + suffix + "是" + company())
            result.append(define_word + suffix + "为" + company())
            result.append(define_word + suffix + company())
    return result


def fake2():
    """甲方：____"""
    name: str = fake.company()[:-2]
    random_end = random.choice(end)
    result = []

    define_words, suffixes = random.choice(((jiafang, jiafang_suffixes), (yifang, yifang_suffixes)))
    for define_word in define_words:
        result.append(define_word + ":" + name + random_end)
        result.append(define_word + "：" + name + random_end)
        result.append(define_word + "是" + name + random_end)
        result.append(define_word + "为" + name + random_end)
        result.append(define_word + name + random_end)
    return result


def fake3():
    """甲方:dfjafja(以下简称甲方)"""
    name: str = fake.company()[:-2]
    random_end = random.choice(end)
    result = []

    define_words, suffixes = random.choice(((jiafang, jiafang_suffixes), (yifang, yifang_suffixes)))
    is_jiafang = False
    if "甲方" in define_words:
        is_jiafang = True
    for define_word in define_words:
        result.append(define_word + ":" + name + random_end + ("(以下简称甲方)" if is_jiafang else "(以下简称乙方)"))
    return result


def fake4():
    """
    采购人(全称)....(甲方)
    :return:
    """
    name: str = fake.company()[:-2]
    random_end = random.choice(end)
    result = []

    define_words, suffixes = random.choice(((jiafang, jiafang_suffixes), (yifang, yifang_suffixes)))
    is_jiafang = False
    if "甲方" in define_words:
        is_jiafang = True
    for define_word in define_words:
        result.append(define_word + ":" + name + random_end + ("(甲方)" if is_jiafang else "(乙方)"))
        result.append(define_word + name + random_end + ("(甲方)" if is_jiafang else "(乙方)"))
    return result


def fake5():
    name: str = fake.company()[:-2]
    random_end = random.choice(end)
    result = []

    define_words, suffixes = random.choice(((jiafang, jiafang_suffixes), (yifang, yifang_suffixes)))

    for define_word in define_words:
        result.append(define_word + ":" + name + random_end + f"({random.choice(define_words)}名称)")
        result.append(define_word + ":" + name + random_end + f"({random.choice(define_words)})")
    return result


def fake6():
    """采购单位（甲方）adjfajfa 采购计划号234ip234"""
    new_result = []
    for result in fake1():
        new_result.append(result + random.choice(others))
    return new_result


def fake7():
    result = []
    for jf in jiafang:
        result.append(f"{jf}:本合同买方系指:{company()}。")
    for yf in yifang:
        result.append(f"{yf}:本合同卖方系指:{company()}。")
    return result
