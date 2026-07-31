# TASK 001 - プロジェクト基盤構築

## 概要

Stock Trainer MVPの土台を構築してください。

今回の目的は、今後の開発で利用するデータ取得・問題生成・チャート表示の基盤を整えることです。

---

# Goal

以下を実現してください。

- Yahoo Financeから日本株データを取得できる
- 問題生成ロジックの土台を作る
- Plotlyでローソク足チャートを表示できる
- Streamlitが正常起動する

---

# 技術スタック

- Python 3.14
- Streamlit
- pandas
- yfinance
- plotly

---

# ディレクトリ構成

必要に応じて以下の構成へ整理してください。

```text
stock_prediction_game/
│
├── app.py
├── data/
│   └── downloader.py
├── game/
│   └── question_generator.py
├── ui/
│   ├── charts.py
│   └── result.py
├── utils/
├── requirements.txt
└── README.md
```

---

# 実装内容

## 1. Yahoo Financeデータ取得

`data/downloader.py` を作成してください。

機能:

- yfinanceを利用する
- 日本株の日足データを取得する
- Open / High / Low / Close / Volume を返す
- 関数化する
- 型ヒントとDocstringを付ける

---

## 2. 問題生成モジュール

`game/question_generator.py` を作成してください。

今回は以下を実装してください。

- ランダムな開始日を選択できる設計
- 60営業日分の表示データ
- その先約3か月後の騰落率を計算できる設計

※MVPなので実装しやすい構成を優先してください。

---

## 3. チャート表示

`ui/charts.py`

Plotlyで

- ローソク足チャート
- タイトルは Chart A
- 会社名は表示しない

を表示する関数を作成してください。

---

## 4. app.py

起動時は以下だけ表示してください。

- Stock Trainer
- 準備中...

正常起動することを確認してください。

---

# 今回は実装しない

- 回答画面
- 結果画面
- UIデザイン
- スコア
- AI解説
- 学習履歴

---

# コード品質

- 可読性を重視
- 関数を適切に分割
- 型ヒントを付ける
- Docstringを付ける
- 将来拡張しやすい設計

---

# Acceptance Criteria

- Streamlitが起動する
- Yahoo Financeから株価取得できる
- Plotlyでローソク足を表示できる
- エラーなく動作する
- ディレクトリ構成が整理されている

---

# PMメモ

Sprint 001では『まず遊べる土台を作る』ことを最優先とします。

デザイン性よりも、保守性・拡張性・読みやすさを重視してください。
