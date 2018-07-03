#-*-coding:utf-8 -*-
from pymongo import MongoClient
import codecs
import os


client = MongoClient()
client = MongoClient("localhost", 27017)
db = client["cci"]

confusionset = dict()

def __load_confusion__():

    file = codecs.open("CCI/data/confusion.txt","w","utf-8")
    confusion_db = db.confusion_set
    for item in confusion_db.find():
        file.write(item["character"]+":"+"".join(set(item["candidates"]))+"\n")
    file.close()

def __load_single_word():
    single_chara = db.single_chara
    single = []
    for item in single_chara.find():
        word = item["character"]
        single.append(word)
    return single

def __load_assist():
    teacher_assist = db.teacher_assist
    file = codecs.open("CCI/data/assist.txt", "w", "utf-8")
    for item in teacher_assist.find():
        file.write(item["Error"] + ":" + item["Replacement"]+ "\n")
    file.close()

def __load_skip_words():
    skip_words_db = db.skip_words
    file = codecs.open("CCI/data/skip.txt", "w", "utf-8")
    for item in skip_words_db.find():
        file.write(item["skip_word"]+"\n")
    file.close()


def __load_qu_words():
    quantifier_db = db.quantifier
    file = codecs.open("CCI/data/quantifier.txt", "w", "utf-8")
    for item in quantifier_db.find():
        file.write(item["word"]+":"+item["quantifier"]+"\n")
    file.close()

def __load_cantonese():
    temp_db = db.dict_appendix
    file = codecs.open("CCI/data/cantonese.txt","w","utf-8")
    for item in temp_db.find():
        file. write(item["_id"])
        file.write("\n")
    temp_db = db.chengyu
    for item in temp_db.find():
        file.write(item["_id"])
        file.write("\n")
    temp_db = db.dict_canto_reverse
    for item in temp_db.find():
        file.write(item["reverse"])
        file.write("\n")
    temp_db = db.dict_oral_label
    for item in temp_db.find():
        file.write(item["_id"])
        file.write("\n")
    temp_db = db.dict_usr
    for item in temp_db.find():
        file.write(item["_id"])
        file.write("\n")
    file.close()

def __load_single_chara():
    temp_db = db.single_chara
    file = codecs.open("CCI/data/singleword.txt", "w", "utf-8")
    for item in temp_db.find():
        file.write(item["character"]+"\n")
    file.close()


__load_single_chara()

