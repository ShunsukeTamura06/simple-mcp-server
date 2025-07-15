# Simple MCP Server

FastMCPを使ったシンプルなローカルMCPサーバーです。

## 機能

- **add_numbers**: 二つの数値を足し算
- **generate_random_number**: ランダム数値生成
- **get_current_timestamp**: 現在の日時取得

## セットアップ

```bash
# 依存関係をインストール
pip install -r requirements.txt

# またはuvを使用
uv add fastmcp
```

## 実行

```bash
python server.py
```

## 使用方法

サーバーが起動したら、MCPクライアント（Claude Desktop等）から接続して利用できます。
