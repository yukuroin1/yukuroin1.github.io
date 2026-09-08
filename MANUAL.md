# yukuroin1.github.io サイト運用・執筆マニュアル

このドキュメントでは、本リポジトリで新しい記事（Markdown や HTML）を公開する方法や、デザイン・スタイル（`style.less`）を変更・調整する具体的な手順を解説します。

---

## 目次
1. [リポジトリの構成と基本方針](#1-リポジトリの構成と基本方針)
2. [記事を公開する手順（AIに依頼する / 最も簡単）](#2-記事を公開する手順aiに依頼する--最も簡単)
3. [記事を手動で公開する手順](#3-記事を手動で公開する手順)
4. [スタイル・デザインを変更する手順](#4-スタイルデザインを変更する手順)
5. [カラーテーマの利用方法](#5-カラーテーマの利用方法)
6. [更新前のローカル確認とトラブルシューティング](#6-更新前のローカル確認とトラブルシューティング)

---

## 1. リポジトリの構成と基本方針

本サイトは **GitHub Pages** を利用して自動公開されています。

```text
yukuroin1.github.io/
├── inbox/                  # 記事の投入口（AIに依頼する際、ここにファイルを置く）
├── content/                # 公開記事の配置先
│   ├── clinical-calc-hub/  # 例: 独立したHTMLツール
│   └── <slug>/             # 例: 新規記事（index.md または index.html）
├── PowerOfName/            # 既存のMarkdownコンテンツ
├── asset/                  # アイコン画像やコンパイル済みCSS
│   ├── icon.jpg
│   └── style.css           # style.less から生成された公開用CSS
├── _layouts/
│   └── default.html        # Markdownページ共通のレイアウト（style.cssを適用）
├── style.less              # Markdown用のスタイルシート原本（VS Codeプレビューと連動）
├── index.html              # サイトのトップページ（記事一覧カード）
├── scripts/
│   ├── build_style.py      # style.less を asset/style.css にコンパイルするスクリプト
│   └── check_site.py       # 文字コード・リンク切れ・スタイル同期を検査するスクリプト
├── AGENTS.md               # AIアシスタント向けの自動化作業指示書
├── MANUAL.md               # 本マニュアル（ユーザー向け操作ガイド）
└── README.md               # リポジトリ概要
```

---

## 2. 記事を公開する手順（AIに依頼する / 最も簡単）

記事の公開作業（URLの命名、配置、トップページへの追加、コミット＆プッシュ、公開確認）は、すべて **AIアシスタントに依頼するだけで自動完了** します。

### ステップ 1: `inbox/` に原稿を置く
公開したい原稿を [`inbox/`](inbox/) に入れます。ファイル名は日本語のままでも構いません。

- **単独の Markdown（`.md`）または HTML（`.html`）の場合**:
  そのまま `inbox/` に置きます。
  ```text
  inbox/
  └── 私の新しい記事.md
  ```

- **画像や関連ファイルがある場合**:
  記事ごとにフォルダを作成し、その中にまとめます。
  ```text
  inbox/
  └── my-article/
      ├── draft.md (または draft.html)
      ├── chart.png
      └── data.csv
  ```

### ステップ 2: AI に依頼する
チャット欄で次のように依頼します：

> **「inbox に入れたファイルを公開してください」**

### ステップ 3: AI が自動で実行する内容
1. `inbox/` 内のファイルを解析し、内容に合わせたタイトル・説明・URL名（`slug`）を決定。
2. `content/<slug>/index.md`（または `index.html`）へ移動し、相対リンクやフロントマターを整備。
3. [`index.html`](index.html) のカード一覧（`CONTENT-CARDS`）に新しい記事リンクを追加。
4. `scripts/check_site.py` で文字コードや内部リンクの破損がないか自動検証。
5. Git コミット＆プッシュを行い、GitHub Actions のデプロイ成功と公開URL（HTTP 200）を確認して報告。

---

## 3. 記事を手動で公開する手順

AI を使わず、自分で手動で公開作業を行う場合の手順です。

### ステップ 1: `content/<slug>/` フォルダを作成
英語のケバブケース（小文字英数字とハイフン）でフォルダを作ります。
（例: `content/cancer-genomics-intro/`）

### ステップ 2: 記事ファイル（`index.md` または `index.html`）を配置
- **Markdown（`index.md`）の場合**:
  先頭に以下の Front Matter（メタ情報）を UTF-8 で記載します：
  ```yaml
  ---
  layout: default
  title: 記事のタイトル
  description: 記事の簡潔な要約（1〜2文）
  theme: blue # 省略可（blue, orange, green, red, purple, brown, cyan, yellow）
  ---
  ```
- **HTML（`index.html`）の場合**:
  `<!DOCTYPE html>`、`lang="ja"`、`<meta charset="UTF-8">`、`<meta name="viewport">`、`<title>`、`<meta name="description">` を記述します。

### ステップ 3: トップページ（`index.html`）にカードを追加
[`index.html`](index.html) を開き、`<!-- CONTENT-CARDS:START -->` と `<!-- CONTENT-CARDS:END -->` の間にリスト項目を追加します：

```html
<li class="project-item">
    <a href="content/cancer-genomics-intro/" class="project-link">
        <div>
            <div class="project-name">記事のタイトル</div>
            <div class="project-desc">記事の簡潔な要約</div>
        </div>
        <span class="arrow">→</span>
    </a>
</li>
```
※ ディレクトリへのリンクは末尾に `/` を付けてください。

### ステップ 4: 検査とプッシュ
PowerShell で次のコマンドを実行します：

```powershell
# サイトの整合性チェック（文字コード、リンク、CSS同期）
python scripts/check_site.py

# Git コミットとプッシュ
git add content/ index.html
git commit -m "feat: 新しい記事を追加"
git push origin master
```

---

## 4. スタイル・デザインを変更する手順

Markdown のデザインは [`style.less`](style.less) で一元管理されています。
このファイルは、**VS Code の拡張機能「Markdown Preview Enhanced (MPE)」のプレビュー表示** と **GitHub Pages の公開表示** の両方に連動しています。

### 反映の流れ
```text
style.less (編集)
    │
    ├─► VS Code でのプレビュー (即座に反映)
    │
    └─► python scripts/build_style.py
            │
            ▼
        asset/style.css (GitHub Pages用の静的CSSに変換)
            │
            ▼
        git commit & push (公開サイトへ反映)
```

### 変更手順

1. **`style.less` を編集する**
   見出しのデザイン、フォントサイズ、余白、テーブルやコードブロックの見た目などを変更します。
2. **CSS へコンパイルする**
   以下のコマンドを実行すると、`style.less` から [`asset/style.css`](asset/style.css) が再生成されます：
   ```powershell
   python scripts/build_style.py
   ```
3. **整合性を検査する**
   ```powershell
   python scripts/check_site.py
   ```
   ※ `style.less` を編集したのに `build_style.py` を実行していない場合、チェッカーが未コンパイルを検知して警告を出します。
4. **プッシュして公開する**
   ```powershell
   git add style.less asset/style.css
   git commit -m "style: Markdownスタイルの調整"
   git push origin master
   ```

※ AI に「スタイルを変更したので反映してほしい」と伝えるだけで、コンパイル・検査・プッシュを代行させることもできます。

---

## 5. カラーテーマの利用方法

本サイトでは、統一された **8色の公式カラーパレット** が定義されています。

| テーマ名 (`theme`) | 色名 | RGB | HEX | 代表的な用途 |
| :--- | :--- | :--- | :--- | :--- |
| `blue` *(初期値)* | 青 | rgb(94, 129, 181) | `#5e81b5` | 標準テーマ、信頼・学術 |
| `orange` | 橙 | rgb(225, 156, 36) | `#e19c24` | 注意喚起、アクセント |
| `green` | 緑 | rgb(143, 177, 49) | `#8fb131` | 生物・自然、成功、完了 |
| `red` | 赤 | rgb(236, 98, 53) | `#ec6235` | 重要事項、警告 |
| `purple` | 紫 | rgb(135, 120, 179) | `#8778b3` | 考察、アドバンスド |
| `brown` | 茶 | rgb(197, 110, 26) | `#c56e1a` | 落ち着き、ログ、アーカイブ |
| `cyan` | 水 | rgb(93, 158, 200) | `#5d9ec8` | ツール、データ、計算 |
| `yellow` | 黄 | rgb(255, 191, 0) | `#ffbf00` | ハイライト、メモ |

### 記事単位でテーマカラーを切り替える
Markdown ファイルの Front Matter に `theme: <テーマ名>` を指定するだけで、見出しの下線・左バー、リンク色、引用枠の色が自動的に切り替わります。

```yaml
---
layout: default
title: 発生生物学ノート
theme: green
---
```

### 全体のデフォルトアクセントカラーを変更する
すべての記事の基本色を変更したい場合は、[`style.less`](style.less) の 19〜58 行目にある `@accent-primary` のコメントアウトを切り替えて `python scripts/build_style.py` を実行してください。

---

## 6. 更新前のローカル確認とトラブルシューティング

### ローカルでの動作確認

1. **文字コード・リンク・スタイル検査**:
   ```powershell
   python scripts/check_site.py
   ```
   エラー（文字コード異常、リンク切れ、未コンパイル）がないか数秒で確認できます。

2. **静的 HTML のプレビュー**:
   ```powershell
   python -m http.server 8000
   ```
   ブラウザで `http://localhost:8000/` を開くと、ローカルでトップページやHTMLツールを確認できます。

3. **Markdown のプレビュー**:
   - VS Code で対象の `.md` ファイルを開き、Markdown Preview Enhanced のプレビュー（`Ctrl + K` → `V`、または右上のプレビューボタン）を開くと、本番と同一のデザインでリアルタイムプレビューできます。

### よくあるトラブルと対処

- **Q: `check_site.py` で `style.less is newer than asset/style.css` と出る**
  - **A**: `style.less` を編集した後に CSS の再コンパイルが行われていません。`python scripts/build_style.py` を実行してください。
- **Q: `check_site.py` で `missing local target` と出る**
  - **A**: 内部リンク先（画像やページ）が存在しないか、パスが間違っています。ファイル名や相対パス（`/asset/...` など）を確認してください。
- **Q: push したのに公開サイトが変わらない**
  - **A**: GitHub リポジトリの **Actions** タブを開き、`pages build and deployment` が完了（緑のチェックマーク）になっているか確認してください。反映には 1〜2 分程度かかる場合があります。また、ブラウザのキャッシュ（スーパーリロード: `Ctrl + F5`）もお試しください。
