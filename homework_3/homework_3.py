from pattern.web import Wikipedia, plaintext
from nltk.util import ngrams
from string import punctuation
from collections import Counter, defaultdict
import unittest
from numpy import log
import codecs
import re


def clean_text(s):
    intro_punc = '"#$%&\'()*+,-/:;<=>@[\\]^_`{|}~'
    s = re.sub('['+re.escape(intro_punc)+']+(?:\s|$)',' ',s)
    s = re.sub('(?:\s|^)['+re.escape(intro_punc)+']+',' ',s)
    s = re.sub('\s+',' ',s)
    s = s.lower().strip()
    return s


class WikiParser:
    def __init__(self):
        pass
  
    def get_articles(self, start, depth, max_count):
        article = Wikipedia().article(start)
        links = article.links
        list_of_strings = []
        for link in links:
            s = Wikipedia().article(link)
            if s is not None:
                s = clean_text(plaintext(s.source))
                list_of_strings.append(s)
        return list_of_strings


class TextStatistics:
    def __init__(self, articles):
        self.articles = articles
     
    def get_top_3grams(self, n, use_idf):
        num_sents = 0
        freqs = defaultdict(float)
        sent_freq = defaultdict(float)
        for a in self.articles:
            a = clean_text(a)
            sents = [x for x in re.split('[.?!]',a) if x]
            num_sents += len(sents)
            for sent in sents:
                threegrams = [''.join(x) for x in ngrams(sent,3)]
                c = Counter(threegrams)
                for ngram,freq in c.items():
                    freqs[ngram] += freq
                    sent_freq[ngram] += 1
        if use_idf and num_sents > 1:
            for ngram in freqs.keys():
                idf = log(num_sents / sent_freq[ngram])
                freqs[ngram] *= idf
        elif num_sents == 1:
            print('There is only one sentence in the list and IDF coefficient will not be used.')
        top_n = sorted(freqs.items(),key=lambda x: (-x[1],x[0]))[:n]
        list_of_3grams_in_descending_order_by_freq = [x[0] for x in top_n]
        list_of_their_corresponding_freq = [x[1] for x in top_n]        
        return (list_of_3grams_in_descending_order_by_freq,
                list_of_their_corresponding_freq)
     
    def get_top_words(self, n, use_idf):
        freqs = defaultdict(float)
        art_freq = defaultdict(float)
        num_art = len(self.articles)
        with codecs.open('stop_words.txt','r',encoding='utf-8') as f:
            stop_words = {x.strip() for x in f.readlines()}
        for a in self.articles:
            a = clean_text(a)
            words = a.split()
            words = [x.strip(punctuation) for x in words
                 if re.search('[0-9]',x) is None and x not in stop_words]
            c = Counter(words)
            for word,freq in c.items():
                freqs[word] += freq
                art_freq[word] += 1
        if use_idf and num_art > 1:
            for word in freqs.keys():
                idf = log(num_art / art_freq[word])
                freqs[word] *= idf
        elif num_art == 1:
            print('There is only one article in the list and IDF coefficient will not be used.')
        top_n = sorted(freqs.items(),key=lambda x: (-x[1],x[0]))[:n]
        list_of_words_in_descending_order_by_freq = [x[0] for x in top_n]
        list_of_their_corresponding_freq = [x[1] for x in top_n]
        return (list_of_words_in_descending_order_by_freq,
                list_of_their_corresponding_freq)


class TestTextStatistics(unittest.TestCase):
    def test_empty_array(self):
        ts = TextStatistics([])
        self.assertFalse(any(ts.get_top_3grams(3,False)))
        self.assertFalse(any(ts.get_top_words(3,False)))

    def test_one_item(self):
        ts = TextStatistics(['This is the only article and the only sentence and IDF coef should not be applied to it.'])
        self.assertEqual(ts.get_top_3grams(3,False),ts.get_top_3grams(3,True))
        self.assertEqual(ts.get_top_words(3,False),ts.get_top_words(3,True))

    def test_abs_counts(self):
        articles = ['I am Sam.',
                    'We adore sam',
                    'I am a student and I adore Sam!']
        ts = TextStatistics(articles)
        result_words = (['i','sam','adore','am'],[3.0,3.0,2.0,2.0])
        result_ngrams = ([' sa','i a','sam'],[3.0,3.0,3.0])
        self.assertEqual(result_words,ts.get_top_words(4,False))
        self.assertEqual(result_ngrams,ts.get_top_3grams(3,False))

    def test_idf_counts(self):
        articles = ['I am Sam.',
                    'We like sam',
                    'I am a student and I like Sam!']
        ts = TextStatistics(articles)
        result_words = (['i','and'],[1.2163953243244932,1.0986122886681098])
        self.assertEqual(result_words[0],ts.get_top_words(2,True)[0]) 
        self.assertAlmostEqual(result_words[1],ts.get_top_words(2,True)[1])  


class Experiment:
    def __init__(self):
        pass

    def show_results(self):
        parser = WikiParser()
        articles = parser.get_articles('Natural language processing',1,1)
        stats = TextStatistics(articles)
        a_stats = (stats.get_top_3grams(20,use_idf=True),
                   stats.get_top_words(20,use_idf=True))
        res = 'top-20 n-grams for articles from NLP article:\n%s\n\ntop-20 words for articles from NLP article:\n%s'
        print(res % ('\n'.join([x+' - '+str(y) for x,y in zip(*a_stats[0])]),
                     '\n'.join([x+' - '+str(y) for x,y in zip(*a_stats[1])])))


'''
top-20 n-grams for articles from NLP article:
 th - 49795.9627851
the - 46322.9236924
he  - 40710.7721979
ion - 37664.7269134
tio - 35442.3528353
ing - 34591.4748179
 in - 34499.8703888
on  - 33593.0601054
ati - 32347.8819629
 of - 32113.4823802
ng  - 32100.1441887
of  - 31293.6360498
 an - 31110.9355395
ed  - 31060.6306166
al  - 30634.7810893
 co - 30480.138641
es  - 29456.1082544
and - 29107.0575038
nd  - 29003.9794951
ent - 27980.3644202

top-20 words for articles from NLP article:
displaystyle - 2311.94885518
turing - 1703.8264438
arabic - 1097.63128411
chomsky - 869.972382725
x - 860.266283207
eu - 840.665673133
tone - 820.52124803
german - 815.170318192
learning - 803.131014984
languages - 791.60546464
european - 786.174821387
english - 760.881182402
turkish - 736.644570723
spanish - 712.556730277
retrieved - 711.970140068
union - 706.694718187
verbs - 684.81316982
speech - 669.431890047
dialects - 663.072877938
french - 653.642223083
'''
    
