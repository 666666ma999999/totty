# データ構造定義 171項目 v1.0

## 1. 基本情報（15項目）

### 001_user_id
```yaml
status: ❌
value: null
field: "user_id"
type: "string"
privacy_level: "low"
format: "UUID"
collection_phase: 0
priority: "critical"
auto_generated: true
```

### 002_session_id
```yaml
status: ❌
value: null
field: "session_id"
type: "string"
privacy_level: "low"
format: "UUID"
collection_phase: 0
priority: "critical"
auto_generated: true
```

### 003_timestamp
```yaml
status: ❌
value: null
field: "timestamp"
type: "datetime"
privacy_level: "low"
format: "ISO 8601"
collection_phase: 0
priority: "critical"
auto_generated: true
```

### 004_age_group
```yaml
status: ❌
value: null
field: "age_group"
type: "enum"
privacy_level: "low"
options: ["10代", "20代前半", "20代後半", "30代前半", "30代後半", "40代以上"]
collection_phase: 1
priority: "high"
collection_method: "implicit_extraction"
```

### 005_gender
```yaml
status: ❌
value: null
field: "gender"
type: "enum"
privacy_level: "medium"
options: ["女性", "男性", "その他", "回答しない"]
collection_phase: 1
priority: "medium"
collection_method: "pronoun_analysis"
```

### 006_occupation_type
```yaml
status: ❌
value: null
field: "occupation_type"
type: "enum"
privacy_level: "low"
options: ["学生", "会社員", "パート・アルバイト", "自営業", "専業主婦", "その他"]
collection_phase: 2
priority: "medium"
collection_method: "contextual_inference"
```

### 007_location_type
```yaml
status: ❌
value: null
field: "location_type"
type: "enum"
privacy_level: "low"
options: ["都市部", "郊外", "地方"]
collection_phase: 3
priority: "low"
collection_method: "lifestyle_inference"
```

### 008_communication_style
```yaml
status: ❌
value: null
field: "communication_style"
type: "enum"
privacy_level: "low"
options: ["直接的", "間接的", "感情的", "論理的"]
collection_phase: 1
priority: "high"
collection_method: "message_analysis"
```

### 009_preferred_tone
```yaml
status: ❌
value: null
field: "preferred_tone"
type: "enum"
privacy_level: "low"
options: ["カジュアル", "丁寧", "フレンドリー", "プロフェッショナル"]
collection_phase: 1
priority: "high"
collection_method: "tone_matching"
```

### 010_emoji_usage
```yaml
status: ❌
value: null
field: "emoji_usage"
type: "integer"
privacy_level: "low"
range: [0, 10]
collection_phase: 1
priority: "medium"
collection_method: "usage_frequency"
```

### 011_response_speed_preference
```yaml
status: ❌
value: null
field: "response_speed_preference"
type: "enum"
privacy_level: "low"
options: ["即レス希望", "ゆっくり", "どちらでも"]
collection_phase: 1
priority: "medium"
collection_method: "pattern_analysis"
```

### 012_session_time_preference
```yaml
status: ❌
value: null
field: "session_time_preference"
type: "enum"
privacy_level: "low"
options: ["朝", "昼", "夕方", "夜", "深夜"]
collection_phase: 2
priority: "low"
collection_method: "access_pattern"
```

### 013_device_type
```yaml
status: ❌
value: null
field: "device_type"
type: "enum"
privacy_level: "low"
options: ["スマートフォン", "タブレット", "PC"]
collection_phase: 0
priority: "low"
auto_detected: true
```

### 014_language_complexity
```yaml
status: ❌
value: null
field: "language_complexity"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 1
priority: "medium"
collection_method: "vocabulary_analysis"
```

### 015_privacy_sensitivity
```yaml
status: ❌
value: null
field: "privacy_sensitivity"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 1
priority: "high"
collection_method: "boundary_detection"
```

## 2. 感情状態（20項目）

### 016_current_emotion
```yaml
status: ❌
value: null
field: "current_emotion"
type: "array"
privacy_level: "low"
max_items: 3
examples: ["悲しい", "不安", "怒り", "寂しい", "混乱"]
collection_phase: 1
priority: "critical"
collection_method: "emotion_detection"
```

### 017_emotion_intensity
```yaml
status: ❌
value: null
field: "emotion_intensity"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 1
priority: "high"
collection_method: "intensity_analysis"
```

### 018_emotion_duration
```yaml
status: ❌
value: null
field: "emotion_duration"
type: "enum"
privacy_level: "low"
options: ["数時間", "数日", "1週間", "1ヶ月以上"]
collection_phase: 2
priority: "medium"
collection_method: "temporal_inquiry"
```

