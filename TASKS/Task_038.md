

# Task 038

## タイトル

Python APIレスポンス設計を決める

---

## 目的

Flutter版Stock Trainerが将来Python APIと接続できるように、APIレスポンスの形を先に設計する。

本Taskでは、実際のAPI通信やFastAPI実装はまだ行わない。

まず、Python側がFlutterへ返すべきデータ構造を明確にする。

---

## 背景

Task036で、Flutter側の `Question` モデルは `Answer` リストを持つ構造になった。

Task037で、問題数表示は実データ件数に統一された。

これにより、Flutter側はAPI接続に向けた最低限の受け皿を持ち始めている。

次に必要なのは、Python APIがどのようなJSONを返すのかを決めること。

ここを曖昧にしたままAPI接続へ進むと、以下の問題が起きやすい。

- Flutter側でどの値をどこに入れるのか分からない
- Chart A/B/Cと銘柄データの紐づけが崩れる
- 正解判定の責任範囲が曖昧になる
- 結果発表画面に必要な情報が不足する
- チャート描画に必要なローソク足・出来高・移動平均線の形が揃わない
- 現金保有の扱いが曖昧になる

そのため、実装前にAPIレスポンスを設計する。

---

## 前提条件

- Task036が完了していること
- Task037が完了していること
- Flutter側に `Answer` モデルが存在すること
- Flutter側に `Question` モデルが存在すること
- Flutter側で3問のダミーデータが動作していること
- flutter analyze が成功していること
- flutter test が成功していること

---

## 対象

設計ドキュメント

必要に応じて、後続Taskで参照しやすいようにAPI仕様用のMarkdownを作成してもよい。

---

## 変更対象

- TASKS/Task_038.md

必要に応じて以下を作成してもよい。

- docs/API_RESPONSE_DESIGN.md

---

## 変更対象外

- Flutterコードの大幅変更
- Pythonコード
- FastAPI実装
- API通信
- yfinance取得処理
- 本物の株価取得
- チャート描画の本格実装
- 10問化
- AIひとこと解説の生成処理

---

## API設計方針

Python APIは、Flutterへ「ゲーム1回分の問題セット」を返す。

Flutter側は、そのレスポンスを受け取り、以下の流れで表示する。

```text
APIレスポンス
↓
Questionリストへ変換
↓
QuestionScreen
↓
AnswerReviewScreen
↓
ResultScreen
```

APIは、1問ずつ返すのではなく、まずは1ゲーム分の問題リストをまとめて返す想定とする。

理由：

- Flutter側の画面遷移が管理しやすい
- 途中で通信が失敗してゲームが止まるリスクを減らせる
- 現在のFlutter実装が `List<Question>` 前提で動いている
- MVPではリアルタイム性より安定性を優先する

---

## エンドポイント案

将来的なエンドポイントは以下を想定する。

```text
GET /api/questions
```

または、ゲーム開始時に条件を指定できるようにする場合は以下。

```text
GET /api/questions?count=10&market=nikkei225
```

MVPでは、まず固定条件でよい。

```text
GET /api/questions
```

---

## レスポンス全体構造

APIレスポンスは以下の構造を想定する。

```json
{
  "gameId": "sample-game-001",
  "questionCount": 3,
  "market": "nikkei225",
  "lookbackDays": 120,
  "evaluationDays": 20,
  "questions": []
}
```

### 各フィールドの意味

| フィールド | 型 | 説明 |
|---|---|---|
| gameId | string | ゲーム1回分のID |
| questionCount | number | 問題数 |
| market | string | 対象市場。MVPでは `nikkei225` |
| lookbackDays | number | 問題画面で見せる過去チャート期間 |
| evaluationDays | number | 何営業日後の騰落率で評価するか |
| questions | array | 問題リスト |

---

## Question構造

1問分の構造は以下を想定する。

```json
{
  "questionId": "q-001",
  "currentNumber": 1,
  "totalQuestions": 3,
  "baseDate": "2024-05-01",
  "evaluationDate": "2024-06-03",
  "choices": [],
  "correctChoiceLabel": "Chart B",
  "explanation": "Chart Bが最も高い騰落率でした。"
}
```

### 各フィールドの意味

