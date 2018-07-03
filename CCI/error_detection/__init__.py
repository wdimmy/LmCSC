# -*- coding:utf-8 -*-
import __load_file__
import kenlm
from CCI import segmentation
import copy
import time
import json

__lm_model = kenlm.LanguageModel(__load_file__.__load_lm__())
__teacher_word = __load_file__.__load_assist()
__skip_word = __load_file__.__load_skip_words()
__quantifier = __load_file__.__load_quantifier()
__cutlist_sub__ = "[-。，,！……!<>\"':：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r".decode('utf-8')
__quantifier_words = u"一二三四五六七八九十百千萬億兆"
__confusionset=__load_file__.__load_confusion__()
__single_word = __load_file__.__load_singleword()

def __sen_score__(sentence, mode=1):
    if mode == 1:
        sen_cut = segmentation.seg(sentence)
        score = __lm_model.score(sen_cut)
        return score
    else:
        score = 0
        for word in sentence:
            score += __lm_model.score(word)
        return score


def __replace_ch__(in_idx, sen_list, sentence, th2):
    in_sen_list = copy.deepcopy(sen_list)
    in_sentence = copy.deepcopy(sentence)
    old_score = __lm_model.score(" ".join(in_sen_list)) + 7.4*th2
    double_check = False
    word = in_sen_list[in_idx]
    word_next_dict = {}
    word_deviation = 0


    ## double check
    if in_idx < len(in_sen_list) - 1:
        temp_count = 0;
        check_len = 0
        while temp_count < 4 and (in_idx+temp_count) < len(in_sen_list)-1 and check_len <=4:
                 check_len += len(in_sen_list[in_idx+temp_count])
                 temp_count+=1
                 word_next_dict[in_sen_list[in_idx + temp_count]] = temp_count

    for word_next in word_next_dict:
        if word == word_next:
            double_check = True
            word_deviation = word_next_dict[word_next]
            break

    candis = dict()
    try:
        candidates = __confusionset[word]
    except:
        return None

    max_score = -100000
    replacement_ch = u""
    for ch in candidates:
        temp_list = copy.deepcopy(in_sen_list)
        if not double_check:
            temp_list[in_idx] = ch
        else:
            temp_list[in_idx] = ch
            temp_list[in_idx+word_deviation] = ch

        new_score = __sen_score__(u"".join(temp_list))

        if len(segmentation.seg(in_sentence)) > len(segmentation.seg(u"".join(temp_list))):
            new_score += 5.4
        if abs(new_score - old_score) <= 1:
            new_score -= 4

        if new_score > old_score:
            candis[new_score] = ch

        if new_score > max_score:
            max_score = new_score
            replacement_ch = ch


    if max_score > old_score:
        candi_top = []
        for i in sorted(candis, reverse=True)[:min(1, len(candis))]:
            candi_top.append({"word":candis[i],"score":i})


        return in_sen_list, u"".join(in_sen_list), replacement_ch, word, candi_top, old_score, [double_check,  word_deviation], max_score
    else:
        return None


def __find_word_index_from_list(sen_list, index):
    count = 0
    for idx, word in enumerate(sen_list):
        for i in word:
            if count == index:
                return idx
            count += 1
    return None


def __qu_words_detection__(sen):
    sen = segmentation.seg(sen, mode=2)
    for w in __quantifier:
        if w in sen:
            w_idx = sen.index(w)

            if w_idx == 0:
                pass
            else:
                if len(sen[w_idx-1]) > 1:
                    first = sen[w_idx-1][0]
                    second = sen[w_idx-1][1]
                    if first in __quantifier_words:
                        if second in __quantifier[w]:
                            pass
                        else:
                            word_len = 0
                            for i in range(w_idx):
                                word_len += len(sen[i])
                            return word_len, sen[w_idx - 1], __quantifier[w][0]
                    else:
                        pass
                else:
                    if sen[w_idx - 2] in __quantifier_words:
                        if sen[w_idx - 1] in __quantifier[w]:
                            pass
                        else:
                            word_len = 0
                            for i in range(w_idx):
                                word_len += len(sen[i])
                            return word_len, sen[w_idx - 1], __quantifier[w][0]
                    else:
                        pass
        else:
            pass
    return None


def __single_pun_scan__(word):
    puns = __cutlist_sub__
    for i in puns:
        if i in word:
            return False
        else:
            pass
    return True