### 019_emotion_triggers
```yaml
status: ❌
value: null
field: "emotion_triggers"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 2
priority: "high"
collection_method: "trigger_exploration"
```

### 020_emotional_patterns
```yaml
status: ❌
value: null
field: "emotional_patterns"
type: "object"
privacy_level: "medium"
properties:
  morning: "string"
  evening: "string"
  weekend: "string"
collection_phase: 3
priority: "medium"
collection_method: "pattern_mapping"
```

### 021_stress_level
```yaml
status: ❌
value: null
field: "stress_level"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 1
priority: "high"
collection_method: "stress_assessment"
```

### 022_anxiety_topics
```yaml
status: ❌
value: null
field: "anxiety_topics"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 2
priority: "high"
collection_method: "anxiety_exploration"
```

### 023_happiness_sources
```yaml
status: ❌
value: null
field: "happiness_sources"
type: "array"
privacy_level: "low"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "positive_exploration"
```

### 024_frustration_points
```yaml
status: ❌
value: null
field: "frustration_points"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 2
priority: "high"
collection_method: "frustration_mapping"
```

### 025_emotional_vocabulary
```yaml
status: ❌
value: null
field: "emotional_vocabulary"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 2
priority: "medium"
collection_method: "vocabulary_assessment"
```

### 026_emotion_regulation
```yaml
status: ❌
value: null
field: "emotion_regulation"
type: "enum"
privacy_level: "medium"
options: ["抑制型", "表出型", "バランス型"]
collection_phase: 2
priority: "medium"
collection_method: "regulation_analysis"
```

### 027_mood_stability
```yaml
status: ❌
value: null
field: "mood_stability"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "stability_tracking"
```

### 028_emotional_support_need
```yaml
status: ❌
value: null
field: "emotional_support_need"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 1
priority: "critical"
collection_method: "need_assessment"
```

### 029_vulnerability_level
```yaml
status: ❌
value: null
field: "vulnerability_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "vulnerability_gauge"
```

### 030_emotional_awareness
```yaml
status: ❌
value: null
field: "emotional_awareness"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 2
priority: "medium"
collection_method: "awareness_evaluation"
```

### 031_crying_frequency
```yaml
status: ❌
value: null
field: "crying_frequency"
type: "enum"
privacy_level: "high"
options: ["毎日", "週数回", "月数回", "ほとんどない"]
collection_phase: 3
priority: "low"
collection_method: "gentle_inquiry"
```

### 032_anger_expression
```yaml
status: ❌
value: null
field: "anger_expression"
type: "enum"
privacy_level: "medium"
options: ["内向型", "外向型", "受動攻撃型", "建設的"]
collection_phase: 3
priority: "medium"
collection_method: "expression_analysis"
```

### 033_joy_capacity
```yaml
status: ❌
value: null
field: "joy_capacity"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "capacity_assessment"
```

### 034_fear_areas
```yaml
status: ❌
value: null
field: "fear_areas"
type: "array"
privacy_level: "medium"
max_items: 3
collection_phase: 3
priority: "medium"
collection_method: "fear_exploration"
```

### 035_emotional_numbness
```yaml
status: ❌
value: null
field: "emotional_numbness"
type: "boolean"
privacy_level: "high"
collection_phase: 3
priority: "medium"
collection_method: "numbness_detection"
```

## 3. ニーズ分析（15項目）

### 036_primary_need
```yaml
status: ❌
value: null
field: "primary_need"
type: "enum"
privacy_level: "low"
options: ["傾聴", "アドバイス", "共感", "励まし", "気晴らし"]
collection_phase: 1
priority: "critical"
collection_method: "need_identification"
```

### 037_secondary_needs
```yaml
status: ❌
value: null
field: "secondary_needs"
type: "array"
privacy_level: "low"
max_items: 3
collection_phase: 2
priority: "high"
collection_method: "multi_need_analysis"
```

### 038_validation_seeking
```yaml
status: ❌
value: null
field: "validation_seeking"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 1
priority: "high"
collection_method: "validation_detection"
```

### 039_advice_receptivity
```yaml
status: ❌
value: null
field: "advice_receptivity"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 2
priority: "medium"
collection_method: "receptivity_gauge"
```

### 040_problem_solving_preference
```yaml
status: ❌
value: null
field: "problem_solving_preference"
type: "enum"
privacy_level: "low"
options: ["自己解決", "相談", "共同", "依存"]
collection_phase: 2
priority: "medium"
collection_method: "preference_analysis"
```

### 041_emotional_dumping_need
```yaml
status: ❌
value: null
field: "emotional_dumping_need"
type: "boolean"
privacy_level: "low"
collection_phase: 1
priority: "high"
collection_method: "dumping_detection"
```

