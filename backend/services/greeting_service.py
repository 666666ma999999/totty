#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
挨拶生成サービス - 統合版
キャラクター設定に基づいた動的挨拶生成サービス
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
from pydantic import BaseModel
from datetime import datetime
import yaml
import re
import os
from core.openai_client import get_openai_manager

# 挨拶用のルーター
greeting_router = APIRouter()

# データモデル
class GreetingRequest(BaseModel):
    visit_count: Optional[int] = 1
    user_context: Optional[Dict] = None

class GreetingResponse(BaseModel):
    greeting: str
    character_name: str
    character_role: str
    timestamp: str

class GreetingGenerator:
    """動的挨拶生成クラス"""

    def __init__(self):
        self.openai_manager = get_openai_manager()

    def load_character_config(self) -> Dict:
        """キャラクター設定を読み込み"""
        try:
            # 直接ファイルから読み込み
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            character_file_path = os.path.join(project_root, 'characters', 'psychic-character.md')

            with open(character_file_path, 'r', encoding='utf-8') as f:
                character_content = f.read()

            # YAML部分を抽出（最初のyamlブロックを取得）
            yaml_match = re.search(r'```yaml\n(.*?)\n```', character_content, re.DOTALL)
            if yaml_match:
                yaml_content = yaml_match.group(1)
                config = yaml.safe_load(yaml_content)
                print(f"✅ キャラクター設定読み込み成功: {config.get('role', 'unknown')}")
                return config
            else:
                print("❌ YAML部分が見つかりません")
                # 基本設定を返す
                return {
                    "role": "心の専門家パートナー",
                    "role_description": "豊富な経験と深い心理理解を持つ専門家でありながら、相談者と同じ目線で対話するパートナー",
                    "target_users": "20-40歳の女性",
                    "consultation_scope": "恋愛・仕事・人生全般"
                }

        except Exception as e:
            print(f"キャラクター設定読み込みエラー: {e}")
            # デフォルト設定
            return {
                "role": "心の専門家パートナー",
                "role_description": "心の専門家パートナー",
                "target_users": "20-40歳の女性",
                "consultation_scope": "恋愛・仕事・人生全般"
            }

    def load_greeting_system_content(self) -> str:
        """挨拶システム設定を直接読み込み"""
        try:
            # dataフォルダから直接読み込み（分割された新ファイル）
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            # コア設定と季節表現を結合
            core_file_path = os.path.join(project_root, 'data', 'greeting_core.md')
            seasonal_file_path = os.path.join(project_root, 'data', 'seasonal_expressions.md')

            greeting_content = ""

            with open(core_file_path, 'r', encoding='utf-8') as f:
                greeting_content += f.read()

            greeting_content += "\n\n"

            with open(seasonal_file_path, 'r', encoding='utf-8') as f:
                greeting_content += f.read()

            print(f"✅ 挨拶システム設定読み込み成功（分割ファイル対応）")
            return greeting_content

        except Exception as e:
            print(f"挨拶システム設定読み込みエラー: {e}")
            return ""

    def get_current_context(self, visit_count: int = 1) -> Dict:
        """現在のコンテキスト情報を取得"""
        now = datetime.now()

        # 時間帯の判定
        hour = now.hour
        if 5 <= hour < 12:
            time_period = "朝"
        elif 12 <= hour < 17:
            time_period = "昼"
        elif 17 <= hour < 21:
            time_period = "夕方"
        else:
            time_period = "夜"

        # 季節の判定
        month = now.month
        if 3 <= month <= 5:
            season = "春"
        elif 6 <= month <= 8:
            season = "夏"
        elif 9 <= month <= 11:
            season = "秋"
        else:
            season = "冬"

        return {
            "current_datetime": now.strftime("%Y年%m月%d日 %H時%M分"),
            "weekday": ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"][now.weekday()],
            "time_period": time_period,
            "season": season,
            "weather": "晴れ",  # デフォルト値
            "visit_count": visit_count
        }

    def build_system_prompt(self, character_config: Dict, context: Dict) -> str:
        """システムプロンプトを構築（完全MDファイル依存）"""

        # greeting_system.mdを直接読み込み（ハードコード一切なし）
        greeting_system_content = self.load_greeting_system_content()

        if not greeting_system_content:
            print("❌ greeting_system.mdの読み込みに失敗しました")
            return "エラー: システムプロンプトが読み込めませんでした"

        # 動的な値のみを追加
        dynamic_context = f"""

現在の状況:
- 日時: {context['current_datetime']}
- 曜日: {context['weekday']}
- 時間帯: {context['time_period']}
- 季節: {context['season']}
- ユーザー訪問回数: {context['visit_count']}回目

キャラクター設定:
- 役割: {character_config.get('role', '心の専門家パートナー')}
- 対象ユーザー: {character_config.get('target_users', '20-40歳の女性')}
- 相談範囲: {character_config.get('consultation_scope', '恋愛・仕事・人生全般')}

上記の状況とキャラクター設定を考慮した自然で温かい挨拶文を生成してください。"""

        print("✅ greeting_system.mdからシステムプロンプト構築完了")
        return greeting_system_content + dynamic_context

    def generate_greeting(self, visit_count: int = 1, user_context: Optional[Dict] = None) -> str:
        """AI挨拶文を生成"""
        try:
            # キャラクター設定読み込み
            character_config = self.load_character_config()

            # コンテキスト取得
            context = self.get_current_context(visit_count)
            if user_context:
                context.update(user_context)

            # システムプロンプト構築
            system_prompt = self.build_system_prompt(character_config, context)

            # OpenAI APIで挨拶生成
            client = self.openai_manager.client
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "キャラクター「蒼司」として、心の専門家パートナーとして、自然で温かい挨拶文を生成してください。"}
                ],
                max_tokens=300,
                temperature=0.8
            )

            greeting_text = response.choices[0].message.content.strip()
            return greeting_text

        except Exception as e:
            print(f"挨拶生成エラー: {e}")
            # フォールバック挨拶
            return "こんにちは。私は蒼司と申します。心の専門家パートナーとして、あなたのお話をお聞きし、一緒に答えを見つけていけたらと思います。今日はどのようなことでお悩みでしょうか？"

# APIエンドポイント
@greeting_router.get("/api/greeting")
def get_greeting(visit_count: int = 1):
    """動的挨拶を取得"""
    try:
        generator = GreetingGenerator()
        greeting_text = generator.generate_greeting(visit_count=visit_count)
        character_config = generator.load_character_config()

        return GreetingResponse(
            greeting=greeting_text,
            character_name="蒼司",
            character_role=character_config.get('role', '心の専門家パートナー'),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"挨拶生成エラー: {str(e)}")

@greeting_router.post("/api/greeting")
def generate_custom_greeting(request: GreetingRequest):
    """カスタム挨拶を生成"""
    try:
        generator = GreetingGenerator()
        greeting_text = generator.generate_greeting(
            visit_count=request.visit_count or 1,
            user_context=request.user_context
        )
        character_config = generator.load_character_config()

        return GreetingResponse(
            greeting=greeting_text,
            character_name="蒼司",
            character_role=character_config.get('role', '心の専門家パートナー'),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"カスタム挨拶生成エラー: {str(e)}")