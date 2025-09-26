#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
チャットサービス - 統合版
チャット処理とレスポンス生成の専用サービスモジュール
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime
import yaml

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.md_loader import get_md_configs, get_character_config
from core.openai_client import get_openai_manager
from core.response_engine import FlexibleResponseEngine
from shared.config import AppConfig
from services.chat_history_service import save_chat_interaction
import uuid

# チャット用のルーター
chat_router = APIRouter()

# データモデル
class ChatMessage(BaseModel):
    message: str
    user_data: Optional[Dict] = None
    chat_history: Optional[List[Dict]] = None
    rally_count: int = 0
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    category: str
    needs_analysis: Dict[str, float]
    emotion_analysis: Dict[str, Any]
    resort_scores: Dict[str, int]
    fortune_timing_score: int
    suggested_fortune: Optional[str] = None
    session_id: str

# ニーズ分析クラス（統合版）
class NeedsAnalyzer:
    def __init__(self, md_configs: Dict[str, str]):
        self.md_configs = md_configs
        self._load_keywords_from_md()

    def _load_keywords_from_md(self):
        """MDファイルからキーワードを読み込み"""
        needs_md = self.md_configs.get('needs_detection', '')

        # 簡易的なキーワード抽出（実際はMDファイルをパースする）
        self.keywords = {
            "complaining_listening": ["疲れ", "つらい", "嫌", "困った", "大変", "ストレス"],
            "emotion_organizing": ["混乱", "わからない", "迷い", "悩み", "もやもや"],
            "recognition_desire": ["頑張", "努力", "認めて", "評価", "褒めて"],
            "encouragement": ["不安", "自信ない", "怖い", "心配", "緊張"],
            "loneliness": ["一人", "寂しい", "孤独", "さみしい", "独り"]
        }

    def analyze(self, message: str) -> Dict[str, float]:
        """ニーズ分析実行"""
        scores = {}

        for need_type, keywords in self.keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword in message:
                    score += 0.7

            scores[need_type] = min(score, 1.0)

        return scores

# カテゴリ選択クラス（統合版）
class CategorySelector:
    def __init__(self, md_configs: Dict[str, str]):
        self.md_configs = md_configs
        self._load_categories_from_md()

    def _load_categories_from_md(self):
        """MDファイルからカテゴリ情報を読み込み"""
        categories_md = self.md_configs.get('third_sentence_categories', '')

        # MDファイルから12カテゴリを抽出
        self.categories = [
            "深い共感", "優しい励まし", "認めと賞賛", "寄り添い",
            "整理支援", "未来志向", "自己価値向上", "安心感提供",
            "愛情表現", "成長促進", "直感重視", "占い誘導"
        ]

    def select_category(self, needs_analysis: Dict[str, float], rally_count: int) -> str:
        """最適カテゴリを選択"""
        max_need = max(needs_analysis.values()) if needs_analysis.values() else 0

        if max_need == 0:
            return "深い共感"

        # 最もスコアの高いニーズに基づいてカテゴリ選択
        top_need = max(needs_analysis, key=needs_analysis.get)

        need_to_category = {
            "complaining_listening": "深い共感",
            "emotion_organizing": "整理支援",
            "recognition_desire": "認めと賞賛",
            "encouragement": "優しい励まし",
            "loneliness": "寄り添い"
        }

        return need_to_category.get(top_need, "深い共感")

# システムプロンプト生成
def generate_system_prompt(
    needs_analysis: Dict[str, float],
    category: str,
    rally_count: int,
    md_configs: Dict[str, str],
    character_config: str
) -> str:
    """MDファイルベースのシステムプロンプト生成"""

    base_prompt = f"""
{character_config}

以下のMDファイル設定に従って応答してください：

【ニーズ判別システム】
{md_configs.get('needs_detection', '')}

【第3文カテゴリシステム】
{md_configs.get('third_sentence_categories', '')}

【カテゴリ選択システム】
{md_configs.get('category_selection', '')}

現在の分析結果：
- 検出ニーズ: {needs_analysis}
- 選択カテゴリ: {category}
- ラリー回数: {rally_count}

重要な制約：
- 必ず3センテンス以内で応答してください
- 150-250文字程度を目安としてください
- 選択されたカテゴリ「{category}」に沿った応答をしてください
- 共感性を最優先に、温かみのある応答をしてください
"""

    return base_prompt

