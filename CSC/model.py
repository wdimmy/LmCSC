# -*- coding:utf-8 -*-
import load_file
import kenlm
import segmentation
import copy
import time
import json
import random

from xpinyin import Pinyin, PinyinToneMark
PIN = Pinyin()


LmModel = kenlm.LanguageModel(load_file.__load_lm__())

TeacherWord = load_file.__load_assist()
SkipWord = load_file.__load_skip_words()
Quantifier = load_file.__load_quantifier()

PUNCTUATIONS = "[-。，,！……!<>\"':：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r"
QuantifierWords = "一二三四五六七八九十百千万亿兆"
Confusionset = load_file.__load_confusion__()
pinyinConfusionset = load_file.__load_pinyinConfusion__()
SingleWord = load_file.__load_singleword()


def sentenceScorer(sentence):
    """
    The language model needs an input in which the sentence is segmented by space

    :param sentence:
    :return:
    """
    sen_cut = " ".join(segmentation.seg(sentence))
    score = LmModel.score(sen_cut)
    return score


def replaceOneCharacter(idx, sen_list, sentence):
    old_score = sentenceScorer(sentence) + 3.7
    double_check = False

    word = sen_list[idx]
    word_next_dict = {}
    word_deviation = 0

    ## To see whether there contains same words in the following three words
    if idx < len(sen_list) - 1:
        temp_count = 1
        check_len = 0 # this variable is used to record the number of words
        while temp_count < 4 and (idx + temp_count) < len(sen_list)-1 and check_len <=4:
           check_len += len(sen_list[idx+temp_count])
           temp_count+=1
           word_next_dict[sen_list[idx + temp_count]] = temp_count

    for word_next in word_next_dict:
        if word == word_next:
            double_check = True
            word_deviation = word_next_dict[word_next]
            break

    candis = dict()
    try:
        candidates = Confusionset[word]
    except:
        return None

    max_score = -100000
    replacement_ch = ""
    for ch in candidates:
        temp_list = sen_list[:]
        if not double_check:
            temp_list[idx] = ch
        else:
            temp_list[idx] = ch
            temp_list[idx+word_deviation] = ch

        new_score = sentenceScorer("".join(temp_list))

        if len(segmentation.seg(sentence)) > len(segmentation.seg("".join(temp_list))):
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

        return  replacement_ch, word, candi_top, old_score, double_check, word_deviation , max_score

    else:
        return None


def qu_words_detection(sen):
    sen = segmentation.seg(sen, mode=True)
    ans = []
    for w in Quantifier:
        if w in sen:
            w_idx = sen.index(w)
            if w_idx == 0:
                pass
            else:
                if w_idx!= 0 and len(sen[w_idx-1]) > 1:
                    first = sen[w_idx-1][-2]
                    second = sen[w_idx-1][-1]
                    if first in QuantifierWords:
                        if second in Quantifier[w]:
                            continue
                        else:
                            word_len = 0
                            for i in range(w_idx):
                                word_len += len(sen[i])

                            detect = {"location": word_len,
                                      "word":second ,
                                      "correction": [{"word": random.choice(Quantifier[w]), "score": None}]}
                            ans.append(detect)
                else:
                    if w_idx > 1 and (sen[w_idx - 2][-1] in QuantifierWords):
                        if len(sen[w_idx - 1])==1 and (sen[w_idx - 1] in Quantifier[w]):
                            pass
                        elif len(sen[w_idx - 1])==1 and (sen[w_idx - 1] not in Quantifier[w]):
                            word_len = 0
                            for i in range(w_idx):
                                word_len += len(sen[i])
                            detect = {"location": word_len,
                                      "word": sen[w_idx - 1],
                                      "correction": [{"word": random.choice(Quantifier[w]), "score": None}]}
                            ans.append(detect)
    return ans


def isPunc(word):
    for i in PUNCTUATIONS:
        if i in word:
            return False
        else:
            pass
    return True


