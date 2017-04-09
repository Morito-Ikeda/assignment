
# coding: utf-8

# In[1]:

import numpy
import MeCab
import urllib.request as req
import re
import numpy as np


# In[2]:

class Tokenizer(object):
    
    def __init__(self, dic, stopword=False):
        self.dic = dic
        self.stopword = stopword
        self.stoplist = []
        
        if self.stopword == True:
            self.stoplist = self._get_stoplist()
            
        self.mecab = MeCab.Tagger('-Ochasen -d ' + self.dic)
        
    def _get_stoplist(self):
        # nltkは日本語用のストップワード一覧がないため、SlothLibを使う
        slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
        res = req.urlopen(slothlib_path)
        stoplist = [line.decode('utf-8').strip() for line in res]

        return stoplist
    

    def tokenize(self, text):
        words = []
       
        self.mecab.parseToNode('')
        node = self.mecab.parseToNode(text)
        while node:
            feature = node.feature.split(',')
            word = feature[-3] # 基本形
            if word == '*':
                word = node.surface
                
            if word in ['http://', '編集部']:
                node = node.next
                continue
            
            # 一文字のアルファベットやひらがなを除去
            pattern = r"[a-zA-Zぁ-んァ-ン]{1}"
            ismatch = re.fullmatch(pattern, word)
            if ismatch:
                node = node.next
                continue
                
            # 〜月〜日を除く
            pattern = '\d{1,2}月\d{1,2}日'
            ismatch = re.fullmatch(pattern, word)
            if ismatch:
                node = node.next
                continue
            
            if feature[0] in ['名詞', '形容詞']  and feature[1] != '数':
                if word not in self.stoplist:
                    words.append(word)
                
            node = node.next
        
        # words = ' '.join(words)

        return words


# In[3]:

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


# In[ ]:



