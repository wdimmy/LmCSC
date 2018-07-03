# -*- coding:utf-8 -*-
import error_detection

def detection(line_str,th1=0.5,th2=0.5):
    return error_detection.__detect_sentence__(line_str, th1,th2)

