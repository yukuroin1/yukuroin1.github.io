# yukuroin1.github.io

[公開サイト](https://yukuroin1.github.io/)のソースです。`master` ブランチのルートが GitHub Pages から自動公開されます。

## ページを追加する

静的 HTML の場合は、ページごとにディレクトリを作り、その中へ `index.html` を置きます。

```text
NewPage/
└── index.html
```

Markdown の場合は、`index.md` の先頭に次の front matter を付けます。

```yaml
---
layout: default
title: ページのタイトル
description: ページの説明
---
```

その後、トップページの `Projects & Content` に `NewPage/` へのリンクを追加します。

## 更新を確認する

文字コードと内部リンクは、次のコマンドで公開前に確認できます。

```powershell
python scripts/check_site.py
```

静的 HTML は、リポジトリのルートで次を実行すると `http://localhost:8000/` から確認できます。

```powershell
python -m http.server 8000
```

Markdown を含む Jekyll の完成形は、push 後の GitHub Pages デプロイで確認します。`master` への push と pull request では、同じ文字コード・リンク検査が GitHub Actions でも自動実行されます。

## 公開する

```powershell
git add <更新したファイル>
git commit -m "ページの追加内容"
git push origin master
```

通常は数分で公開サイトへ反映されます。公開状況はリポジトリの **Actions** 画面にある `pages build and deployment` で確認できます。
