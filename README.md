# yukuroin1.github.io

[公開サイト](https://yukuroin1.github.io/)のソースです。`master` ブランチのルートが GitHub Pages から自動公開されます。

## `inbox` から公開する

新しい Markdown、HTML、関連画像などを `inbox/` に置き、AIアシスタントへ次のように依頼します。

```text
inbox に入れたファイルを公開してください。
```

単独の `.md` または `.html` は、そのまま `inbox/` へ置けます。関連ファイルがある場合は、1ページ分を1つのサブフォルダへまとめます。

```text
inbox/
├── article.md
└── another-article/
    ├── draft.html
    └── figure.png
```

公開作業では、内容からタイトル・説明・URL名を決め、`content/<URL名>/` へ移動し、トップページへカードを追加します。検査後に `master` へpushし、GitHub Pagesの公開完了まで確認します。

`inbox/` はJekyllの公開対象と自動検査から除外されています。ファイルを置いただけでは公開されません。

記事の執筆やスタイル変更の全体的な手順は [**サイト運用・執筆マニュアル (`MANUAL.md`)**](MANUAL.md) をご覧ください。詳しい投入ルールは [`inbox/README.md`](inbox/README.md)、AIアシスタント向けの公開処理規則は [`AGENTS.md`](AGENTS.md) に記載しています。

## 更新を確認する

文字コード、内部リンク、および `style.less` と `asset/style.css` の同期は、次のコマンドで公開前に確認できます。

```powershell
python scripts/check_site.py
```

`style.less`（Markdown プレビュー用のスタイルシート）を編集した場合は、次のコマンドで `asset/style.css` へコンパイルします。

```powershell
python scripts/build_style.py
```

Markdown ページ（`.md`）の front matter に `theme: green` や `theme: orange` などを指定することで、アクセントカラーを8色（青・橙・緑・赤・紫・茶・水・黄）から切り替えることも可能です（初期値: `blue`）。

静的 HTML は、リポジトリのルートで次を実行すると `http://localhost:8000/` から確認できます。

```powershell
python -m http.server 8000
```

Markdown を含む Jekyll の完成形は、push 後の GitHub Pages デプロイで確認します。`master` への push と pull request では、同じ文字コード・リンク検査が GitHub Actions でも自動実行されます。

## 手動で公開する場合

```powershell
git add <更新したファイル>
git commit -m "ページの追加内容"
git push origin master
```

通常は数分で公開サイトへ反映されます。公開状況はリポジトリの **Actions** 画面にある `pages build and deployment` で確認できます。
