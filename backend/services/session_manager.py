#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
セッション管理・データ収集システム
171項目のユーザーデータを管理し、重複質問を防ぐシステム
"""

import json
import uuid
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from copy import deepcopy

@dataclass
class DataField:
    """データフィールドの基本構造"""
    value: Any = None
    confidence: float = 0.0
    source: str = ""
    timestamp: str = ""

@dataclass
class UserSession:
    """ユーザーセッションデータ"""
    user_id: str
    session_id: str
    timestamp: str
    basic_info: Dict[str, DataField]
    psychology_emotion: Dict[str, DataField]
    love_relationships: Dict[str, DataField]
    work_career: Dict[str, DataField]
    spiritual_values: Dict[str, DataField]
    analysis_results: Dict[str, Any]
    chat_history: List[Dict[str, Any]]

class SessionManager:
    """セッション管理システム"""

    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
        self.init_data_structure()

    def init_data_structure(self):
        """171項目データ構造の初期化テンプレート"""
        self.basic_info_template = {
            "age": DataField(),
            "gender": DataField(),
            "occupation": DataField(),
            "location": DataField(),
            "family_structure": DataField(),
            "relationship_status": DataField(),
            "hobbies": DataField(value=[]),
            "personality_traits": DataField(value=[]),
            "values": DataField(value=[]),
            "lifestyle": DataField(),
            "income_level": DataField(),
            "education": DataField(),
            "health_status": DataField(),
            "stress_level": DataField(value=0),
            "sleep_hours": DataField(value=0),
            "exercise_habits": DataField(),
            "dietary_habits": DataField(),
            "sociability": DataField(value=0),
            "future_goals": DataField(value=[]),
            "happiness_level": DataField(value=0)
        }

        self.psychology_emotion_template = {
            "emotional_state": DataField(),
            "anxiety_level": DataField(value=0),
            "confidence_level": DataField(value=0),
            "stress_factors": DataField(value=[]),
            "coping_mechanisms": DataField(value=[]),
            "emotional_triggers": DataField(value=[]),
            "support_system": DataField(value=[]),
            "communication_style": DataField(),
            "conflict_resolution": DataField(),
            "decision_making_style": DataField(),
            "motivation_factors": DataField(value=[]),
            "fear_concerns": DataField(value=[]),
            "self_esteem": DataField(value=0),
            "optimism_level": DataField(value=0),
            "resilience": DataField(value=0),
            "perfectionism": DataField(value=0),
            "impulsivity": DataField(value=0),
            "introversion_extroversion": DataField(value=0),
            "emotional_intelligence": DataField(value=0),
            "empathy_level": DataField(value=0),
            "trust_issues": DataField(value=0),
            "abandonment_fears": DataField(value=0),
            "attachment_style": DataField(),
            "jealousy_tendency": DataField(value=0),
            "control_needs": DataField(value=0)
        }

        self.love_relationships_template = {
            "relationship_history": DataField(value=[]),
            "current_relationship": DataField(),
            "ideal_partner": DataField(value={}),
            "love_language": DataField(),
            "commitment_level": DataField(value=0),
            "romantic_experience": DataField(),
            "dating_patterns": DataField(value=[]),
            "relationship_goals": DataField(value=[]),
            "intimacy_comfort": DataField(value=0),
            "communication_in_love": DataField(),
            "conflict_in_relationships": DataField(),
            "past_heartbreaks": DataField(value=[]),
            "forgiveness_ability": DataField(value=0),
            "jealousy_in_love": DataField(value=0),
            "independence_vs_togetherness": DataField(value=0),
            "family_approval_importance": DataField(value=0),
            "long_distance_tolerance": DataField(value=0),
            "marriage_views": DataField(),
            "children_desire": DataField(),
            "sexual_compatibility_importance": DataField(value=0),
            "financial_compatibility": DataField(value=0),
            "age_gap_tolerance": DataField(value=0),
            "cultural_differences_tolerance": DataField(value=0),
            "friendship_quality": DataField(value=0),
            "social_circle_size": DataField(value=0)
        }

    def create_session(self, user_id: str = None, session_id: str = None) -> str:
        """新しいセッションを作成"""
        if not session_id:
            session_id = str(uuid.uuid4())

        if not user_id:
            user_id = f"user_{uuid.uuid4().hex[:8]}"

        session = UserSession(
            user_id=user_id,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            basic_info=deepcopy(self.basic_info_template),
            psychology_emotion=deepcopy(self.psychology_emotion_template),
            love_relationships=deepcopy(self.love_relationships_template),
            work_career={},  # 簡略化
            spiritual_values={},  # 簡略化
            analysis_results={
                "resort_ti_scores": {},
                "detected_needs": {},
                "emotional_analysis": {},
                "fortune_suggestion": {},
                "data_completeness": {"total": 0.0}
            },
            chat_history=[]
        )

        self.sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[UserSession]:
        """セッションを取得"""
        return self.sessions.get(session_id)

    def update_data_field(self, session_id: str, category: str, field_name: str,
                         value: Any, confidence: float, source: str) -> bool:
        """データフィールドを更新"""
        session = self.get_session(session_id)
        if not session:
            return False

        category_data = getattr(session, category, None)
        if not category_data or field_name not in category_data:
            return False

        current_field = category_data[field_name]

        # 信頼度が高い場合のみ更新
        if confidence > current_field.confidence:
            category_data[field_name] = DataField(
                value=value,
                confidence=confidence,
                source=source,
                timestamp=datetime.now().isoformat()
            )
            return True
        return False

    def extract_data_from_message(self, session_id: str, message: str,
                                confidence: float = 0.7) -> Dict[str, Dict[str, Any]]:
        """メッセージから情報を抽出してデータを更新"""
        extracted = {}

        # 基本的な情報抽出パターン
        patterns = {
            "relationship_status": {
                "彼氏": ("彼氏がいる", "inferred"),
                "彼女": ("彼女がいる", "inferred"),
                "恋人": ("恋人がいる", "inferred"),
                "独身": ("独身", "direct"),
                "一人": ("独身", "inferred")
            },
            "emotional_state": {
                "不安": ("不安", "direct"),
                "心配": ("心配", "direct"),
                "寂しい": ("寂しい", "direct"),
                "つらい": ("つらい", "direct"),
                "嬉しい": ("嬉しい", "direct")
            },
            "communication_style": {
                "連絡": ("連絡重視", "inferred"),
                "メッセージ": ("メッセージ重視", "inferred")
            }
        }

        for field, pattern_dict in patterns.items():
            for keyword, (value, source) in pattern_dict.items():
                if keyword in message:
                    # 適切なカテゴリを判定
                    category = self._determine_category(field)
                    if category:
                        success = self.update_data_field(
                            session_id, category, field, value, confidence, source
                        )
                        if success:
                            extracted.setdefault(category, {})[field] = value

        return extracted

    def _determine_category(self, field_name: str) -> Optional[str]:
        """フィールド名からカテゴリを判定"""
        field_to_category = {
            "relationship_status": "basic_info",
            "emotional_state": "psychology_emotion",
            "anxiety_level": "psychology_emotion",
            "communication_style": "psychology_emotion",
            "current_relationship": "love_relationships",
            "love_language": "love_relationships"
        }
        return field_to_category.get(field_name)

    def add_chat_turn(self, session_id: str, user_message: str, bot_response: str,
                     analysis_data: Dict[str, Any]) -> bool:
        """チャット履歴にターンを追加"""
        session = self.get_session(session_id)
        if not session:
            return False

        turn = {
            "turn": len(session.chat_history) + 1,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().isoformat(),
            "detected_needs": analysis_data.get("needs_analysis", {}),
            "selected_category": analysis_data.get("category", ""),
            "data_collected": self.extract_data_from_message(session_id, user_message),
            "resort_scores": analysis_data.get("resort_scores", {}),
            "emotional_analysis": analysis_data.get("emotion_analysis", {})
        }

        session.chat_history.append(turn)
        return True

    def get_asked_questions(self, session_id: str) -> List[str]:
        """過去に聞いた質問を取得"""
        session = self.get_session(session_id)
        if not session:
            return []

        questions = []
        question_patterns = [
            r"いつから.+？",
            r"どんな.+？",
            r"何.+？",
            r"どのくらい.+？",
            r"最後に.+？",
            r".+はどう？"
        ]

        for turn in session.chat_history:
            bot_response = turn.get("bot_response", "")
            for pattern in question_patterns:
                matches = re.findall(pattern, bot_response)
                questions.extend(matches)

        return questions

    def calculate_data_completeness(self, session_id: str) -> Dict[str, float]:
        """データ完成度を計算"""
        session = self.get_session(session_id)
        if not session:
            return {}

        completeness = {}

        # 基本情報の完成度
        basic_filled = sum(1 for field in session.basic_info.values()
                          if field.value is not None and field.confidence > 0)
        completeness["basic_info"] = basic_filled / len(session.basic_info)

        # 心理・感情データの完成度
        psych_filled = sum(1 for field in session.psychology_emotion.values()
                          if field.value is not None and field.confidence > 0)
        completeness["psychology_emotion"] = psych_filled / len(session.psychology_emotion)

        # 恋愛・人間関係の完成度
        love_filled = sum(1 for field in session.love_relationships.values()
                         if field.value is not None and field.confidence > 0)
        completeness["love_relationships"] = love_filled / len(session.love_relationships)

        # 総合完成度
        completeness["total"] = sum(completeness.values()) / len(completeness)

        return completeness

    def get_next_priority_questions(self, session_id: str, count: int = 3) -> List[str]:
        """次に聞くべき優先度の高い質問を取得"""
        session = self.get_session(session_id)
        if not session:
            return []

        # データ完成度を確認
        completeness = self.calculate_data_completeness(session_id)
        asked_questions = self.get_asked_questions(session_id)

        priority_questions = []

        # 基本情報の重要な質問
        if completeness["basic_info"] < 0.3:
            if not any("いつから" in q for q in asked_questions):
                priority_questions.append("いつから連絡ないの？")
            if not any("どのくらい" in q for q in asked_questions):
                priority_questions.append("どのくらいの期間お付き合いしてるの？")
            if not any("普段" in q for q in asked_questions):
                priority_questions.append("普段はどんな感じで連絡取り合ってた？")

        # 感情・心理の質問
        if completeness["psychology_emotion"] < 0.2:
            if not any("どんな気持ち" in q for q in asked_questions):
                priority_questions.append("今どんな気持ちが一番強いかな？")
            if not any("何が心配" in q for q in asked_questions):
                priority_questions.append("何が一番心配？")

        return priority_questions[:count]

# グローバルセッションマネージャー
session_manager = SessionManager()