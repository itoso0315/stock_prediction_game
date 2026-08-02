

# Task 018

## 1. Task名

Flutter開発環境構築とStock Trainer初回起動

## 2. Sprint

Sprint 3：Flutterによるアプリ化

## 3. 目的

現在のStock TrainerはPythonとStreamlitで実装されている。

Sprint 3では、既存のPython版を維持したまま、スマートフォン向けUIをFlutterで構築していく。

Task018では、その最初の作業としてFlutter開発環境を整え、Flutter版Stock Trainerの新規プロジェクトを作成し、Mac上で初回画面を起動できる状態にする。

このTaskの目的は、既存機能の移植ではなく、今後Flutterで画面を実装していくための安全な土台を作ることである。

## 4. 基本方針

既存のPython版Stock Trainerは変更しない。

Flutter版は、現在のPythonプロジェクトとは別のフォルダへ作成する。

推奨構成：

```text
/Users/Soichiro/Python/
├── stock_prediction_game/     # 既存のPython・Streamlit版
└── stock_trainer_flutter/     # 新しいFlutter版
```

Flutter版を別フォルダにする理由は次のとおり。

- Python版とFlutter版の依存関係を混在させない
- Git差分を分離する
- 将来Python側をAPIとして独立運用しやすくする
- Flutter固有の`lib`、`ios`、`android`などを既存Pythonリポジトリへ混在させない
- 問題発生時に既存のStreamlit版へ影響させない

## 5. 今回の実装対象

Task018で実施する内容は次のとおり。

- Flutter SDKの導入状況確認
- Dart SDKの利用可能状態確認
- VS CodeのFlutter拡張とDart拡張の導入確認
- `flutter doctor`による環境診断
- Flutter版Stock Trainerの新規プロジェクト作成
- Flutterプロジェクトの初回起動
- 初期サンプル画面をStock Trainer用の簡易画面へ置き換え
- Hot Reloadの動作確認
- Flutter版プロジェクトのGit管理開始
- 起動方法をFlutter側READMEへ記載

## 6. 今回の対象外

Task018では次を実装しない。

- Python版とのAPI連携
- FastAPI
- 株価データ取得
- 問題生成
- 正解判定
- 10問チャレンジ
- AIひとこと解説
- 本物のチャート表示
- 画面遷移
- 状態管理ライブラリ
- ログイン
- ユーザー登録
- データベース
- iOS App Store公開
- Google Play公開
- TestFlight配布
- アプリアイコンの本制作
- スプラッシュ画面の本制作

## 7. Flutter版プロジェクトの配置場所

Flutter版は次の絶対パスへ新規作成する。

```text
/Users/Soichiro/Python/stock_trainer_flutter
```

既存の次のフォルダ内には作成しない。

```text
/Users/Soichiro/Python/stock_prediction_game
```

Task018仕様書は既存Python版の`TASKS`フォルダで管理するが、Flutter本体は兄弟フォルダとして分離する。

## 8. プロジェクト名

Flutterプロジェクト名は次へ固定する。

```text
stock_trainer_flutter
```

Dartのpackage nameとして利用可能な、小文字とアンダースコアだけの名称とする。

画面上のアプリ名は次とする。

```text
Stock Trainer
```

## 9. 対象プラットフォーム

Task018では、Mac上でFlutter画面が起動できれば完了とする。

優先順位は次のとおり。

1. macOSデスクトップ
2. Chrome Web
3. iOS Simulator

Task018ではAndroid環境の完成を必須としない。

macOSデスクトップまたはChromeのどちらか一方で起動できれば初回起動条件を満たす。

ただし、`flutter doctor`の結果はすべて記録し、未設定項目を隠さない。

## 10. Flutter SDK確認

次のコマンドが利用できることを確認する。

```bash
flutter --version
```

確認項目：

- Flutterコマンドが実行できる
- Flutterのバージョンが表示される
- Dartのバージョンが表示される
- コマンドが見つからない場合は、Flutter SDKを導入する