### 042_reality_check_need
```yaml
status: ❌
value: null
field: "reality_check_need"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 2
priority: "medium"
collection_method: "reality_assessment"
```

### 043_comfort_style_preference
```yaml
status: ❌
value: null
field: "comfort_style_preference"
type: "enum"
privacy_level: "low"
options: ["論理的", "感情的", "実践的", "精神的"]
collection_phase: 2
priority: "high"
collection_method: "style_identification"
```

### 044_independence_level
```yaml
status: ❌
value: null
field: "independence_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "independence_measure"
```

### 045_reassurance_frequency
```yaml
status: ❌
value: null
field: "reassurance_frequency"
type: "enum"
privacy_level: "low"
options: ["常時", "頻繁", "時々", "稀"]
collection_phase: 2
priority: "high"
collection_method: "frequency_tracking"
```

### 046_perspective_need
```yaml
status: ❌
value: null
field: "perspective_need"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 2
priority: "medium"
collection_method: "perspective_assessment"
```

### 047_distraction_preference
```yaml
status: ❌
value: null
field: "distraction_preference"
type: "boolean"
privacy_level: "low"
collection_phase: 2
priority: "medium"
collection_method: "preference_detection"
```

### 048_depth_preference
```yaml
status: ❌
value: null
field: "depth_preference"
type: "enum"
privacy_level: "low"
options: ["表面的", "中程度", "深い", "非常に深い"]
collection_phase: 2
priority: "high"
collection_method: "depth_calibration"
```

### 049_action_orientation
```yaml
status: ❌
value: null
field: "action_orientation"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "orientation_measure"
```

### 050_closure_need
```yaml
status: ❌
value: null
field: "closure_need"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "closure_assessment"
```

## 4. 関係性情報（25項目）

### 051_relationship_status
```yaml
status: ❌
value: null
field: "relationship_status"
type: "enum"
privacy_level: "medium"
options: ["交際中", "破局", "複雑", "片思い", "既婚"]
collection_phase: 1
priority: "critical"
collection_method: "status_clarification"
```

### 052_relationship_duration
```yaml
status: ❌
value: null
field: "relationship_duration"
type: "enum"
privacy_level: "low"
options: ["1ヶ月未満", "1-3ヶ月", "3-6ヶ月", "6-12ヶ月", "1年以上"]
collection_phase: 2
priority: "high"
collection_method: "duration_inquiry"
```

### 053_partner_age_difference
```yaml
status: ❌
value: null
field: "partner_age_difference"
type: "integer"
privacy_level: "low"
range: [-20, 20]
collection_phase: 3
priority: "low"
collection_method: "age_exploration"
```

### 054_meeting_frequency
```yaml
status: ❌
value: null
field: "meeting_frequency"
type: "enum"
privacy_level: "low"
options: ["毎日", "週数回", "週1", "月数回", "遠距離"]
collection_phase: 2
priority: "medium"
collection_method: "frequency_check"
```

### 055_communication_frequency
```yaml
status: ❌
value: null
field: "communication_frequency"
type: "enum"
privacy_level: "low"
options: ["常時", "毎日", "週数回", "不定期"]
collection_phase: 2
priority: "high"
collection_method: "communication_assessment"
```

### 056_intimacy_level
```yaml
status: ❌
value: null
field: "intimacy_level"
type: "integer"
privacy_level: "high"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "intimacy_gauge"
```

### 057_trust_level
```yaml
status: ❌
value: null
field: "trust_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "trust_evaluation"
```

### 058_conflict_frequency
```yaml
status: ❌
value: null
field: "conflict_frequency"
type: "enum"
privacy_level: "medium"
options: ["毎日", "週数回", "月数回", "稀"]
collection_phase: 2
priority: "high"
collection_method: "conflict_tracking"
```

### 059_conflict_topics
```yaml
status: ❌
value: null
field: "conflict_topics"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 2
priority: "high"
collection_method: "topic_identification"
```

### 060_resolution_pattern
```yaml
status: ❌
value: null
field: "resolution_pattern"
type: "enum"
privacy_level: "medium"
options: ["建設的", "回避", "爆発", "冷戦"]
collection_phase: 3
priority: "medium"
collection_method: "pattern_analysis"
```

### 061_attachment_style
```yaml
status: ❌
value: null
field: "attachment_style"
type: "enum"
privacy_level: "medium"
options: ["安定型", "不安型", "回避型", "混乱型"]
collection_phase: 3
priority: "medium"
collection_method: "attachment_assessment"
```

### 062_jealousy_level
```yaml
status: ❌
value: null
field: "jealousy_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "jealousy_measure"
```

### 063_dependency_level
```yaml
status: ❌
value: null
field: "dependency_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "dependency_evaluation"
```

