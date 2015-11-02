#!/usr/bin/python
#coding: utf-8
#
# NLP_study
# $Id: back_redis.py 2015-09-30 Qiu $
#
# history:
# 2015-09-30 Qiu created
# 2015-09-30 Qiu modified
# 2015-10-08 Qiu modified
#
# qiuqiu@kunyan-inc.com
# http://www.kunyandata.com
#
# --------------------------------------------------------------------
# back_redis.py is
#
# Copyright (c) by ShangHai KunYan Data Service Co. Ltd.. All rights reserved.
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

import snownlp
import jieba
import MySQLdb
import jieba.posseg as tagseg
import sklearn
from sklearn.datasets import fetch_20newsgroups
import sys
reload(sys)

sys.setdefaultencoding('utf-8')
# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print "Full Mode:", "/ ".join(seg_list)
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print "Default Mode:", "/ ".join(seg_list)
#
# seg_list = jieba.cut("他来到了网易杭研大厦")
# print "Default Mode:", "/ ".join(seg_list)
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print ", ".join(seg_list)

conn = MySQLdb.connect(host="192.168.0.2", user="root",
                       passwd="hadoop", db='stock', charset='utf8')
cur = conn.cursor()
title_num = cur.execute('select t_title from stock.finance_news where i_tag is not null')
title_seg = []
for line in range(title_num):
    title_seg.append(jieba.lcut(cur.fetchone()[0].encode('utf8'), HMM=True))




