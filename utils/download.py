import time
import pickle
import urllib.request as req
import urllib

from bs4 import BeautifulSoup
import numpy as np

from .processing import Tokenizer


category = ['エンタメ', 'スポーツ', 'おもしろ', '国内', '海外', 'コラム', 'IT・科学', 'グルメ']
cat_nums = {}
for i, cat in enumerate(category):
    cat_nums[cat] = i


def get_newsdata(maxp, save_path='../../../pkl_objects/data.pkl', dict_path=None, stopword=False):
    t = Tokenizer(dict_path, stopword)
    docs = []
    labels = []

    cat_urls = {}
    for i in range(8):
        cat = category[i]
        url = 'https://gunosy.com/categories/{0}'.format(i+1)
        cat_urls[cat] = url

    print('\ndownloading ...')

    for cat in cat_urls.keys():
        cat_url = cat_urls[cat]
        label = cat_nums[cat]

        for i in range(1, maxp+1):
            listpage_url = cat_url + '?page=' + str(i)
            res = req.urlopen(listpage_url)
            soup = BeautifulSoup(res, 'html.parser')
            a_list = soup.select('div.list_content > div.list_thumb > a')
            artcle_urls = [a.attrs['href'] for a in a_list if a != None]

            for article_url in artcle_urls:
                try:
                    res = req.urlopen(article_url)
                except urllib.error.HTTPError as e:
                    print('HTTPError ' + str(e.code))

                soup = BeautifulSoup(res, 'html.parser')
                article = soup.find(class_='article').text.strip()
                if article:
                    words = t.tokenize(article)
                    docs.append(words)
                    labels.append(label)

                time.sleep(0.5)

    docs = np.array(docs).reshape((-1, 1))
    labels = np.array(labels).reshape((-1, 1))

    data = np.hstack((docs, labels))
    np.random.shuffle(data)


    with open(save_path, 'wb') as f:
        pickle.dump(data, f)

    print('finished !')

    return
