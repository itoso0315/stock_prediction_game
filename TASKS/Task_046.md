

# Task 046: 本物の株価データをChart Aへ表示する

## 目的
ダミーのローソク足データを廃止し、Yahoo Financeから取得した実際のOHLCデータをFlutterへ渡して表示する。

## 現状
- Flutterではローソク足を描画できる。
- Chart Aのみ表示できる。
- Backendはsample_questions.jsonの固定データを返している。

## 実装内容
1. yfinanceを利用して実際の株価データを取得する。
2. 問題生成時にcandlesへOHLCデータを格納する。
3. sample_questions.jsonのダミーcandlesを使わない構成に変更する。
4. APIレスポンスのJSON形式は変更しない（Flutter側の修正を不要にする）。
5. Chart Aで本物のローソク足が表示されることを確認する。

## 完了条件
- Chart Aに実在銘柄のローソク足が表示される。
- Flutter側の画面修正は不要。
- flutter analyze が成功する。
- flutter test が成功する。
- Backend起動確認を行う。

## 制約
- Chart B/Cはこのタスクでは変更しない。
- UIデザインは変更しない。
- Git commit・Git pushは行わない.