### 064_power_balance
```yaml
status: ❌
value: null
field: "power_balance"
type: "enum"
privacy_level: "medium"
options: ["対等", "自分優位", "相手優位", "不安定"]
collection_phase: 3
priority: "medium"
collection_method: "balance_assessment"
```

### 065_future_vision_alignment
```yaml
status: ❌
value: null
field: "future_vision_alignment"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "alignment_check"
```

### 066_values_compatibility
```yaml
status: ❌
value: null
field: "values_compatibility"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "values_comparison"
```

### 067_physical_affection_level
```yaml
status: ❌
value: null
field: "physical_affection_level"
type: "integer"
privacy_level: "high"
range: [1, 10]
collection_phase: 3
priority: "low"
collection_method: "gentle_exploration"
```

### 068_emotional_support_balance
```yaml
status: ❌
value: null
field: "emotional_support_balance"
type: "enum"
privacy_level: "medium"
options: ["相互的", "自分が多い", "相手が多い", "なし"]
collection_phase: 2
priority: "high"
collection_method: "support_analysis"
```

### 069_shared_activities
```yaml
status: ❌
value: null
field: "shared_activities"
type: "array"
privacy_level: "low"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "activity_mapping"
```

### 070_relationship_satisfaction
```yaml
status: ❌
value: null
field: "relationship_satisfaction"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "satisfaction_measure"
```

### 071_breakup_consideration
```yaml
status: ❌
value: null
field: "breakup_consideration"
type: "boolean"
privacy_level: "high"
collection_phase: 3
priority: "high"
collection_method: "consideration_detection"
```

### 072_commitment_level
```yaml
status: ❌
value: null
field: "commitment_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "commitment_gauge"
```

### 073_relationship_goals
```yaml
status: ❌
value: null
field: "relationship_goals"
type: "array"
privacy_level: "medium"
max_items: 3
collection_phase: 3
priority: "medium"
collection_method: "goal_exploration"
```

### 074_past_relationship_count
```yaml
status: ❌
value: null
field: "past_relationship_count"
type: "enum"
privacy_level: "medium"
options: ["0", "1-2", "3-5", "6以上"]
collection_phase: 3
priority: "low"
collection_method: "history_inquiry"
```

### 075_longest_relationship
```yaml
status: ❌
value: null
field: "longest_relationship"
type: "enum"
privacy_level: "medium"
options: ["なし", "1年未満", "1-3年", "3年以上"]
collection_phase: 3
priority: "low"
collection_method: "duration_check"
```

## 5. パートナー情報（20項目）

### 076_partner_personality
```yaml
status: ❌
value: null
field: "partner_personality"
type: "array"
privacy_level: "medium"
max_items: 5
examples: ["優しい", "真面目", "マイペース", "感情的"]
collection_phase: 2
priority: "high"
collection_method: "personality_description"
```

### 077_partner_occupation
```yaml
status: ❌
value: null
field: "partner_occupation"
type: "enum"
privacy_level: "medium"
options: ["学生", "会社員", "自営業", "その他"]
collection_phase: 3
priority: "low"
collection_method: "occupation_inquiry"
```

### 078_partner_communication_style
```yaml
status: ❌
value: null
field: "partner_communication_style"
type: "enum"
privacy_level: "medium"
options: ["積極的", "受動的", "回避的", "攻撃的"]
collection_phase: 2
priority: "high"
collection_method: "style_observation"
```

### 079_partner_love_language
```yaml
status: ❌
value: null
field: "partner_love_language"
type: "enum"
privacy_level: "medium"
options: ["言葉", "行動", "贈り物", "時間", "スキンシップ"]
collection_phase: 3
priority: "medium"
collection_method: "language_identification"
```

### 080_partner_strengths
```yaml
status: ❌
value: null
field: "partner_strengths"
type: "array"
privacy_level: "low"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "strength_exploration"
```

### 081_partner_weaknesses
```yaml
status: ❌
value: null
field: "partner_weaknesses"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "weakness_identification"
```

### 082_partner_stress_response
```yaml
status: ❌
value: null
field: "partner_stress_response"
type: "enum"
privacy_level: "medium"
options: ["攻撃的", "引きこもり", "相談", "気晴らし"]
collection_phase: 3
priority: "medium"
collection_method: "response_observation"
```

### 083_partner_family_relationship
```yaml
status: ❌
value: null
field: "partner_family_relationship"
type: "enum"
privacy_level: "high"
options: ["良好", "普通", "複雑", "疎遠"]
collection_phase: 3
priority: "low"
collection_method: "family_exploration"
```

### 084_partner_friend_circle
```yaml
status: ❌
value: null
field: "partner_friend_circle"
type: "enum"
privacy_level: "medium"
options: ["広い", "普通", "狭い", "なし"]
collection_phase: 3
priority: "low"
collection_method: "social_assessment"
```

