# ナイーブベイズによる文書分類
ナイーブベイズ分類器を実装し、webアプリ上でurlを入力することで記事のカテゴリー判別をできるようにした。

## 環境
・python 3.5.2

## 使用方法
assignmentディレクトリ上で操作を行います。

1. 学習用データのダウンロード(pickle形式)
ターミナルで

```
./manage.py downloadTokenizedData [maxp] [save_path] [dict_path] [stopword]
```

```
maxp: Gunosyニュースの各カテゴリページの最大取得ページ数
save_path: 取得・解析した記事の保存のパス
dict_path: 使用したいシステム辞書のパス(デフォルトはipadic)
stopword: データの解析時にSlothLibによるストップワードを使うかどうか
```


