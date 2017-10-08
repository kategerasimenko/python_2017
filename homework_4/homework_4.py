# cложность, кажется, O(N(T+nP)), где N - кол-во паттернов,
# тк мы для каждого паттерна проделываем все то, что делали для одного паттерна в оригинальном алгоритме

import numpy as np
import unittest

def poly_hash(s, x=31, p=997):
    h = 0
    for j in range(len(s)-1, -1, -1):
        h = (h * x + ord(s[j]) + p) % p
    return h

def search_rabin_multi(text, patterns):
    """
    text - строка, в которой выполняется поиск
    patterns = [pattern_1, pattern_2, ..., pattern_n] - массив паттернов, которые нужно найти в строке text
    По аналогии с оригинальным алгоритмом, функция возвращает массив [indices_1, indices_2, ... indices_n]
    При этом indices_i - массив индексов [pos_1, pos_2, ... pos_n], с которых начинаетй pattern_i в строке text.
    Если pattern_i ни разу не встречается в строке text, ему соотвествует пустой массив, т.е. indices_i = []
    """
    p = 997
    x = 31
    indices = [list() for x in range(len(patterns))]
    hashes = {}
    pattern_idx = {x:i for i,x in enumerate(patterns)}
    min_len = min([len(x) for x in patterns])
    if len(text) < min_len:
        return indices
    
    # precompute hashes
    precomputed = np.zeros(((len(text) - min_len + 1),len(patterns)))

    for pattern in patterns:
        precomputed[len(text) - len(pattern)][pattern_idx[pattern]] = poly_hash(text[-len(pattern):], x, p)
        factor = 1
        for i in range(len(pattern)):
            factor = (factor*x + p) % p

        for i in range(len(text) - len(pattern)-1, -1, -1):
            precomputed[i][pattern_idx[pattern]] = (precomputed[i+1][pattern_idx[pattern]] * x +
                                                    ord(text[i]) - factor * ord(text[i+len(pattern)]) + p) % p

        hashes[pattern] = poly_hash(pattern, x, p)

    for i in range(len(precomputed)):
        for pattern,pattern_hash in hashes.items():
            if precomputed[i][pattern_idx[pattern]] == pattern_hash:
                if text[i: i + len(pattern)] == pattern:
                    indices[pattern_idx[pattern]].append(i)
    
    return indices


class TestRabinMulti(unittest.TestCase):
    def test_usual(self):
        self.assertEqual([[1]],search_rabin_multi('cab',['ab']))
        self.assertEqual([[1],[]],search_rabin_multi('cab',['ab','df']))
        self.assertEqual([[],[]],search_rabin_multi('cab',['ajdhg','df']))

    def test_many(self):
        self.assertEqual([[0],[2]],search_rabin_multi('abcd',['ab','cd']))
        self.assertEqual([[2],[0]],search_rabin_multi('abcd',['cd','ab']))

    def test_multiple(self):
        self.assertEqual([[0,4],[2,6]],search_rabin_multi('abcdabcd',['ab','cd']))

    def test_overlap(self):
        self.assertEqual([[0],[0]],search_rabin_multi('abacd',['ab','aba']))

    def test_overlap_hardcore(self):
        self.assertEqual([[0,1,2],[4]],search_rabin_multi('aaaaab',['aaa','ab']))

    def test_empty(self):
        self.assertEqual([[],[],[]],search_rabin_multi('a',['aaa','ab','sfg']))

    def test_empty_pattern(self):
        self.assertEqual([[]],search_rabin_multi('cab',['']))
    
        
unittest.main()