## 11. 環境診断

次を実行する。

```bash
flutter doctor -v
```

診断結果を確認し、次を区別する。

- Task018の初回起動を妨げるエラー
- 将来iOS開発時に必要な未設定
- 将来Android開発時に必要な未設定
- 現時点では無視できる警告

警告を無理にすべて解消しない。

初回起動に必要なものだけをTask018で対応する。

## 12. VS Code拡張

次の拡張機能が導入済みであることを確認する。

- Flutter
- Dart

Flutter拡張を導入するとDart拡張も依存関係として導入される場合がある。

同じ拡張を重複導入しない。

## 13. Flutterプロジェクト作成

次の親フォルダへ移動する。

```bash
cd /Users/Soichiro/Python
```

次を実行する。

```bash
flutter create stock_trainer_flutter
```

すでに同名フォルダが存在する場合は上書きしない。

中身を確認し、既存プロジェクトか、作成途中の不完全フォルダかを判断してから作業する。

## 14. 初期ファイル構成

作成直後に最低限、次が存在することを確認する。

```text
stock_trainer_flutter/
├── lib/
│   └── main.dart
├── test/
├── macos/
├── ios/
├── android/
├── web/
├── pubspec.yaml
├── analysis_options.yaml
└── README.md
```

Flutterのバージョンや作成オプションにより補助ファイルが増減してもよい。

## 15. 初回画面

Flutter標準のカウンターアプリは削除し、Task018用の簡易画面へ置き換える。

画面には次だけを表示する。

- アプリ名：`Stock Trainer`
- Sprint表示：`Sprint 3 - Flutter App`
- 状態表示：`Flutter版の開発環境が整いました`
- 次の案内：`次は問題画面を作ります`

Task018ではチャートや回答ボタンを表示しない。

## 16. 初回画面のUI

画面はMaterial 3を使用する。

最低限の構成：

- `MaterialApp`
- `Scaffold`
- `AppBar`
- 中央配置のコンテンツ
- `Column`
- 適切な余白

過度な装飾は行わない。

配色や細かなデザインはTask019以降で扱う。

## 17. main.dart

`lib/main.dart`は、初心者が読める簡潔な構成にする。

最低限、次のWidgetを分ける。

```dart
void main()
```

```dart
class StockTrainerApp extends StatelessWidget
```

```dart
class HomeScreen extends StatelessWidget
```

Task018では状態変更がないため、`StatefulWidget`を使用しない。

## 18. コード品質

次を満たす。

- Dartの標準フォーマットに従う
- 不要なimportを残さない
- 未使用変数を残さない
- 意味のないコメントを大量に追加しない
- 1ファイルで理解できる範囲に保つ
- Task018では過度なファイル分割をしない

## 19. 起動方法

プロジェクトフォルダへ移動する。

```bash
cd /Users/Soichiro/Python/stock_trainer_flutter
```

利用可能デバイスを確認する。

```bash
flutter devices
```

macOSで起動する場合：

```bash
flutter run -d macos
```

Chromeで起動する場合：

```bash
flutter run -d chrome
```

利用できる対象だけを実行する。

## 20. Hot Reload

アプリ起動中に`lib/main.dart`の表示文字列を一時的に変更し、Hot Reloadで画面へ反映されることを確認する。

確認後は仕様どおりの表示文へ戻す。

Hot Reloadの確認だけを目的とした不要な差分を残さない。

## 21. Git管理

Flutter版はPython版とは別のGitリポジトリとして管理する。

対象：

```text
/Users/Soichiro/Python/stock_trainer_flutter
```

Flutterプロジェクト作成時点でGit初期化済みか確認する。

未初期化の場合だけ次を実行する。

```bash
git init
```

Python版リポジトリへFlutter版を含めない。

## 22. README

Flutter側の`README.md`へ最低限、次を記載する。

