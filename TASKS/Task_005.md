# TASK 005 - 将来60営業日後の騰落率を持つ問題データを生成する

## 1. Taskの目的

Task004で作成した、3銘柄の共通60営業日のローソク足・出来高データに対して、各銘柄の将来60営業日後の騰落率を計算し、ゲーム1問分の問題データとしてまとめる。

このTaskでは、画面上の回答操作や正解発表は実装しない。

目的は、UIとは独立して「出題データ・将来結果・正解」を保持できるゲーム用データ構造を完成させることである。

---

## 2. ゴール

3銘柄について、以下を1つの問題データとして生成できること。

- Chart A / Chart B / Chart C の表示用60営業日データ
- 各Chartの証券コード
- 表示期間の開始日と終了日
- 表示開始日は `display_data.index[0]` から導出し、終了日は `base_date` とする
- 将来評価日
- 表示最終日の終値
- 将来評価日の終値
- 将来60営業日後の騰落率
- 3つの中で最も騰落率が高いChartラベル

画面表示はTask004の状態を維持し、将来情報や正解は利用者画面へ表示しない。

---

## 3. 予測期間の定義

- 表示期間は共通60営業日とする
- 基準日は表示期間の最終日とする
- 将来評価日は、基準日の次の共通取引日を1日目として数えた60営業日後とする
- 騰落率は、基準日の終値と将来評価日の終値から計算する

計算式：

```text
騰落率（%） = (将来評価日の終値 - 基準日の終値) / 基準日の終値 × 100
```

基準日の終値が0以下の場合は `ValueError` とする。

---

## 4. データ取得範囲

各銘柄の株価データは、表示用60営業日と将来評価用60営業日の両方を確保できる期間として取得する。

Task004と同様に `period="5y"` を使用する。

3銘柄すべてについて、以下を満たす共通取引日が必要である。

- 表示用60営業日
- その後の将来評価用60営業日

したがって、問題生成に必要な共通取引日は最低120件とする。

共通取引日が120件未満の場合は `ValueError` とする。

---

## 5. 問題データ構造

`game/question_generator.py` に、3銘柄の問題を表すデータクラスを追加する。

推奨構造：

```python
@dataclass(frozen=True)
class ChartQuestion:
    label: str
    ticker: str
    display_data: pd.DataFrame
    base_date: pd.Timestamp
    evaluation_date: pd.Timestamp
    base_close: float
    future_close: float
    future_return_percent: float


@dataclass(frozen=True)
class GameQuestion:
    charts: tuple[ChartQuestion, ChartQuestion, ChartQuestion]
    correct_label: str
```

要件：

- `ChartQuestion` は1銘柄分の問題情報を保持する
- `GameQuestion` はChart A / Chart B / Chart Cの3件を保持する
- 3件の順番は必ずChart A、Chart B、Chart Cとする
- `correct_label` は最も `future_return_percent` が高いChartのラベルとする
- データクラスは `frozen=True` とする
- 型ヒントとDocstringを付ける
- `display_data` は60営業日分のみを保持する
- `display_data` は入力DataFrameから独立したディープコピーとして保持する
- `frozen=True` は属性の再代入を防ぐために使用し、DataFrame内部の完全な不変性までは保証しない
- 将来評価用データ全体は保持しない
- 会社名は保持しない
- `ChartQuestion` と `GameQuestion` の不変条件は `generate_game_question()` が保証する
- データクラスへ `__post_init__()` は追加しない

---

## 6. 問題生成API

`game/question_generator.py` に、ゲーム1問分を生成する公開関数を追加する。

推奨API：

```python
def generate_game_question(
    tickers: tuple[str, str, str],
    price_frames: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    rng: random.Random | None = None,
) -> GameQuestion:
    ...
```

要件：

- `tickers` と `price_frames` は同じ順番で対応する
- 3銘柄分でない場合は `ValueError`
- 証券コードが重複している場合は `ValueError`
- 証券コードは空でない文字列であることを確認する
- 証券コードの4文字形式、大小文字、`.T` の有無の正規化はこの関数では行わず、呼び出し元が `NIKKEI_225_TICKERS` の値を渡す前提とする
- 空のDataFrameを含む場合は `ValueError`
- 各DataFrameには `Open / High / Low / Close / Volume` 列を必須とし、不足時は `ValueError`
- 日付インデックスに `NaT` が含まれる場合は `ValueError`
- 基準終値と将来終値は数値かつ有限値であることを確認する
- 基準終値が0以下の場合は `ValueError`
- 将来終値が0以下の場合も `ValueError`
- 入力DataFrameは変更しない
- Task004と同じ日付インデックス正規化ルールを利用する
- 3銘柄の日付インデックスの積集合を共通取引日とする
- 共通取引日が120件未満の場合は `ValueError`
- 有効な開始位置から表示用60営業日をランダムに選択する
- 同じ乱数シードでは同じ問題を再現できる
- `rng=None` の場合はPython標準のモジュールレベル `random` を使用する
- 3銘柄すべてで同じ表示期間・基準日・評価日を使用する
- Chartラベルは `("Chart A", "Chart B", "Chart C")` をゲーム層内の非公開定数として定義し、入力順に割り当てる
- `display_data` は必ず `copy(deep=True)` したものを保持する
- 既存の `calculate_return_percent()` を再利用する
- 既存の `DISPLAY_TRADING_DAYS` と `FORECAST_TRADING_DAYS` を再利用する
- 新たに同じ意味の定数を重複定義しない

---

## 7. 有効な開始位置

共通取引日を昇順に並べたものを使用する。

開始位置は、以下の両方を満たす範囲から選択する。

- 表示用60営業日を確保できる
- 表示期間終了後に将来評価用60営業日を確保できる

共通取引日数を `N` とした場合、有効な開始位置は次の範囲とする。

```text
0 以上、N - DISPLAY_TRADING_DAYS - FORECAST_TRADING_DAYS 以下
```

境界条件：

- 共通取引日が120件ちょうどの場合、開始位置は0のみ
- 共通取引日が121件以上の場合、有効な開始位置からランダムに選択
- 共通取引日が119件以下の場合、`ValueError`

---

## 8. 正解判定

`correct_label` は、3銘柄の `future_return_percent` を比較して決定する。

要件：

- 最も騰落率が高いChartラベルを正解とする
- 騰落率が最大値で完全に同じ銘柄が複数ある場合は、Chart A、Chart B、Chart Cの順で先に登場したものを正解とする
- 浮動小数点値は計算結果を保持し、表示用の丸めは行わない

---

## 9. app.pyへの組み込み

`app.py` ではTask003・Task004で使用している3銘柄選択と5年データ取得を維持し、`generate_game_question()` を呼び出す。

処理順：

1. 日経225から3銘柄を選択する
2. 3銘柄の株価データを `period="5y"` で取得する
3. `generate_game_question()` で問題データを生成する
4. 各 `ChartQuestion.display_data` からFigureを生成する
5. 3つのFigureをすべて生成する
6. すべて成功した後、Chart A / Chart B / Chart Cを縦方向に表示する

Task005では、以下を画面へ表示しない。

- 証券コード
- 会社名
- 基準日
- 評価日
- 基準終値
- 将来終値
- 将来騰落率
- 正解ラベル

Task005では、選択された銘柄で共通取引日120件を確保できない場合の自動再選択・差し替えは実装しない。

失敗時は部分表示せず、次のメッセージだけを表示する。

```text
問題データを生成できませんでした。時間をおいて再度お試しください。
```

例外詳細、会社名、証券コード、ティッカーは通常画面へ表示しない。

---

## 10. 既存APIとの整合性

以下の既存公開要素は削除・改名しない。

- `Question`
- `calculate_return_percent()`
- `generate_question()`
- `DISPLAY_TRADING_DAYS`
- `FORECAST_TRADING_DAYS`
- `select_random_tickers()`
- `select_common_window()`
- `normalize_japanese_ticker()`
- `download_daily_prices()`
- `create_candlestick_chart()`

Task005では、Task001の `Question` を削除しない。

`ChartQuestion` と `GameQuestion` は、3銘柄ゲーム用として新たに追加する。

---

## 11. 今回の対象外

- チャートの選択
- 回答ボタン
- 正解・不正解表示
- 将来チャートの表示
- 将来騰落率の画面表示
- 証券コード・会社名の公開
- Session State
- 次の問題ボタン
- スコア
- ランキング
- AI解説
- 移動平均線
- ボリンジャーバンド
- UIデザイン改善
- スマートフォン最適化
- 永続キャッシュ
- 自動テストファイルの新規作成

---

## 12. 作成・変更予定のファイル

変更予定：

- `app.py`
- `game/question_generator.py`

既存APIを利用：

- `data/downloader.py`
- `data/nikkei225.py`
- `ui/charts.py`

新規ファイル作成は予定しない。

---

## 13. 実装手順

1. `ChartQuestion` と `GameQuestion` を追加する
2. 入力値を検証する
3. 3銘柄の日付インデックスを正規化する
4. 共通取引日の積集合を求める
5. 共通取引日が120件以上あることを確認する
6. 有効な開始位置をランダムに選択する
7. 表示用60営業日を切り出す
8. 基準日と将来評価日を決定する
9. 各銘柄の基準終値と将来終値を取得する
10. 各銘柄の将来騰落率を計算する
11. 正解ラベルを決定する
12. `GameQuestion` を返す
13. `app.py` から問題生成APIを呼び出す
14. 表示用データだけをチャートとして表示する
15. 将来情報と正解が画面へ出ていないことを確認する
16. 構文チェックとStreamlit起動確認を行う

---

## 14. 受け入れ条件

以下をすべて満たした場合、Task005を完了とする。

- [ ] `ChartQuestion` が追加されている
- [ ] `GameQuestion` が追加されている
- [ ] 3件のChartがA/B/C順で保持される
- [ ] 各 `display_data` が60営業日分である
- [ ] 3件の表示期間の日付インデックスが完全に一致する
- [ ] 3件の基準日が一致する
- [ ] 3件の評価日が一致する
- [ ] 評価日が基準日の60共通取引日後である
- [ ] 各銘柄の基準終値が保持される
- [ ] 各銘柄の将来終値が保持される
- [ ] 各銘柄の将来騰落率が正しく計算される
- [ ] 最大騰落率のChartラベルが `correct_label` に設定される
- [ ] 最大騰落率が同値の場合はA/B/C順で先のChartが正解になる
- [ ] 同じ乱数シードで同じ問題を再現できる
- [ ] 共通取引日119件以下で `ValueError` となる
- [ ] 共通取引日120件ちょうどで正常生成される
- [ ] 入力DataFrameが変更されない
- [ ] `display_data` が入力DataFrameから独立したディープコピーである
- [ ] OHLCV列不足時に `ValueError` となる
- [ ] 日付インデックスに `NaT` が含まれる場合に `ValueError` となる
 - [ ] 基準終値または将来終値が非数値・非有限・0以下の場合に `ValueError` となる
 - [ ] 既存公開APIが維持される
 - [ ] 将来情報・正解・銘柄情報が画面に表示されない
 - [ ] 生成失敗時に部分表示されない
 - [ ] `app.py` からyfinanceを直接呼び出していない
 - [ ] 構文チェックが成功する
 - [ ] Streamlitが正常に起動する

---

## 15. 動作確認

1. 3銘柄分でない入力は `ValueError` となること
2. 重複した証券コードは `ValueError` となること
3. 空のDataFrameを含む場合は `ValueError` となること
4. 共通取引日119件では `ValueError` となること
5. 共通取引日120件では開始位置0で正常生成されること
6. 共通取引日121件以上では有効な開始位置が選ばれること
7. 同一シードで同じ問題になること
8. 3件の表示期間の日付インデックスが完全一致すること
9. 各表示データが60件であること
10. 基準日が表示期間の最終日であること
11. 評価日が基準日の60共通取引日後であること
12. 基準終値と将来終値が正しいこと
13. 騰落率が計算式どおりであること
14. 最大騰落率のChartが正解になること
15. 最大騰落率同値時にA/B/C順で先のChartが正解になること
16. 入力DataFrameが変更されないこと
17. `display_data` が入力DataFrameから独立したディープコピーであること
18. OHLCV列不足時に `ValueError` となること
19. 日付インデックスに `NaT` が含まれる場合に `ValueError` となること
20. 基準終値または将来終値が非数値・非有限・0以下の場合に `ValueError` となること
21. 画面に将来情報・正解・銘柄情報が表示されないこと
22. 生成失敗時に部分表示されないこと
23. 既存公開APIが維持されていること
24. Streamlitが正常起動すること

---

## 16. 残課題

Task006では、Chart A / Chart B / Chart Cを利用者が選択し、回答を確定できるUIを実装する予定とする。

Task007では、Task005で保持した将来騰落率と正解ラベルを利用して、正解・不正解と結果を表示する予定とする。