### 085_partner_hobbies
```yaml
status: ❌
value: null
field: "partner_hobbies"
type: "array"
privacy_level: "low"
max_items: 5
collection_phase: 3
priority: "low"
collection_method: "hobby_discussion"
```

### 086_partner_values
```yaml
status: ❌
value: null
field: "partner_values"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "high"
collection_method: "value_exploration"
```

### 087_partner_life_goals
```yaml
status: ❌
value: null
field: "partner_life_goals"
type: "array"
privacy_level: "medium"
max_items: 3
collection_phase: 3
priority: "medium"
collection_method: "goal_discussion"
```

### 088_partner_financial_status
```yaml
status: ❌
value: null
field: "partner_financial_status"
type: "enum"
privacy_level: "high"
options: ["安定", "普通", "不安定", "不明"]
collection_phase: 3
priority: "low"
collection_method: "indirect_assessment"
```

### 089_partner_health_status
```yaml
status: ❌
value: null
field: "partner_health_status"
type: "enum"
privacy_level: "high"
options: ["良好", "普通", "課題あり"]
collection_phase: 3
priority: "low"
collection_method: "health_mention"
```

### 090_partner_past_relationships
```yaml
status: ❌
value: null
field: "partner_past_relationships"
type: "enum"
privacy_level: "high"
options: ["少ない", "普通", "多い", "不明"]
collection_phase: 3
priority: "low"
collection_method: "history_mention"
```

### 091_partner_marriage_intention
```yaml
status: ❌
value: null
field: "partner_marriage_intention"
type: "enum"
privacy_level: "high"
options: ["積極的", "考慮中", "消極的", "なし", "不明"]
collection_phase: 3
priority: "high"
collection_method: "intention_exploration"
```

### 092_partner_children_preference
```yaml
status: ❌
value: null
field: "partner_children_preference"
type: "enum"
privacy_level: "high"
options: ["希望", "考慮中", "希望しない", "不明"]
collection_phase: 3
priority: "medium"
collection_method: "preference_discussion"
```

### 093_partner_conflict_style
```yaml
status: ❌
value: null
field: "partner_conflict_style"
type: "enum"
privacy_level: "medium"
options: ["対話型", "回避型", "支配型", "妥協型"]
collection_phase: 2
priority: "high"
collection_method: "conflict_observation"
```

### 094_partner_emotional_availability
```yaml
status: ❌
value: null
field: "partner_emotional_availability"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "availability_assessment"
```

### 095_partner_reliability
```yaml
status: ❌
value: null
field: "partner_reliability"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "reliability_evaluation"
```

## 6. コミュニケーション詳細（18項目）

### 096_primary_communication_channel
```yaml
status: ❌
value: null
field: "primary_communication_channel"
type: "enum"
privacy_level: "low"
options: ["LINE", "電話", "対面", "その他SNS"]
collection_phase: 2
priority: "medium"
collection_method: "channel_identification"
```

### 097_message_response_time
```yaml
status: ❌
value: null
field: "message_response_time"
type: "enum"
privacy_level: "low"
options: ["即レス", "数分", "数時間", "1日以上"]
collection_phase: 2
priority: "medium"
collection_method: "response_tracking"
```

### 098_conversation_topics
```yaml
status: ❌
value: null
field: "conversation_topics"
type: "array"
privacy_level: "low"
max_items: 5
collection_phase: 2
priority: "medium"
collection_method: "topic_analysis"
```

### 099_communication_satisfaction
```yaml
status: ❌
value: null
field: "communication_satisfaction"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "satisfaction_gauge"
```

### 100_misunderstanding_frequency
```yaml
status: ❌
value: null
field: "misunderstanding_frequency"
type: "enum"
privacy_level: "medium"
options: ["頻繁", "時々", "稀", "なし"]
collection_phase: 2
priority: "high"
collection_method: "frequency_assessment"
```

### 101_expression_difficulty
```yaml
status: ❌
value: null
field: "expression_difficulty"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "difficulty_evaluation"
```

### 102_listening_quality
```yaml
status: ❌
value: null
field: "listening_quality"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "quality_assessment"
```

### 103_nonverbal_awareness
```yaml
status: ❌
value: null
field: "nonverbal_awareness"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "awareness_check"
```

### 104_conflict_communication
```yaml
status: ❌
value: null
field: "conflict_communication"
type: "enum"
privacy_level: "medium"
options: ["建設的", "感情的", "回避的", "攻撃的"]
collection_phase: 2
priority: "high"
collection_method: "conflict_analysis"
```

