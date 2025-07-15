# Bloomberg MCP Server

FastMCPを使ったBloomberg API市場データ取得サーバーです。

## 🚀 **サーバー起動方式**

### **方式1: stdio (推奨) - プロセス間通信**
```bash
# デフォルト - Claude Desktop等での標準的な使用方法
python server.py

# または明示的にstdio指定
python server_http.py --stdio
```
- **ホスト・ポート不要**
- **Claude Desktop設定例** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "bloomberg-server": {
      "command": "python",
      "args": ["/path/to/your/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

### **方式2: HTTP/SSE - ネットワーク経由**
```bash
# HTTPサーバーとして起動 (デフォルト: localhost:8080)
python server_http.py

# カスタムホスト・ポート指定
python server_http.py --host 0.0.0.0 --port 3000
```
- **アクセスURL**: `http://localhost:8080/sse`
- **他のマシンからもアクセス可能**
- **Web UIやカスタムクライアントでの使用に適している**

## 📊 **機能**

### 市場データ取得ツール

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

## 🔧 **セットアップ**

### 前提条件

- Bloomberg Terminal契約およびログイン
- Bloomberg Desktop APIアクセス権限  
- Python 3.8以上

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
# stdio方式（Claude Desktop用）
python server.py

# HTTP方式（Web UI等用）
python server_http.py --host 0.0.0.0 --port 8080
```

## 🌐 **ネットワーク接続詳細**

### **stdio方式の仕組み**
```
[Claude Desktop] ←→ [MCPサーバープロセス]
      ↑                    ↓
   JSON-RPC          Bloomberg API
   (stdin/stdout)    (localhost:8194)
```

### **HTTP/SSE方式の仕組み**  
```
[Webクライアント] ←→ [HTTPサーバー:8080] ←→ [Bloomberg API]
      ↑                     ↓                    ↓
   HTTP/SSE             FastMCP              localhost:8194
```

## 📡 **Bloomberg API接続**

サーバーは以下のサービスを使用します：

- **Bloomberg Terminal**: `localhost:8194` (Desktop API)
- **//blp/refdata** - 参照データサービス（価格、ボリューム等）
- **//blp/apiflds** - フィールド検索サービス

## 🔍 **よく使用されるフィールド**

- `PX_LAST` - 最終価格
- `PX_VOLUME` - 出来高
- `SECURITY_NAME` - 証券名
- `GICS_SECTOR_NAME` - GICS セクター
- `MARKET_CAP` - 時価総額
- `DVD_HIST_ALL` - 配当履歴
- `INDX_MEMBERS` - インデックス構成銘柄

## 📈 **証券コード形式**

- 株式: `AAPL US Equity`
- インデックス: `SPX Index`
- 債券: `T 4.75 05/15/25 Govt`
- 通貨: `USDJPY Curncy`
- コモディティ: `CL1 Comdty`

## 🛠 **トラブルシューティング**

### 接続エラー
```bash
# Bloomberg Terminal起動確認
# Windows: Ctrl+Alt+T でターミナル起動
# Bloomberg API状態確認: API <GO>
```

### ポート競合（HTTP方式）
```bash
# 別ポートで起動
python server_http.py --port 3001

# プロセス確認
netstat -an | grep :8080
```

### デバッグモード
```bash
# 詳細ログ出力
python server.py --debug

# 接続テスト
python examples.py
```

## 🎯 **使用方法**

### Claude Desktop統合
1. `claude_desktop_config.json`にサーバー設定追加
2. Claude Desktop再起動
3. チャットで市場データ分析を依頼

### カスタムクライアント開発
```python
import requests

# HTTP API呼び出し例
response = requests.post(
    "http://localhost:8080/mcp",
    json={
        "method": "tools/call",
        "params": {
            "name": "get_reference_data",
            "arguments": {
                "securities": "AAPL US Equity",
                "fields": "PX_LAST"
            }
        }
    }
)
```

## 📄 **ライセンス**

このプロジェクトは個人使用を想定しています。Bloomberg APIの利用規約に従ってご使用ください。

## 🔗 **関連ファイル**

- `server.py` - stdio版メインサーバー
- `server_http.py` - HTTP/SSE版サーバー  
- `utils.py` - ユーティリティ関数
- `examples.py` - 使用例デモ
