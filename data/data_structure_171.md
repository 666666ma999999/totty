# データ構造定義（171項目）

## データ構造概要
占いチャットシステムで収集・管理する171項目のデータ構造定義

## JSON基本構造
```json
{
  "user_id": "string",
  "session_id": "string", 
  "timestamp": "datetime",
  "basic_info": {},
  "psychology_emotion": {},
  "love_relationships": {},
  "work_career": {},
  "spiritual_values": {},
  "analysis_results": {},
  "chat_history": []
}
```

## 1. 基本情報（basic_info: 20項目）

```json
{
  "age": {"value": null, "confidence": 0.0, "source": ""},
  "gender": {"value": null, "confidence": 0.0, "source": ""},
  "occupation": {"value": null, "confidence": 0.0, "source": ""},
  "location": {"value": null, "confidence": 0.0, "source": ""},
  "family_structure": {"value": null, "confidence": 0.0, "source": ""},
  "relationship_status": {"value": null, "confidence": 0.0, "source": ""},
  "hobbies": {"value": [], "confidence": 0.0, "source": ""},
  "personality_traits": {"value": [], "confidence": 0.0, "source": ""},
  "values": {"value": [], "confidence": 0.0, "source": ""},
  "lifestyle": {"value": null, "confidence": 0.0, "source": ""},
  "income_level": {"value": null, "confidence": 0.0, "source": ""},
  "education": {"value": null, "confidence": 0.0, "source": ""},
  "health_status": {"value": null, "confidence": 0.0, "source": ""},
  "stress_level": {"value": 0, "confidence": 0.0, "source": ""},
  "sleep_hours": {"value": 0, "confidence": 0.0, "source": ""},
  "exercise_habits": {"value": null, "confidence": 0.0, "source": ""},
  "dietary_habits": {"value": null, "confidence": 0.0, "source": ""},
  "sociability": {"value": 0, "confidence": 0.0, "source": ""},
  "future_goals": {"value": [], "confidence": 0.0, "source": ""},
  "happiness_level": {"value": 0, "confidence": 0.0, "source": ""}
}
```

## 2. 心理・感情データ（psychology_emotion: 50項目）

```json
{
  "emotional_state": {"value": null, "confidence": 0.0, "source": ""},
  "anxiety_level": {"value": 0, "confidence": 0.0, "source": ""},
  "confidence_level": {"value": 0, "confidence": 0.0, "source": ""},
  "stress_factors": {"value": [], "confidence": 0.0, "source": ""},
  "coping_mechanisms": {"value": [], "confidence": 0.0, "source": ""},
  "emotional_triggers": {"value": [], "confidence": 0.0, "source": ""},
  "support_system": {"value": [], "confidence": 0.0, "source": ""},
  "communication_style": {"value": null, "confidence": 0.0, "source": ""},
  "conflict_resolution": {"value": null, "confidence": 0.0, "source": ""},
  "decision_making_style": {"value": null, "confidence": 0.0, "source": ""},
  "motivation_factors": {"value": [], "confidence": 0.0, "source": ""},
  "fear_concerns": {"value": [], "confidence": 0.0, "source": ""},
  "self_esteem": {"value": 0, "confidence": 0.0, "source": ""},
  "optimism_level": {"value": 0, "confidence": 0.0, "source": ""},
  "resilience": {"value": 0, "confidence": 0.0, "source": ""},
  "perfectionism": {"value": 0, "confidence": 0.0, "source": ""},
  "impulsivity": {"value": 0, "confidence": 0.0, "source": ""},
  "introversion_extroversion": {"value": 0, "confidence": 0.0, "source": ""},
  "emotional_intelligence": {"value": 0, "confidence": 0.0, "source": ""},
  "empathy_level": {"value": 0, "confidence": 0.0, "source": ""},
  "trust_issues": {"value": 0, "confidence": 0.0, "source": ""},
  "abandonment_fears": {"value": 0, "confidence": 0.0, "source": ""},
  "attachment_style": {"value": null, "confidence": 0.0, "source": ""},
  "jealousy_tendency": {"value": 0, "confidence": 0.0, "source": ""},
  "control_needs": {"value": 0, "confidence": 0.0, "source": ""}
}
```