| フィールド | 型 | 説明 |
|---|---|---|
| questionId | string | 問題ID |
| currentNumber | number | 何問目か |
| totalQuestions | number | 全問題数 |
| baseDate | string | 予測開始日 |
| evaluationDate | string | 評価日 |
| choices | array | Chart A/B/C/現金保有の選択肢 |
| correctChoiceLabel | string | 正解選択肢のlabel |
| explanation | string | 結果発表画面用のひとこと解説 |

---

## Choice構造

選択肢1つ分の構造は以下を想定する。

```json
{
  "label": "Chart A",
  "type": "stock",
  "ticker": "3099.T",
  "code": "3099",
  "companyName": "三越伊勢丹ホールディングス",
  "baseClose": 2733.5,
  "evaluationClose": 2631.5,
  "returnRate": -3.73,
  "yahooFinanceUrl": "https://finance.yahoo.co.jp/quote/3099.T/chart",
  "candles": [],
  "ma20": [],
  "ma40": [],
  "ma70": []
}
```

現金保有の場合は以下のようにする。

```json
{
  "label": "現金保有",
  "type": "cash",
  "ticker": null,
  "code": null,
  "companyName": "現金保有",
  "baseClose": null,
  "evaluationClose": null,
  "returnRate": 0,
  "yahooFinanceUrl": null,
  "candles": [],
  "ma20": [],
  "ma40": [],
  "ma70": []
}
```

### 各フィールドの意味

| フィールド | 型 | 説明 |
|---|---|---|
| label | string | `Chart A` / `Chart B` / `Chart C` / `現金保有` |
| type | string | `stock` または `cash` |
| ticker | string/null | yfinance用ティッカー。例：`3099.T` |
| code | string/null | 日本株コード。例：`3099` |
| companyName | string/null | 銘柄名 |
| baseClose | number/null | 予測開始日の終値 |
| evaluationClose | number/null | 評価日の終値 |
| returnRate | number | 騰落率。現金保有は0 |
| yahooFinanceUrl | string/null | Yahoo!ファイナンスのチャートURL |
| candles | array | ローソク足データ |
| ma20 | array | 20日移動平均線 |
| ma40 | array | 40日移動平均線 |
| ma70 | array | 70日移動平均線 |

---

## Candle構造

ローソク足データは以下の構造を想定する。

```json
{
  "date": "2024-05-01",
  "open": 2700.0,
  "high": 2760.0,
  "low": 2685.0,
  "close": 2733.5,
  "volume": 1234567
}
```

### 各フィールドの意味

| フィールド | 型 | 説明 |
|---|---|---|
| date | string | 日付 |
| open | number | 始値 |
| high | number | 高値 |
| low | number | 安値 |
| close | number | 終値 |
| volume | number | 出来高 |

---

## 移動平均線データ構造

移動平均線は、ローソク足の日付と対応できるようにする。

```json
{
  "date": "2024-05-01",
  "value": 2710.4
}
```

値が計算できない序盤の日付は、`null` を許容する。

```json
{
  "date": "2024-05-01",
  "value": null
}
```

---

## 正解判定の責任範囲

正解判定はPython API側で行う。

理由：

- 騰落率計算の基準をPython側に統一できる
- Flutter側で株価計算ロジックを持たなくてよい
- Flutter側は表示とユーザー操作に集中できる

Flutter側は、以下の値を使って判定する。

```text
selectedAnswerLabel == correctChoiceLabel
```

将来的にID方式へ移行する場合は、以下のようにする。

```text
selectedChoiceId == correctChoiceId
```

MVPではlabel判定を継続してよい。

---

## 現金保有の扱い

現金保有は、リターン0%の選択肢として扱う。

```text
returnRate: 0
```

株式3択すべてがマイナスの場合、現金保有が正解になる可能性がある。

例：

| 選択肢 | 騰落率 |
|---|---:|
| Chart A | -4.2% |
| Chart B | -1.8% |
| Chart C | -6.1% |
| 現金保有 | 0.0% |

この場合、正解は `現金保有`。

---

## 銘柄名の表示方針

問題画面では、銘柄名・コード・ティッカーを表示しない。

理由：