def replaceWord(sentence):
    ans = []
    sen_list = segmentation.seg(sentence, mode=True)
    old_score = sentenceScorer(sentence)

    temp_sen_list = sen_list[:]

    for idx in range(len(sen_list)):
        pinyin = PIN.get_pinyin(sen_list[idx],"")
        local_score = -10000
        if len(sen_list[idx]) > 1 and pinyin  in pinyinConfusionset:
            for candi in pinyinConfusionset[pinyin]:
                temp_sen_list[idx] = candi
                current_score = sentenceScorer("".join(temp_sen_list))
                if current_score > local_score:
                    local_score = current_score
                    replace_word = candi
                    replace_score = current_score

            if local_score - old_score > 4:
                word_len = 0
                for i in range(idx):
                    word_len += len(sen_list[i])
                if len(sen_list[idx]) == len(replace_word):
                    for i in range(len(replace_word)):
                        if replace_word[i] != sen_list[idx][i]:
                            detect = {"location": word_len+i+1,
                                      "sentence_score": old_score,
                                      "word": sen_list[idx][i],
                                      "correction": [{"word": replace_word[i], "score":replace_score}]
                            }
                            ans.append(detect)
        temp_sen_list = sen_list[:]
    return ans



def detectSentence(sentence):
    t1 = time.time()
    final_result = dict()
    sen_list = segmentation.seg(sentence)
    temp_sen_list = sen_list[:]

    error = {"error": []}
    index = 0
    local_res = None # this variable is used for keeping the detected result
    skip_index = []
    location = 1

    for idx in range(len(temp_sen_list)):
        """
       Since we use the segmentation tool, the location need some more operations.
       """
        if idx == 0:
            location = 1
        else:
            location += len(temp_sen_list[idx-1])

        word = temp_sen_list[idx]

        if index in skip_index:  # If double check is True, we will not continue to detect the following 3 words
            continue

        if len(word) == 1 and isPunc(word) and word not in SkipWord and word not in SingleWord:
            if LmModel.score(word) <= -6.2:
                ans = replaceOneCharacter(idx, temp_sen_list, sentence)
                if ans is not None and (local_res is None or ans[-1] > local_res[-1]):
                    error_location = location
                    local_res = copy.deepcopy(ans)
                    error_idx = idx

        else:
            if local_res is not None:
                detect_word = local_res[1]
                tops = local_res[2]
                double_check = local_res[4]
                word_deviation =  local_res[5]
                old_score = local_res[3]
                if not double_check:
                    detect = {"location": error_location,
                              "sentence_score": old_score,
                              "word": detect_word,
                              "correction": tops}
                    error["error"].append(detect)
                else:
                    detect1 = {"location": error_location,
                               "sentence_score": old_score,
                               "word": detect_word,
                               "correction": tops}
                    detect2 = {"location": error_location + sum([len(temp_sen_list[k]) for k in range(error_idx, error_idx + word_deviation)]),
                               "sentence_score": old_score,
                               "word": detect_word,
                               "correction": tops}
                    error["error"].append(detect1)
                    error["error"].append(detect2)

                    skip_index.extend([k for k  in range(error_idx, error_idx + word_deviation)])
                local_res = None

            if word in TeacherWord:
                temp_location = location
                for i in range(len(word)):
                    temp_location += i
                    if word[i] != TeacherWord[word[i]]:
                        detect = {"location": temp_location,
                                  "word": word[i],
                                  "correction": [{"word":TeacherWord[word[i]],"score":None}]}
                        error["error"].append(detect)

    if local_res is not None:
        detect_word = local_res[1]
        tops = local_res[2]
        double_check = local_res[4]
        word_deviation = local_res[5]
        old_score = local_res[3]
        if not double_check:
            detect = {"location": error_location,
                      "sentence_score": old_score,
                      "word": detect_word,
                      "correction": tops}
            error["error"].append(detect)
        else:
            detect1 = {"location": error_location,
                       "sentence_score": old_score,
                       "word": detect_word,
                       "correction": tops}
            detect2 = {"location": error_location + sum(
                [len(temp_sen_list[k]) for k in range(error_idx, error_idx + word_deviation)]),
                       "sentence_score": old_score,
                       "word": detect_word,
                       "correction": tops}
            error["error"].append(detect1)
            error["error"].append(detect2)

    t2 = time.time()
    qu_res = qu_words_detection(sentence)

    if qu_res:
        error["error"].extend(qu_res)

    word_res = replaceWord(sentence)
    if len(word_res) > 0:
        error["error"].extend(word_res)

    time_usage = {"time_usage":  "%.4f" % (t2 - t1)}
    final_result = dict(final_result, **error)
    final_result = dict(final_result, **time_usage)

    return final_result


def detection(line):
    return detectSentence(line)