## 3. 恋愛・人間関係（love_relationships: 50項目）

```json
{
  "relationship_history": {"value": [], "confidence": 0.0, "source": ""},
  "current_relationship": {"value": null, "confidence": 0.0, "source": ""},
  "ideal_partner": {"value": {}, "confidence": 0.0, "source": ""},
  "love_language": {"value": null, "confidence": 0.0, "source": ""},
  "commitment_level": {"value": 0, "confidence": 0.0, "source": ""},
  "romantic_experience": {"value": null, "confidence": 0.0, "source": ""},
  "dating_patterns": {"value": [], "confidence": 0.0, "source": ""},
  "relationship_goals": {"value": [], "confidence": 0.0, "source": ""},
  "intimacy_comfort": {"value": 0, "confidence": 0.0, "source": ""},
  "communication_in_love": {"value": null, "confidence": 0.0, "source": ""},
  "conflict_in_relationships": {"value": null, "confidence": 0.0, "source": ""},
  "past_heartbreaks": {"value": [], "confidence": 0.0, "source": ""},
  "forgiveness_ability": {"value": 0, "confidence": 0.0, "source": ""},
  "jealousy_in_love": {"value": 0, "confidence": 0.0, "source": ""},
  "independence_vs_togetherness": {"value": 0, "confidence": 0.0, "source": ""},
  "family_approval_importance": {"value": 0, "confidence": 0.0, "source": ""},
  "long_distance_tolerance": {"value": 0, "confidence": 0.0, "source": ""},
  "marriage_views": {"value": null, "confidence": 0.0, "source": ""},
  "children_desire": {"value": null, "confidence": 0.0, "source": ""},
  "sexual_compatibility_importance": {"value": 0, "confidence": 0.0, "source": ""},
  "financial_compatibility": {"value": 0, "confidence": 0.0, "source": ""},
  "age_gap_tolerance": {"value": 0, "confidence": 0.0, "source": ""},
  "cultural_differences_tolerance": {"value": 0, "confidence": 0.0, "source": ""},
  "friendship_quality": {"value": 0, "confidence": 0.0, "source": ""},
  "social_circle_size": {"value": 0, "confidence": 0.0, "source": ""}
}
```

## 4. 仕事・キャリア（work_career: 30項目）

```json
{
  "job_satisfaction": {"value": 0, "confidence": 0.0, "source": ""},
  "career_ambition": {"value": 0, "confidence": 0.0, "source": ""},
  "work_life_balance": {"value": 0, "confidence": 0.0, "source": ""},
  "workplace_relationships": {"value": 0, "confidence": 0.0, "source": ""},
  "leadership_style": {"value": null, "confidence": 0.0, "source": ""},
  "team_collaboration": {"value": 0, "confidence": 0.0, "source": ""},
  "work_stress_sources": {"value": [], "confidence": 0.0, "source": ""},
  "career_change_desire": {"value": 0, "confidence": 0.0, "source": ""},
  "skill_development_focus": {"value": [], "confidence": 0.0, "source": ""},
  "work_environment_preference": {"value": null, "confidence": 0.0, "source": ""},
  "salary_importance": {"value": 0, "confidence": 0.0, "source": ""},
  "job_security_importance": {"value": 0, "confidence": 0.0, "source": ""},
  "creative_expression_need": {"value": 0, "confidence": 0.0, "source": ""},
  "autonomy_preference": {"value": 0, "confidence": 0.0, "source": ""},
  "recognition_importance": {"value": 0, "confidence": 0.0, "source": ""},
  "mentorship_experience": {"value": null, "confidence": 0.0, "source": ""},
  "networking_ability": {"value": 0, "confidence": 0.0, "source": ""},
  "public_speaking_comfort": {"value": 0, "confidence": 0.0, "source": ""},
  "risk_taking_in_career": {"value": 0, "confidence": 0.0, "source": ""},
  "entrepreneurial_spirit": {"value": 0, "confidence": 0.0, "source": ""}
}
```

## 5. スピリチュアル・価値観（spiritual_values: 21項目）

