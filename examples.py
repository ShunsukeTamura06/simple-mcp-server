#!/usr/bin/env python3
"""
Bloomberg MCP Server使用例
"""

from server import bbg_api
import json


def main():
    """使用例のデモンストレーション"""
    
    print("=== Bloomberg MCP Server 使用例 ===\n")
    
    try:
        # 接続テスト
        print("Bloomberg APIに接続中...")
        bbg_api.connect()
        print("✓ 接続成功\n")
        
        # 1. 証券検索の例
        print("1. 証券検索の例")
        print("検索キーワード: 'Apple'")
        
        # search_securities のシミュレーション
        print("検索結果例:")
        print("- AAPL US Equity: Apple Inc")
        print("- AAPL LN Equity: Apple Inc - London")
        print()
        
        # 2. フィールド検索の例
        print("2. フィールド検索の例")
        print("検索キーワード: 'price'")
        print("検索結果例:")
        print("- PX_LAST: 最終価格")
        print("- PX_OPEN: 始値")
        print("- PX_HIGH: 高値")
        print("- PX_LOW: 安値")
        print()
        
        # 3. 現在データ取得の例
        print("3. 現在データ取得の例")
        print("証券: AAPL US Equity")
        print("フィールド: PX_LAST, PX_VOLUME")
        print("取得結果例:")
        print({
            "AAPL US Equity": {
                "PX_LAST": 185.50,
                "PX_VOLUME": 45230000
            }
        })
        print()
        
        # 4. 過去データ取得の例
        print("4. 過去データ取得の例")
        print("証券: AAPL US Equity")
        print("フィールド: PX_LAST")
        print("期間: 2024-01-01 to 2024-01-05")
        print("取得結果例:")
        print({
            "AAPL US Equity": [
                {"date": "2024-01-01", "PX_LAST": 181.00},
                {"date": "2024-01-02", "PX_LAST": 182.50},
                {"date": "2024-01-03", "PX_LAST": 184.20},
                {"date": "2024-01-04", "PX_LAST": 183.80},
                {"date": "2024-01-05", "PX_LAST": 185.50}
            ]
        })
        print()
        
        # 5. バルクデータ取得の例
        print("5. バルクデータ取得の例")
        print("証券: SPX Index")
        print("フィールド: INDX_MEMBERS")
        print("取得結果例（最初の3件）:")
        print([
            {"Member Ticker and Exchange Code": "AAPL US", "Percentage Weight": 7.25},
            {"Member Ticker and Exchange Code": "MSFT US", "Percentage Weight": 6.89},
            {"Member Ticker and Exchange Code": "NVDA US", "Percentage Weight": 5.43}
        ])
        print()
        
        print("=== デモ完了 ===")
        print("実際の使用時は、Bloomberg Terminalにログインしてサーバーを起動してください。")
        
    except Exception as e:
        print(f"エラー: {e}")
        print("Bloomberg Terminalが起動していることを確認してください。")
    
    finally:
        if bbg_api.session:
            bbg_api.disconnect()
            print("Bloomberg API接続を終了しました。")


if __name__ == "__main__":
    main()
