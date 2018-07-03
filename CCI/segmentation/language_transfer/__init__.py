# -*- coding: utf8 -*-
# import opencc as oc
# import time
#
#
# def __opencc_to_sim(text):
#     sim = oc.convert(text, config='t2s.json')
#     return sim
#
#
# def __opencc_to_trad(text):
#     trad = oc.convert(text, config='s2t.json')
#     return trad
#
#
# def to_simplified(content, func=__opencc_to_sim):
#     _sim_ = func(content)
#     return _sim_
#
#
# def to_tradition(content, func=__opencc_to_trad):
#     _trad_ = func(content)
#     return _trad_

import opencc


def __opencc_to_sim(text):
    # oc = opencc.OpenCC('t2s')
    # sim = oc.convert(text)#, config='t2s.json'
    oc = opencc.OpenCC('t2s.json')#'zht2zhs.ini'
    sim = oc.convert(text)#, config='t2s.json')
    return sim


def __opencc_to_trad(text):
    # oc = opencc.OpenCC('s2t')
    oc = opencc.OpenCC('s2t.json')#'zhs2zht.ini'
    trad = oc.convert(text)#, config='s2t.json'
    return trad


def to_simplified(content, func=__opencc_to_sim):
    _sim_ = func(content)
    return _sim_


def to_tradition(content, func=__opencc_to_trad):
    _trad_ = func(content)
    return _trad_

# str1 = u'Open Chinese Convert（OpenCC）「開放中文轉換」，是一個致力於中文簡繁轉換的項目，提供高質量詞庫和函數庫(libopencc)。'
#
# print __opencc_to_sim(str1)