```json
{
  "spiritual_beliefs": {"value": null, "confidence": 0.0, "source": ""},
  "fortune_telling_interest": {"value": 0, "confidence": 0.0, "source": ""},
  "intuition_trust": {"value": 0, "confidence": 0.0, "source": ""},
  "fate_vs_free_will": {"value": 0, "confidence": 0.0, "source": ""},
  "meditation_practice": {"value": 0, "confidence": 0.0, "source": ""},
  "energy_sensitivity": {"value": 0, "confidence": 0.0, "source": ""},
  "dream_importance": {"value": 0, "confidence": 0.0, "source": ""},
  "synchronicity_awareness": {"value": 0, "confidence": 0.0, "source": ""},
  "chakra_knowledge": {"value": 0, "confidence": 0.0, "source": ""},
  "crystal_healing_belief": {"value": 0, "confidence": 0.0, "source": ""},
  "astrology_interest": {"value": 0, "confidence": 0.0, "source": ""},
  "tarot_experience": {"value": 0, "confidence": 0.0, "source": ""},
  "psychic_abilities_belief": {"value": 0, "confidence": 0.0, "source": ""},
  "afterlife_beliefs": {"value": null, "confidence": 0.0, "source": ""},
  "karma_concept": {"value": 0, "confidence": 0.0, "source": ""},
  "soul_mate_belief": {"value": 0, "confidence": 0.0, "source": ""},
  "past_life_interest": {"value": 0, "confidence": 0.0, "source": ""},
  "guardian_angel_belief": {"value": 0, "confidence": 0.0, "source": ""},
  "manifestation_practice": {"value": 0, "confidence": 0.0, "source": ""},
  "gratitude_practice": {"value": 0, "confidence": 0.0, "source": ""},
  "mindfulness_level": {"value": 0, "confidence": 0.0, "source": ""}
}
```

## 6. 分析結果（analysis_results）

```json
{
  "resort_ti_scores": {
    "relationship": {"value": 0, "timestamp": null},
    "emotion": {"value": 0, "timestamp": null},
    "spirit": {"value": 0, "timestamp": null},
    "occupation": {"value": 0, "timestamp": null},
    "romance": {"value": 0, "timestamp": null},
    "time": {"value": 0, "timestamp": null},
    "intelligence": {"value": 0, "timestamp": null},
    "total": {"value": 0, "timestamp": null}
  },
  "detected_needs": {
    "complaining_listening": {"score": 0, "confidence": 0},
    "emotion_organizing": {"score": 0, "confidence": 0},
    "recognition_desire": {"score": 0, "confidence": 0},
    "encouragement": {"score": 0, "confidence": 0},
    "loneliness": {"score": 0, "confidence": 0}
  },
  "emotional_analysis": {
    "polarity": 0.0,
    "intensity": 0.0,
    "dominant_emotion": null
  },
  "fortune_suggestion": {
    "timing_score": 0,
    "recommended_menu": null,
    "confidence": 0
  },
  "data_completeness": {
    "basic_info": 0.0,
    "psychology_emotion": 0.0,
    "love_relationships": 0.0,
    "work_career": 0.0,
    "spiritual_values": 0.0,
    "total": 0.0
  }
}
```

## 7. チャット履歴（chat_history）

```json
[
  {
    "turn": 1,
    "user_message": "string",
    "bot_response": "string",
    "timestamp": "datetime",
    "detected_needs": {},
    "selected_category": null,
    "data_collected": {},
    "resort_scores": {},
    "emotional_analysis": {}
  }
]
```

## データ更新ルール

### 信頼度スコア
- **1.0**: 直接回答・明確な発言
- **0.7**: 強い推測・文脈から明確
- **0.5**: 中程度の推測
- **0.3**: 弱い推測・仮定

### データソース種別
- **direct**: 直接質問への回答
- **inferred**: 発言内容からの推測
- **assumed**: パターンからの仮定
- **updated**: 新情報による更新

### 更新条件
- 新しい情報の信頼度 > 既存情報の信頼度
- 矛盾する情報は確認プロセスを経る
- 時系列考慮（新しい情報を優先）