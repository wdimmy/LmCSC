# -*- coding: UTF-8 -*-

import seg_mode as sm
import language_transfer as tr

_cutlist = "。，,！……!:：？\?、；;\n\r".decode('utf-8')


'''
Abstract functions
'''


def maximum_cut(str):
    return sm.mp_segment(str)


def hmm_cut(str):
    return sm.hmm_segment(str)


def pos_tag(str):
    return sm.pos_tag(str)


def pos_hmm(str):
    return sm.pos_tag_hmm(str)



'''
functions to call
'''

def __cut_sentence__(line, cutlist=_cutlist):
    sentence = ""
    text_list = []
    line = line.strip()
    for word in line:
        added = False
        sentence += word
        if word in cutlist:
            text_list.append(sentence)
            sentence = ""
            added = True
    if added is False:
        if sentence.strip() not in _cutlist:
            text_list.append(sentence)
    return text_list

def __sent_list(lists):
    list_length = len(lists)
    idxs = range(list_length)
    sen_list = zip(lists, idxs)
    return [i[0] for i in sen_list], sen_list


def sent(sen, mode=1):
    if mode == 1:
        return __sent_list(__cut_sentence__(sen))[0]
    else:
        return __sent_list(__cut_sentence__(sen))[1]


def seg(line_to_seg, mode='ori', fn=maximum_cut):
    sim_line = u" ".join(list(fn(line_to_seg.strip())))
    if mode == 'ori':
        return sim_line
    else:
        return sim_line.split(" ")


def __sentence_bias(senlist):
    bias = dict()
    for i in range(len(senlist)):
        if i == 0:
            bias[i] = 0
        else:
            bias[i] = len(senlist[i - 1]) + bias[i - 1]
    return bias

def __sen_bias_apply(jsonfile, bias, mode=None):
    if mode == None:
        return None
    elif mode == "can":
        try:
            if jsonfile["cantonese_word"] != []:
                for item in jsonfile["cantonese_word"]:
                    item["location"] += bias
        except:
            pass
        try:
            if jsonfile["cantonese_usage"] != []:
                for item in jsonfile["cantonese_usage"]:
                    item["location"] += bias
        except:
            pass
    elif mode == "error":
        if jsonfile["error"] != []:
            for item in jsonfile["error"]:
                item["location"] += bias

    elif mode == "idioms_phrases":
        if jsonfile["idioms"] != []:
            for item in jsonfile["idioms"]:
                item["location"] += bias
        if jsonfile["phrases"] != []:
            for item in jsonfile["phrases"]:
                item["location"] += bias
    return jsonfile

def pos(line_str, fn=pos_tag):
    trad_pos = []
    line_to_seg = tr.to_simplified(line_str)
    sim_pos = fn(line_to_seg)
    for word, tag in sim_pos:
        trad_pos.append((word, tag))
    return trad_pos


def cut(line_to_cut):
    return pos(seg(line_to_cut.strip()))

