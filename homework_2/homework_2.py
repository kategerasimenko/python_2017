from pattern.web import Wikipedia, plaintext
from nltk.util import ngrams
from string import punctuation
from collections import Counter
import codecs
import re

class WikiParser:
    def __init__(self):
        pass

    @staticmethod
    def clean_text(s):
        s = re.sub('['+re.escape(punctuation)+']+(?:\s|$)',' ',s)
        s = re.sub('(?:\s|^)['+re.escape(punctuation)+']+',' ',s)
        s = re.sub('\s+',' ',s)
        s = s.lower().strip()
        return s
        
    def get_articles(self, start, depth, max_count):
        article = Wikipedia().article(start)
        links = article.links
        list_of_strings = []
        for link in links:
            s = Wikipedia().article(link)
            if s is not None:
                s = self.clean_text(plaintext(s.source))
                list_of_strings.append(s)
        return list_of_strings

class TextStatistics:
    def __init__(self, articles):
        self.articles = articles
     
    def get_top_3grams(self, n):
        threegrams = []
        for a in self.articles:
            a = a.split()
            a = [x.strip(punctuation) for x in a
                 if re.search('[0-9]',x) is None]
            threegrams += ngrams(a,3)
        c = Counter(threegrams)
        top_n = c.most_common(n)
        list_of_3grams_in_descending_order_by_freq = [x[0] for x in top_n]
        list_of_their_corresponding_freq = [x[1] for x in top_n]
        return (list_of_3grams_in_descending_order_by_freq,
                list_of_their_corresponding_freq)
     
    def get_top_words(self, n):
        words = []
        with codecs.open('stop_words.txt','r',encoding='utf-8') as f:
            stop_words = {x.strip() for x in f.readlines()}
        for a in self.articles:
            a = a.split()
            a = [x.strip(punctuation) for x in a
                 if re.search('[0-9]',x) is None and x not in stop_words]
            words += a
        c = Counter(words)
        top_n = c.most_common(n)
        list_of_words_in_descending_order_by_freq = [x[0] for x in top_n]
        list_of_their_corresponding_freq = [x[1] for x in top_n]
        return (list_of_words_in_descending_order_by_freq,
                list_of_their_corresponding_freq)

class Experiment:
    def __init__(self):
        pass

    def show_results(self):
        parser = WikiParser()
        articles = parser.get_articles('Natural language processing',1,1)
        stats = TextStatistics(articles)
        a_stats = (stats.get_top_3grams(20),stats.get_top_words(20))
        res = 'top-20 n-grams for articles from NLP article:\n%s\n\ntop-20 n-grams for articles from NLP article:\n%s\n\n'
        print(res % ('\n'.join([' '.join(x)+' - '+str(y) for x,y in zip(*a_stats[0])]),
                     '\n'.join([x+' - '+str(y) for x,y in zip(*a_stats[1])])))
        
        nlp = Wikipedia().article('Natural language processing')
        nlp = [WikiParser.clean_text(plaintext(nlp.source))]
        stats = TextStatistics(nlp)
        nlp_stats = (stats.get_top_3grams(5),stats.get_top_words(5))
        res = 'top-5 n-grams for NLP article:\n%s\n\ntop-20 n-grams for NLP article:\n%s'
        print(res % ('\n'.join([' '.join(x)+' - '+str(y) for x,y in zip(*nlp_stats[0])]),
                     '\n'.join([x+' - '+str(y) for x,y in zip(*nlp_stats[1])])))


'''
top-20 n-grams for articles from NLP article:
natural language processing - 333
from the original - 306
archived from the - 296
v t e - 276
the original on - 238
the use of - 238
as well as - 223
one of the - 205
a b c - 186
proceedings of the - 182
cambridge university press - 158
the european union - 157
of the european - 155
such as the - 153
the number of - 143
a number of - 141
university press isbn - 140
for example the - 136
based on the - 133
a set of - 131

top-20 n-grams for articles from NLP article:
and - 16860
is - 8681
that - 4823
are - 4298
language - 3998
or - 3851
be - 3397
it - 2711
this - 2528
which - 2198
can - 1965
not - 1943
was - 1799
english - 1768
retrieved - 1721
speech - 1720
such - 1698
also - 1658
have - 1655
languages - 1642


top-5 n-grams for NLP article:
natural language processing - 16
a chunk of - 6
chunk of text - 6
of natural language - 5
systems based on - 4

top-20 n-grams for NLP article:
and - 72
language - 59
is - 48
natural - 39
such - 30
'''
    
