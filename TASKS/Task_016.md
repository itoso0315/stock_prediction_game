# Task 016

## 1. タイトル

10問チャレンジと正答率70%目標の追加

## 2. 目的

現在のStock Trainerは、1問ずつ問題へ回答し、結果を確認して次の問題へ進む構成である。

Task016では、これを1セット10問のチャレンジ形式へ拡張する。

利用者は10問連続で回答し、チャレンジ終了時に次を確認できるようにする。

- 正解数
- 不正解数
- 正答率
- 目標70%を達成したか

今回のTaskでは、仮想資金、投資金額、損益、資産推移は導入しない。

回答方法はTask015までと同じく、各問題で次の4択から1つを選ぶ方式を維持する。

- Chart A
- Chart B
- Chart C
- どれにも投資しない（現金で保有）

## 3. ゲームルール

1チャレンジは10問で構成する。

各問題の正誤判定は、Task014までの既存ルールを維持する。

- Chart A/B/Cの未丸め将来騰落率を比較する
- 最大騰落率が0より大きい場合は、そのChartが正解
- 最大騰落率が0以下の場合は、現金保有が正解
- 正の同率最大はChart A、B、Cの順で先頭を優先する

1問正解するごとに正解数を1加算する。

10問終了時の正答率は次で計算する。

正答率 = 正解数 ÷ 10 × 100

目標は70%とする。

- 7問以上正解：目標達成
- 6問以下正解：目標未達成

## 4. 実装対象

- 10問を1チャレンジとして管理する
- 現在の問題番号を表示する
- 正解数を保持する
- 回答済み問題数を保持する
- 各問題の正誤をチャレンジ成績へ反映する
- 10問終了後にチャレンジ結果画面を表示する
- 正答率を表示する
- 目標70%の達成・未達成を表示する
- 新しい10問チャレンジを開始できるようにする
- 問題画面、1問ごとの結果画面、チャレンジ結果画面を明確に分離する
- Task015までの企業名・証券コード・Yahoo!ファイナンスリンクを維持する

## 5. 今回の対象外

- 仮想資金
- 1問ごとの投資金額
- 保有現金残高
- 損益金額
- 資産推移
- 複利計算
- リスク調整後リターン
- 投資比率
- 複数Chartへの分散投資
- スコアの永続保存
- 過去チャレンジ履歴
- ランキング
- ユーザー登録
- 難易度選択
- 制限時間
- 連続正解ボーナス
- AI解説
- ファンダメンタルズ情報
- 自動テストファイルの新規作成

資金を投資するゲーム形式は、Task016完了後の将来Taskで検討する。

## 6. 画面構成

Task016では、画面を次の3種類とする。

- `question`
- `result`
- `challenge_result`

### question

現在の問題へ回答する画面。

Task015までの問題画面を維持し、進捗表示を追加する。

### result

1問ごとの答え合わせ画面。

Task015までの結果画面を維持し、現在のチャレンジ成績と次の操作を追加する。

### challenge_result

10問すべて終了した後に表示するチャレンジ最終結果画面。

Chartや銘柄情報は表示せず、10問全体の成績を中心に表示する。

## 7. Session State

既存のSession Stateを維持する。

- `game_question`
- `answer_choice`
- `selected_label`
- `submitted`
- `current_view`

Task016では、次のアプリ状態用Session Stateキーを追加する。

- `challenge_question_number`
- `challenge_correct_count`
- `challenge_answered_count`

### challenge_question_number

現在表示中の問題番号を保持する。

- 初期値：`1`
- 許容値：`1`から`10`

### challenge_correct_count

現在のチャレンジにおける正解数を保持する。

- 初期値：`0`
- 許容値：`0`から`10`

### challenge_answered_count

現在のチャレンジで回答を確定した問題数を保持する。

- 初期値：`0`
- 許容値：`0`から`10`

### 状態間の不変条件

各状態は単独の範囲だけでなく、次の関係を必ず満たす。

```text
0 <= challenge_correct_count <= challenge_answered_count <= 10
```

画面ごとの有効状態は次とする。

#### question

```text
current_view = "question"
submitted = False
selected_label = None
challenge_answered_count = challenge_question_number - 1
1 <= challenge_question_number <= 10
```

#### result

```text
current_view = "result"
submitted = True
selected_label is not None
answer_choice = selected_label
challenge_answered_count = challenge_question_number
1 <= challenge_question_number <= 10
```

#### challenge_result

```text
current_view = "challenge_result"
submitted = True
selected_label is not None
answer_choice = selected_label
challenge_question_number = 10
challenge_answered_count = 10
0 <= challenge_correct_count <= 10
```

`challenge_result`では、10問目の`game_question`、`selected_label`、`answer_choice`をそのまま保持してよい。ただし、チャレンジ最終結果画面ではChart、企業情報、最後の回答内容を表示しない。

### 状態正規化

`normalize_session_state()`は`question`、`result`、`challenge_result`の3画面へ対応させる。

次のいずれかを満たさない状態は不正状態とする。

- `current_view`が3種類のいずれか
- 各カウンターが許容範囲内
- `challenge_correct_count <= challenge_answered_count`
- 画面ごとの不変条件を満たす

不正状態を検出した場合は、推測で一部だけ補正しない。現在のチャレンジを破棄し、次の初期状態へ一括で戻す。

```text
challenge_question_number = 1
challenge_correct_count = 0
challenge_answered_count = 0
answer_choice = None
selected_label = None
submitted = False
current_view = "question"
```

不正状態リセット時は既存の`game_question`も破棄し、新しい1問目を通常の問題生成処理で生成する。

不正状態リセット時の新しい1問目の生成に失敗した場合は、初期状態への一括更新を行わない。既存のSession Stateをそのまま維持し、画面には次の固定メッセージだけを表示する。

```text
チャレンジを初期化できませんでした。時間をおいて再度お試しください。
```

この場合は`st.rerun()`を呼ばず、次回の再実行時に再度初期化を試みる。

### Task015以前のSession Stateからの移行

Task016追加後、3つのチャレンジ状態キーのいずれかが存在しない場合は、Task015以前のSession Stateが残っているものとして扱う。

この場合は、古い回答状態や結果画面を引き継がず、新しい10問チャレンジとして初期化する。

- 既存の`game_question`を破棄する
- 既存5状態を初期状態へ戻す
- チャレンジ状態3件を初期化する
- 新しい1問目を生成する

サーバー再起動を必須とはしない。

旧Session Stateからの移行時も、新しい1問目の生成成功を確認してから8状態を一括更新する。

新しい1問目の生成に失敗した場合は、旧Session Stateを変更せず、次の固定メッセージだけを表示する。

```text
チャレンジを開始できませんでした。時間をおいて再度お試しください。
```

この場合は`st.rerun()`を呼ばず、次回の再実行時に再度移行処理を試みる。

## 8. 初期状態

アプリ初回起動時、または新しい10問チャレンジ開始時は次の状態とする。

- `challenge_question_number = 1`
- `challenge_correct_count = 0`
- `challenge_answered_count = 0`
- `answer_choice = None`
- `selected_label = None`
- `submitted = False`
- `current_view = "question"`

新しい問題を1件生成し、1問目として表示する。

## 9. 問題画面

Task015までの問題画面を維持する。

追加する表示：

- `問題 1 / 10`
- `現在の正解数：0`
- `目標：7問正解で70%`

問題番号は`challenge_question_number`を使用する。

現在の正解数は`challenge_correct_count`を使用する。

問題画面では、まだ回答していない現在問題の結果を正解数へ加算しない。

表示位置は、Stock Trainerのタイトル・サブタイトルの下、観察期間・基準日情報より前とする。

進捗表示はカード形式とし、次の3項目を横並びで表示する。

1. 現在の問題番号
2. 現在の正解数
3. 目標正答率

問題画面の匿名性を維持する。

次は表示しない。

- 企業名
- 証券コード
- ticker
- Yahoo!ファイナンスリンク
- 将来価格
- 将来騰落率
- `future_data`
- Figureタイトルは`Chart A/B/C`の匿名ラベルを維持する。
- 問題画面では`create_review_chart()`を呼ばない。
- 問題画面用Figure生成へ`future_data`を渡さない。

## 10. 回答確定

回答確定時の既存処理を維持する。

- `selected_label = answer_choice`
- `submitted = True`
- `current_view = "result"`

回答確定前に、次の条件をすべて検証する。

```text
submitted = False
current_view = "question"
challenge_answered_count = challenge_question_number - 1
answer_choice is not None
```

条件を満たす場合だけ正誤を判定し、次の5状態を1回の`st.session_state.update()`相当で原子的に更新する。

- `selected_label`
- `submitted`
- `current_view`
- `challenge_answered_count`
- `challenge_correct_count`

正解数は正解時だけ1増やし、不正解時は現在値をそのまま設定する。

コールバックとボタン戻り値の両方で成績更新を行わない。成績更新処理は回答確定ボタンの1か所だけに置く。

同じ問題で回答確定処理が重複実行されても、成績が二重加算されないようにする。

`submitted`が`False`から`True`へ変わる回答確定時だけ加算する。

未選択状態で回答ボタンを押した場合は、既存の警告を表示し、チャレンジ成績を変更しない。

## 11. 1問ごとの結果画面

Task015までの結果画面を維持する。

結果画面では、「🏆 結果発表」見出しの直後、基準日・評価日カードより前へチャレンジ進捗を追加する。

- 結果
- あなたの回答
- 正解
- 基準日・評価日
- 現金0.00%
- 現金正解時の補足
- Chart A/B/Cの企業名
- 証券コード
- Yahoo!ファイナンスリンク
- 基準日終値
- 評価日終値
- 騰落率
- Reviewチャート3件

結果画面上部へ、チャレンジ進捗を追加する。

表示例：

- `問題 1 / 10`
- `現在の成績：1問正解 / 1問回答`
- `現在の正答率：100%`
- `目標：70%`

現在の正答率は次で計算する。

`challenge_correct_count ÷ challenge_answered_count × 100`

`challenge_answered_count`が0の場合は0%とする。

## 12. 結果画面のボタン

### 1問目から9問目

結果画面下部のボタン文言を次とする。

`次の問題へ`

押下時に新しい問題を生成する。

新しい問題生成と表示用Figureの事前確認がすべて成功した場合だけ、次へ更新する。

- `game_question = 新しい問題`
- `challenge_question_number += 1`
- `answer_choice = None`
- `selected_label = None`
- `submitted = False`
- `current_view = "question"`

`challenge_correct_count`と`challenge_answered_count`は変更しない。

全状態の更新後に`st.rerun()`を1回だけ呼ぶ。

次の問題生成に失敗した場合：

- 既存の5状態を変更しない
- チャレンジ状態3件を変更しない
- 旧結果画面を維持する
- `st.rerun()`を呼ばない
- 再度ボタンを押せる

### 10問目

10問目の結果画面下部のボタン文言を次とする。

`10問の結果を見る`

遷移前に次の条件を検証する。

```text
challenge_question_number = 10
challenge_answered_count = 10
submitted = True
current_view = "result"
```

条件を満たさない場合は`challenge_result`へ遷移せず、不正状態として状態正規化のルールを適用する。

10問目の`game_question`、`selected_label`、`answer_choice`は保持し、問題番号を11へ増やさない。

押下時は新しい問題を生成せず、次へ更新する。

- `current_view = "challenge_result"`

更新後に`st.rerun()`を1回呼ぶ。

## 13. チャレンジ結果画面

10問終了時だけ表示する。

表示条件は次とする。

```text
current_view = "challenge_result"
submitted = True
selected_label is not None
answer_choice = selected_label
challenge_question_number = 10
challenge_answered_count = 10
0 <= challenge_correct_count <= 10
```

条件を満たさない場合はチャレンジ結果を表示せず、状態正規化のルールを適用する。

表示内容：

- `10問チャレンジ結果`
- `正解数：X / 10`
- `不正解数：Y / 10`
- `正答率：Z%`
- `目標：70%`

不正解数は次で計算する。

`10 - challenge_correct_count`

正答率は次で計算する。

`challenge_correct_count ÷ 10 × 100`

### 目標達成

正解数が7以上の場合：

- `🎉 目標達成！`
- `チャート判断の正答率70%以上を達成しました。`

緑系のカードで強調する。

### 目標未達成

正解数が6以下の場合：

- `あと少し！`
- `目標70%まで、あとN問です。`

`N = 7 - challenge_correct_count`

青またはオレンジ系のカードで表示し、失敗を過度に否定的に見せない。

## 14. チャレンジ結果画面のボタン

チャレンジ結果画面に次のボタンを1件表示する。

`もう一度10問に挑戦する`

押下時に、新しい1問目を事前生成する。

問題生成と表示用Figureの確認が成功した場合だけ、次の状態へ更新する。

- `challenge_question_number = 1`
- `challenge_correct_count = 0`
- `challenge_answered_count = 0`
- `game_question = 新しい問題`
- `answer_choice = None`
- `selected_label = None`
- `submitted = False`
- `current_view = "question"`

その後、`st.rerun()`を1回呼ぶ。

生成に失敗した場合：

- すべての状態を変更しない
- 旧チャレンジ結果画面を維持する
- `st.rerun()`を呼ばない
- 再度ボタンを押せる

## 15. 正答率表示

途中経過の正答率は次で計算する。

```python
accuracy_percent = round(
    challenge_correct_count / challenge_answered_count * 100
)
```

`challenge_answered_count == 0`の場合は0とする。

チャレンジ最終結果では分母を10に固定する。

```python
final_accuracy_percent = round(
    challenge_correct_count / 10 * 100
)
```

10問固定のため、最終正答率は10%刻みとなる。

目標達成判定は丸め後の正答率では行わない。必ず次で判定する。

```python
target_achieved = challenge_correct_count >= 7
```

## 16. UI・デザイン

現在の問題画面・結果画面のデザインシステムを維持する。

追加するチャレンジ進捗カードは、既存のカードUIと統一する。

進捗表示の推奨構成：

- 問題：`3 / 10`
- 正解数：`2問`
- 目標：`70%`

チャレンジ結果画面では、正解数と正答率を最も目立たせる。

70%達成時は緑、未達成時は青またはオレンジを使用する。

赤色は1問ごとの不正解表示に限定し、最終結果画面では利用者を強く否定する表現を避ける。

## 17. Figure事前生成と部分表示防止

Task009以降の部分表示防止を維持する。

### 次の問題

新しい問題を生成し、問題画面用Figure 3件の生成成功を確認してから状態を更新する。

### 新しいチャレンジ

新しい1問目を生成し、問題画面用Figure 3件の生成成功を確認してからチャレンジ状態を初期化する。

### 1問ごとの結果

Review Figure 3件と、次の表示情報をすべて準備してから描画を開始する。

- 企業情報
- Yahoo!ファイナンスURL
- 価格比較情報
- 問題番号
- 正解数
- 回答済み数
- 途中正答率
- 目標表示
- 結果画面下部のボタン文言

状態不変条件の検証も描画開始前に完了する。

失敗時はチャレンジ進捗を含む結果画面を部分表示しない。

### チャレンジ結果画面

チャレンジ結果画面では、状態不変条件の検証と表示準備の失敗を分けて扱う。

- 状態不変条件に違反した場合は、チャレンジ結果を表示せず、状態正規化のルールを適用する。
- 状態不変条件を満たしているが、正解数、不正解数、最終正答率、目標達成判定、あと何問かの表示文字列の計算または描画準備に失敗した場合は、Session Stateを変更せず、チャレンジ結果を部分表示しない。

後者の場合だけ、次の固定メッセージを表示する。

```text
チャレンジ結果を表示できませんでした。時間をおいて再度お試しください。
```

## 18. 既存機能への影響

次を維持する。

- Chart A/B/Cと現金保有の4択
- Task014の正解判定
- Task015の企業名・証券コード表示
- Yahoo!ファイナンスリンク
- 観察120共通取引日
- 予測20共通取引日
- `period="5y"`
- 問題画面の匿名性
- Reviewチャート3件
- 現金正解時の補足文
- 入力DataFrame非破壊
- 出力DataFrame独立性
- `create_candlestick_chart()`
- `create_review_chart()`
- `generate_game_question()`の公開シグネチャ
- `generate_question()`
- `select_common_window()`
- `calculate_return_percent()`

## 19. 変更予定ファイル

変更：

- `app.py`

変更しない：

- `game/question_generator.py`
- `ui/charts.py`
- `data`配下
- `README.md`

新規作成：

- なし

削除：

- なし

Task016はチャレンジ進行とUIの追加であり、問題生成ロジックやチャート生成ロジックの変更を必要としない。

## 20. 実装手順

1. 既存Session State初期化処理を確認する。
2. チャレンジ状態3件を追加する。
3. 回答確定時の正解数・回答数加算を追加する。
4. 二重加算を防止する。
5. 問題画面へ進捗カードを追加する。
6. 1問ごとの結果画面へ現在成績を追加する。
7. 1～9問目の「次の問題へ」を実装する。
8. 10問目の「10問の結果を見る」を実装する。
9. `challenge_result`画面を追加する。
10. 「もう一度10問に挑戦する」を実装する。
11. 次問題・新チャレンジ開始時の事前生成を維持する。
12. エラー時の状態不変・部分表示防止を確認する。
13. Task015までの画面と状態遷移を回帰確認する。
14. Python構文・差分・Streamlit起動を確認する。

## 21. 受け入れ条件

- 1チャレンジが10問である。
- 初期問題番号が1である。
- 10問目まで問題番号が正しく増える。
- 問題画面に`問題 X / 10`が表示される。
- 問題画面に現在の正解数が表示される。
- 問題画面に目標70%が表示される。
- 回答確定時に回答済み問題数が1回だけ増える。
- 正解時に正解数が1回だけ増える。
- 不正解時に正解数が増えない。
- 未選択回答時に成績が変わらない。
- 同じ問題で二重加算されない。
- 1問ごとの結果画面に現在成績が表示される。
- 1問ごとの結果画面に現在の正答率が表示される。
- 1～9問目では「次の問題へ」が表示される。
- 10問目では「10問の結果を見る」が表示される。
- 10問目終了後に新しい問題を生成しない。
- チャレンジ結果画面に正解数が表示される。
- チャレンジ結果画面に不正解数が表示される。
- チャレンジ結果画面に正答率が表示される。
- 7問以上正解で目標達成になる。
- 6問以下正解で目標未達成になる。
- 目標未達成時に目標まであと何問か表示される。
- 「もう一度10問に挑戦する」で成績がリセットされる。
- 新チャレンジが1問目から開始する。
- 次問題生成失敗時にすべての状態が不変である。
- 新チャレンジ生成失敗時にすべての状態が不変である。
- エラー時に`st.rerun()`を呼ばない。
- 問題画面の匿名性を維持する。
- 結果画面の企業情報・リンクを維持する。
- 現金保有を含む4択を維持する。
- 正解判定を変更しない。
- Reviewチャート3件を維持する。
- `period="5y"`を維持する。
- 新しいアプリ状態用Session Stateキーが指定3件だけである。
- `current_view`の許容値が`question`、`result`、`challenge_result`の3種類である。
- `0 <= challenge_correct_count <= challenge_answered_count <= 10`を常に満たす。
- question画面では`challenge_answered_count = challenge_question_number - 1`を満たす。
- result画面では`challenge_answered_count = challenge_question_number`を満たす。
- challenge_result画面では`challenge_question_number = challenge_answered_count = 10`を満たす。
- challenge_result画面では`submitted = True`を満たす。
- challenge_result画面では`selected_label is not None`を満たす。
- challenge_result画面では`answer_choice = selected_label`を満たす。
- Task015以前のSession Stateが残っている場合、新しい10問チャレンジとして安全に初期化される。
- 回答確定時の状態更新が1回の一括更新で行われる。
- 回答確定前にカウンター関係を検証する。
- 1～9問目の次問題成功後に`st.rerun()`を1回だけ呼ぶ。
- 次問題成功時に正解数と回答済み数を維持する。
- 10問目で問題番号が11にならない。
- 10問目の最後の問題・回答情報をchallenge_result遷移時に保持する。
- challenge_resultの状態不変条件違反時は、状態正規化のルールを適用する。
- challenge_resultが有効状態で表示計算または描画準備だけに失敗した場合は、Session Stateを変更せず、固定の結果表示用エラーメッセージだけを表示する。
- 1～9問目の次問題成功時に`st.rerun()`を1回だけ呼ぶ。
- 10問目で問題番号が11にならない。
- 10問目の最後の問題・回答情報をchallenge_result遷移時に保持する。
- challenge_resultではChart・企業情報・Yahoo!リンクを表示しない。
- 問題画面では`create_review_chart()`を呼ばない。
- 問題画面用Figureへ`future_data`を渡さない。
- Task015以前のSession Stateから安全に新チャレンジへ移行できる。

## 22. 動作確認

### 初期状態

- 問題番号が`1 / 10`である。
- 正解数が0である。
- 回答済み数が0である。
- 目標70%が表示される。

### 回答確定

- 正解時に正解数と回答済み数が1増える。
- 不正解時に回答済み数だけが1増える。
- 未選択回答時に成績が変わらない。
- 同じ結果画面の再描画で成績が増えない。
- 回答ボタンを連打しても成績が1回だけ増える。
- ブラウザを再読み込みしても成績が増えない。
- コールバックとbutton戻り値の両方で成績更新していない。
- 回答確定時の状態が1回の一括更新で反映される。

### 次の問題

- 1～9問目で新しい問題を生成できる。
- 問題番号だけが1増える。
- 正解数・回答済み数を維持する。
- 選択状態が未選択へ戻る。
- 次問題生成失敗時に全状態が不変である。
- 次問題生成失敗時に`st.rerun()`を呼ばない。
- 次問題成功時に正解数・回答済み数が変わらない。
- 問題番号と回答済み数の関係がquestion画面の不変条件と一致する。

### 10問目

- 10問目の結果画面に「10問の結果を見る」が表示される。
- 押下時に11問目を生成しない。
- `challenge_result`へ遷移する。
- 10問目で問題生成関数を呼ばない。
- 問題番号が11にならない。
- 最後の`game_question`、`selected_label`、`answer_choice`を保持する。

### チャレンジ結果

- 10問中0～10問の各正解数で正答率が正しい。
- 7問正解で70%・目標達成になる。
- 6問正解で60%・あと1問と表示される。
- 10問正解で100%になる。
- 不正解数が`10 - 正解数`と一致する。
- 10問未終了状態で`challenge_result`へ遷移しない。
- `challenge_result`ではChart、企業情報、Yahoo!リンクを表示しない。
- 不正なSession State値ではチャレンジ結果を表示せず、安全に新チャレンジへ初期化する。
- challenge_resultの状態不変条件違反時に、状態正規化のルールが適用される。
- challenge_resultが有効状態で表示計算または描画準備だけに失敗した場合、Session Stateを変更せず、固定の結果表示用エラーメッセージだけが表示される。
- challenge_resultで`submitted = True`を維持する。
- challenge_resultで`selected_label`を維持する。
- challenge_resultで`answer_choice = selected_label`を維持する。

### 新しいチャレンジ

- 再挑戦成功時に`challenge_question_number`が1へ戻る。
- 再挑戦成功時に`challenge_correct_count`が0へ戻る。
- 再挑戦成功時に`challenge_answered_count`が0へ戻る。
- 再挑戦成功時に4択が未選択へ戻る。
- 再挑戦成功時に新しい1問目へ切り替わる。
- 再挑戦成功時に8状態を1回の一括更新で反映する。
- 再挑戦成功時に`st.rerun()`を1回だけ呼ぶ。
- 再挑戦失敗時に8状態を変更しない。
- 再挑戦失敗時に旧challenge_resultを維持する。
- 再挑戦失敗時に`st.rerun()`を呼ばない。
- 再挑戦失敗後に再度ボタンを押せる。
- 不正状態リセット時の新問題生成失敗で既存状態を維持する。
- Task015以前からの移行時の新問題生成失敗で旧状態を維持する。

### 回帰確認

- 問題画面の4択を維持する。
- 現金保有の正解判定を維持する。
- 問題画面に企業情報が表示されない。
- 結果画面に企業名・証券コード・Yahoo!リンクが表示される。
- Reviewチャート3件が表示される。
- 基準日・評価日・価格・騰落率を維持する。
- `period="5y"`を維持する。
- `app.py`からyfinanceを直接利用しない。
- 問題画面で`create_review_chart()`を呼ばない。
- 問題画面用Figureへ`future_data`を渡さない。
- Task015以前のSession Stateから安全に新チャレンジへ移行できる。

### 静的確認

- Python構文チェック
- `git diff --check`
- Streamlit起動
- Task016としての差分が`app.py`だけ
- 自動テストファイルなし

## 23. 完了条件

10問を1セットとして連続回答でき、10問終了後に正解数・不正解数・正答率・70%目標の達成状況を確認できること。

`question`、`result`、`challenge_result`の各画面でSession Stateの不変条件を満たし、回答の二重加算、11問目の生成、不正な最終結果表示が発生しないこと。

Task015までの4択、匿名問題画面、企業情報、Yahoo!ファイナンスリンク、Reviewチャート、現金保有判定、既存UIを維持していること。

次問題、新チャレンジ、不正状態リセット、旧Session State移行の各処理で、事前生成失敗時に状態を部分更新せず、再試行可能であること。