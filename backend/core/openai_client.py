#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI統合クライアント
統合サーバー用の単一OpenAI APIクライアント管理
"""

from openai import OpenAI
from typing import Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.config import AppConfig

class OpenAIClientManager:
    """OpenAI APIクライアント管理クラス（シングルトン）"""

    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = OpenAI(api_key=AppConfig.OPENAI_API_KEY)
        return cls._instance

    @property
    def client(self) -> OpenAI:
        """OpenAIクライアントインスタンスを取得"""
        return self._client

    async def generate_chat_response(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """チャット応答生成（統合版）"""

        try:
            response = self._client.chat.completions.create(
                model=AppConfig.CHAT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens or AppConfig.MAX_TOKENS,
                temperature=temperature or AppConfig.TEMPERATURE
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI API エラー: {e}")
            return "申し訳ございません。一時的にお答えできません。少し時間をおいてからもう一度お試しください。"

    async def generate_fortune_reading(
        self,
        fortune_prompt: str,
        user_data: Dict[str, Any],
        fortune_type: str
    ) -> str:
        """占い結果生成（専用メソッド）"""

        try:
            # 占い専用プロンプトを構築
            system_content = f"""
{fortune_prompt}

占いタイプ: {fortune_type}
ユーザーデータ: {user_data}

占い結果は以下の形式で生成してください：
- 具体的で的確な洞察
- 前向きで建設的なアドバイス
- 神秘的で魅力的な表現
- 3-5文程度での構成
"""

            response = self._client.chat.completions.create(
                model=AppConfig.CHAT_MODEL,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": f"{fortune_type}の占いをお願いします"}
                ],
                max_tokens=400,  # 占いは少し長めに
                temperature=0.8  # 創造性を高めに
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"占い生成エラー: {e}")
            return "星の導きが一時的に見えません。少し時間をおいてからもう一度お試しください。"


# シングルトンインスタンス
openai_manager = OpenAIClientManager()

def get_openai_client() -> OpenAI:
    """依存関係注入用のクライアント取得"""
    return openai_manager.client

def get_openai_manager() -> OpenAIClientManager:
    """マネージャーインスタンス取得"""
    return openai_manager