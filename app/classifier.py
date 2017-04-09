import urllib.request as req
import urllib
from bs4 import BeautifulSoup

import sys
sys.path.append('/Users/ikedamorito/Desktop/Gunosy/assignment')
from utils import Tokenizer
import pickle
import numpy as np


# articleを解析器・分類器にかけ、結果(article_cat)を取得する関数
def classify(article):
    with open('./pkl_objects/naivebayes.pkl', 'rb') as f:
        model = pickle.load(f)
    t = Tokenizer(dic='/usr/local/lib/mecab/dic/mecab-ipadic-neologd/', stopword=False)
    words = t.tokenize(article)
    X = np.array(words)
    cat_num = model.predict(X)[0]
    cat_name = {
        0: 'IT・科学',
        1: 'おもしろ',
        2: 'エンタメ',
        3: 'グルメ',
        4: 'コラム',
        5: 'スポーツ',
        6: '国内',
        7: '海外'
    }
    article_cat = cat_name[cat_num]

    return article_cat

def get_cat(article_url):
    try:
        res = req.urlopen(article_url)
    except urllib.error.HTTPError:
        raise HTTPError('404 ERROR ! Page not Found')

    soup = BeautifulSoup(res, 'html.parser')
    article = soup.find(class_='article').text.strip()
    article_cat = classify(article)

    return article_cat