- プロジェクト名
- 目的
- 現在の状態
- 必要環境
- 起動方法
- 現時点ではPython版と未接続であること

既存のFlutterテンプレートREADMEは、Stock Trainer用の内容へ置き換える。

## 23. Python版への影響

Task018では次の既存Python版ファイルを変更しない。

- `app.py`
- `game`配下
- `ui`配下
- `analytics`配下
- `data`配下
- Python版README
- Task001〜Task017

Task018仕様書自身を除き、Python版リポジトリへ実装差分を追加しない。

## 24. エラー対応

作業中にエラーが発生した場合は、次の順で対応する。

1. エラーメッセージを省略せず確認
2. 実行したコマンドを確認
3. 現在の作業フォルダを確認
4. `flutter doctor -v`を確認
5. 対象デバイスを`flutter devices`で確認
6. 既存ファイルを無断削除しない
7. 不明な場合は推測で大規模変更せず停止して報告

## 25. 変更予定ファイル

Python版で変更：

- `TASKS/Task_018.md`

Flutter版で新規作成・変更：

- Flutterプロジェクト生成物一式
- `lib/main.dart`
- `README.md`

Flutterが自動生成する標準ファイルは作成を許可する。

## 26. 受け入れ条件

- Flutter SDKが利用できる
- `flutter --version`が成功する
- `flutter doctor -v`を実行して結果を確認している
- Flutter・DartのVS Code拡張を確認している
- `/Users/Soichiro/Python/stock_trainer_flutter`が作成されている
- Python版とFlutter版が別フォルダである
- Flutter版が独立したGitリポジトリである
- `lib/main.dart`から標準カウンター画面が削除されている
- 画面に`Stock Trainer`が表示される
- 画面に`Sprint 3 - Flutter App`が表示される
- 画面に`Flutter版の開発環境が整いました`が表示される
- 画面に`次は問題画面を作ります`が表示される
- macOSまたはChromeで起動できる
- Hot Reloadが動作する
- Flutter側READMEに起動方法がある
- Python版の実装ファイルを変更していない
- Python版とAPI接続していない
- 株価データやチャートを実装していない

## 27. 動作確認

### 27.1 環境

- `flutter --version`
- `dart --version`
- `flutter doctor -v`
- `flutter devices`

### 27.2 静的確認

- `dart format .`
- `flutter analyze`
- `git status`

### 27.3 起動

- macOSまたはChromeで起動
- 初回画面の4つの文字列を確認
- Flutter標準カウンターが表示されない

### 27.4 Hot Reload

- 表示文字列の一時変更がHot Reloadで反映される
- 確認後に正式文言へ戻っている

### 27.5 回帰

- Python版Streamlitプロジェクトが変更されていない
- Python版の既存Git差分を破棄していない
- Flutter版がPython版Gitリポジトリの配下にない

## 28. 実装手順

1. Python版の現在のGit差分を確認する
2. Flutter SDKの有無を確認する
3. VS Code拡張を確認する
4. `flutter doctor -v`を実行する
5. `/Users/Soichiro/Python`へ移動する
6. `stock_trainer_flutter`の存在有無を確認する
7. Flutterプロジェクトを新規作成する
8. 生成されたファイル構成を確認する
9. `lib/main.dart`を簡易Stock Trainer画面へ変更する
10. Flutter側READMEを更新する
11. 利用可能デバイスを確認する
12. macOSまたはChromeで起動する
13. Hot Reloadを確認する
14. `dart format .`を実行する
15. `flutter analyze`を実行する
16. Flutter側Git状態を確認する
17. Python版に不要な差分がないことを確認する
18. 実装完了報告を作成する

## 29. 完了条件

- Flutter版Stock Trainerの独立プロジェクトが作成されている
- Mac上でFlutter版初回画面を起動できる
- Hot Reloadを利用できる
- Python版とFlutter版が安全に分離されている
- 次のTaskで問題画面UIの開発を始められる
- 実施した確認結果と未解決の警告を正確に報告している