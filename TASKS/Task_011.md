# Task 011

## タイトル
観察期間を約6か月、予測期間を約1か月へ変更する

---

## 目的

ゲーム性と学習効果を高めるため、問題生成ルールを変更する。

現在は約3か月分のチャートを見て約3か月後を予測しているが、より実際の投資判断に近づけるため、約6か月分のチャートを観察し、約1か月後を予測するルールへ変更する。

変更理由は以下のとおり。

- 長期トレンドを読む力を養う
- 実際の投資判断に近い時間軸にする
- 約3か月後より約1か月後の方がテクニカル分析を学びやすい
- トレンド継続・押し目・ブレイクアウトなどの判断を学びやすくする

本Taskはゲームルールのみ変更し、UIデザインや学習機能追加は対象外とする。

---

## 実装対象

- `DISPLAY_TRADING_DAYS` を120へ変更
- `FORECAST_TRADING_DAYS` を20へ変更
- `generate_game_question()` に120日観察・20日予測ルールを適用
- `generate_question()` にも同じ120日観察・20日予測ルールを適用
- `select_common_window()` のデフォルト抽出件数を120へ変更
- 基準日・評価日の計算変更
- 問題画面説明文の更新
- 結果画面説明文の更新
- 関連Docstringの更新
- 境界値、再現性、入力非破壊、部分表示防止の動作確認

---

## 対象外

- AI解説
- テクニカル分析
- UIデザイン変更
- Session State変更
- 画面遷移変更
- 会社情報表示
- 新しいチャートUI
- データ取得方法変更
- 取得期間不足銘柄の自動差し替え
- READMEの更新
- 自動テストファイルの新規作成

---

## 作成・変更予定ファイル

### 変更予定

- game/question_generator.py
- app.py

変更しない

- ui/charts.py
- data配下
- README.md

### 新規作成

- なし

### 削除

- なし

---

## 実装内容

### 問題生成

- `DISPLAY_TRADING_DAYS = 120`
- `FORECAST_TRADING_DAYS = 20`
- `display_data` は3銘柄すべてに共通する連続120共通取引日
- `future_data` は基準日の次の共通取引日から始まる連続20共通取引日
- 3件の `display_data.index` は完全一致
- 3件の `future_data.index` は完全一致
- `base_date` は `display_data.index[-1]`
- `evaluation_date` は `future_data.index[-1]`
- `evaluation_date` は基準日の次の共通取引日を1日目として20共通取引日目
- `future_close` は `future_data.iloc[-1]["Close"]`
- 正解判定は既存どおり、未丸めの `future_return_percent` が最大のChartを正解とする
- 同率時のChart A/B/C優先ルールは変更しない
- 同一入力・同一乱数シードで同じ問題を再現できる
- 入力DataFrameを変更しない
- `display_data` と `future_data` は入力から独立したディープコピーとして保持する

#### 必要な共通取引日数

必要な最低共通取引日数は140件とする。

```text
120共通取引日（観察期間）
+ 20共通取引日（予測期間）
= 140共通取引日
```

境界条件：

- 139件以下：`ValueError`
- 140件：開始位置は0のみで正常生成
- 141件以上：`0` から `共通取引日数 - 140` までを有効開始位置とする

期間不足時の銘柄自動差し替えは行わず、既存の問題生成エラー処理へ委ねる。

### 問題画面

表示例

```text
観察期間：YYYY-MM-DD ～ YYYY-MM-DD
基準日（予測時点）：YYYY-MM-DD
観察データ：120共通取引日（おおむね約6か月）
```

3つのチャート直後・回答ボタン直前に、次の文言を表示する。

```text
📈 あなたが利用できる情報はここまでです。この先約1か月（20共通取引日）の値動きを予測してください。
```

### 結果画面

共通表示

```text
基準日：YYYY-MM-DD
評価日：YYYY-MM-DD（20共通取引日後・おおむね約1か月後）
```

各Chart

- 基準日終値
- 評価日終値
- 騰落率
- 20共通取引日の将来チャート

### 既存公開API・定数への適用範囲

新ルールは、期間定数を共有している既存APIすべてへ適用する。

対象：

- `generate_game_question()`
- `generate_question()`
- `select_common_window()` のデフォルト件数

既存公開APIの関数名、引数、戻り値、データクラスのフィールドは変更しない。

Task011でいう「既存公開APIを変更しない」とは、シグネチャを維持することを意味する。観察期間・予測期間・デフォルト抽出件数の意味上の変更は、Task011の意図した仕様変更として許容する。

### 既存Session Stateの扱い

Task011への更新前からブラウザに残っている60日観察・60日予測の旧 `game_question` は移行対象外とする。

実装・動作確認時はStreamlitサーバーを再起動し、新しいSession Stateで確認する。

旧問題の件数検出、自動破棄、Session State移行処理は追加しない。

---

## 受け入れ条件

- `DISPLAY_TRADING_DAYS == 120`
- `FORECAST_TRADING_DAYS == 20`
- `generate_game_question()` が120共通取引日観察・20共通取引日予測になる
- `generate_question()` も同じ120日・20日ルールになる
- `select_common_window()` のデフォルト抽出件数が120になる
- 3件の `display_data` が各120件
- 3件の `display_data.index` が完全一致
- 3件の `future_data` が各20件
- 3件の `future_data.index` が完全一致
- 139共通取引日以下で `ValueError`
- 140共通取引日で開始位置0として正常生成
- 141共通取引日で開始位置が0または1
- `base_date == display_data.index[-1]`
- `evaluation_date == future_data.index[-1]`
- 評価日が基準日の次から20共通取引日目
- `future_close` が `future_data` 最終日のCloseと一致
- 正解判定ロジックと同率時優先順位を変更しない
- 同一入力・同一乱数シードで同じ問題を再現できる
- 入力DataFrameを変更しない
- `display_data` と `future_data` が入力から独立している
- 問題画面に120共通取引日・おおむね約6か月と表示される
- 問題画面文言が約1か月・20共通取引日へ更新される
- 結果画面文言が20共通取引日後・おおむね約1か月後へ更新される
- 次の問題にも120日・20日ルールが適用される
- 共通取引日不足時の自動差し替えを行わない
- 既存の問題画面・結果画面の部分表示防止を維持する
- Session Stateのキーと状態遷移を変更しない
- 既存公開APIのシグネチャを変更しない
- `period="5y"` を維持する
- `ui/charts.py` と `data` 配下を変更しない
- READMEの古い期間説明はTask011では更新しない
- 自動テストファイルを新規作成しない
- `app.py` からyfinanceを直接利用しない
- Git管理対象の差分が `game/question_generator.py` と `app.py` だけである
- Python構文チェックが成功する
- `git diff --check` が成功する
- Streamlitが正常起動する

---

## 動作確認

- `DISPLAY_TRADING_DAYS == 120`
- `FORECAST_TRADING_DAYS == 20`
- 共通取引日139件で `ValueError`
- 共通取引日140件で正常生成
- 共通取引日141件で開始位置上限が1
- `display_data` が3件とも120件
- `future_data` が3件とも20件
- 3件の表示日付インデックスが完全一致
- 3件の将来日付インデックスが完全一致
- 基準日と表示最終日が一致
- 評価日と将来最終日が一致
- 評価日が基準日の次から20共通取引日目
- 基準日終値・評価日終値が正しい
- 正解が未丸め騰落率の最大Chartになる
- 同率時のChart A/B/C優先順位が維持される
- 同一シードで同じ問題を再現できる
- 入力DataFrameが変更されない
- 出力DataFrameが入力から独立している
- `select_common_window()` のデフォルト件数が120
- `generate_question()` も120日観察・20日予測になる
- 問題画面に120共通取引日・おおむね約6か月が表示される
- 問題画面の説明文が約1か月・20共通取引日になる
- 結果画面の評価日文言が20共通取引日後・おおむね約1か月後になる
- 次の問題も120日観察・20日予測になる
- 共通取引日不足時に自動差し替えを行わない
- 問題画面・結果画面のFigure失敗時に部分表示されない
- Task009の回答確定・次問題成功・失敗時の状態遷移が変わらない
- 新しいSession Stateキーが追加されていない
- `period="5y"` が維持される
- `ui/charts.py` と `data` 配下に差分がない
- 自動テストファイルが作成されていない
- Git管理対象の差分が `game/question_generator.py` と `app.py` だけ
- Python構文チェック成功
- `git diff --check` 成功
- Streamlit起動成功