# 戦略決定ルール完全定義

## 感情強度ベース戦略

### 高強度感情（80+）
```yaml
high_intensity_strategy:
  conditions:
    emotion_intensity: "> 80"
  strategy:
    first_sentence: "deep_empathy"
    second_sentence: "emotion_validation"
    third_sentence: "accompaniment"
    priority_score: 9.0
    reasoning: "高強度感情対応"
  special_instructions:
    - "即座の安心感提供"
    - "解決提案は避ける"
    - "感情の受容に専念"
  avoid_patterns:
    - "前向き過ぎる表現"
    - "急かす表現"
```

### 中強度感情（50-80）
```yaml
medium_intensity_strategy:
  conditions:
    emotion_intensity: "50-80"
  strategy:
    first_sentence: "emotional_acceptance"
    second_sentence: "self_worth_confirmation"
    third_sentence: "empowerment"
    priority_score: 7.0
    reasoning: "中強度感情対応"
  special_instructions:
    - "理解と温かさのバランス"
    - "軽い視点転換可能"
  allow_patterns:
    - "建設的な視点提示"
    - "優しい現実認識"
```

### 軽度感情（50未満）
```yaml
low_intensity_strategy:
  conditions:
    emotion_intensity: "< 50"
  strategy:
    first_sentence: "gentle_support"
    second_sentence: "gentle_reality_check"
    third_sentence: "empowerment"
    priority_score: 5.0
    reasoning: "軽度感情対応"
  special_instructions:
    - "親しみやすく希望的"
    - "前向きな提案歓迎"
  allow_patterns:
    - "実践的提案"
    - "希望的視点"
```

## リソースレベルベース戦略

### 低リソース（<4）
```yaml
low_resource_strategy:
  conditions:
    resort_scores.resource: "< 4"
  strategy:
    first_sentence: "deep_empathy"
    second_sentence: "self_worth_confirmation"
    third_sentence: "self_affirmation_boost"
    priority_score: 8.0
    reasoning: "低リソース対応"
  focus_areas:
    - "自己価値の回復"
    - "存在肯定"
    - "無条件の受容"
```

### 中程度リソース（4-6）
```yaml
medium_resource_strategy:
  conditions:
    resort_scores.resource: "4-6"
  strategy:
    first_sentence: "emotional_acceptance"
    second_sentence: "gentle_reality_check"
    third_sentence: "empowerment"
    priority_score: 6.0
    reasoning: "中程度リソース対応"
  approach:
    - "バランス型アプローチ"
    - "段階的な視点転換"
```

### 高リソース（7+）
```yaml
high_resource_strategy:
  conditions:
    resort_scores.resource: "> 6"
  strategy:
    first_sentence: "gentle_support"
    second_sentence: "gentle_reality_check"
    third_sentence: "empowerment"
    priority_score: 6.5
    reasoning: "高リソース対応"
  allow_advanced:
    - "建設的な提案"
    - "行動指向のサポート"
```

## 深層感情ベース戦略

### 愛されたい欲求
```yaml
love_need_strategy:
  conditions:
    deep_emotion: "愛されたい・認められたい"
  strategy:
    first_sentence: "deep_empathy"
    second_sentence: "self_worth_confirmation"
    third_sentence: "self_affirmation_boost"
    priority_score: 9.5
    reasoning: "愛情欲求対応"
  key_messages:
    - "無条件の価値確認"
    - "存在そのものの肯定"
    - "愛される資格の確認"
```

### 安全欲求
```yaml
safety_need_strategy:
  conditions:
    deep_emotion: "安心して愛されたい"
  strategy:
    first_sentence: "deep_empathy"
    second_sentence: "emotion_validation"
    third_sentence: "accompaniment"
    priority_score: 8.5
    reasoning: "安全欲求対応"
  key_messages:
    - "安全な環境の提供"
    - "予測可能性の保証"
    - "継続的な支援の約束"
```

## 組み合わせルール

### 複数条件マッチング
```yaml
combination_rules:
  high_intensity_low_resource:
    conditions:
      - emotion_intensity: "> 80"
      - resort_scores.resource: "< 4"
    strategy_override:
      first_sentence: "deep_empathy"
      second_sentence: "self_worth_confirmation"
      third_sentence: "self_affirmation_boost"
      priority_score: 10.0
      reasoning: "危機的状況への統合対応"

  medium_intensity_love_need:
    conditions:
      - emotion_intensity: "50-80"
      - deep_emotion: "愛されたい"
    strategy_override:
      first_sentence: "emotional_acceptance"
      second_sentence: "self_worth_confirmation"
      third_sentence: "self_affirmation_boost"
      priority_score: 8.5
      reasoning: "中強度感情での愛情欲求対応"
```

### 戦略優先順位ルール
```yaml
priority_rules:
  crisis_detection: 10.0
  high_intensity_emotions: 9.0
  deep_psychological_needs: 8.5
  resource_considerations: 8.0
  relationship_factors: 7.0
  consultation_type_match: 6.5
  general_emotional_support: 5.0
```

## 戦略適用禁止ルール

### 組み合わせ禁止パターン
```yaml
forbidden_combinations:
  deep_empathy_with_reality_check:
    reason: "共感と現実認識の衝突"
    avoid_when:
      - first_sentence: "deep_empathy"
      - second_sentence: "gentle_reality_check"

  high_intensity_with_empowerment:
    reason: "高強度感情時の負担増加"
    avoid_when:
      - emotion_intensity: "> 80"
      - third_sentence: "empowerment"
    exception: "resource_score > 6"
```

### タイミング制限ルール
```yaml
timing_restrictions:
  early_rallies:
    rally_count: "< 3"
    restrictions:
      - "現実認識型は避ける"
      - "深い洞察は控える"
    preferred:
      - "基本的な共感"
      - "受容と理解"

  established_relationship:
    rally_count: "> 5"
    allow_advanced:
      - "建設的な視点転換"
      - "具体的な提案"
      - "深い心理的洞察"
```

## カスタマイズポイント

### 新戦略追加テンプレート
```yaml
new_strategy_template:
  strategy_name:
    conditions:
      parameter1: "condition"
      parameter2: "condition"
    strategy:
      first_sentence: "pattern_name"
      second_sentence: "pattern_name"
      third_sentence: "pattern_name"
      priority_score: 0.0-10.0
      reasoning: "戦略の理由"
    special_instructions:
      - "特別な指示1"
      - "特別な指示2"
    allow_patterns: []
    avoid_patterns: []
```