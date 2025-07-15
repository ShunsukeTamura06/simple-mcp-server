# Bloomberg MCP Server

FastMCPを使ったBloomberg API市場データ取得サーバーです。

## 機能

### 📊 市場データ取得ツール

- **search_securities** - 証券検索（会社名、ティッカー等から候補を検索）
- **search_fields** - フィールド検索（利用可能なBloombergフィールドを検索）
- **get_reference_data** - 現在の市場データ取得（BDP機能相当）
- **get_historical_data** - 過去データ取得（BDH機能相当）
- **get_bulk_data** - バルクデータ取得（BDS機能相当）

### 使用例

```python
# 証券検索
search_securities("Apple", max_results=10)

# フィールド検索  
search_fields("price", max_results=20)

# 現在の株価取得
get_reference_data("AAPL US Equity", ["PX_LAST", "VOLUME"])

# 過去データ取得
get_historical_data(
    "AAPL US Equity", 
    ["PX_LAST", "PX_VOLUME"], 
    "2024-01-01", 
    "2024-12-31"
)

# インデックス構成銘柄取得
get_bulk_data("SPX Index", "INDX_MEMBERS")
```

## 前提条件

- Bloomberg Terminal契約およびログイン
- Bloomberg Desktop APIアクセス権限
- Python 3.8以上

## セットアップ

### 1. 依存関係のインストール

```bash
# pip使用の場合
pip install -r requirements.txt

# uv使用の場合（推奨）
uv sync
```

### 2. Bloomberg Terminalの起動

Bloomberg Terminalにログインし、APIが利用可能な状態にしてください。

### 3. サーバー起動

```bash
python server.py
```

## Bloomberg APIについて

このサーバーは以下のBloomberg APIサービスを使用します：

- **//blp/refdata** - 参照データサービス（価格、ボリューム等）
- **//blp/apiflds** - フィールド検索サービス

## よく使用されるフィールド

- `PX_LAST` - 最終価格
- `PX_VOLUME` - 出来高
- `SECURITY_NAME` - 証券名
- `GICS_SECTOR_NAME` - GICS セクター
- `MARKET_CAP` - 時価総額
- `DVD_HIST_ALL` - 配当履歴
- `INDX_MEMBERS` - インデックス構成銘柄

## 証券コード形式

- 株式: `AAPL US Equity`
- インデックス: `SPX Index`
- 債券: `T 4.75 05/15/25 Govt`
- 通貨: `USDJPY Curncy`
- コモディティ: `CL1 Comdty`

## エラーハンドリング

- Bloomberg Terminalが起動していない場合は接続エラーが発生
- 無効なティッカーやフィールドの場合は適切なエラーメッセージを返却
- ネットワーク接続問題は自動的に検出・報告

## 使用方法

サーバーが起動したら、MCPクライアント（Claude Desktop等）から接続して、市場データ分析や投資リサーチに活用できます。

## ライセンス

このプロジェクトは個人使用を想定しています。Bloomberg APIの利用規約に従ってご使用ください。
