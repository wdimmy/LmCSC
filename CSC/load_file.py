import codecs
import os

__current_path__ = os.path.split(os.path.realpath(__file__))[0]
__lm_url = __current_path__ + "/data/kenlm_3.bin"
__confusion_url__ = __current_path__ + "/data/confusion.txt"
__assist_url__ = __current_path__ + "/data/assist.txt"
__skip_url__ = __current_path__ + "/data/skip.txt"
__quantifier_url__ = __current_path__ + "/data/quantifier.txt"
__singleword_url__ = __current_path__ + "/data/singleword.txt"
__pinyinConfusion_url__ = __current_path__ + "/data/pinyin.txt"

def __load_lm__():
    return __lm_url


def __load_confusion__():
    confusion = dict()
    with codecs.open(__confusion_url__, 'r', 'utf-8') as con:
        for line in con:
            t = line.strip().split(':')
            confusion[t[0]] = t[1]
    return confusion

def __load_pinyinConfusion__():
    confusion = dict()
    with codecs.open(__pinyinConfusion_url__,"r","utf-8") as con:
        for line in con:
            t = line.strip().split(":")
            confusion[t[0]] = t[1].split(" ")
        return confusion

def __load_assist():
    assist = dict()
    with codecs.open(__assist_url__, 'r', 'utf-8') as con:
        for line in con:
            t = line.strip().split(':')
            assist[t[0]] = t[1]
    return assist

def __load_skip_words():
    skip = []
    with codecs.open(__skip_url__, 'r', 'utf-8') as con:
        for line in con:
            t = line.strip()
            skip.append(t)
    return skip

def __load_quantifier():
    quantifier= dict()
    with codecs.open(__assist_url__, 'r', 'utf-8') as con:
        for line in con:
            t = line.strip().split(':')
            quantifier[t[0]] = t[1].split(",")
    return quantifier

def __load_singleword():
    singlewords = []
    with codecs.open(__singleword_url__, "r", "utf-8") as con:
        for line in con:
            t  = line.strip()
            singlewords.append(t)
    return singlewords


