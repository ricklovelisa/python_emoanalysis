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

import jieba
import MySQLdb
import codecs
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
        self.word_seg = jieba.lcut
        self.dir = 'D:/dicts/'


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
            self.cur.execute("SELECT i_id, t_article FROM finance_news limit 5")
        except Exception, e:
            print e
        temp = self.cur.fetchall()
        result = []
        for line in temp:
            result.append([line[0], line[1].encode()])
        return result

    # def _word_seg(self, sent):
    #
    #     """sentence segmentation
    #
    #
    #     Attributes:
    #         no.
    #     """
    #     seg_list = jieba.cut(sent)
    #     seg_result = ' '.join(seg_list)
    #     return seg_result

    # def _word_pos_tag(self, sent):
    #
    #     """sentence pos tagging
    #
    #
    #     Attributes:
    #         no.
    #     """
    #     pos_data2 = jieba.posseg.cut(sent)
    #     pos_list2 = []
    #     for w2 in pos_data2:
    #         pos_list2.extend([w2.word.encode('utf8'), w2.flag])
    #     pos_str = ' '.join(pos_list2)
    #     return pos_str

    def _sent_seg(self, paragraph):

        """sentences segmentation


        Attributes:
            no.
        """
        punt_list = '：，。！？；…'.decode('utf8')
        for punt in punt_list:
            paragraph.replace(punt, ' ')
        result = paragraph.split(' ')
        return result

    def _paragraph_seg(self, article):

        """paragraph segmentation


        Attributes:
            no.
        """
        temp = article.split(u'\u3000'u'\u3000')
        result = []
        for line in temp:
            if len(line):
                result.append(line)
        return result

    def _get_dicts(self, dir):

        """get posdict, negdict, mostdict
               moredict, ishdict, insuffdict
               and inversedict


        Attributes:
            no.
        """
        dict_name = ['posdict', 'negdict', 'mostdict', 'verydict', 'moredict',
                     'ishdict', 'insuffdict', 'inversedict']
        dict = []
        for name in dict_name:
            temp = codecs.open(dir+name, 'r', 'utf8')
            dict.append(temp.readlines())
            temp.close()
        return dict

    def _compute_sent_socre(self, word, dict, sent_score):

        """sentiment score


        Attributes:
            no.
        """
        if word in dict[2]:
            sent_score *= 4.0
        elif word in dict[3]:
            sent_score *= 3.0
        elif word in dict[4]:
            sent_score *= 2.0
        elif word in dict[5]:
            sent_score /= 2.0
        elif word in dict[6]:
            sent_score /= 4.0
        elif word in dict[7]:
            sent_score *= -1
        return sent_score

    def _transfrom_scores(self, poscount, negcount):

        """sentiment score


        Attributes:
            no.
        """
        pos_count = 0
        neg_count = 0
        if poscount < 0 and negcount >= 0:
            neg_count += negcount - poscount
            pos_count = 0
        elif negcount < 0 and poscount >= 0:
            pos_count = poscount - negcount
            neg_count = 0
        elif poscount < 0 and negcount < 0:
            neg_count = -poscount
            pos_count = -negcount
        else:
            pos_count = poscount
            neg_count = negcount
        return [pos_count, neg_count]



    def sentiment_score(self, article, dict):

        """sentiment score


        Attributes:
            no.
        """
        count_cent = []
        count_para = []
        count_article = []
        for text in article:
            paras = self._paragraph_seg(text[1])
            for para in paras:
                sents = self._sent_seg(para)
                for sent in sents:
                    words = self.word_seg(sent)
                    i = 0  # index of counter
                    a = 0  # index of emo word
                    pos_count = 0
                    neg_count = 0
                    for word in words:
                        if word in dict[0]:
                            pos_count += 1
                            for w in words[a:i]:
                                pos_count = self._compute_sent_socre(w, dict, pos_count)
                            a = i + 1
                        elif word in dict[1]:
                            neg_count += 1
                            for w in words[a:i]:
                                neg_count = self._compute_sent_socre(w, dict, pos_count)
                            a = i + 1
                        i += 1
                    count_cent.append(self._transfrom_scores(pos_count, neg_count))
                count_para.append(count_cent)
                count_cent = []
            count_article.append(count_para)
            count_para = []
        return count_article

    def main(self):

        """main function


        Attributes:
            no.
        """
        articles = self._get_text_from_MySQL()
        dicts = self._get_dicts(self.dir)
        result = self.sentiment_score(articles, dicts)
        print result

if __name__ == '__main__':
    Emo_analysis = Sent_emoanal()
    Emo_analysis.main()