- 先入観を排除するため
- チャート形状だけで判断する学習ゲームにするため

結果発表画面では、銘柄名・コード・騰落率を表示してよい。

---

## Flutterモデルとの対応

現在のFlutterモデルとの対応は以下。

| API | Flutter |
|---|---|
| questions | List<Question> |
| choices | List<Answer> |
| correctChoiceLabel | correctAnswerLabel |
| label | Answer.label |
| type | Answer.type |
| ticker | Answer.ticker |
| companyName | Answer.companyName |
| baseClose | Answer.baseClose |
| evaluationClose | Answer.evaluationClose |
| returnRate | Answer.returnRate |

現時点では、Flutterの `Answer` モデルに `code`、`yahooFinanceUrl`、`candles`、`ma20`、`ma40`、`ma70` はまだ存在しない。

これらは後続Taskで追加する。

---

## サンプルレスポンス

```json
{
  "gameId": "sample-game-001",
  "questionCount": 3,
  "market": "nikkei225",
  "lookbackDays": 120,
  "evaluationDays": 20,
  "questions": [
    {
      "questionId": "q-001",
      "currentNumber": 1,
      "totalQuestions": 3,
      "baseDate": "2024-05-01",
      "evaluationDate": "2024-06-03",
      "choices": [
        {
          "label": "Chart A",
          "type": "stock",
          "ticker": "3099.T",
          "code": "3099",
          "companyName": "三越伊勢丹ホールディングス",
          "baseClose": 2733.5,
          "evaluationClose": 2631.5,
          "returnRate": -3.73,
          "yahooFinanceUrl": "https://finance.yahoo.co.jp/quote/3099.T/chart",
          "candles": [],
          "ma20": [],
          "ma40": [],
          "ma70": []
        },
        {
          "label": "Chart B",
          "type": "stock",
          "ticker": "6723.T",
          "code": "6723",
          "companyName": "ルネサスエレクトロニクス",
          "baseClose": 1662.5,
          "evaluationClose": 1871.0,
          "returnRate": 12.54,
          "yahooFinanceUrl": "https://finance.yahoo.co.jp/quote/6723.T/chart",
          "candles": [],
          "ma20": [],
          "ma40": [],
          "ma70": []
        },
        {
          "label": "Chart C",
          "type": "stock",
          "ticker": "7186.T",
          "code": "7186",
          "companyName": "横浜フィナンシャルグループ",
          "baseClose": 1118.0,
          "evaluationClose": 1109.5,
          "returnRate": -0.76,
          "yahooFinanceUrl": "https://finance.yahoo.co.jp/quote/7186.T/chart",
          "candles": [],
          "ma20": [],
          "ma40": [],
          "ma70": []
        },
        {
          "label": "現金保有",
          "type": "cash",
          "ticker": null,
          "code": null,
          "companyName": "現金保有",
          "baseClose": null,
          "evaluationClose": null,
          "returnRate": 0,
          "yahooFinanceUrl": null,
          "candles": [],
          "ma20": [],
          "ma40": [],
          "ma70": []
        }
      ],
      "correctChoiceLabel": "Chart B",
      "explanation": "Chart Bが最も高い騰落率でした。"
    }
  ]
}
```

---

## 後続Task案

### Task039

Flutter側にAPIレスポンス風JSONを読み込む処理を追加する。

実API通信ではなく、まずローカルのサンプルJSONを `Question` / `Answer` に変換する。

### Task040

Python側で実際のAPIエンドポイントを作成する。

### Task041

FlutterからPython APIへ接続する。

---

## 受け入れ条件

- Python APIがFlutterへ返すJSON構造が明文化されている
- Question単位の構造が明文化されている
- Choice単位の構造が明文化されている
- Candle構造が明文化されている
- 移動平均線データ構造が明文化されている
- 正解判定の責任範囲が明文化されている
- 現金保有の扱いが明文化されている
- 問題画面では銘柄名を隠す方針が明文化されている
- 結果発表画面では銘柄名・騰落率を出す方針が明文化されている
- 後続Task039以降の方向性が明文化されている

---

## 完了条件

- 受け入れ条件を満たす
- ChatGPTレビュー完了
- Git Commit
- Git Push