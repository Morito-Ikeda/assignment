import pickle

import numpy as np
from sklearn.metrics import accuracy_score

from .classifier import NaiveBayes


# 交差検証をして平均精度を計算
def get_cv_accuracy(clf, data, K):

    print('--- {0}-fold cross validation ---'.format(K))

    n = len(data)
    scores = []
    for k in range(K):
        test_index = [i for i in range(int(n/K)*k, int(n/K)*(k+1))]
        train_index = list(set([i for i in range(n)]) - set(test_index))
        test_data = data[test_index]
        train_data = data[train_index]
        X_train = train_data[:, 0]
        X_test = test_data[:, 0]
        y_train = train_data[:, 1]
        y_test = test_data[:, 1]

        # 予測
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        # 精度を計算
        y_test = list(y_test)
        y_pred = list(y_pred)
        score = accuracy_score(y_true=y_test, y_pred=y_pred)
        scores.append(score)

    scores = np.array(scores)
    print('Accuracy: {0} (+/- {1})'.format(scores.mean(), 2*scores.std()))

    return


# # 分類器を学習させ、シリアライズ
def output_model(alpha, data_path, save_path):
    # (形態素解析済みのデータ + ラベル) をデシリアライズ
    with open(data_path, 'rb') as f:
        data = pickle.load(f)

    np.random.shuffle(data)

    print('\nTraining Model ...')

    # ナイーブベイズ分類
    nb = NaiveBayes(alpha)
    get_cv_accuracy(nb, data, K=10)

    # pickleで保存
    with open(save_path, 'wb') as f:
        pickle.dump(nb, f)

    return
