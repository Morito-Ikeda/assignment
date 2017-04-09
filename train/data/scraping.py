
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import time
import os


# In[2]:

category = ['エンタメ', 'スポーツ', 'おもしろ', '国内', '海外', 'コラム', 'IT・科学', 'グルメ']
cat_urls = {}
for i in range(8):
    cat = category[i]
    url = 'https://gunosy.com/categories/{0}'.format(i+1)
    cat_urls[cat] = url


# In[3]:

cat_urls


# In[4]:

max_page = 45
for cat in cat_urls.keys():
    cat_url = cat_urls[cat]
    os.mkdir(cat)
    save_path = cat + '/' + 'articles.txt'
    
    for i in range(1, max_page+1):
        listpage_url = cat_url + '?page=' + str(i)
        res = req.urlopen(listpage_url)
        soup = BeautifulSoup(res, 'html.parser')
        a_list = soup.select('div.list_content > div.list_thumb > a')
        artcle_urls = [a.attrs['href'] for a in a_list if a != None]
        
        for article_url in artcle_urls:
            try:
                res = req.urlopen(article_url)
                soup = BeautifulSoup(res, 'html.parser')
                article = soup.find(class_='article').text.strip()
                article = article + '\n'
            except urllib.error.HTTPError as e:
                print('HTTPError ' + str(e.code))
            
            with open(save_path, 'a') as f:
                f.write(article)
            
            time.sleep(0.5)


# In[ ]:



