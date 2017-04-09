
# coding: utf-8

# In[1]:

import sys
import glob

import numpy as np

sys.path.append('/Users/ikedamorito/Desktop/Gunosy/assignment')
from utils import Tokenizer, NaiveBayes


# In[2]:

cat_pathes = glob.glob('data/*/articles.txt')


# In[3]:

cat_pathes


# In[4]:

category = [path.split('/')[1] for path in cat_pathes]
cat_nums = {}
for i, cat in enumerate(category):
    cat_nums[cat] = i


# In[5]:

cat_nums


# In[6]:

docs = []
labels = []


# In[7]:

t = Tokenizer(dic='/usr/local/lib/mecab/dic/mecab-ipadic-neologd/', stopword=True)

for file_path in cat_pathes:
    cat = file_path.split('/')[1]
    label = cat_nums[cat]
    with open(file_path, 'r') as f:
        texts = f.readlines()
        for text in texts:
            words = t.tokenize(text)
            docs.append(words)
            labels.append(label)

docs = np.array(docs).reshape((-1, 1))
labels = np.array(labels).reshape((-1, 1))

data = np.hstack((docs, labels))
np.random.shuffle(data)


# In[8]:

import pickle
with open('../pkl_objects/processed_data.pkl', 'wb') as f:
    pickle.dump(data, f)

# In[9]:

with open('../pkl_objects/processed_data.pkl', 'rb') as f:
    data = pickle.load(f)

X = data[:, 0]
y = data[:, 1]

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# In[10]:

# ナイーブベイズ分類
nb = NaiveBayes(alpha=1)
nb.fit(X_train, y_train)
y_pred = nb.predict(X_test)


# In[11]:

y_test = list(y_test)
y_pred = list(y_pred)


# In[15]:

# 精度で評価
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
print('accuracy: {0}'.format(accuracy))


# In[16]:

# 学習した分類器をシリアライズ
import pickle
pickle.dump(nb, open('../pkl_objects/naivebayes.pkl', 'wb'), protocol=4)


# In[ ]:




# ## グリッドサーチとCVによるチューニング

# In[ ]:

# グリッドサーチ用のパラメータ

# dics = ['/usr/local/lib/mecab/dic/mecab-ipadic-neologd/', '/usr/local/lib/mecab/dic/ipadic/']


# In[ ]:

# 最も良かったモデルをpickleで保存
# それをwebアプリに搭載
# できればweb上でモデルのリアルタイム更新を可能にする