### 105_apology_pattern
```yaml
status: ❌
value: null
field: "apology_pattern"
type: "enum"
privacy_level: "medium"
options: ["素直", "防御的", "回避", "過剰"]
collection_phase: 3
priority: "medium"
collection_method: "pattern_observation"
```

### 106_compliment_frequency
```yaml
status: ❌
value: null
field: "compliment_frequency"
type: "enum"
privacy_level: "low"
options: ["頻繁", "適度", "少ない", "なし"]
collection_phase: 3
priority: "medium"
collection_method: "frequency_tracking"
```

### 107_criticism_style
```yaml
status: ❌
value: null
field: "criticism_style"
type: "enum"
privacy_level: "medium"
options: ["建設的", "直接的", "間接的", "攻撃的"]
collection_phase: 3
priority: "medium"
collection_method: "style_analysis"
```

### 108_boundary_setting
```yaml
status: ❌
value: null
field: "boundary_setting"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "boundary_assessment"
```

### 109_emotional_expression
```yaml
status: ❌
value: null
field: "emotional_expression"
type: "enum"
privacy_level: "medium"
options: ["オープン", "選択的", "抑制的", "爆発的"]
collection_phase: 2
priority: "high"
collection_method: "expression_evaluation"
```

### 110_digital_communication_preference
```yaml
status: ❌
value: null
field: "digital_communication_preference"
type: "enum"
privacy_level: "low"
options: ["テキスト", "音声", "ビデオ", "スタンプ"]
collection_phase: 2
priority: "medium"
collection_method: "preference_detection"
```

### 111_communication_timing
```yaml
status: ❌
value: null
field: "communication_timing"
type: "enum"
privacy_level: "low"
options: ["朝型", "昼型", "夜型", "不規則"]
collection_phase: 2
priority: "low"
collection_method: "timing_analysis"
```

### 112_serious_talk_ability
```yaml
status: ❌
value: null
field: "serious_talk_ability"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "ability_assessment"
```

### 113_humor_compatibility
```yaml
status: ❌
value: null
field: "humor_compatibility"
type: "integer"
privacy_level: "low"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "compatibility_check"
```

## 7. 問題・課題（15項目）

### 114_main_concerns
```yaml
status: ❌
value: null
field: "main_concerns"
type: "array"
privacy_level: "medium"
max_items: 3
collection_phase: 1
priority: "critical"
collection_method: "concern_identification"
```

### 115_problem_severity
```yaml
status: ❌
value: null
field: "problem_severity"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 1
priority: "high"
collection_method: "severity_assessment"
```

### 116_problem_duration
```yaml
status: ❌
value: null
field: "problem_duration"
type: "enum"
privacy_level: "medium"
options: ["最近", "数週間", "数ヶ月", "長期間"]
collection_phase: 2
priority: "medium"
collection_method: "duration_check"
```

### 117_trigger_events
```yaml
status: ❌
value: null
field: "trigger_events"
type: "array"
privacy_level: "medium"
max_items: 3
collection_phase: 2
priority: "high"
collection_method: "trigger_exploration"
```

### 118_attempted_solutions
```yaml
status: ❌
value: null
field: "attempted_solutions"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "solution_review"
```

### 119_solution_effectiveness
```yaml
status: ❌
value: null
field: "solution_effectiveness"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "effectiveness_evaluation"
```

### 120_recurring_patterns
```yaml
status: ❌
value: null
field: "recurring_patterns"
type: "array"
privacy_level: "medium"
max_items: 3
collection_phase: 3
priority: "high"
collection_method: "pattern_identification"
```

### 121_root_causes
```yaml
status: ❌
value: null
field: "root_causes"
type: "array"
privacy_level: "high"
max_items: 3
collection_phase: 3
priority: "high"
collection_method: "cause_analysis"
```

### 122_external_factors
```yaml
status: ❌
value: null
field: "external_factors"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "factor_identification"
```

### 123_internal_factors
```yaml
status: ❌
value: null
field: "internal_factors"
type: "array"
privacy_level: "high"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "self_reflection"
```

### 124_change_readiness
```yaml
status: ❌
value: null
field: "change_readiness"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "readiness_assessment"
```

### 125_support_system
```yaml
status: ❌
value: null
field: "support_system"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "support_mapping"
```

### 126_professional_help_consideration
```yaml
status: ❌
value: null
field: "professional_help_consideration"
type: "boolean"
privacy_level: "high"
collection_phase: 3
priority: "medium"
collection_method: "help_exploration"
```

### 127_problem_ownership
```yaml
status: ❌
value: null
field: "problem_ownership"
type: "enum"
privacy_level: "medium"
options: ["自分", "相手", "両方", "外部"]
collection_phase: 3
priority: "medium"
collection_method: "ownership_clarification"
```

