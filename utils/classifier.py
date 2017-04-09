import re
import urllib.request as req

import MeCab
import numpy as np


# tokenizeしたものを入力にする
class NaiveBayes(object):

    def __init__(self, alpha):
        self.words = set() # 総語彙数
        self.N_cat = {} # {'スポーツ': 101, 'IT・科学': 85, ...}
        self.N_cat_word = {} # {'スポーツ': {'野球': 2, 'サッカー': 3, ...}, 'IT・科学': {'パソコン': 5, 'スマホ': 2, ...}, ...}
        self.alpha = alpha
        self.den = {}


    def fit(self, docs, labels):
        for doc, label in zip(docs, labels):
            if not label in self.N_cat:
                self.N_cat[label] = 0
            self.N_cat[label] += 1

            for word in doc:
                self.words.add(word)
                if not label in self.N_cat_word:
                    self.N_cat_word[label] = {}
                if not word in self.N_cat_word[label]:
                    self.N_cat_word[label][word] = 0
                self.N_cat_word[label][word] += 1

        for cat in self.N_cat.keys():
            self.den[cat] = sum(self.N_cat.values()) + (self.alpha*len(self.words))


    def predict(self, docs):
        labels = []
        for doc in docs:
            maxv = -10**9
            best_label = None
            for cat in self.N_cat.keys():
                point = self._score(doc, cat)
                if point > maxv:
                    maxv = point
                    best_label = cat
            labels.append(best_label)
        labels = np.array(labels, dtype=object)

        return labels


    def _score(self, doc, label):
        score = self._cat_prob(label)
        for word in doc:
            score += np.log(self._word_prob(word, label))

        return score


    def _word_prob(self, word, label):
        if word not in self.N_cat_word[label]:
            self.N_cat_word[label][word] = 0

        return (self.N_cat_word[label][word] + self.alpha) / self.den[label]


    def _cat_prob(self, label):
        return self.N_cat[label] / sum(self.N_cat.values())
