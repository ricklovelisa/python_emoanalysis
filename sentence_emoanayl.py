#!/usr/bin/python
#coding: utf-8
#
# backup_remote_data_files
# $Id: backup_remote_data_files.py  2015-09-30 Qiu $
#
# history:
# 2015-10-19 Qiu   created
#
# wangQiu@kunyandata.com
# http://www.kunyandata.com
#
# --------------------------------------------------------------------
# backup_remote_data_files.py is
#
# Copyright (c)  by ShangHai KunYan Data Service Co. Ltd..  All rights reserved.
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# ShangHai KunYan Data Service Co. Ltd. or the author
# not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# --------------------------------------------------------------------

"""
sent emoanal


"""

import pickle
import numpy
import jieba
import MySQLdb
import jieba.posseg as tagseg
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Sent_emoanal(object):

    """sent emoanal.


    Attributes:
        no.
    """

    def __init__(self):

        """initiate object


        Attributes:
            no.
        """
        try:
            self.conn = MySQLdb.connect(host='127.0.0.1', user='root',
                                        passwd='root', db='stock',
                                        charset='utf8')
        except Exception, e:
            print e
        self.cur = self.conn.cursor()


    def _judge_odd(self, num):

        """judge if it's an odd?


        Attributes:
            no.
        """
        if (num/2)*2 == num:
            return 'even'
        else:
            return 'odd'

    def _get_text_from_MySQL(self):

        """get text from Mysql


        Attributes:
            no.
        """
        try:
            self.cur.execute("SELECT i_id, t_article FROM finance_news")
        except Exception, e:
            print e
        temp = self.cur.fetchall()
        result_id = []
        result_text = []
        for line in temp:
            result_id.append(line[0])
            result_id.append(line[1])
        result = list(result_id, result_text)
        return result

    def _word_seg(self, sent):

        """sentence segmentation


        Attributes:
            no.
        """
        seg_list = jieba.cut(sent)
        seg_result = ' '.join(seg_list)
        return seg_result

    def _word_pos_tag(self, sent):

        """sentence pos tagging


        Attributes:
            no.
        """
        pos_data2 = jieba.posseg.cut(sent)
        pos_list2 = []
        for w2 in pos_data2:
            pos_list2.extend([w2.word.encode('utf8'), w2.flag])
        pos_str = ' '.join(pos_list2)
        return pos_str

    def _sent_seg(self, paragraph):

        """paragraph segmentation


        Attributes:
            no.
        """
        punt_list = '：，。！？；… '.decode('utf8')
        for punt in punt_list:
            paragraph.replace(punt, '')



    #words = (words).decode('utf8')

    #i is the position of words
    token = 'meaningless'
    sents = []
    punt_list = ',.!?;~，。！？；～… '.decode('utf8')
    for word in words:
        if word not in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
            #print token
        elif word in punt_list and token in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
        else:
            sents.append(words[start:i+1])
            start = i+1
            i += 1
    if start < len(words):
        sents.append(words[start:])
    return sents

    def