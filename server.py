#!/usr/bin/env python3
"""
シンプルなFastMCPサーバー
個人用ローカルツール
"""

import random
import datetime
from typing import int as Int
from fastmcp import FastMCP

# MCPサーバーのインスタンスを作成
mcp = FastMCP("Simple Tools Server")


@mcp.tool
def add_numbers(a: Int, b: Int) -> Int:
    """二つの数値を足し算します"""
    return a + b


@mcp.tool
def generate_random_number(min_val: Int = 1, max_val: Int = 100) -> Int:
    """指定された範囲でランダムな数値を生成します"""
    return random.randint(min_val, max_val)


@mcp.tool
def get_current_timestamp() -> str:
    """現在の日時を取得します"""
    return datetime.datetime.now().isoformat()


if __name__ == "__main__":
    print("MCPサーバーを起動しています...")
    mcp.run()
