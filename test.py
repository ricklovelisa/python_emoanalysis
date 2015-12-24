import MySQLdb
import jieba
import codecs
import numpy

word_seg = jieba.lcut
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
            cur.execute("SELECT i_id, t_article FROM finance_news where i_id = 8")
        except Exception, e:
            print e
        temp = cur.fetchall()
        result_id = []
        result_article = []
        for line in temp:
            result_id.append(line[0])
            result_article.append(line[1])
        cur.close()
        conn.close()
        return [result_id, result_article]

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
        punt_list = '：，。！？；…'.decode('utf8')
        for punt in punt_list:
            paragraph = paragraph.replace(punt, u'\u3000')
        result = paragraph.split(u'\u3000')
        return result

# def word_seg(sent):
#
#         """sentence segmentation
#
#
#         Attributes:
#             no.
#         """
#         seg_list = jieba.lcut(sent)
#         return seg_list

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
            temps = []
            for word in temp.readlines():
                temps.append(word.replace('\r\n', ''))
            dict.append(temps)
            temp.close()
        return dict

def compute_sent_socre(word, dict, score):

        """sentiment score


        Attributes:
            no.
        """
        if word in dict[2]:
            score *= 2.0
        elif word in dict[3]:
            score *= 1.5
        elif word in dict[4]:
            score *= 1.25
        elif word in dict[5]:
            score *= 0.5
        elif word in dict[6]:
            score *= 0.25
        elif word in dict[7]:
            score *= -1
        return score

def transfrom_scores(p, n):

    if p < 0 and n >= 0:
        neg_count = n - p
        pos_count = 0
    elif n < 0 and p >= 0:
        pos_count = p - n
        neg_count = 0
    elif p < 0 and n < 0:
        neg_count = -p
        pos_count = -n
    else:
        pos_count = p
        neg_count = n
    if pos_count == 1:
        pos_count = 0
    if neg_count == 1:
        neg_count = 0
    return [pos_count, neg_count]


# text = ["我不是很喜欢北京天安门，但是我爱你。我讨厌你，非常非常讨厌！".decode('utf8'), "这样不好，你不要这样，真的不好".decode('utf8'), "这个东西不错，挺好的".decode('utf8')]
# dir = 'D:/dicts/'
# dict = get_dicts(dir)
# count_words = []
# count_sents = []
# count_para = []
# for para in text:
#     sents = sent_seg(para)
#     for sent in sents:
#         words = word_seg(sent)
#         i = 0  # index of counter
#         a = 0  # index of emo word
#         pos_count = 0
#         neg_count = 0
#         for word in words:
#             if word in dict[0]:
#                 pos_count += 1
#                 for w in words[a:i]:
#                     pos_count = compute_sent_socre(w, dict, pos_count)
#                 a = i + 1
#             elif word in dict[1]:
#                 neg_count += 1
#                 for w in words[a:i]:
#                     neg_count = compute_sent_socre(w, dict, pos_count)
#                 a = i + 1
#             i += 1
#         count_words.append(transfrom_scores(pos_count, neg_count))
#     count_sents.append(count_words)
#     count_words = []
# count_para.append(count_sents)
# count_sents = []
# print count_para




def sentiment_score(article, dict):

        """sentiment score


        Attributes:
            no.
        """
        count_sents = []
        count_paras = []
        count_articles = []
        ID = 1
        for text in article[1]:
            paras = paragraph_seg(text)
            for para in paras:
                sents = sent_seg(para)
                for sent in sents:
                    words = word_seg(sent)
                    i = 0  # index of counter
                    s = 0  # index of emo word
                    pos_score = 1
                    neg_score = 1
                    for word in words:
                        if word in dict[0]:
                            for w in words[s:i]:
                                pos_score = compute_sent_socre(w, dict, pos_score)
                            s = i + 1
                        elif word in dict[1]:
                            for w in words[s:i]:
                                neg_score = compute_sent_socre(w, dict, neg_score)
                            s = i + 1
                        i += 1
                    count_sents.append(transfrom_scores(pos_score, neg_score))
                count_paras.append(count_sents)
                count_sents = []
            count_articles.append(count_paras)
            count_paras = []
            print ID
            ID += 1
        # result = regroup_article(article[0], count_articles)
        # return result
        return count_articles

def statistic(array):

        """statistic computing


        Attributes:
            no.
        """
        np_temp = numpy.array(array)
        pos_mean = numpy.mean(np_temp[:, 0])
        neg_mean = numpy.mean(np_temp[:, 1])
        pos_std = numpy.std(np_temp[:, 0])
        neg_std = numpy.std(np_temp[:, 1])
        pos_sum = numpy.sum(np_temp[:, 0])
        neg_sum = numpy.sum(np_temp[:, 1])

        return {'sum':[pos_sum, neg_sum], 'mean':[pos_mean, neg_mean],
                'std':[pos_std, neg_std]}

def regroup_article(id, article):


    temp = zip(id, article)
    dic = {}
    for line in temp:
        dic[str(line[0])] = line[1]
    return dic

def compute_stat(array, arg):

    paras_stat = []
    articles_stat = []
    paras_stat_temp = []
    articles_stat_temp = []
    for i in array:
        for j in i:
            x = statistic(j)
            paras_stat_temp.append(x)
            articles_stat_temp.append(x['sum'])
        articles_stat.append(statistic(articles_stat_temp))
        paras_stat.append(paras_stat_temp)
        paras_stat_temp = []
    if arg == 'paras':
        return paras_stat
    elif arg == 'articles':
        return articles_stat
    else:
        print "invald arg.(it should be 'paras' or 'article')"


articles = get_text_from_MySQL()
dicts = get_dicts('D:/dicts/')
result = sentiment_score(articles, dicts)
stat = compute_stat(result, 'articles')
data = regroup_article(articles[0], stat)
print result