

# Task 045: FlutterでChart Aにローソク足チャートを1枚表示する

## 目的
FastAPIから受け取った株価データを使い、QuestionScreenのChart Aカード内に本物のローソク足チャートを1枚表示する。

## 現在地
- FlutterとFastAPIのHTTP通信は成功済み。
- QuestionScreenは `/api/questions` から問題データを取得している。
- Chart A/B/Cのカードは表示できている。
- 現在はカード中央に `Chart A` などの文字だけが表示されている。
- BackendのJSONには各選択肢ごとに `candles` があるが、現時点では空配列になっている。

## 実装方針
最初からChart A/B/Cすべてを変更せず、まずChart Aだけにローソク足チャートを表示する。
Chart Aで表示確認とテストができた後、次タスクでChart B/Cへ横展開する。

## 実装内容

### 1. Candleモデルを追加する
- Flutter側にローソク足1本分のデータモデルを追加する。
- 少なくとも以下の値を持つ。
  - date
  - open
  - high
  - low
  - close
- JSONから生成できる `fromJson` を実装する。

### 2. Answerモデルでcandlesを受け取れるようにする
- `Answer` に `List<Candle>` を追加する。
- `Answer.fromJson` で `candles` を変換する。
- `candles` が空配列でもクラッシュしないようにする。
- 既存の `ticker`、`companyName`、`returnRate` などの挙動を壊さない。

### 3. BackendのサンプルJSONにChart A用ローソク足データを追加する
- 1問目のChart Aに、表示確認用のローソク足データを追加する。
- 最初は10〜20本程度の固定データでよい。
- 日付順に並べる。
- 各ローソク足について以下を満たす。
  - high >= open
  - high >= close
  - low <= open
  - low <= close
- Chart B/Cの `candles` はこのタスクでは空配列のままでよい。

### 4. ローソク足描画Widgetを追加する
- Flutter標準の `CustomPainter` を使って描画する。
- 新しい外部チャートライブラリは追加しない。
- 1つのWidgetとして切り出す。
- ローソク足の実体とヒゲを描画する。
- 上昇足と下落足を見分けられるようにする。
- 背景や余白は既存のダークUIに合わせる。
- 軸ラベル、価格目盛り、出来高、移動平均線はこのタスクでは追加しない。

### 5. Chart Aカードだけ差し替える
- Chart Aのカード内で、文字だけのプレースホルダーをローソク足Widgetへ置き換える。
- Chart B/Cは現在の文字表示のまま残す。
- Chart Aカード下部のラベル `Chart A` は残す。
- カード選択、回答ボタン、画面遷移は変更しない。

### 6. 空データ時のフォールバックを維持する
- `candles` が空の場合は、現在と同じ `Chart A` の文字表示へ戻す。
- APIデータ不足で画面全体がクラッシュしないようにする。

### 7. テストを追加・更新する
少なくとも以下を確認する。
- CandleをJSONから生成できる。
- Answerがcandlesを読み込める。
- Chart Aにcandlesがある場合、ローソク足Widgetが表示される。
- Chart Aのcandlesが空の場合、文字プレースホルダーが表示される。
- 既存の回答・結果画面テストが壊れていない。

## 変更対象
- `frontend/lib/models/candle.dart`（新規）
- `frontend/lib/models/answer.dart`
- `frontend/lib/widgets/candlestick_chart.dart`（新規）
- Chartカードを描画している既存Widget
- `backend/sample_questions.json`
- 必要なテストファイル

## 変更しないもの
- Chart B/Cの表示
- 出来高
- MA20、MA40、MA70
- ズーム、スクロール、タップ操作
- Backendのエンドポイント仕様
- QuestionScreenのAPI取得処理
- 回答ロジック
- 結果画面のデザイン

## 完了条件
- macOS実機でQuestion 1を開いたとき、Chart Aカード内にローソク足が表示される。
- Chart B/Cは文字表示のまま維持される。
- Chart Aを選択して回答できる。
- 結果画面まで進める。
- `flutter analyze` が成功する。
- `flutter test` が全件成功する。
- FastAPI起動中に実機確認できる。

## 実装後の確認手順
1. FastAPIを起動する。
2. `/api/questions` の1問目Chart Aに `candles` が入っていることを確認する。
3. FlutterをmacOSで起動する。
4. Question 1を開く。
5. Chart Aカード内にローソク足が表示されることを確認する。
6. Chart B/Cは文字表示のままであることを確認する。
7. Chart Aを選び、回答から結果画面まで進める。

## 制約
- Task045の範囲外のリファクタリングをしない。
- UI全体のデザイン変更をしない。
- Chart B/Cへ横展開しない。
- 外部チャートライブラリを追加しない。
- Git commit、Git pushは行わない。