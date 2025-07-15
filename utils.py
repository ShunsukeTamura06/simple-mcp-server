"""
Bloomberg MCP Server ユーティリティ関数
"""

import blpapi
from typing import Dict, Any, List, Optional
import datetime


def format_bloomberg_date(date_str: str) -> str:
    """
    YYYY-MM-DD形式の日付をBloomberg形式（YYYYMMDD）に変換
    
    Args:
        date_str: YYYY-MM-DD形式の日付文字列
    
    Returns:
        YYYYMMDD形式の日付文字列
    """
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y%m%d")
    except ValueError:
        raise ValueError(f"無効な日付形式: {date_str}. YYYY-MM-DD形式で入力してください。")


def validate_securities(securities: List[str]) -> List[str]:
    """
    証券コードの形式をバリデーション
    
    Args:
        securities: 証券コードのリスト
    
    Returns:
        バリデーション済み証券コードのリスト
    """
    validated = []
    for security in securities:
        if not security or not isinstance(security, str):
            raise ValueError(f"無効な証券コード: {security}")
        validated.append(security.strip().upper())
    return validated


def validate_fields(fields: List[str]) -> List[str]:
    """
    フィールド名をバリデーション
    
    Args:
        fields: フィールド名のリスト
    
    Returns:
        バリデーション済みフィールド名のリスト
    """
    validated = []
    for field in fields:
        if not field or not isinstance(field, str):
            raise ValueError(f"無効なフィールド名: {field}")
        validated.append(field.strip().upper())
    return validated


def extract_element_value(element: blpapi.Element) -> Any:
    """
    Bloomberg Elementから値を安全に抽出
    
    Args:
        element: Bloomberg Element
    
    Returns:
        抽出された値
    """
    try:
        if element.isNull():
            return None
        
        data_type = element.datatype()
        
        if data_type == blpapi.DataType.STRING:
            return element.getValueAsString()
        elif data_type == blpapi.DataType.INT32:
            return element.getValueAsInt32()
        elif data_type == blpapi.DataType.INT64:
            return element.getValueAsInt64()
        elif data_type == blpapi.DataType.FLOAT32:
            return element.getValueAsFloat32()
        elif data_type == blpapi.DataType.FLOAT64:
            return element.getValueAsFloat64()
        elif data_type == blpapi.DataType.BOOL:
            return element.getValueAsBool()
        elif data_type == blpapi.DataType.DATE:
            return str(element.getValueAsDate())
        elif data_type == blpapi.DataType.TIME:
            return str(element.getValueAsTime())
        elif data_type == blpapi.DataType.DATETIME:
            return str(element.getValueAsDatetime())
        else:
            return element.getValue()
    except Exception:
        return None


def format_error_message(error_element: blpapi.Element) -> str:
    """
    Bloomberg APIエラーを整形
    
    Args:
        error_element: Bloomberg Error Element
    
    Returns:
        整形されたエラーメッセージ
    """
    try:
        source = error_element.getElementAsString("source") if error_element.hasElement("source") else "Unknown"
        code = error_element.getElementAsInt("code") if error_element.hasElement("code") else 0
        category = error_element.getElementAsString("category") if error_element.hasElement("category") else "Unknown"
        message = error_element.getElementAsString("message") if error_element.hasElement("message") else "Unknown error"
        
        return f"Bloomberg API Error [{code}] {category}: {message} (Source: {source})"
    except Exception:
        return "Bloomberg API Error: Unknown error occurred"


def get_common_fields() -> Dict[str, str]:
    """
    よく使用されるBloombergフィールドの辞書を返す
    
    Returns:
        フィールド名と説明の辞書
    """
    return {
        "PX_LAST": "最終価格",
        "PX_OPEN": "始値",
        "PX_HIGH": "高値", 
        "PX_LOW": "安値",
        "PX_VOLUME": "出来高",
        "SECURITY_NAME": "証券名",
        "SECURITY_NAME_REALTIME": "証券名（リアルタイム）",
        "GICS_SECTOR_NAME": "GICSセクター名",
        "GICS_INDUSTRY_NAME": "GICS業種名",
        "MARKET_CAP": "時価総額",
        "CUR_MKT_CAP": "現在時価総額",
        "PE_RATIO": "PER",
        "PX_TO_BOOK_RATIO": "PBR",
        "DIVIDEND_YIELD": "配当利回り",
        "VOLATILITY_30D": "30日ボラティリティ",
        "BETA_OVERRIDE_REL_INDEX": "ベータ値",
        "52WK_HIGH": "52週高値",
        "52WK_LOW": "52週安値",
        "VOLUME_AVG_20D": "20日平均出来高",
        "RSI_14D": "14日RSI",
        "COUNTRY": "国",
        "CRNCY": "通貨",
        "EXCH_CODE": "取引所コード",
        "ID_ISIN": "ISIN",
        "ID_CUSIP": "CUSIP",
        "INDUSTRY_SECTOR": "業界セクター",
        "INDX_MEMBERS": "インデックス構成銘柄",
        "DVD_HIST_ALL": "配当履歴",
        "EQY_FUND_CRNCY": "株式ファンド通貨",
        "OPT_CHAIN": "オプションチェーン",
        "FUT_CHAIN": "先物チェーン"
    }


def get_security_examples() -> Dict[str, List[str]]:
    """
    証券コードの例を返す
    
    Returns:
        証券タイプ別の例の辞書
    """
    return {
        "US株式": [
            "AAPL US Equity",
            "MSFT US Equity", 
            "GOOGL US Equity",
            "TSLA US Equity"
        ],
        "日本株式": [
            "7203 JP Equity",  # トヨタ
            "6758 JP Equity",  # ソニー
            "9984 JP Equity",  # ソフトバンクG
            "6861 JP Equity"   # キーエンス
        ],
        "インデックス": [
            "SPX Index",       # S&P 500
            "NDX Index",       # NASDAQ 100
            "INDU Index",      # Dow Jones
            "NKY Index",       # 日経225
            "TPX Index"        # TOPIX
        ],
        "通貨": [
            "USDJPY Curncy",
            "EURUSD Curncy",
            "GBPUSD Curncy",
            "AUDUSD Curncy"
        ],
        "債券": [
            "USGG10YR Index",  # 10年米国債
            "JGBS10 Index",    # 10年日本国債
            "GDBR10 Index"     # 10年ドイツ債
        ],
        "コモディティ": [
            "CL1 Comdty",      # 原油
            "GC1 Comdty",      # 金
            "SI1 Comdty",      # 銀
            "C 1 Comdty"       # コーン
        ]
    }


def normalize_input(input_data):
    """
    入力データを正規化（文字列または文字列のリストに対応）
    
    Args:
        input_data: 文字列または文字列のリスト
    
    Returns:
        文字列のリスト
    """
    if isinstance(input_data, str):
        return [input_data]
    elif isinstance(input_data, list):
        return input_data
    else:
        raise ValueError(f"無効な入力データ型: {type(input_data)}. 文字列またはリストを指定してください。")