### 128_resolution_timeline
```yaml
status: ❌
value: null
field: "resolution_timeline"
type: "enum"
privacy_level: "medium"
options: ["緊急", "短期", "中期", "長期"]
collection_phase: 3
priority: "high"
collection_method: "timeline_setting"
```

## 8. 環境要因（18項目）

### 129_social_support
```yaml
status: ❌
value: null
field: "social_support"
type: "object"
privacy_level: "medium"
properties:
  friends_support: [1-10]
  family_support: [1-10]
collection_phase: 2
priority: "medium"
collection_method: "support_assessment"
```

### 130_external_stressors
```yaml
status: ❌
value: null
field: "external_stressors"
type: "array"
privacy_level: "medium"
max_items: 5
examples: ["仕事", "家族", "健康", "金銭", "人間関係"]
collection_phase: 2
priority: "medium"
collection_method: "stressor_exploration"
```

### 131_life_changes
```yaml
status: ❌
value: null
field: "life_changes"
type: "array"
privacy_level: "medium"
max_items: 3
time_frame: "過去半年"
collection_phase: 3
priority: "medium"
collection_method: "change_exploration"
```

### 132_work_life_balance
```yaml
status: ❌
value: null
field: "work_life_balance"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "medium"
collection_method: "balance_assessment"
```

### 133_financial_status
```yaml
status: ❌
value: null
field: "financial_status"
type: "enum"
privacy_level: "high"
options: ["余裕", "普通", "厳しい", "非公開"]
collection_phase: 3
priority: "low"
collection_method: "avoid_direct"
```

### 134_health_status
```yaml
status: ❌
value: null
field: "health_status"
type: "enum"
privacy_level: "high"
options: ["良好", "普通", "不調", "治療中"]
collection_phase: 3
priority: "low"
sensitive: true
collection_method: "health_inquiry"
```

### 135_living_situation
```yaml
status: ❌
value: null
field: "living_situation"
type: "enum"
privacy_level: "medium"
options: ["一人暮らし", "実家", "同棲", "その他"]
collection_phase: 3
priority: "medium"
collection_method: "living_check"
```

### 136_distance_from_partner
```yaml
status: ❌
value: null
field: "distance_from_partner"
type: "enum"
privacy_level: "low"
options: ["同居", "近距離", "中距離", "遠距離"]
collection_phase: 2
priority: "medium"
collection_method: "distance_assessment"
```

### 137_cultural_differences
```yaml
status: ❌
value: null
field: "cultural_differences"
type: "boolean"
privacy_level: "medium"
collection_phase: 3
priority: "low"
collection_method: "difference_detection"
```

### 138_family_approval
```yaml
status: ❌
value: null
field: "family_approval"
type: "enum"
privacy_level: "high"
options: ["賛成", "中立", "反対", "知らない"]
collection_phase: 3
priority: "medium"
collection_method: "approval_check"
```

### 139_friend_opinions
```yaml
status: ❌
value: null
field: "friend_opinions"
type: "enum"
privacy_level: "medium"
options: ["肯定的", "中立", "否定的", "知らない"]
collection_phase: 3
priority: "low"
collection_method: "opinion_gathering"
```

### 140_work_impact
```yaml
status: ❌
value: null
field: "work_impact"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "impact_assessment"
```

### 141_sleep_quality
```yaml
status: ❌
value: null
field: "sleep_quality"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "quality_check"
```

### 142_appetite_changes
```yaml
status: ❌
value: null
field: "appetite_changes"
type: "boolean"
privacy_level: "high"
collection_phase: 3
priority: "low"
collection_method: "change_detection"
```

### 143_social_isolation
```yaml
status: ❌
value: null
field: "social_isolation"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "isolation_assessment"
```

### 144_daily_routine_disruption
```yaml
status: ❌
value: null
field: "daily_routine_disruption"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "disruption_check"
```

### 145_seasonal_factors
```yaml
status: ❌
value: null
field: "seasonal_factors"
type: "boolean"
privacy_level: "low"
collection_phase: 3
priority: "low"
collection_method: "seasonal_check"
```

### 146_major_life_decisions
```yaml
status: ❌
value: null
field: "major_life_decisions"
type: "array"
privacy_level: "high"
max_items: 3
collection_phase: 3
priority: "medium"
collection_method: "decision_exploration"
```

## 9. 個人の特性（10項目）

### 147_personality_type
```yaml
status: ❌
value: null
field: "personality_type"
type: "enum"
privacy_level: "medium"
options: ["外向的", "内向的", "両向的"]
collection_phase: 3
priority: "medium"
collection_method: "personality_assessment"
```

