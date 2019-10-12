#-*-coding:utf-8-*-
from __future__ import print_function
import code
import prettytable
import CSC.model as model


def process(sentence, candidates=None, top_n=1,n_docs=5):
    table = prettytable.PrettyTable(["Location","Error",
                                    "Correction", "Old Score","New Score"])
    result = model.detection(sentence.decode("utf-8"))
    errors = result["error"]
    print (sentence+":\n")
    for error in errors:
       table.add_row([error["location"], error["word"].encode("utf-8"), error["correction"][0]["word"].encode("utf-8"), error["sentence_score"],error["correction"][0]["score"]])
    print(table)

banner="""
Interactive CSC
>> process(question, candidates=None, top_n=1, n_docs=5)
>> usage()
"""

def usage():
    print(banner)

code.interact(banner=banner, local=locals())

