import re
import urllib.request as req

import MeCab
import numpy as np


class Tokenizer(object):

    def __init__(self, dict_path=None, stopword=False):
        self.dict_path = dict_path
        self.stopword = stopword
        self.stoplist = []

        if self.stopword == True:
            self.stoplist = self._get_stoplist()

        if dict_path:
            self.mecab = MeCab.Tagger('-Ochasen -d ' + self.dict_path)
        else:
            self.mecab = MeCab.Tagger('-Ochasen')


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
