

# Architecture

## プロジェクト構成

```text
stock_prediction_game/
├── frontend/              # Flutterアプリ
│   ├── lib/
│   │   ├── screens/        # 画面
│   │   ├── widgets/        # 再利用Widget
│   │   ├── models/         # データモデル
│   │   └── main.dart       # エントリーポイント
│   └── test/               # Widgetテスト
│
├── TASKS/                  # 開発仕様書
├── .codex/                 # Codex用プロジェクトルール
│
├── analytics/              # Python分析ロジック
├── data/                   # データ取得
├── game/                   # ゲームロジック
└── api.py                  # 将来のAPI入口
```

## レイヤー構成

### Flutter

- screens：画面全体のレイアウト
- widgets：再利用可能なUI部品
- models：画面で扱うデータ構造
- main.dart：アプリ起動のみ担当

### Python

- データ取得
- 問題生成
- チャート生成
- 将来的なFastAPI

## 設計原則

- 画面はscreensへ配置する
- 再利用可能な部品はwidgetsへ配置する
- データ構造はmodelsへ配置する
- Widgetごとに責務を分離する
- Taskで指定されていない構成変更は行わない

## 依存関係

- screens → widgets / models
- widgets → models（必要な場合のみ）
- models → 他レイヤーへ依存しない
- FlutterはPythonコードへ直接依存しない
- PythonとFlutterの連携は将来的にAPI経由で行う