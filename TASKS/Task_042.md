# Task 042

## タイトル

Python側でFastAPIの最小APIを作る

---

## 目的

Flutterと接続するためのPython APIの最小構成を作る。

本Taskでは、本物の株価取得や問題生成はまだ行わない。

まずはPython側でFastAPIを起動し、Flutterが将来アクセスする予定の `/api/questions` エンドポイントから、固定のサンプルJSONを返せる状態にする。

---

## 背景

Task039で、FlutterはローカルJSONから `Question` リストを生成できるようになった。

Task040で、QuestionScreenは `QuestionJsonRepository` から問題を読み込むようになった。

Task041で、1ゲーム分のQuestionリストを画面間で持ち回れるようになった。

これにより、Flutter側は以下の状態まで来ている。

```text
ローカルJSON
↓
QuestionJsonRepository
↓
QuestionScreen
↓
AnswerReviewScreen
↓
ResultScreen
```

次に行うべきことは、ローカルJSONの取得元をPython APIへ近づけることである。

ただし、いきなり本物の株価取得やランダム問題生成まで行うと、問題発生時の切り分けが難しくなる。

そのため本Taskでは、まずPython側に最小APIを作り、固定JSONを返すところまでに限定する。

---

## 前提条件

- Task041が完了していること
- Flutter側でローカルJSON読み込みが成功していること
- `sample_questions.json` が存在すること
- Flutter側の `Question.fromJson` / `Answer.fromJson` が実装済みであること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

Backend（Python）

---

## 変更対象

想定変更対象は以下。

- backend/main.py
- backend/sample_questions.json
- backend/requirements.txt

必要に応じて以下を作成してよい。

- backend/README.md

---

## 変更対象外

- Flutterの大幅変更
- FlutterからのHTTP接続
- yfinance取得処理
- 本物の株価データ取得
- ランダム問題生成
- チャート描画の本格実装
- 10問化
- デプロイ
- 認証
- DB接続

---

## 実装方針

Python側に `backend` ディレクトリを作成し、FastAPIの最小構成を置く。

APIはまず以下の1本でよい。

```text
GET /api/questions
```

このエンドポイントは、固定の `sample_questions.json` を読み込み、そのままJSONとして返す。

---

## ディレクトリ構成案

```text
stock_prediction_game/
├── backend/
│   ├── main.py
│   ├── sample_questions.json
│   └── requirements.txt
└── frontend/
```

---

## main.py 方針

FastAPIアプリを作成する。

想定コード：

```python
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Stock Trainer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_QUESTIONS_PATH = BASE_DIR / "sample_questions.json"


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/questions")
def get_questions():
    with SAMPLE_QUESTIONS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)
```

---

## requirements.txt 方針

最小構成は以下。

```text
fastapi
uvicorn[standard]
```

---

## sample_questions.json 方針

まずはFlutter側で使っている以下のJSONと同じ内容をコピーする。

```text
frontend/assets/sample_questions.json
```

コピー先：

```text
backend/sample_questions.json
```

本Taskでは内容を変えない。

理由：

- Flutter側で既に読み込み確認済みのJSONを使うため
- API側の問題とJSON構造の問題を切り分けやすくするため

---

## 起動コマンド

backendディレクトリで以下を実行する想定。

```bash
cd ~/Python/stock_prediction_game/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

---

## 動作確認

API起動後、ブラウザまたはターミナルで確認する。

### health確認

```text
http://127.0.0.1:8000/api/health
```

期待値：

```json
{"status":"ok"}
```

### questions確認

```text
http://127.0.0.1:8000/api/questions
```

期待値：

- `gameId` が返る
- `questions` が返る
- `questions` が3件ある
- `choices` が含まれる
- `correctChoiceLabel` が含まれる

---

## テスト方針

本TaskではPython側の自動テストは必須にしない。

まずはFastAPIを起動し、ブラウザでレスポンス確認できればよい。

ただし、余裕があれば後続TaskでAPIテストを追加する。

---

## 受け入れ条件

- `backend/main.py` が存在する
- `backend/requirements.txt` が存在する
- `backend/sample_questions.json` が存在する
- FastAPIアプリを起動できる
- `/api/health` が `{"status":"ok"}` を返す
- `/api/questions` がサンプル問題JSONを返す
- CORS設定が入っている
- 本物の株価取得はまだ実装していない
- FlutterからのHTTP接続はまだ実装していない

---

## 後続Task案

### Task043

Flutter側にHTTP API Repositoryを追加する。

### Task044

QuestionScreenをAPI Repositoryに切り替えられるようにする。

### Task045

FlutterからPython APIへ接続し、API由来の問題でゲームを開始する。

### Task046

Python側でyfinance取得処理の土台を作る。

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commitはまだ不要
- Git Pushは1日の最後にまとめて行う