# Claude Sonnet API感情分析システム（v3.2対応）
# 旧キーワードベース分析システムは削除済み

def analyze_emotion_advanced(message: str, md_configs: Dict[str, str]) -> Dict[str, Any]:
    """Claude Sonnet APIベース高度感情分析（v3.2仕様）"""
    import json
    try:
        # 環境変数からAPIキーをチェック
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            print("ANTHROPIC_API_KEY not found, using fallback analysis")
            return analyze_emotion_fallback(message)

        # Anthropic Claude APIを使用した感情分析
        import requests

        emotion_md = md_configs.get('emotion_analysis_system', '')

        # Claude APIプロンプト生成
        analysis_prompt = f"""
以下のMDファイル設定に基づいて、ユーザーメッセージの感情分析を行ってください：

{emotion_md}

【分析対象メッセージ】
"{message}"

【要求する分析結果（JSON形式で返答）】
{{
  "primary_emotion": "主要感情（日本語）",
  "emotion_intensity": 0-100の整数値,
  "emotion_layers": {{
    "surface": "表層感情",
    "middle": "中層感情",
    "deep": "深層感情"
  }},
  "empathy_level": 1-5の整数値,
  "tone_matching": "推奨トーン",
  "analysis_quality": "primary または enhanced",
  "crisis_level": 0-5の危機レベル
}}

特に「彼氏から連絡がこない」のようなメッセージは不安感情として強度70で判定してください。
文脈を理解して適切な感情分析を行ってください。
JSONのみを返答してください。
"""

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }

        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": analysis_prompt}
            ]
        }

        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=data,
            timeout=30
        )

        if response.status_code == 200:
            result_data = response.json()
            result_text = result_data["content"][0]["text"]

            # JSON抽出
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "{" in result_text:
                json_start = result_text.find("{")
                json_end = result_text.rfind("}") + 1
                result_text = result_text[json_start:json_end]

            analysis_result = json.loads(result_text)

            # 後方互換性のための追加データ
            analysis_result.update({
                "polarity": 1.0 if analysis_result["primary_emotion"] in ["喜び", "愛情", "感謝", "安心", "期待"] else -1.0,
                "intensity": analysis_result["emotion_intensity"] / 100.0,
                "dominant_emotion": analysis_result["primary_emotion"]
            })

            return analysis_result
        else:
            print(f"Claude API error: {response.status_code}")
            return analyze_emotion_fallback(message)

    except Exception as e:
        print(f"Claude API感情分析エラー: {e}")
        return analyze_emotion_fallback(message)

def analyze_emotion_fallback(message: str) -> Dict[str, Any]:
    """フォールバック用簡易感情分析"""
    # 特別パターン検出
    if "連絡" in message and ("こない" in message or "来ない" in message or "ない" in message):
        return {
            "primary_emotion": "不安",
            "emotion_intensity": 70,
            "emotion_layers": {
                "surface": "不安",
                "middle": "愛情欲求・安全欲求",
                "deep": "安心して愛されたい"
            },
            "empathy_level": 4,
            "tone_matching": "優しく安定した",
            "analysis_quality": "primary",
            "crisis_level": 2,
            "polarity": -1.0,
            "intensity": 0.7,
            "dominant_emotion": "不安"
        }

    # デフォルト（ニュートラル）
    return {
        "primary_emotion": "ニュートラル",
        "emotion_intensity": 0,
        "emotion_layers": {
            "surface": "平静",
            "middle": "安定",
            "deep": "現状維持"
        },
        "empathy_level": 1,
        "tone_matching": "丁寧・落ち着いた",
        "analysis_quality": "primary",
        "crisis_level": 0,
        "polarity": 0.0,
        "intensity": 0.0,
        "dominant_emotion": "ニュートラル"
    }

def infer_middle_emotion(primary_emotion: str, message: str) -> str:
    """中層感情推論"""
    middle_patterns = {
        "怒り": "不安・失望" if "心配" in message or "期待" in message else "コントロール欲求",
        "不安": "安全欲求・愛情欲求",
        "悲しみ": "愛されたい欲求・承認欲求",
        "孤独": "つながり欲求・理解されたい欲求",
        "嫉妬": "自己価値の不安・愛情独占欲求",
        "迷い": "自己効力感の低下・方向性への不安",
        "喜び": "達成感・承認獲得",
        "期待": "変化への不安・希望"
    }

    return middle_patterns.get(primary_emotion, "自己理解の欲求")

def infer_deep_emotion(primary_emotion: str, message: str) -> str:
    """深層感情推論"""
    deep_patterns = {
        "怒り": "愛されたい・認められたい",
        "不安": "安心して愛されたい",
        "悲しみ": "深く愛されたい・価値を感じたい",
        "孤独": "無条件に愛されたい・理解されたい",
        "嫉妬": "唯一無二の存在でありたい",
        "迷い": "自分らしく生きたい・意味を感じたい",
        "喜び": "存在価値を感じたい・つながりたい",
        "期待": "成長したい・可能性を実現したい"
    }

    return deep_patterns.get(primary_emotion, "ありのままの自分を愛されたい")

def calculate_empathy_level(intensity: int, thresholds: List[int]) -> int:
    """共感レベル判定"""
    if intensity >= thresholds[3]:  # 85+
        return 5
    elif intensity >= thresholds[2]:  # 70+
        return 4
    elif intensity >= thresholds[1]:  # 50+
        return 3
    elif intensity >= thresholds[0]:  # 30+
        return 2
    else:
        return 1

def analyze_tone_matching(message: str) -> str:
    """トーンマッチング分析"""
    if any(word in message for word in ["やばい", "マジで", "めっちゃ", "だわ"]):
        return "カジュアル・親しみやすい"
    elif any(word in message for word in ["です", "ます", "恐れ入りますが"]):
        return "丁寧・落ち着いた"
    elif "！！" in message or "。。。" in message:
        return "感情的・不安定"
    elif any(word in message for word in ["思うに", "考えてみると", "分析すると"]):
        return "理知的・分析的"
    else:
        return "自然体・バランス型"

def detect_crisis_level(message: str) -> int:
    """危機レベル検出"""
    level_5_keywords = ["死にたい", "消えたい", "いなくなりたい", "終わりにしたい"]
    level_4_keywords = ["もうダメ", "限界", "耐えられない", "壊れそう"]
    level_3_keywords = ["疲れた", "辛すぎる", "苦しい"]

    for keyword in level_5_keywords:
        if keyword in message:
            return 5

    for keyword in level_4_keywords:
        if keyword in message:
            return 4

    for keyword in level_3_keywords:
        if keyword in message:
            return 3

    return 0

def calculate_polarity(primary_emotion: str) -> float:
    """後方互換性のための極性計算"""
    positive_emotions = ["喜び", "安心", "感謝", "期待", "愛情"]
    negative_emotions = ["不安", "悲しみ", "怒り", "絶望", "孤独", "嫉妬", "恥"]

    if primary_emotion in positive_emotions:
        return 0.7
    elif primary_emotion in negative_emotions:
        return -0.7
    else:
        return 0.0

# 既存の関数名を維持（後方互換性）
def analyze_emotion(message: str, md_configs: Dict[str, str] = None) -> Dict[str, Any]:
    """感情分析（改良版）"""
    if md_configs:
        return analyze_emotion_advanced(message, md_configs)
    else:
        # フォールバック（従来の簡易版）
        return {
            "primary_emotion": "ニュートラル",
            "emotion_intensity": 0,
            "emotion_layers": {"surface": "平静", "middle": "安定", "deep": "現状維持"},
            "empathy_level": 1,
            "tone_matching": "自然体",
            "analysis_quality": "basic",
            "polarity": 0.0,
            "intensity": 0.0,
            "dominant_emotion": "ニュートラル"
        }

def load_resort_rules(md_content: str) -> Dict[str, Any]:
    """リゾート計算ルールをMDファイルから読み込み"""
    import re
    import yaml

    rules = {
        "relationship": {},
        "emotion": {},
        "situation": {},
        "objective": {},
        "resource": {},
        "time": {},
        "fortune_mapping": {},
        "timing_calculation": {}
    }

    # YAMLブロックを抽出
    yaml_blocks = re.findall(r'```yaml\n(.*?)\n```', md_content, re.DOTALL)

    for block in yaml_blocks:
        try:
            yaml_data = yaml.safe_load(block)
            if yaml_data:
                # 各セクションのルールを統合
                if "relationship_keywords" in yaml_data:
                    rules["relationship"] = yaml_data["relationship_keywords"]
                if "emotion_keywords" in yaml_data:
                    rules["emotion"] = yaml_data["emotion_keywords"]
                    if "special_patterns" in yaml_data:
                        rules["emotion"]["special_patterns"] = yaml_data["special_patterns"]
                    if "default_emotion" in yaml_data:
                        rules["emotion"]["default_emotion"] = yaml_data["default_emotion"]
                if "situation_keywords" in yaml_data:
                    rules["situation"] = yaml_data["situation_keywords"]
                if "objective_keywords" in yaml_data:
                    rules["objective"] = yaml_data["objective_keywords"]
                if "resource_keywords" in yaml_data:
                    rules["resource"] = yaml_data["resource_keywords"]
                    if "calculation_logic" in yaml_data:
                        rules["resource"]["calculation_logic"] = yaml_data["calculation_logic"]
                if "time_keywords" in yaml_data:
                    rules["time"] = yaml_data["time_keywords"]
                if "fortune_mapping" in yaml_data:
                    rules["fortune_mapping"] = yaml_data["fortune_mapping"]
                if "timing_calculation" in yaml_data:
                    rules["timing_calculation"] = yaml_data["timing_calculation"]
        except:
            continue

    return rules

def calculate_resort_scores(message: str, needs_analysis: Dict[str, float], rally_count: int, md_configs: Dict[str, str] = None) -> Dict[str, int]:
    """RESORT 6次元スコア計算（v3.2仕様 - MDベース）"""
    combined_text = message.lower()
    scores = {}

    # MDファイルからルールを読み込み
    if md_configs and "resort_v32_analysis" in md_configs:
        rules = load_resort_rules(md_configs["resort_v32_analysis"])
    else:
        # フォールバック: 簡易ルール
        rules = {}

    # 1. Relationship (関係性の深さ・親密度)
    if rules.get("relationship"):
        rel_rules = rules["relationship"]
        if "high_intimacy" in rel_rules and any(word in combined_text for word in rel_rules["high_intimacy"].get("keywords", [])):
            scores["relationship"] = rel_rules["high_intimacy"].get("score", 7)
        elif "medium_intimacy" in rel_rules and any(word in combined_text for word in rel_rules["medium_intimacy"].get("keywords", [])):
            scores["relationship"] = rel_rules["medium_intimacy"].get("score", 5)
        else:
            scores["relationship"] = max(1, rally_count)
    else:
        # フォールバック
        if any(word in combined_text for word in ["彼氏", "彼女", "恋人"]):
            scores["relationship"] = 7
        elif any(word in combined_text for word in ["友人", "職場", "家族"]):
            scores["relationship"] = 5
        else:
            scores["relationship"] = max(1, rally_count)

    # 2. Emotion (感情の強度・種類)
    if rules.get("emotion"):
        emo_rules = rules["emotion"]
        strong_emotions = emo_rules.get("strong_emotions", [])
        emotion_count = sum(1 for word in strong_emotions if word in combined_text)

        if emotion_count > 0:
            scores["emotion"] = min(8, 5 + emotion_count)
        elif "special_patterns" in emo_rules and "contact_anxiety" in emo_rules["special_patterns"]:
            contact_pattern = emo_rules["special_patterns"]["contact_anxiety"].get("pattern", [])
            if len(contact_pattern) >= 2 and all(word in combined_text for word in contact_pattern):
                scores["emotion"] = emo_rules["special_patterns"]["contact_anxiety"].get("score", 7)
            else:
                scores["emotion"] = max(1, int(sum(needs_analysis.values()) * 5))
        else:
            scores["emotion"] = max(1, int(sum(needs_analysis.values()) * 5))
    else:
        # フォールバック
        emotion_indicators = ["不安", "心配", "寂しい", "辛い", "悲しい", "怒り"]
        emotion_count = sum(1 for word in emotion_indicators if word in combined_text)
        if emotion_count > 0:
            scores["emotion"] = min(8, 5 + emotion_count)
        elif "連絡" in combined_text and "ない" in combined_text:
            scores["emotion"] = 7
        else:
            scores["emotion"] = max(1, int(sum(needs_analysis.values()) * 5))

    # 3. Situation (状況の緊急度・深刻度)
    if rules.get("situation"):
        sit_rules = rules["situation"]
        if "urgency_high" in sit_rules and any(word in combined_text for word in sit_rules["urgency_high"].get("keywords", [])):
            scores["situation"] = sit_rules["urgency_high"].get("score", 8)
        elif "contact_situation" in sit_rules:
            contact_pattern = sit_rules["contact_situation"].get("pattern", [])
            if len(contact_pattern) >= 2 and all(word in combined_text for word in contact_pattern):
                scores["situation"] = sit_rules["contact_situation"].get("score", 5)
            else:
                scores["situation"] = max(1, min(7, rally_count + 2))
        else:
            scores["situation"] = max(1, min(7, rally_count + 2))
    else:
        # フォールバック
        urgency_words = ["緊急", "今すぐ", "どうしよう", "大変"]
        if any(word in combined_text for word in urgency_words):
            scores["situation"] = 8
        elif "連絡" in combined_text and "ない" in combined_text:
            scores["situation"] = 5
        else:
            scores["situation"] = max(1, min(7, rally_count + 2))

    # 4. Objective (相談者の目的の明確さ)
    if rules.get("objective"):
        obj_rules = rules["objective"]
        if "clear_purpose" in obj_rules and any(word in combined_text for word in obj_rules["clear_purpose"].get("keywords", [])):
            scores["objective"] = obj_rules["clear_purpose"].get("score", 6)
        else:
            scores["objective"] = obj_rules.get("default", {}).get("score", 3)
    else:
        # フォールバック
        if any(word in combined_text for word in ["どうしたら", "方法", "解決"]):
            scores["objective"] = 6
        else:
            scores["objective"] = 3

    # 5. Resource (相談者の心理的リソース)
    if rules.get("resource"):
        res_rules = rules["resource"]
        positive_count = 0
        negative_count = 0

        if "positive" in res_rules:
            positive_count = sum(1 for word in res_rules["positive"].get("keywords", []) if word in combined_text)
        if "negative" in res_rules:
            negative_count = sum(1 for word in res_rules["negative"].get("keywords", []) if word in combined_text)

        if "calculation_logic" in res_rules:
            calc_logic = res_rules["calculation_logic"]
            if negative_count > positive_count:
                scores["resource"] = calc_logic.get("if_negative_dominates", 3)
            else:
                scores["resource"] = calc_logic.get("default", 5)
        else:
            scores["resource"] = 3 if negative_count > positive_count else 5
    else:
        # フォールバック
        positive_words = ["頑張る", "できる", "強い", "大丈夫"]
        negative_words = ["疲れた", "無理", "限界", "もうダメ"]
        positive_count = sum(1 for word in positive_words if word in combined_text)
        negative_count = sum(1 for word in negative_words if word in combined_text)
        scores["resource"] = 3 if negative_count > positive_count else 5

    # 6. Time (時間的要因・タイミング)
    if rules.get("time"):
        time_rules = rules["time"]
        if "temporal_indicators" in time_rules and any(word in combined_text for word in time_rules["temporal_indicators"].get("keywords", [])):
            scores["time"] = time_rules["temporal_indicators"].get("score", 8)
        elif "contact_temporal" in time_rules:
            contact_pattern = time_rules["contact_temporal"].get("pattern", [])
            if any(word in combined_text for word in contact_pattern):
                scores["time"] = time_rules["contact_temporal"].get("score", 8)
            else:
                scores["time"] = max(1, rally_count)
        else:
            scores["time"] = max(1, rally_count)
    else:
        # フォールバック
        time_words = ["最近", "今", "以前から", "長い間", "いつも"]
        if any(word in combined_text for word in time_words):
            scores["time"] = 8
        elif "連絡" in combined_text:
            scores["time"] = 8
        else:
            scores["time"] = max(1, rally_count)

    # スコアを1-10に正規化
    for key in scores:
        scores[key] = min(10, max(1, scores[key]))

    return scores

def calculate_fortune_timing(resort_scores: Dict[str, int], needs_analysis: Dict[str, float], md_configs: Dict[str, str] = None) -> int:
    """占いタイミングスコア計算（MDベース）"""
    # MDファイルからルールを読み込み
    if md_configs and "resort_v32_analysis" in md_configs:
        rules = load_resort_rules(md_configs["resort_v32_analysis"])
        timing_rules = rules.get("timing_calculation", {})

        resort_weight = timing_rules.get("resort_weight", 0.4)
        needs_weight = timing_rules.get("needs_weight", 0.6)
    else:
        # フォールバック
        resort_weight = 0.4
        needs_weight = 0.6

    total_resort = sum(resort_scores.values()) / len(resort_scores)
    needs_strength = sum(needs_analysis.values()) * 10

    timing_score = int(total_resort * resort_weight + needs_strength * needs_weight)
    return min(100, max(0, timing_score))

def suggest_fortune_menu(resort_scores: Dict[str, int], needs_analysis: Dict[str, float], md_configs: Dict[str, str] = None) -> Optional[str]:
    """占いメニュー提案（MDベース）"""
    max_resort_key = max(resort_scores, key=resort_scores.get)

    # MDファイルからルールを読み込み
    if md_configs and "resort_v32_analysis" in md_configs:
        rules = load_resort_rules(md_configs["resort_v32_analysis"])
        fortune_mapping = rules.get("fortune_mapping", {})
    else:
        # フォールバック
        fortune_mapping = {
            "romance": "相手の本音占い",
            "relationship": "人間関係修復",
            "emotion": "恋愛進展タイミング",
            "spirit": "運命の相手探し",
            "occupation": "総合運勢・人生指針"
        }

    default_menu = fortune_mapping.get("default", "総合運勢・人生指針")
    return fortune_mapping.get(max_resort_key, default_menu)

def generate_fallback_response(message: str) -> str:
    """フォールバック応答生成"""
    return "お話を聞かせていただき、ありがとうございます。あなたの気持ちに寄り添いたいと思います。どのようなことでも、遠慮なくお話しください。"

# チャットエンドポイント
@chat_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatMessage,
    md_configs: Dict[str, str] = Depends(get_md_configs),
    openai_manager = Depends(get_openai_manager)
):
    """メインチャット応答エンドポイント"""
    try:
        # MDファイル設定でインスタンス作成
        needs_analyzer = NeedsAnalyzer(md_configs)
        category_selector = CategorySelector(md_configs)
        character_config = get_character_config()

        # ニーズ分析
        needs_analysis = needs_analyzer.analyze(request.message)

        # 高度な感情分析を先に実行
        emotion_analysis = analyze_emotion_advanced(request.message, md_configs)
        resort_scores = calculate_resort_scores(request.message, needs_analysis, request.rally_count, md_configs)

        # 柔軟レスポンス生成エンジンを使用
        try:
            # プロジェクトルートからsystemsへのパスを構築 (backend/../systems)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            systems_path = os.path.join(project_root, "systems")
            response_engine = FlexibleResponseEngine(systems_path)

            # レスポンス生成（OpenAI連携対応）
            response_result = await response_engine.get_best_response(
                message=request.message,
                emotion_analysis=emotion_analysis,
                resort_scores=resort_scores,
                rally_count=request.rally_count,
                openai_manager=openai_manager
            )

            ai_response = response_result['response']
            # 新システムで生成されたパターンをカテゴリとして使用
            selected_category = response_result.get('pattern', 'unknown_pattern')

            # デバッグ情報（開発時）
            if AppConfig.DEBUG:
                print(f"=== レスポンス生成結果 ===")
                print(f"パターン: {response_result.get('pattern', 'unknown')}")
                print(f"スコア: {response_result.get('score', 0)}")
                print(f"理由: {response_result.get('reasoning', 'unknown')}")

        except Exception as response_error:
            print(f"柔軟レスポンス生成エラー: {response_error}")

            # フォールバック：従来のカテゴリ選択システム
            selected_category = category_selector.select_category(needs_analysis, request.rally_count)
            system_prompt = generate_system_prompt(
                needs_analysis, selected_category, request.rally_count,
                md_configs, character_config
            )

            ai_response = await openai_manager.generate_chat_response(
                system_prompt, request.message
            )

        # 占い提案タイミング計算
        fortune_timing_score = calculate_fortune_timing(resort_scores, needs_analysis, md_configs)

        # 占い提案判定
        suggested_fortune = None
        if fortune_timing_score >= AppConfig.RESORT_ANALYSIS_THRESHOLD:
            suggested_fortune = suggest_fortune_menu(resort_scores, needs_analysis, md_configs)

        # セッション継続機能付きでチャット履歴保存
        session_id = save_chat_interaction(
            session_id=request.session_id,
            user_message=request.message,
            ai_response=ai_response,
            analysis_data={
                "category": selected_category,
                "needs_analysis": needs_analysis,
                "emotion_analysis": emotion_analysis,
                "resort_scores": resort_scores,
                "fortune_timing_score": fortune_timing_score,
                "suggested_fortune": suggested_fortune,
                "rally_count": request.rally_count,
                "user_data": request.user_data or {}
            }
        )

        return ChatResponse(
            response=ai_response,
            category=selected_category,
            needs_analysis=needs_analysis,
            emotion_analysis=emotion_analysis,
            resort_scores=resort_scores,
            fortune_timing_score=fortune_timing_score,
            suggested_fortune=suggested_fortune,
            session_id=session_id
        )

    except Exception as e:
        print(f"チャットサービスエラー: {str(e)}")

        # エラー時のフォールバック
        fallback_response = generate_fallback_response(request.message)

        return ChatResponse(
            response=fallback_response,
            category="深い共感",
            needs_analysis={k: 0.0 for k in ["complaining_listening", "emotion_organizing", "recognition_desire", "encouragement", "loneliness"]},
            emotion_analysis={"polarity": 0.0, "intensity": 0.0, "dominant_emotion": "ニュートラル"},
            resort_scores={k: 1 for k in ["relationship", "emotion", "situation", "objective", "resource", "time"]},
            fortune_timing_score=0,
            session_id=request.session_id or "fallback_session"
        )

# ログエンドポイント
@chat_router.post("/log")
async def log_endpoint(log_data: dict):
    """ログ受信エンドポイント"""
    try:
        timestamp = log_data.get('timestamp', datetime.now().isoformat())
        log_type = log_data.get('type', 'unknown')

        print(f"[{timestamp}] Frontend Log - {log_type}: {log_data}")

        return {"status": "ok", "message": "ログを受信しました"}

    except Exception as e:
        print(f"ログエラー: {str(e)}")
        raise HTTPException(status_code=500, detail="ログ処理エラー")

# JavaScript互換性のための占い実行エンドポイント
@chat_router.post("/fortune")
async def fortune_endpoint(
    request: Dict,
    openai_manager = Depends(get_openai_manager)
):
    """占い実行エンドポイント（JavaScript互換）"""
    try:
        fortune_type = request.get('fortune_type', '総合運勢・人生指針')
        user_data = request.get('user_data', {})
        specific_context = request.get('specific_context', '')

        # 占い専用プロンプト生成
        fortune_prompt = f"""
あなたは霊能師「蒼司」として、以下の占いを実行してください：

占いタイプ: {fortune_type}
ユーザーデータ: {user_data}
追加コンテキスト: {specific_context}

占い結果は以下の特徴で生成してください：
- 神秘的で魅力的な表現
- 具体的で的確な洞察
- 前向きで建設的なアドバイス
- 3-5文程度での構成
- 蒼司らしい温かく上品な口調
"""

        # OpenAI API呼び出し
        result = await openai_manager.generate_fortune_reading(
            fortune_prompt, user_data, fortune_type
        )

        return {"fortune_result": result}

    except Exception as e:
        print(f"占い実行エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"占い実行エラー: {str(e)}")