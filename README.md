# JCDb-scraper

[日本映画情報システム](https://www.japanese-cinema-db.jp/)から映画の情報をスクレイピングできます

## 環境構築

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## 実行方法

```sh
$ cd jcdb
$ scrapy crawl jcdb -o jcdb-movies.jsonlines
```