### 148_self_esteem
```yaml
status: ❌
value: null
field: "self_esteem"
type: "integer"
privacy_level: "high"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "esteem_evaluation"
```

### 149_resilience_level
```yaml
status: ❌
value: null
field: "resilience_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "resilience_assessment"
```

### 150_coping_strategies
```yaml
status: ❌
value: null
field: "coping_strategies"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "high"
collection_method: "strategy_identification"
```

### 151_love_language
```yaml
status: ❌
value: null
field: "love_language"
type: "enum"
privacy_level: "low"
options: ["言葉", "行動", "贈り物", "時間", "スキンシップ"]
collection_phase: 3
priority: "medium"
collection_method: "language_assessment"
```

### 152_conflict_avoidance
```yaml
status: ❌
value: null
field: "conflict_avoidance"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "avoidance_measure"
```

### 153_emotional_intelligence
```yaml
status: ❌
value: null
field: "emotional_intelligence"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "eq_assessment"
```

### 154_decision_making_style
```yaml
status: ❌
value: null
field: "decision_making_style"
type: "enum"
privacy_level: "medium"
options: ["直感的", "分析的", "依存的", "回避的"]
collection_phase: 3
priority: "medium"
collection_method: "style_identification"
```

### 155_risk_tolerance
```yaml
status: ❌
value: null
field: "risk_tolerance"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "low"
collection_method: "tolerance_assessment"
```

### 156_optimism_level
```yaml
status: ❌
value: null
field: "optimism_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "optimism_gauge"
```

## 10. 将来展望（15項目）

### 157_ideal_relationship
```yaml
status: ❌
value: null
field: "ideal_relationship"
type: "object"
privacy_level: "medium"
properties:
  communication: "string"
  intimacy: "string"
  lifestyle: "string"
collection_phase: 3
priority: "high"
collection_method: "ideal_exploration"
```

### 158_marriage_intention
```yaml
status: ❌
value: null
field: "marriage_intention"
type: "enum"
privacy_level: "high"
options: ["すぐにでも", "数年内", "いつか", "考えていない"]
collection_phase: 3
priority: "high"
collection_method: "intention_check"
```

### 159_children_preference
```yaml
status: ❌
value: null
field: "children_preference"
type: "enum"
privacy_level: "high"
options: ["欲しい", "考慮中", "欲しくない", "未定"]
collection_phase: 3
priority: "medium"
collection_method: "preference_exploration"
```

### 160_career_priority
```yaml
status: ❌
value: null
field: "career_priority"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "priority_assessment"
```

### 161_lifestyle_goals
```yaml
status: ❌
value: null
field: "lifestyle_goals"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "goal_discussion"
```

### 162_financial_goals
```yaml
status: ❌
value: null
field: "financial_goals"
type: "array"
privacy_level: "high"
max_items: 3
collection_phase: 3
priority: "low"
collection_method: "goal_exploration"
```

### 163_personal_growth_areas
```yaml
status: ❌
value: null
field: "personal_growth_areas"
type: "array"
privacy_level: "medium"
max_items: 5
collection_phase: 3
priority: "medium"
collection_method: "growth_identification"
```

### 164_relationship_timeline
```yaml
status: ❌
value: null
field: "relationship_timeline"
type: "object"
privacy_level: "medium"
properties:
  next_step: "string"
  timeframe: "string"
collection_phase: 3
priority: "high"
collection_method: "timeline_discussion"
```

### 165_compromise_willingness
```yaml
status: ❌
value: null
field: "compromise_willingness"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "willingness_assessment"
```

### 166_sacrifice_readiness
```yaml
status: ❌
value: null
field: "sacrifice_readiness"
type: "integer"
privacy_level: "high"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "readiness_gauge"
```

### 167_growth_mindset
```yaml
status: ❌
value: null
field: "growth_mindset"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "medium"
collection_method: "mindset_evaluation"
```

### 168_change_capacity
```yaml
status: ❌
value: null
field: "change_capacity"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 3
priority: "high"
collection_method: "capacity_assessment"
```

### 169_hope_level
```yaml
status: ❌
value: null
field: "hope_level"
type: "integer"
privacy_level: "medium"
range: [1, 10]
collection_phase: 2
priority: "high"
collection_method: "hope_measurement"
```

### 170_recovery_expectation
```yaml
status: ❌
value: null
field: "recovery_expectation"
type: "enum"
privacy_level: "medium"
options: ["楽観的", "現実的", "悲観的", "不確実"]
collection_phase: 3
priority: "high"
collection_method: "expectation_assessment"
```

### 171_alternative_plans
```yaml
status: ❌
value: null
field: "alternative_plans"
type: "array"
privacy_level: "high"
max_items: 3
collection_phase: 3
priority: "medium"
collection_method: "plan_exploration"
```