def __detect_sentence__(sentence, th1, th2, mode="list"):

    t1 = time.time()
    sen_json_list = dict()
    sen_list = segmentation.seg(sentence, mode=2)


    temp_sen_list = copy.deepcopy(sen_list)
    temp_sentence = copy.deepcopy(sentence)


    error = {"error": []}
    index = 0
    local_new = None
    __skip = []
    location = 1

    for idx in range(len(temp_sen_list)):
        if idx == 0:
            location = 1
        else:
            location += len(temp_sen_list[idx-1])

        word = temp_sen_list[idx]
        if len(word) == 1 and __single_pun_scan__(word) and word not in __skip_word and idx not in __skip and word not in __single_word:
            if __lm_model.score(word) <= -12.4*th1:
                temp_new = __replace_ch__(idx, temp_sen_list, temp_sentence,th2)
                if temp_new is not None and (local_new is None or temp_new[-1] > local_new[-1]):
                    error_location = location
                    local_new = copy.deepcopy(temp_new)
                    error_idx = idx
        else:
            if local_new is not None:
                detect_word = local_new[3]
                tops = local_new[4]
                double_check = local_new[-2][0]
                word_deviation = local_new[-2][1]
                old_score = local_new[-3]
                if not double_check:
                    detect = {"location": error_location,
                              "sentence_score": old_score,
                              "word": detect_word.encode("utf-8").decode("utf-8"),
                              "correction": tops}#replacement.encode("utf-8").decode("utf-8")
                    error["error"].append(detect)
                else:
                    detect1 = {"location": error_location,
                               "sentence_score": old_score,
                              "word": detect_word.encode("utf-8").decode("utf-8"),
                              "correction": tops}
                    detect2 = {"location": error_location + sum([len(temp_sen_list[k]) for k in range(error_idx, error_idx + word_deviation)]),
                               "sentence_score": old_score,
                               "word": detect_word.encode("utf-8").decode("utf-8"),
                               "correction": tops}
                    error["error"].append(detect1)
                    error["error"].append(detect2)
                    __skip.append(location + word_deviation )
                local_new = None
            if word in __teacher_word:
                temp_location = location
                for i in range(len(word)):
                    temp_location += i
                    if word[i] != __teacher_word[word][i]:
                        detect = {"location": temp_location,
                                  "word": word[i].encode("utf-8").decode("utf-8"),
                                  "correction": [{"word": __teacher_word[word][i],"score":None}]}
                        error["error"].append(detect)
                index += len(word) - 1
                temp_sen_list[idx] = __teacher_word[word]
    if local_new is not None:
        detect_word = local_new[3]
        tops = local_new[4]
        double_check = local_new[-2][0]
        word_deviation = local_new[-2][1]
        old_score = local_new[-3]
        if not double_check:
            detect = {"location": error_location,
                      "sentence_score": old_score,
                      "word": detect_word.encode("utf-8").decode("utf-8"),
                      "correction": tops}  # replacement.encode("utf-8").decode("utf-8")
            error["error"].append(detect)
        else:
            detect1 = {"location": location,
                       "sentence_score": old_score,
                       "word": detect_word.encode("utf-8").decode("utf-8"),
                       "correction": tops}
            detect2 = {"location": location + sum(
                [len(temp_sen_list[k]) for k in range(error_idx, error_idx + word_deviation)]),
                       "sentence_score": old_score,
                       "word": detect_word.encode("utf-8").decode("utf-8"),
                       "correction": tops}
            error["error"].append(detect1)
            error["error"].append(detect2)
            __skip.append(location + word_deviation)

    t2 = time.time()
    time_usage = {"time_usage":  "%.4f" % (t2 - t1)}
    sen_json_list = dict(sen_json_list, **error)
    sen_json_list = dict(sen_json_list, **time_usage)
    if mode == "list":
        return sen_json_list
    else:
        return json.dumps(sen_json_list)


def __detect_sentence_list__(sen_list, th1, th2, mode="list", biasfuc=None, biaslist=None, line_idx=None, type = "error"):
    sen_list_json = []

    if type != "mix":
        sen_list = segmentation.sent(sen_list)
        biaslist = segmentation.__sentence_bias(sen_list)
        biasfuc = segmentation.__sen_bias_apply
        line_idx = [i for i in range(len(sen_list))]

    for si, sen in enumerate(sen_list):
        idx = line_idx[si]
        single_json = __detect_sentence__(sen, th1, th2)
        qu_word = __qu_words_detection__(sen)
        if qu_word is not None:
            qu_dict = {"correction": [{"word":qu_word[2],"score": None}],"word": qu_word[1], "location": qu_word[0], "sentence_score": None}
            single_json['error'].append(qu_dict)
        if biasfuc is not None and biaslist is not None and line_idx is not None:
            bias = biaslist[idx]
            single_json = biasfuc(single_json, bias, mode="error")
            sen_list_json.append(single_json)

    if mode == "list":
        return sen_list_json
    else:
        return json.dumps(sen_list_json)







