import MySQLdb
import jieba
import codecs

def judge_odd(num):

        """judge if it's an odd?


        Attributes:
            no.
        """
        if (num/2)*2 == num:
            return 'even'
        else:
            return 'odd'

def get_text_from_MySQL():

        """get text from Mysql


        Attributes:
            no.
        """
        conn = MySQLdb.connect(host='127.0.0.1', user='root',
                                        passwd='root', db='stock',
                                        charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("SELECT i_id, t_article FROM finance_news")
        except Exception, e:
            print e
        temp = cur.fetchall()
        result = []
        for line in temp:
            result.append([line[0], line[1]])
        return result

def paragraph_seg(article):

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

def sent_seg(paragraph):

        """sentences segmentation


        Attributes:
            no.
        """
        punt_list = '£º£¬¡££¡£¿£»¡­'.decode('utf8')
        for punt in punt_list:
            paragraph = paragraph.replace(punt, u'\u3000')
        result = paragraph.split(u'\u3000')
        return result

def word_seg(sent):

        """sentence segmentation


        Attributes:
            no.
        """
        seg_list = jieba.lcut(sent)
        return seg_list

def get_dicts(dir):

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

def sentiment_score(article, dict):

        """sentiment score


        Attributes:
            no.
        """
        for text in article:
            paragraphs = paragraph_seg(text[1])
            count_1 = []
            count_2 = []
            count_3 = []
            for para in paragraphs:
                sents = sent_seg(para)
                for sent in sents:
                    sent_seg = word_seg(sent)
                    word_index = 0  # scan words index
                    emo_index = 0  # emotional words index
                    posscore_1 = 0  # pos word first score
                    posscore_2 = 0  # pos word reversed score
                    posscore_3 = 0  # pos word final score
                    negscore_1 = 0
                    negscore_2 = 0
                    negscore_3 = 0
                    for word in sent_seg:
                        if word in dict[0]:
                            posscore_1 += 1
                            c = 0  # inverse adverb number
                            for i in sent_seg[emo_index:word_index]:
                                if i in dict[2]:
                                    posscore_1 *= 4.0
                                elif i in dict[3]:
                                    posscore_1 *= 3.0
                                elif i in dict[4]:
                                    posscore_1 *= 2.0
                                elif i in dict[5]:
                                    posscore_1 /= 2.0
                                elif i in dict[6]:
                                    posscore_1 /= 4.0
                                elif i in dict[7]:
                                    c += 1
                                if judge_odd(c) == 'odd':
                                    posscore_1 *= -1.0
                                    posscore_2 += posscore_1
                                    posscore_1 = 0
                                    posscore_3 += (posscore_1 + posscore_2)
                                    posscore_2 = 0
                                else:
                                    posscore_3 += (posscore_1 + posscore_2)
                                    posscore_1 = 0
                                emo_index += 1
                        elif word in dict[1]:
                            negscore_1 += 1
                            c = 0
                            for i in sent_seg[emo_index:word_index]:
                                if i in dict[2]:
                                    negscore_1 *= 4.0
                                elif i in dict[3]:
                                    negscore_1 *= 3.0
                                elif i in dict[4]:
                                    negscore_1 *= 2.0
                                elif i in dict[5]:
                                    negscore_1 /= 2.0
                                elif i in dict[6]:
                                    negscore_1 /= 4.0
                                elif i in dict[7]:
                                    c += 1
                                if judge_odd(c) == 'odd':
                                    negscore_1 *= -1.0
                                    negscore_2 += negscore_1
                                    negscore_1 = 0
                                    negscore_3 += (negscore_1 + negscore_2)
                                    negscore_2 = 0
                                else:
                                    negscore_3 += (negscore_1 + negscore_2)
                                    negscore_1 = 0
                                emo_index += 1
                            word_index += 1
                    pos_score = 0
                    neg_score = 0
                    if posscore_3 < 0 and negscore_3 > 0:
                        neg_score += (negscore_3 - posscore_3)
                        posscore_1 = 0
                    elif negscore_3 < 0 and posscore_3 > 0:
                        pos_score += (posscore_3 - negscore_3)
                        negscore_1 = 0
                    elif negscore_3 < 0 and posscore_3 < 0:
                        pos_score += -negscore_3
                        neg_score += -posscore_3
                    else:
                        pos_score += posscore_3
                        neg_score += negscore_3
                    count_1.append([pos_score, neg_score])
                count_2.append(count_1)
                count_1 = []
            count_3.append(count_2)
            count_2 = []
        return count_3