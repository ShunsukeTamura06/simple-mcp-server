#!/usr/bin/env python3
"""
Bloomberg MCP Server
FastMCPを使ったBloomberg API市場データ取得サーバー
"""

import blpapi
import datetime
import pandas as pd
from typing import List, Dict, Any, Optional, Union
from fastmcp import FastMCP

# MCPサーバーのインスタンスを作成
mcp = FastMCP("Bloomberg Market Data Server")


class BloombergAPI:
    """Bloomberg API接続管理クラス"""
    
    def __init__(self):
        self.session = None
        self.refdata_service = None
        self.apiflds_service = None
        self.instruments_service = None
    
    def connect(self):
        """Bloomberg APIに接続"""
        try:
            # セッションオプションを設定
            session_options = blpapi.SessionOptions()
            session_options.setServerHost("localhost")
            session_options.setServerPort(8194)
            
            # セッションを作成・開始
            self.session = blpapi.Session(session_options)
            if not self.session.start():
                raise Exception("Failed to start Bloomberg session")
            
            # サービスを開く
            if not self.session.openService("//blp/refdata"):
                raise Exception("Failed to open refdata service")
            
            if not self.session.openService("//blp/apiflds"):
                raise Exception("Failed to open apiflds service") 
                
            if not self.session.openService("//blp/instruments"):
                raise Exception("Failed to open instruments service")
                
            self.refdata_service = self.session.getService("//blp/refdata")
            self.apiflds_service = self.session.getService("//blp/apiflds")
            self.instruments_service = self.session.getService("//blp/instruments")
            
            return True
            
        except Exception as e:
            raise Exception(f"Bloomberg接続エラー: {str(e)}")
    
    def disconnect(self):
        """Bloomberg APIから切断"""
        if self.session:
            self.session.stop()
            self.session = None


# グローバルAPI接続インスタンス
bbg_api = BloombergAPI()


def ensure_connection():
    """API接続を確認し、必要に応じて接続"""
    if bbg_api.session is None:
        bbg_api.connect()


@mcp.tool
def search_securities(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """
    証券をキーワードで検索します。会社名、ティッカー等から候補を見つけます。
    
    Args:
        query: 検索キーワード（会社名、ティッカー等）
        max_results: 最大結果数（デフォルト: 20）
    
    Returns:
        検索結果のリスト
    """
    try:
        ensure_connection()
        
        # InstrumentListRequestを作成（正しいサービスを使用）
        request = bbg_api.instruments_service.createRequest("instrumentListRequest")
        request.set("query", query)
        request.set("maxResults", max_results)
        
        # リクエストを送信
        bbg_api.session.sendRequest(request)
        
        results = []
        done = False
        
        while not done:
            event = bbg_api.session.nextEvent(500)
            
            for msg in event:
                if msg.messageType() == blpapi.Name("InstrumentListResponse"):
                    results_array = msg.getElement("results")
                    
                    for i in range(results_array.numValues()):
                        result = results_array.getValue(i)
                        security_info = {
                            "security": result.getElementAsString("security"),
                            "description": result.getElementAsString("description") if result.hasElement("description") else ""
                        }
                        results.append(security_info)
                
                if event.eventType() == blpapi.Event.RESPONSE:
                    done = True
        
        return results
        
    except Exception as e:
        raise Exception(f"証券検索エラー: {str(e)}")


@mcp.tool
def search_fields(field_query: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """
    Bloomberg APIのフィールドを検索します。
    
    Args:
        field_query: フィールド検索キーワード（例: "price", "volume", "market cap"）
        max_results: 最大結果数（デフォルト: 50）
    
    Returns:
        フィールド情報のリスト
    """
    try:
        ensure_connection()
        
        # FieldSearchRequestを作成
        request = bbg_api.apiflds_service.createRequest("FieldSearchRequest")
        request.set("searchSpec", field_query)
        
        # 静的フィールドのみを検索
        include_element = request.getElement("include")
        include_element.setElement("fieldType", "Static")
        
        # リクエストを送信
        bbg_api.session.sendRequest(request)
        
        results = []
        done = False
        
        while not done:
            event = bbg_api.session.nextEvent(500)
            
            for msg in event:
                if msg.messageType() == blpapi.Name("fieldResponse"):
                    field_data = msg.getElement("fieldData")
                    
                    for i in range(field_data.numValues()):
                        field = field_data.getValue(i)
                        
                        # 基本情報（fieldレベルのid）
                        field_info = {
                            "field_id": field.getElementAsString("id") if field.hasElement("id") else ""
                        }
                        
                        # fieldInfo要素から詳細情報を取得
                        if field.hasElement("fieldInfo"):
                            field_info_element = field.getElement("fieldInfo")
                            
                            field_info.update({
                                "mnemonic": field_info_element.getElementAsString("mnemonic") if field_info_element.hasElement("mnemonic") else "",
                                "description": field_info_element.getElementAsString("description") if field_info_element.hasElement("description") else "",
                                "data_type": field_info_element.getElementAsString("datatype") if field_info_element.hasElement("datatype") else "",
                                "documentation": field_info_element.getElementAsString("documentation") if field_info_element.hasElement("documentation") else "",
                                "category_name": field_info_element.getElementAsString("categoryName") if field_info_element.hasElement("categoryName") else "",
                                "property": field_info_element.getElementAsString("property") if field_info_element.hasElement("property") else ""
                            })
                        
                        results.append(field_info)
                        
                        if len(results) >= max_results:
                            break
                
                if event.eventType() == blpapi.Event.RESPONSE:
                    done = True
        
        return results[:max_results]
        
    except Exception as e:
        raise Exception(f"フィールド検索エラー: {str(e)}")


@mcp.tool
def get_reference_data(securities: Union[str, List[str]], fields: Union[str, List[str]]) -> Dict[str, Any]:
    """
    現在の参照データを取得します（BDP機能相当）。
    
    Args:
        securities: 証券コード（文字列または文字列のリスト）
        fields: フィールド名（文字列または文字列のリスト）
    
    Returns:
        市場データの辞書
    """
    try:
        ensure_connection()
        
        # 入力を正規化
        if isinstance(securities, str):
            securities = [securities]
        if isinstance(fields, str):
            fields = [fields]
        
        # ReferenceDataRequestを作成
        request = bbg_api.refdata_service.createRequest("ReferenceDataRequest")
        
        # 証券を追加
        for security in securities:
            request.append("securities", security)
        
        # フィールドを追加
        for field in fields:
            request.append("fields", field)
        
        # リクエストを送信
        bbg_api.session.sendRequest(request)
        
        results = {}
        done = False
        
        while not done:
            event = bbg_api.session.nextEvent(500)
            
            for msg in event:
                if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                    security_data_array = msg.getElement("securityData")
                    
                    for i in range(security_data_array.numValues()):
                        security_data = security_data_array.getValue(i)
                        security = security_data.getElementAsString("security")
                        
                        # エラーチェック
                        if security_data.hasElement("securityError"):
                            continue
                        
                        field_data = security_data.getElement("fieldData")
                        security_results = {}
                        
                        for field in fields:
                            if field_data.hasElement(field):
                                value = field_data.getElement(field).getValue()
                                security_results[field] = value
                            else:
                                security_results[field] = None
                        
                        results[security] = security_results
                
                if event.eventType() == blpapi.Event.RESPONSE:
                    done = True
        
        return results
        
    except Exception as e:
        raise Exception(f"参照データ取得エラー: {str(e)}")


@mcp.tool
def get_historical_data(
    securities: Union[str, List[str]], 
    fields: Union[str, List[str]], 
    start_date: str, 
    end_date: str,
    periodicity: str = "DAILY"
) -> Dict[str, Any]:
    """
    過去データを取得します（BDH機能相当）。
    
    Args:
        securities: 証券コード（文字列または文字列のリスト）
        fields: フィールド名（文字列または文字列のリスト）
        start_date: 開始日（YYYY-MM-DD形式）
        end_date: 終了日（YYYY-MM-DD形式）
        periodicity: 周期（DAILY, WEEKLY, MONTHLY等）
    
    Returns:
        過去データの辞書
    """
    try:
        ensure_connection()
        
        # 入力を正規化
        if isinstance(securities, str):
            securities = [securities]
        if isinstance(fields, str):
            fields = [fields]
        
        # 日付をBloomberg形式に変換
        start_date_bbg = datetime.datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y%m%d")
        end_date_bbg = datetime.datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y%m%d")
        
        # HistoricalDataRequestを作成
        request = bbg_api.refdata_service.createRequest("HistoricalDataRequest")
        
        # 証券を追加
        for security in securities:
            request.append("securities", security)
        
        # フィールドを追加
        for field in fields:
            request.append("fields", field)
        
        # 日付設定
        request.set("startDate", start_date_bbg)
        request.set("endDate", end_date_bbg)
        request.set("periodicitySelection", periodicity)
        
        # リクエストを送信
        bbg_api.session.sendRequest(request)
        
        results = {}
        done = False
        
        while not done:
            event = bbg_api.session.nextEvent(500)
            
            for msg in event:
                if msg.messageType() == blpapi.Name("HistoricalDataResponse"):
                    security_data = msg.getElement("securityData")
                    security = security_data.getElementAsString("security")
                    
                    # エラーチェック
                    if security_data.hasElement("securityError"):
                        continue
                    
                    field_data_array = security_data.getElement("fieldData")
                    
                    security_results = []
                    for i in range(field_data_array.numValues()):
                        field_data = field_data_array.getValue(i)
                        
                        row = {
                            "date": field_data.getElementAsString("date")
                        }
                        
                        for field in fields:
                            if field_data.hasElement(field):
                                value = field_data.getElement(field).getValue()
                                row[field] = value
                            else:
                                row[field] = None
                        
                        security_results.append(row)
                    
                    results[security] = security_results
                
                if event.eventType() == blpapi.Event.RESPONSE:
                    done = True
        
        return results
        
    except Exception as e:
        raise Exception(f"過去データ取得エラー: {str(e)}")


@mcp.tool
def get_bulk_data(security: str, field: str) -> List[Dict[str, Any]]:
    """
    バルクデータを取得します（BDS機能相当）。
    
    Args:
        security: 証券コード
        field: バルクフィールド名（例: "INDX_MEMBERS", "DVD_HIST_ALL"）
    
    Returns:
        バルクデータのリスト
    """
    try:
        ensure_connection()
        
        # ReferenceDataRequestを作成
        request = bbg_api.refdata_service.createRequest("ReferenceDataRequest")
        request.append("securities", security)
        request.append("fields", field)
        
        # リクエストを送信
        bbg_api.session.sendRequest(request)
        
        results = []
        done = False
        
        while not done:
            event = bbg_api.session.nextEvent(500)
            
            for msg in event:
                if msg.messageType() == blpapi.Name("ReferenceDataResponse"):
                    security_data_array = msg.getElement("securityData")
                    
                    for i in range(security_data_array.numValues()):
                        security_data = security_data_array.getValue(i)
                        
                        # エラーチェック
                        if security_data.hasElement("securityError"):
                            continue
                        
                        field_data = security_data.getElement("fieldData")
                        
                        if field_data.hasElement(field):
                            bulk_data = field_data.getElement(field)
                            
                            for j in range(bulk_data.numValues()):
                                row_data = bulk_data.getValue(j)
                                row = {}
                                
                                # 各要素を辞書に変換
                                for k in range(row_data.numElements()):
                                    element = row_data.getElement(k)
                                    row[element.name()] = element.getValue()
                                
                                results.append(row)
                
                if event.eventType() == blpapi.Event.RESPONSE:
                    done = True
        
        return results
        
    except Exception as e:
        raise Exception(f"バルクデータ取得エラー: {str(e)}")


if __name__ == "__main__":
    print("Bloomberg MCP サーバーを起動しています...")
    
    # 起動時に接続テスト
    try:
        bbg_api.connect()
        print("Bloomberg API接続成功")
        bbg_api.disconnect()
    except Exception as e:
        print(f"警告: Bloomberg API接続失敗 - {e}")
        print("Bloomberg Terminalが起動していることを確認してください")
    
    mcp.run()
