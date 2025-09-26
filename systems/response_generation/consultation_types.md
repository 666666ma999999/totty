# 相談タイプ完全定義システム

## 基本相談タイプ

### 急性の不安
```yaml
characteristics: "最近発生、高い感情強度、即座の対応必要"
optimal_rallies: [3, 4]
key_emotions: ["不安", "焦り", "パニック"]
detection_patterns:
  keywords: ["急に", "突然", "どうしよう", "パニック"]
  emotion_intensity: "> 70"
  emotion_duration: "短期間"
response_strategy:
  priority: "感情安定化"
  approach: "早期の感情安定化"
  first_sentence: "deep_empathy"
  second_sentence: "emotion_validation"
  third_sentence: "accompaniment"
timing_adjustments:
  extend_if: "症状悪化"
  reduce_if: "安定兆候"
```

### 深い悲しみ
```yaml
characteristics: "喪失感、低リソース、時間をかけた回復必要"
optimal_rallies: [5, 7]
key_emotions: ["悲しみ", "絶望", "喪失感"]
detection_patterns:
  keywords: ["失った", "もう", "終わった", "絶望"]
  emotion_intensity: "> 60"
  resort_scores.resource: "< 4"
response_strategy:
  priority: "感情解放と自己価値回復"
  approach: "十分な感情解放と段階的回復"
  first_sentence: "deep_empathy"
  second_sentence: "self_worth_confirmation"
  third_sentence: "self_affirmation_boost"
timing_adjustments:
  extend_if: "深層問題発覚"
  maintain_if: "順調な回復過程"
```

### 慢性的な悩み
```yaml
characteristics: "長期継続、固定化した感情パターン"
optimal_rallies: [4, 5]
key_emotions: ["疲れ", "諦め", "不満"]
detection_patterns:
  keywords: ["いつも", "ずっと", "毎回", "また"]
  emotion_intensity: "30-60"
  pattern_repetition: "高"
response_strategy:
  priority: "パターン認識と新視点"
  approach: "パターンの気づきと新視点"
  first_sentence: "emotional_acceptance"
  second_sentence: "gentle_reality_check"
  third_sentence: "empowerment"
timing_adjustments:
  standard_flow: "予定通り進行"
  breakthrough_moment: "延長検討"
```

### 関係性の迷い
```yaml
characteristics: "複雑な感情、整理が必要"
optimal_rallies: [3, 5]
key_emotions: ["迷い", "不安", "期待"]
detection_patterns:
  keywords: ["わからない", "どうして", "複雑", "迷い"]
  emotion_layers.middle: "不安・恐れ"
  resort_scores.relationship: "> 5"
response_strategy:
  priority: "感情整理と明確化"
  approach: "感情の整理と明確化"
  first_sentence: "gentle_support"
  second_sentence: "gentle_reality_check"
  third_sentence: "empowerment"
timing_adjustments:
  clarity_achieved: "短縮可能"
  deeper_complexity: "延長必要"
```

### 自己肯定感の問題
```yaml
characteristics: "深層の問題、根本的サポート必要"
optimal_rallies: [5, 8]
key_emotions: ["自己否定", "無価値感"]
detection_patterns:
  keywords: ["ダメ", "価値ない", "嫌い", "できない"]
  deep_emotion: "愛されたい・認められたい"
  resort_scores.resource: "< 5"
response_strategy:
  priority: "存在価値の再確認"
  approach: "存在の肯定と価値の再発見"
  first_sentence: "deep_empathy"
  second_sentence: "self_worth_confirmation"
  third_sentence: "self_affirmation_boost"
timing_adjustments:
  core_issue: "最大延長適用"
  progress_signs: "継続サポート"
```

### 軽い相談
```yaml
characteristics: "低い感情強度、実践的解決可能"
optimal_rallies: [2, 3]
key_emotions: ["好奇心", "軽い不安"]
detection_patterns:
  keywords: ["ちょっと", "少し", "なんとなく"]
  emotion_intensity: "< 40"
  tone_matching: "カジュアル・親しみやすい"
response_strategy:
  priority: "実践的サポート"
  approach: "気軽な対話と実践的サポート"
  first_sentence: "gentle_support"
  second_sentence: "emotion_validation"
  third_sentence: "empowerment"
timing_adjustments:
  quick_resolution: "短縮推奨"
  hidden_depth: "タイプ変更検討"
```

## 相談タイプ変化パターン

### 変化検出ルール
```yaml
transition_detection:
  surface_to_deep:
    pattern: ["急性の不安", "関係性の迷い", "自己肯定感の問題"]
    indicators:
      - emotion_intensity増加
      - deep_emotion変化
      - 過去の言及増加
    action: "+3回延長"

  anger_to_sadness:
    pattern: ["怒り表出", "関係性の問題", "深い悲しみ"]
    indicators:
      - primary_emotion変化
      - 攻撃性→脆弱性
    action: "感情解放優先、+2回延長"

  light_to_serious:
    pattern: ["軽い相談", "慢性的な悩み", "深い問題"]
    indicators:
      - 詳細な背景情報
      - 感情強度の段階的上昇
    action: "慎重に深堀り、+4回延長"

  crisis_emergence:
    pattern: ["any", "緊急状態"]
    indicators:
      - crisis_keywords検出
      - emotion_intensity > 90
    action: "緊急時プロトコル発動"
```

### 変化時対応戦略
```yaml
transition_strategies:
  maintain_trust:
    - 突然のトーン変更を避ける
    - 継続性を保ちながら深化
    - 相談者のペースを尊重

  adjust_expectations:
    - 新しいタイプの特性を考慮
    - 延長理由を内部的に記録
    - 段階的な対応変更

  preserve_progress:
    - 既築の信頼関係を活用
    - これまでの洞察を継承
    - 新しい視点で再構築
```

## カスタマイズガイド

### 新タイプ追加時のテンプレート
```yaml
new_consultation_type:
  characteristics: "具体的な特徴説明"
  optimal_rallies: [min, max]
  key_emotions: ["主要感情1", "主要感情2"]
  detection_patterns:
    keywords: []
    conditions: {}
  response_strategy:
    priority: "最重要目標"
    approach: "基本的なアプローチ"
    first_sentence: "pattern_name"
    second_sentence: "pattern_name"
    third_sentence: "pattern_name"
  timing_adjustments:
    condition1: "対応方針"
    condition2: "対応方針"
```