import os

import jieba
import codecs

'''
Load the jieba dicts files into jieba
'''
__current_path__ = os.path.split(os.path.realpath(__file__))[0]

defaut_freq = ''
defaut_tag = ''
dicts = [__current_path__ + '/data/customized.txt']

for dictionary in dicts:
    file = codecs.open(dictionary,"r","utf-8")
    for item in file:
        items = item.strip()
        jieba.add_word(items[0], None, None)
    file.close()

def seg(s, mode=False):
    if not mode:
        seg_list = jieba.cut(s, HMM=False)
        seg_list  = [item for item in seg_list]
        return seg_list
    else:
        seg_list = jieba.cut(s, HMM=True)
        seg_list = [item for item in seg_list]
        return seg_list

