#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合アプリケーション設定管理
共有リソースと設定の一元管理
"""

import os
from typing import List
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

class AppConfig:
    """アプリケーション統合設定クラス"""

    # OpenAI API設定
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # サーバー設定
    HOST = "127.0.0.1"
    PORT = 8011
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # CORS設定
    CORS_ORIGINS = [
        "http://localhost:8011",
        "http://127.0.0.1:8011"
    ]

    # MDファイル設定
    MD_FILES_ROOT = "../systems"
    CHARACTER_FILES_ROOT = "../characters"

    # API設定
    API_PREFIX = "/api"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"

    # OpenAI設定
    CHAT_MODEL = "gpt-4"
    MAX_TOKENS = 300  # 3文以内制約
    TEMPERATURE = 0.7

    # レスポンス設定
    MAX_RESPONSE_SENTENCES = 3
    TARGET_CHARACTER_COUNT = 150  # 150-250文字目安の最小値

    # ログ設定
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # データ分析設定
    RESORT_ANALYSIS_THRESHOLD = 70  # 占い提案閾値
    FORTUNE_TIMING_MULTIPLIERS = {
        "resort_total": 0.4,
        "data_completeness": 0.3,
        "needs_clarity": 0.3
    }

    @classmethod
    def validate_config(cls) -> bool:
        """設定の妥当性をチェック"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        return True

# 設定検証
AppConfig.validate_config()

# エクスポート
__all__ = ["AppConfig"]