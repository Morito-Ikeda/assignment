# ナイーブベイズによる文書分類
ナイーブベイズ分類器を実装し、webアプリ上でURLを入力することで記事のカテゴリー判別をできるようにしました。

## 環境
・Python 3.5.2  
・Anaconda 4.2.0  
・Django 1.11

## 使用方法
assignmentディレクトリ上で操作を行います。

### 1. 学習用データのダウンロード(pickle形式)  
まずターミナルで

```terminal
./manage.py downloadTokenizedData [maxp] [save_path] [dict_path] [stopword]
```

と入力します。  
save_pathで指定した場所に、形態素解析やストップワード除去などを行ったニュース記事のデータが保存されます。

```
maxp: Gunosyニュースの各カテゴリページの最大取得ページ数
save_path: 取得・解析した記事の保存のパス
dict_path: 使用したいシステム辞書のパス(デフォルトはipadic)
stopword: データの解析時にSlothLibによるストップワードを使うかどうか
```

### 2. ナイーブベイズモデルの学習と保存(pickle形式)  
次に、先ほどダウンロードしたデータを使って学習を行います。  
ターミナルで

```terminal
./manage.py trainModel [alpha] [data_path] [save_path]
```

と入力します。

```
alpha: スムージングの係数
data_path: 処理済みのデータ(pickle)へのパス
save_path: 学習させたモデルを保存するパス
```

### 3. web上で記事分類アプリとして動かす
最後に、先ほどの学習済みモデルを使って、web上で記事分類アプリとして動かします。  
ターミナルで

```
./manage.py runserver
```

と入力すると、

```
http://127.0.0.1:8000/
```

でアプリが起動します。  
分類したいニュース記事のURLを入力することで、その記事の予測カテゴリーが表示されます。



