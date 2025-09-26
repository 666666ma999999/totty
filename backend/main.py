#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合占いチャットシステム - FastAPI統合サーバー
Port 8011での単一サーバー統合実装

すべてのマイクロサービスを統合し、MDファイル直接参照システムを維持
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 共有リソースのインポート
from shared.config import AppConfig

# サービスモジュールのインポート
from services.chat_service import chat_router
from services.fortune_service import fortune_router
from services.analysis_service import analysis_router
from services.chat_history_service import chat_history_router
from services.greeting_service import greeting_router

# コアモジュールの初期化
from core.md_loader import md_loader
from core.openai_client import openai_manager

# FastAPI アプリケーション初期化
app = FastAPI(
    title="統合占いチャットシステム API",
    description="イケメン霊能師蒼司のAI応答システム - 統合版",
    version="2.0.0",
    docs_url=AppConfig.DOCS_URL,
    redoc_url=AppConfig.REDOC_URL
)

# CORS ミドルウェア設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=AppConfig.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル配信設定（フロントエンド統合）
static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 静的ファイル（CSS, JS等）をマウント
app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

# サービスルーターの統合
app.include_router(
    chat_router,
    prefix=AppConfig.API_PREFIX,
    tags=["Chat Service"]
)

app.include_router(
    fortune_router,
    prefix=AppConfig.API_PREFIX,
    tags=["Fortune Service"]
)

app.include_router(
    analysis_router,
    prefix=AppConfig.API_PREFIX,
    tags=["Analysis Service"]
)

app.include_router(
    chat_history_router,
    tags=["Chat History Service"]
)

app.include_router(
    greeting_router,
    tags=["Greeting Service"]
)

# フロントエンド（Webアプリ）エンドポイント
@app.get("/")
async def serve_frontend():
    """フロントエンドアプリケーション配信"""
    index_path = os.path.join(static_path, "index.html")
    return FileResponse(index_path)

@app.get("/app")
async def serve_frontend_app():
    """フロントエンドアプリケーション配信（/app経由）"""
    index_path = os.path.join(static_path, "index.html")
    return FileResponse(index_path)

# API用ヘルスチェックエンドポイント
@app.get("/api/health")
async def api_health_check():
    """統合サーバーAPIヘルスチェック"""
    return {
        "status": "ok",
        "message": "統合占いチャットシステム API",
        "version": "2.0.0",
        "services": ["chat", "fortune", "analysis", "greeting"],
        "md_files_loaded": len(md_loader.load_system_configs())
    }

@app.get("/status")
async def system_status():
    """システム状態確認"""
    try:
        md_configs = md_loader.load_system_configs()

        return {
            "server_status": "running",
            "port": AppConfig.PORT,
            "md_files_status": {
                "loaded_files": list(md_configs.keys()),
                "loaded_count": len([v for v in md_configs.values() if v]),
                "last_loaded": md_loader._last_loaded.isoformat() if md_loader._last_loaded else None
            },
            "openai_status": "configured" if AppConfig.OPENAI_API_KEY else "not_configured",
            "cors_origins": AppConfig.CORS_ORIGINS,
            "configuration": {
                "max_tokens": AppConfig.MAX_TOKENS,
                "max_sentences": AppConfig.MAX_RESPONSE_SENTENCES,
                "fortune_threshold": AppConfig.RESORT_ANALYSIS_THRESHOLD
            }
        }

    except Exception as e:
        return {
            "server_status": "error",
            "error": str(e)
        }

@app.get("/reload-config")
async def reload_configuration():
    """MDファイル設定の強制再読み込み"""
    try:
        configs = md_loader.reload_configs()

        return {
            "status": "reloaded",
            "message": "MDファイル設定を再読み込みしました",
            "loaded_files": list(configs.keys()),
            "loaded_count": len([v for v in configs.values() if v]),
            "timestamp": md_loader._last_loaded.isoformat() if md_loader._last_loaded else None
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"設定再読み込みエラー: {str(e)}"
        }

# アプリケーション起動時の初期化処理
def initialize_application():
    """アプリケーション初期化"""
    print("=" * 60)
    print("🔮 統合占いチャットシステム サーバー起動中...")
    print("=" * 60)

    # MDファイル読み込み
    try:
        configs = md_loader.load_system_configs()
        loaded_count = len([v for v in configs.values() if v])
        print(f"✅ MDファイル読み込み完了: {loaded_count}個のファイル")

        for key, content in configs.items():
            status = "✅ 読み込み成功" if content else "❌ 読み込み失敗"
            print(f"   - {key}: {status}")

    except Exception as e:
        print(f"❌ MDファイル読み込みエラー: {e}")

    # OpenAIクライアント確認
    try:
        client = openai_manager.client
        print(f"✅ OpenAI クライアント初期化完了")

    except Exception as e:
        print(f"❌ OpenAI クライアントエラー: {e}")

    print(f"🚀 サーバー起動完了: http://{AppConfig.HOST}:{AppConfig.PORT}")
    print(f"📚 API ドキュメント: http://{AppConfig.HOST}:{AppConfig.PORT}{AppConfig.DOCS_URL}")
    print("=" * 60)

# メイン実行部分
if __name__ == "__main__":
    print("統合占いチャットシステム - 起動準備中...")

    # 設定検証
    try:
        AppConfig.validate_config()
        print("✅ 設定検証完了")
    except Exception as e:
        print(f"❌ 設定エラー: {e}")
        exit(1)

    # アプリケーション初期化
    initialize_application()

    # サーバー起動
    uvicorn.run(
        app,
        host=AppConfig.HOST,
        port=AppConfig.PORT,
        reload=False,
        log_level=AppConfig.LOG_LEVEL.lower(),
        access_log=True
    )