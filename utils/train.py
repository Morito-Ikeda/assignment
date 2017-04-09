import picle

from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score

from .classifier import NaiveBayes

def output_model(alpha, data_path, save_path):
    with open(data_path, 'rb') as f:
        data = pickle.load(f)

    X = data[:, 0]
    y = data[:, 1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # ナイーブベイズ分類
    nb = NaiveBayes(alpha)
    nb.fit(X_train, y_train)
    y_pred = nb.predict(X_test)

    y_test = list(y_test)
    y_pred = list(y_pred)

    # 精度で評価
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    print('accuracy: {0}'.format(accuracy))

    # 学習した分類器をシリアライズ
    with open(save_path, 'wb') as f:
        pickle.dump(nb, f)

    return
