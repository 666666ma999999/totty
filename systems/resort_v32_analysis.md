# RESORT 6次元分析システム（v3.2仕様）

## システム概要
v3.2仕様に基づく6次元RESORT心理分析システム。
恋愛相談に特化した心理状態の多角的評価を行います。

## 6つの分析次元

### 1. R - Relationship（関係性の深さ・親密度）
**分析項目**:
- 相談者と相手との関係の親密さ
- 関係性の発展段階
- 感情的つながりの強さ

**評価範囲**: 1-10
**重要度**: 高

### 2. E - Emotion（感情の強度・種類）
**分析項目**:
- 感情の種類と強度
- 感情の安定性
- 感情表現の明確さ

**評価範囲**: 1-10
**重要度**: 最高

### 3. S - Situation（状況の緊急度・深刻度）
**分析項目**:
- 相談内容の緊急性
- 問題の深刻さ
- 解決の急務性

**評価範囲**: 1-10
**重要度**: 高

### 4. O - Objective（相談者の目的の明確さ）
**分析項目**:
- 相談の目的の明確性
- 解決への意欲
- 具体的な行動指針の求め度

**評価範囲**: 1-10
**重要度**: 中

### 5. R - Resource（相談者の心理的リソース）
**分析項目**:
- 精神的な余力
- 問題対処能力
- 前向きな思考の有無

**評価範囲**: 1-10
**重要度**: 中

### 6. T - Time（時間的要因・タイミング）
**分析項目**:
- 時間的な緊迫感
- 継続期間の長さ
- タイミングの重要性

**評価範囲**: 1-10
**重要度**: 中

## 具体的計算ルール

### 1. R - Relationship（関係性）計算ルール
```yaml
relationship_keywords:
  high_intimacy:
    keywords: ["彼氏", "彼女", "恋人"]
    score: 7
  medium_intimacy:
    keywords: ["友人", "職場", "家族"]
    score: 5
  default:
    formula: "max(1, rally_count)"
```

### 2. E - Emotion（感情）計算ルール
```yaml
emotion_keywords:
  strong_emotions: ["不安", "心配", "寂しい", "辛い", "悲しい", "怒り"]
  calculation: "min(8, 5 + emotion_count)"

special_patterns:
  contact_anxiety:
    pattern: ["連絡", "ない"]
    score: 7

default_emotion:
  formula: "max(1, int(sum(needs_analysis.values()) * 5))"
```

### 3. S - Situation（状況）計算ルール
```yaml
situation_keywords:
  urgency_high:
    keywords: ["緊急", "今すぐ", "どうしよう", "大変"]
    score: 8

  contact_situation:
    pattern: ["連絡", "ない"]
    score: 5

  default:
    formula: "max(1, min(7, rally_count + 2))"
```

### 4. O - Objective（目的）計算ルール
```yaml
objective_keywords:
  clear_purpose:
    keywords: ["どうしたら", "方法", "解決"]
    score: 6

  default:
    score: 3
```

### 5. R - Resource（心理リソース）計算ルール
```yaml
resource_keywords:
  positive:
    keywords: ["頑張る", "できる", "強い", "大丈夫"]
    weight: +1

  negative:
    keywords: ["疲れた", "無理", "限界", "もうダメ"]
    weight: -1

calculation_logic:
  if_negative_dominates: 3
  default: 5
```

### 6. T - Time（時間要因）計算ルール
```yaml
time_keywords:
  temporal_indicators:
    keywords: ["最近", "今", "以前から", "長い間", "いつも"]
    score: 8

  contact_temporal:
    pattern: ["連絡"]
    score: 8

  default:
    formula: "max(1, rally_count)"
```

## スコア算出方式

### 総合RESORT値
```
総合値 = (R + E + S + O + Resource + T) / 6
最大値: 10.0
最小値: 1.0
正規化: min(10, max(1, calculated_score))
```

### 占い提案タイミング算出
```yaml
timing_calculation:
  resort_weight: 0.4
  needs_weight: 0.6
  formula: |
    total_resort = sum(resort_scores) / 6
    needs_strength = sum(needs_analysis.values()) * 10
    timing_score = int(total_resort * 0.4 + needs_strength * 0.6)
    return min(100, max(0, timing_score))
```

### 占いメニュー推奨マッピング（7種類対応）
```yaml
fortune_mapping:
  relationship: "相手の本音占い"        # 関係性が高い場合
  emotion: "恋愛進展タイミング"          # 感情が高い場合
  situation: "人間関係修復"             # 状況が深刻な場合
  objective: "恋愛相性診断"             # 目的が明確な場合
  resource: "復縁可能性診断"            # 心理リソース低い場合
  time: "運命の相手探し"               # 時間要因が高い場合
  default: "総合運勢・人生指針"         # デフォルト・バランス型

selection_method: "max_resort_dimension"
description: "最も高いRESORT次元に基づいて7種類の占いメニューから選択"
```

## 分析アルゴリズム

### 基本分析ロジック
1. **メッセージ分析**: テキストから感情・状況・関係性を抽出
2. **次元別評価**: 各次元の個別スコア算出
3. **総合評価**: 6次元の統合スコア計算
4. **動的調整**: ラリー回数・文脈による補正

### 評価基準
- **高評価（8-10）**: 明確で強い要素
- **中評価（5-7）**: 中程度の要素
- **低評価（1-4）**: 弱いまたは不明確な要素

## 恋愛相談特化調整

### 恋愛関係キーワード
- 高親密度: 彼氏、彼女、恋人
- 中親密度: 友達、知り合い
- 感情表現: 不安、心配、寂しい、嬉しい

### 状況緊急度判定
- 緊急: 今すぐ、どうしよう、大変
- 中程度: 最近、困っている
- 継続的: いつも、ずっと

## リアルタイム更新

### 更新トリガー
- 新しいメッセージの受信
- ラリー回数の増加
- ニーズ分析結果の変更

### 更新方式
- 即座に全次元を再評価
- 履歴データとの統合
- 傾向分析による補正

## 出力フォーマット

### 分析結果
```json
{
  "relationship": 7,
  "emotion": 8,
  "situation": 5,
  "objective": 3,
  "resource": 5,
  "time": 8,
  "total": 6.0,
  "analysis_details": {
    "relationship": "恋愛関係での高い親密度",
    "emotion": "不安感情が強く検出",
    "situation": "中程度の状況深刻度",
    "objective": "目的が不明確",
    "resource": "中程度の心理的余力",
    "time": "時間的緊迫感が高い"
  }
}
```

## チューニングパラメータ

### 調整可能要素
- 各次元の重み係数
- キーワード検出の感度
- ラリー回数の影響度
- ニーズ分析との連携度

### 最適化指標
- 占い提案の適切性
- ユーザー満足度
- 応答品質の一貫性

---

*このシステムはv3.2仕様に完全準拠し、恋愛相談に特化した6次元心理分析を提供します。*