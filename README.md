# Stock Trainer

実際の過去チャートを使い、テクニカル分析を学ぶためのアプリです。
Task 001では、株価データ取得・問題生成・ローソク足チャート生成の基盤と、
準備中画面のみを実装しています。

## 必要環境

- Python 3.14

## セットアップ

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## 起動

```bash
streamlit run app.py
```

ブラウザに「Stock Trainer」と「準備中...」が表示されます。

## モジュール構成

```text
app.py                       Streamlitのエントリーポイント
data/downloader.py           Yahoo Financeから日本株の日足OHLCVを取得
game/question_generator.py   60営業日の表示データと約3か月後の騰落率を生成
ui/charts.py                 Plotlyのローソク足チャートを生成
```

## 基盤モジュールの使用例

```python
from data.downloader import download_daily_prices
from game.question_generator import generate_question
from ui.charts import create_candlestick_chart

prices = download_daily_prices("7203", period="5y")
question = generate_question(prices)
figure = create_candlestick_chart(question.display_data)
```
