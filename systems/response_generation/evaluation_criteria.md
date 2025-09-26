# 評価基準システム

## 基本評価項目（感情重視型）

### 重要度設定
```yaml
evaluation_weights:
  sincerity: 0.25      # 誠実さ
  encouragement: 0.25  # 励まし度
  empathy: 0.25        # 共感度
  originality: 0.15    # 独創性
  practicality: 0.10   # 実用性
```

### 詳細評価基準

#### 誠実さ（25%）
```yaml
sincerity_criteria:
  high_score_indicators:
    - "押し付けがましくない表現"
    - "素直で自然な言葉選び"
    - "相談者の立場を尊重"
    - "判断を急かさない"

  medium_score_indicators:
    - "適度な距離感を保持"
    - "専門用語を避けている"

  low_score_indicators:
    - "説教っぽい表現"
    - "上から目線の言い回し"
    - "決めつけるような表現"

  forbidden_phrases:
    - "〜すべき"
    - "〜しなさい"
    - "間違っている"
    - "考え直して"
```

#### 励まし度（25%）
```yaml
encouragement_criteria:
  high_score_indicators:
    - "希望を感じられる表現"
    - "相談者の力を信じる言葉"
    - "前向きな可能性の提示"
    - "成長への期待"

  medium_score_indicators:
    - "現状を肯定的に捉える"
    - "小さな変化を評価"

  low_score_indicators:
    - "諦めを促す表現"
    - "否定的な予測"

  context_adjustments:
    high_intensity_emotions:
      - "直接的な励ましは控えめに"
      - "まずは受容を優先"
    low_resource_state:
      - "無理のない励まし"
      - "存在価値の確認を重視"
```

#### 共感度（25%）
```yaml
empathy_criteria:
  high_score_indicators:
    - "感情への深い理解"
    - "体験への共感表現"
    - "孤独感の軽減"
    - "感情の正当化"

  evaluation_methods:
    surface_empathy: "表面的な感情への反応"
    middle_empathy: "中層感情への理解"
    deep_empathy: "根本的なニーズへの共感"

  scoring_formula:
    base_score: 40
    surface_match: "+10"
    middle_match: "+20"
    deep_match: "+30"
    max_score: 100
```

#### 独創性（15%）
```yaml
originality_criteria:
  high_score_indicators:
    - "新しい視点の提供"
    - "ユニークな比喩や表現"
    - "意外な気づきの提示"

  medium_score_indicators:
    - "一般的でない視点"
    - "クリエイティブな言い回し"

  balance_with_empathy:
    - "独創性は共感を損なわない範囲で"
    - "奇抜さより洞察の深さを重視"
```

#### 実用性（10%）
```yaml
practicality_criteria:
  high_score_indicators:
    - "具体的で実行可能な提案"
    - "相談者の状況に適した助言"
    - "段階的なアプローチ"

  context_limits:
    early_rallies: "実用性は最小限に"
    high_emotion_intensity: "実践提案は避ける"
    low_resource_state: "負担の少ない提案のみ"
```

## 品質チェック基準

### 必須要件
```yaml
mandatory_requirements:
  response_length:
    min_characters: 150
    max_characters: 250
    target_range: "150-200文字"

  sentence_structure:
    max_sentences: 3
    preferred_sentences: 3
    min_sentences: 2

  tone_requirements:
    warmth: "必須"
    respect: "必須"
    non_judgmental: "必須"

  empathy_threshold:
    min_empathy_score: 20
    target_empathy_score: 30
    excellent_empathy_score: 40
```

### 禁止事項チェック
```yaml
prohibition_checks:
  forbidden_in_high_intensity:
    - "頑張って系の表現"
    - "前向き過ぎる励まし"
    - "問題の軽視"

  forbidden_in_low_resource:
    - "自己責任系の表現"
    - "努力を強要する表現"
    - "比較を促す表現"

  universally_forbidden:
    - "批判的な表現"
    - "否定的な決めつけ"
    - "専門用語の多用"
```

## 相談タイプ別評価調整

### 急性の不安
```yaml
anxiety_evaluation_adjustments:
  empathy_weight: 0.35  # 通常より高く
  sincerity_weight: 0.30
  encouragement_weight: 0.20  # 通常より低く
  originality_weight: 0.10
  practicality_weight: 0.05

  special_criteria:
    - "即座の安心感提供"
    - "解決提案は減点対象"
```

### 深い悲しみ
```yaml
sadness_evaluation_adjustments:
  empathy_weight: 0.40  # 最重視
  sincerity_weight: 0.25
  encouragement_weight: 0.15  # 控えめに
  originality_weight: 0.10
  practicality_weight: 0.10

  special_criteria:
    - "感情解放の促進"
    - "存在価値の確認"
```

## 自動評価アルゴリズム

### スコア計算式
```yaml
scoring_algorithm:
  base_calculation: |
    total_score = (
      sincerity_score * sincerity_weight +
      encouragement_score * encouragement_weight +
      empathy_score * empathy_weight +
      originality_score * originality_weight +
      practicality_score * practicality_weight
    ) * context_multiplier

  context_multipliers:
    perfect_match: 1.2
    good_match: 1.0
    acceptable_match: 0.9
    poor_match: 0.7

  penalty_deductions:
    forbidden_phrase: -10
    excessive_length: -5
    insufficient_empathy: -15
```

## カスタマイズ設定

### 評価重み調整
```yaml
weight_customization:
  empathy_focused:
    empathy: 0.40
    sincerity: 0.25
    encouragement: 0.20
    originality: 0.10
    practicality: 0.05

  balanced_approach:
    empathy: 0.25
    sincerity: 0.25
    encouragement: 0.25
    originality: 0.15
    practicality: 0.10

  support_focused:
    empathy: 0.30
    sincerity: 0.20
    encouragement: 0.30
    originality: 0.10
    practicality: 0.10
```