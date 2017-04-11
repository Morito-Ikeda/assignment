
# coding: utf-8

# In[1]:

import sys
import pickle

import numpy as np

sys.path.append('/Users/ikedamorito/Desktop/Gunosy/assignment')
from utils.classifier import NaiveBayes
from utils.train import get_cv_accuracy


# ## スムージングのパラメータをチューニング

# In[2]:

with open('../pkl_objects/processed_data.pkl', 'rb') as f:
    data = pickle.load(f)
np.random.shuffle(data)
    
# グリッドサーチ用のパラメータ
alphas = [1, 0.01, 0.05, 0.1, 0.5]

for alpha in alphas:
    # ナイーブベイズ分類
    nb = NaiveBayes(alpha)   

    # 10-fold cross validationの精度で評価
    get_cv_accuracy(nb, data, K=10)
    print('alpha = {0}\n'.format(alpha))


# In[ ]:



