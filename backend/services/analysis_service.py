#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析サービス - 統合版
RESORT-TI分析とデータ分析の専用サービスモジュール
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.md_loader import get_md_configs
from shared.config import AppConfig

# 分析用のルーター
analysis_router = APIRouter()

# データモデル
class AnalysisRequest(BaseModel):
    user_messages: List[str]
    chat_history: List[Dict[str, Any]]
    user_data: Dict[str, Any]

class ResortAnalysisResponse(BaseModel):
    resort_scores: Dict[str, int]
    total_score: int
    dominant_aspects: List[str]
    analysis_summary: str

class NeedsAnalysisResponse(BaseModel):
    detected_needs: Dict[str, float]
    primary_need: str
    need_strength: float
    recommendations: List[str]

class ComprehensiveAnalysisResponse(BaseModel):
    resort_analysis: ResortAnalysisResponse
    needs_analysis: NeedsAnalysisResponse
    data_completeness: Dict[str, float]
    fortune_readiness_score: int

# RESORT-TI分析システム
class ResortAnalysisSystem:
    def __init__(self, md_configs: Dict[str, str]):
        self.md_configs = md_configs
        self._load_analysis_configs()

    def _load_analysis_configs(self):
        """MDファイルから分析設定を読み込み"""
        analysis_md = self.md_configs.get('analysis_system', '')

        # RESORT 6次元定義（v3.2仕様）
        self.resort_dimensions = {
            "relationship": {
                "keywords": ["彼氏", "彼女", "恋人", "友人", "家族", "職場", "人間関係", "付き合い", "関係"],
                "weight": 1.0,
                "description": "関係性の深さ・親密度",
                "scoring_factors": ["関係の質", "親密度", "相互理解度"]
            },
            "emotion": {
                "keywords": ["感情", "気持ち", "心", "悲しい", "嬉しい", "不安", "怒り", "ストレス", "辛い", "寂しい"],
                "weight": 1.2,
                "description": "感情の強度・種類",
                "scoring_factors": ["感情強度", "感情の複雑さ", "表現力"]
            },
            "situation": {
                "keywords": ["状況", "問題", "困った", "大変", "緊急", "急ぎ", "危機", "深刻", "今すぐ", "どうしよう"],
                "weight": 1.1,
                "description": "状況の緊急度・深刻度",
                "scoring_factors": ["緊急性", "深刻度", "複雑さ"]
            },
            "objective": {
                "keywords": ["目的", "目標", "したい", "欲しい", "どうしたら", "方法", "解決", "明確", "はっきり"],
                "weight": 0.9,
                "description": "相談者の目的の明確さ",
                "scoring_factors": ["目的の明確性", "具体性", "実現可能性"]
            },
            "resource": {
                "keywords": ["頑張る", "できる", "強い", "大丈夫", "乗り越える", "支え", "力", "エネルギー", "余裕"],
                "weight": 1.0,
                "description": "相談者の心理的リソース",
                "scoring_factors": ["心理的余裕", "回復力", "対処能力"]
            },
            "time": {
                "keywords": ["時間", "未来", "将来", "今後", "タイミング", "いつ", "最近", "今", "以前から", "長い間"],
                "weight": 1.0,
                "description": "時間的要因・タイミング",
                "scoring_factors": ["時間的切迫感", "継続性", "変化への準備"]
            }
        }

    def analyze_resort_scores(
        self,
        messages: List[str],
        user_data: Dict[str, Any],
        rally_count: int = 0
    ) -> Dict[str, int]:
        """RESORT 6次元スコア分析（v3.2仕様）"""

        scores = {}
        combined_text = " ".join(messages).lower()

        # 「彼氏から連絡がこない」の例に基づく詳細分析
        for dimension, config in self.resort_dimensions.items():
            base_score = 0

            # キーワードマッチングによる基本スコア
            keyword_matches = 0
            for keyword in config["keywords"]:
                if keyword in combined_text:
                    keyword_matches += 1

            # キーワード密度による加重
            if keyword_matches > 0:
                base_score = min(10, keyword_matches * 2)

            # 次元別の特別なロジック（v3.2仕様準拠）
            if dimension == "relationship":
                if any(word in combined_text for word in ["彼氏", "彼女", "恋人"]):
                    base_score = 7  # 彼氏との関係があることが前提
                elif any(word in combined_text for word in ["友人", "職場", "家族"]):
                    base_score = 5

            elif dimension == "emotion":
                emotion_indicators = ["不安", "心配", "寂しい", "辛い", "悲しい", "怒り"]
                emotion_count = sum(1 for word in emotion_indicators if word in combined_text)
                if emotion_count > 0:
                    base_score = min(8, 5 + emotion_count)  # 不安・心配・寂しさが混在
                elif "連絡" in combined_text and "ない" in combined_text:
                    base_score = 7  # 連絡がないという状況による感情

            elif dimension == "situation":
                urgency_words = ["緊急", "今すぐ", "どうしよう", "大変"]
                if any(word in combined_text for word in urgency_words):
                    base_score = 8
                elif "連絡" in combined_text and "ない" in combined_text:
                    base_score = 5  # 連絡がないという状況、緊急性は中程度

            elif dimension == "objective":
                if any(word in combined_text for word in ["どうしたら", "方法", "解決"]):
                    base_score = 6
                else:
                    base_score = 3  # 何を求めているか不明確

            elif dimension == "resource":
                positive_words = ["頑張る", "できる", "強い", "大丈夫"]
                negative_words = ["疲れた", "無理", "限界", "もうダメ"]

                positive_count = sum(1 for word in positive_words if word in combined_text)
                negative_count = sum(1 for word in negative_words if word in combined_text)

                if negative_count > positive_count:
                    base_score = 3
                else:
                    base_score = 5  # 現在の心理的余裕は中程度

            elif dimension == "time":
                time_words = ["最近", "今", "以前から", "長い間", "いつも"]
                if any(word in combined_text for word in time_words):
                    base_score = 8  # 継続的な状況
                elif "連絡" in combined_text:
                    base_score = 8  # 「連絡がこない」という継続的な状況

            # ユーザーデータからの補正
            if dimension in str(user_data).lower():
                base_score += 1

            # ラリー回数による微調整
            rally_adjustment = min(1, rally_count * 0.1)

            # 最終スコア計算（1-10の範囲）
            final_score = int(min(10, max(1, base_score + rally_adjustment)))
            scores[dimension] = final_score

        return scores

    def get_dominant_aspects(self, resort_scores: Dict[str, int], top_n: int = 3) -> List[str]:
        """主要な側面を特定"""
        sorted_scores = sorted(resort_scores.items(), key=lambda x: x[1], reverse=True)
        return [aspect for aspect, score in sorted_scores[:top_n] if score > 30]

    def generate_analysis_summary(self, resort_scores: Dict[str, int]) -> str:
        """分析サマリー生成（v3.2仕様準拠）"""

        # 各次元の説明を生成
        analysis_details = {}

        if resort_scores.get("relationship", 0) >= 7:
            analysis_details["relationship"] = "彼氏との関係があることが前提、ある程度の親密度"
        elif resort_scores.get("relationship", 0) >= 5:
            analysis_details["relationship"] = "人間関係の基盤はある"

        if resort_scores.get("emotion", 0) >= 7:
            analysis_details["emotion"] = "不安・心配・寂しさが混在、中〜高程度"
        elif resort_scores.get("emotion", 0) >= 5:
            analysis_details["emotion"] = "感情的な動揺が見られる"

        if resort_scores.get("situation", 0) >= 5:
            analysis_details["situation"] = "連絡がないという状況、緊急性は中程度"
        elif resort_scores.get("situation", 0) >= 3:
            analysis_details["situation"] = "問題状況が存在"

        if resort_scores.get("objective", 0) <= 3:
            analysis_details["objective"] = "何を求めているか不明確（理由を知りたい？対処法？）"
        elif resort_scores.get("objective", 0) >= 6:
            analysis_details["objective"] = "目的がある程度明確"

        if resort_scores.get("resource", 0) == 5:
            analysis_details["resource"] = "現在の心理的余裕は中程度"
        elif resort_scores.get("resource", 0) < 4:
            analysis_details["resource"] = "心理的リソースが不足気味"
        elif resort_scores.get("resource", 0) > 6:
            analysis_details["resource"] = "心理的余裕がある"

        if resort_scores.get("time", 0) >= 8:
            analysis_details["time"] = "「連絡がこない」という継続的な状況"
        elif resort_scores.get("time", 0) >= 6:
            analysis_details["time"] = "時間的な要因が影響している"

        # 分析詳細テキストを組み立て
        summary_parts = []
        for dimension, description in analysis_details.items():
            dimension_name = {
                "relationship": "関係性(R)",
                "emotion": "感情強度(E)",
                "situation": "状況深刻度(S)",
                "objective": "目的明確性(O)",
                "resource": "リソース(R)",
                "time": "時間的要因(T)"
            }.get(dimension, dimension)
            summary_parts.append(f"{dimension_name}: {description}")

        return "分析詳細：\n\n" + "\n".join(summary_parts)

    def display_resort_analysis_v32(self, resort_scores: Dict[str, int]) -> str:
        """v3.2仕様のRESORTスコア表示フォーマット"""

        total_score = sum(resort_scores.values()) / len(resort_scores)
        analysis_summary = self.generate_analysis_summary(resort_scores)

        display_text = "=" * 50 + "\n"
        display_text += "【RESORT 6次元分析結果】\n"
        display_text += "=" * 50 + "\n"
        display_text += f"R (Relationship/関係性): {resort_scores.get('relationship', 0)}/10\n"
        display_text += f"E (Emotion/感情強度): {resort_scores.get('emotion', 0)}/10\n"
        display_text += f"S (Situation/状況深刻度): {resort_scores.get('situation', 0)}/10\n"
        display_text += f"O (Objective/目的明確性): {resort_scores.get('objective', 0)}/10\n"
        display_text += f"R (Resource/心理的リソース): {resort_scores.get('resource', 0)}/10\n"
        display_text += f"T (Time/時間的要因): {resort_scores.get('time', 0)}/10\n"
        display_text += f"総合スコア: {total_score:.1f}/10\n"
        display_text += analysis_summary

        return display_text

# ニーズ分析システム（詳細版）
class DetailedNeedsAnalyzer:
    def __init__(self, md_configs: Dict[str, str]):
        self.md_configs = md_configs
        self._load_needs_configs()

    def _load_needs_configs(self):
        """MDファイルからニーズ設定を読み込み"""
        needs_md = self.md_configs.get('needs_detection', '')

        self.needs_categories = {
            "complaining_listening": {
                "keywords": ["疲れた", "つらい", "嫌になる", "困った", "大変", "ストレス", "愚痴"],
                "weight": 0.9,
                "description": "愚痴・傾聴ニーズ"
            },
            "emotion_organizing": {
                "keywords": ["混乱", "わからない", "迷い", "悩み", "もやもや", "整理"],
                "weight": 0.8,
                "description": "感情整理ニーズ"
            },
            "recognition_desire": {
                "keywords": ["頑張った", "努力", "認めて", "評価", "褒めて", "すごい"],
                "weight": 0.7,
                "description": "承認欲求ニーズ"
            },
            "encouragement": {
                "keywords": ["不安", "自信ない", "怖い", "心配", "緊張", "励まし"],
                "weight": 0.8,
                "description": "励ましニーズ"
            },
            "loneliness": {
                "keywords": ["一人", "寂しい", "孤独", "さみしい", "独り", "仲間"],
                "weight": 0.9,
                "description": "孤独感ニーズ"
            }
        }

    def analyze_detailed_needs(
        self,
        messages: List[str],
        context: Dict[str, Any]
    ) -> Dict[str, float]:
        """詳細ニーズ分析"""

        scores = {}
        combined_text = " ".join(messages).lower()

        for need_type, config in self.needs_categories.items():
            score = 0.0

            # キーワードマッチング
            for keyword in config["keywords"]:
                if keyword in combined_text:
                    score += 0.3 * config["weight"]

            # コンテキスト分析
            if need_type.replace("_", " ") in str(context).lower():
                score += 0.2

            # 最終スコア
            scores[need_type] = min(1.0, score)

        return scores

    def get_recommendations(self, needs: Dict[str, float]) -> List[str]:
        """ニーズベースの推奨事項"""
        recommendations = []

        for need_type, score in needs.items():
            if score > 0.5:
                if need_type == "complaining_listening":
                    recommendations.append("傾聴と共感的サポート")
                elif need_type == "emotion_organizing":
                    recommendations.append("感情整理と状況分析")
                elif need_type == "recognition_desire":
                    recommendations.append("努力の承認と称賛")
                elif need_type == "encouragement":
                    recommendations.append("励ましと勇気づけ")
                elif need_type == "loneliness":
                    recommendations.append("寄り添いと共感的同伴")

        return recommendations[:3]  # トップ3のみ

# データ完全性分析
def calculate_data_completeness(user_data: Dict[str, Any]) -> Dict[str, float]:
    """データ完全性の計算"""
    categories = {
        "basic_info": ["age", "gender", "occupation", "location"],
        "psychology_emotion": ["personality", "stress_level", "emotional_state"],
        "love_relationships": ["relationship_status", "love_history", "ideal_type"],
        "work_career": ["job_satisfaction", "career_goals", "work_environment"],
        "spiritual_values": ["beliefs", "fortune_interest", "life_philosophy"]
    }

    completeness = {}
    for category, required_fields in categories.items():
        present_fields = sum(1 for field in required_fields if user_data.get(field))
        completeness[category] = present_fields / len(required_fields)

    return completeness

# 分析エンドポイント
@analysis_router.post("/analysis/resort", response_model=ResortAnalysisResponse)
async def analyze_resort(
    request: AnalysisRequest,
    md_configs: Dict[str, str] = Depends(get_md_configs)
):
    """RESORT-TI分析エンドポイント"""
    try:
        analyzer = ResortAnalysisSystem(md_configs)

        rally_count = len(request.chat_history)
        resort_scores = analyzer.analyze_resort_scores(
            request.user_messages, request.user_data, rally_count
        )

        total_score = sum(resort_scores.values())
        dominant = analyzer.get_dominant_aspects(resort_scores)
        summary = analyzer.generate_analysis_summary(resort_scores)

        return ResortAnalysisResponse(
            resort_scores=resort_scores,
            total_score=total_score,
            dominant_aspects=dominant,
            analysis_summary=summary
        )

    except Exception as e:
        print(f"RESORT分析エラー: {str(e)}")
        raise HTTPException(status_code=500, detail="RESORT分析エラー")

@analysis_router.post("/analysis/needs", response_model=NeedsAnalysisResponse)
async def analyze_needs(
    request: AnalysisRequest,
    md_configs: Dict[str, str] = Depends(get_md_configs)
):
    """ニーズ分析エンドポイント"""
    try:
        analyzer = DetailedNeedsAnalyzer(md_configs)

        needs = analyzer.analyze_detailed_needs(request.user_messages, request.user_data)
        primary_need = max(needs, key=needs.get) if needs else "complaining_listening"
        need_strength = max(needs.values()) if needs else 0.0
        recommendations = analyzer.get_recommendations(needs)

        return NeedsAnalysisResponse(
            detected_needs=needs,
            primary_need=primary_need,
            need_strength=need_strength,
            recommendations=recommendations
        )

    except Exception as e:
        print(f"ニーズ分析エラー: {str(e)}")
        raise HTTPException(status_code=500, detail="ニーズ分析エラー")

@analysis_router.post("/analysis/comprehensive", response_model=ComprehensiveAnalysisResponse)
async def comprehensive_analysis(
    request: AnalysisRequest,
    md_configs: Dict[str, str] = Depends(get_md_configs)
):
    """包括分析エンドポイント"""
    try:
        # RESORT分析
        resort_analyzer = ResortAnalysisSystem(md_configs)
        rally_count = len(request.chat_history)
        resort_scores = resort_analyzer.analyze_resort_scores(
            request.user_messages, request.user_data, rally_count
        )

        # ニーズ分析
        needs_analyzer = DetailedNeedsAnalyzer(md_configs)
        needs = needs_analyzer.analyze_detailed_needs(request.user_messages, request.user_data)

        # データ完全性
        data_completeness = calculate_data_completeness(request.user_data)

        # 占い準備スコア
        total_resort = sum(resort_scores.values())
        avg_completeness = sum(data_completeness.values()) / len(data_completeness)
        needs_strength = sum(needs.values())

        fortune_readiness = int(
            total_resort * AppConfig.FORTUNE_TIMING_MULTIPLIERS["resort_total"] +
            avg_completeness * 100 * AppConfig.FORTUNE_TIMING_MULTIPLIERS["data_completeness"] +
            needs_strength * 100 * AppConfig.FORTUNE_TIMING_MULTIPLIERS["needs_clarity"]
        )

        return ComprehensiveAnalysisResponse(
            resort_analysis=ResortAnalysisResponse(
                resort_scores=resort_scores,
                total_score=sum(resort_scores.values()),
                dominant_aspects=resort_analyzer.get_dominant_aspects(resort_scores),
                analysis_summary=resort_analyzer.generate_analysis_summary(resort_scores)
            ),
            needs_analysis=NeedsAnalysisResponse(
                detected_needs=needs,
                primary_need=max(needs, key=needs.get) if needs else "complaining_listening",
                need_strength=max(needs.values()) if needs else 0.0,
                recommendations=needs_analyzer.get_recommendations(needs)
            ),
            data_completeness=data_completeness,
            fortune_readiness_score=min(100, fortune_readiness)
        )

    except Exception as e:
        print(f"包括分析エラー: {str(e)}")
        raise HTTPException(status_code=500, detail="包括分析エラー")