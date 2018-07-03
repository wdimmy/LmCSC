import os

import jieba
import codecs
import jieba.posseg as pseg

'''
Load the jieba dicts files into jieba
'''
__current_path__ = os.path.split(os.path.realpath(__file__))[0]
main_dict = __current_path__ + "/../data/dict.txt.big.dic"
jieba.set_dictionary(main_dict)

defaut_freq = ''
defaut_tag = ''
dicts = [__current_path__ + '/../data/cantonese.txt']


for dictionary in dicts:
    file = codecs.open(dictionary,"r","utf-8")
    for item in file:
        items = item.strip()
        jieba.add_word(items[0], None, None)
    file.close()

def mp_segment(s):
    seg_list = jieba.cut(s, HMM=False)
    return seg_list


def hmm_segment(s):
    seg_list = jieba.cut(s, HMM=True)
    return seg_list


def pos_tag(s):
    return pseg.cut(s, HMM=False)


def pos_tag_hmm(s):
    return pseg.cut(s, HMM=True)
