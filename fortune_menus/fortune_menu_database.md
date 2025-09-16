# 占いメニューデータベース

## データベース概要
7種類の占いメニューの詳細情報とサンプル占い結果を定義

## メニューデータベース構造

### 1. 相手の本音占い
```json
{
  "menu_id": "honesty_reading",
  "title": "相手の本音占い",
  "description": "気になるあの人の本当の気持ちを占います",
  "target_users": ["Romance値>50", "R値>60", "人間関係の悩み"],
  "required_data": ["relationship_status", "target_person_info", "interaction_history"],
  "resort_weights": {
    "relationship": 0.4,
    "emotion": 0.3,
    "romance": 0.3
  },
  "sample_results": [
    {
      "title": "隠された想い",
      "content": "あの人はあなたに対して、表面的には見せていない深い関心を抱いています。普段はクールに振る舞っていますが、心の奥では...",
      "key_points": [
        "相手はあなたを特別視している",
        "照れ隠しで素っ気ない態度を取っている",
        "今後アプローチのチャンスがある"
      ],
      "advice": "相手からの小さなサインを見逃さないでください。"
    }
  ]
}
```

### 2. 恋愛相性診断
```json
{
  "menu_id": "love_compatibility",
  "title": "恋愛相性診断",
  "description": "お二人の恋愛相性を詳しく分析します",
  "target_users": ["Romance値>70", "特定の相手あり"],
  "required_data": ["personality_traits", "values", "love_language", "ideal_partner"],
  "resort_weights": {
    "romance": 0.4,
    "relationship": 0.3,
    "spirit": 0.3
  },
  "sample_results": [
    {
      "title": "運命的な相性",
      "content": "お二人の相性は89%と非常に高い数値を示しています。特に精神的な繋がりが深く...",
      "compatibility_score": 89,
      "strengths": ["価値観の一致", "コミュニケーション能力", "お互いを成長させる関係"],
      "challenges": ["時々の意見の相違", "ペースの違い"],
      "advice": "お互いの個性を尊重しながら歩んでください"
    }
  ]
}
```

### 3. 恋愛進展タイミング
```json
{
  "menu_id": "love_timing",
  "title": "恋愛進展タイミング占い", 
  "description": "関係を進展させる最適なタイミングを占います",
  "target_users": ["T値>65", "Romance値>60", "タイミング重視"],
  "required_data": ["current_relationship_stage", "interaction_frequency", "mutual_friends"],
  "resort_weights": {
    "time": 0.4,
    "romance": 0.3,
    "intelligence": 0.3
  },
  "sample_results": [
    {
      "title": "絶好のチャンス到来",
      "content": "今月下旬から来月上旬にかけて、恋愛運が最高潮に達します。特に...",
      "best_timing": "今月23日頃",
      "approach_method": "自然な流れでの食事の誘い",
      "success_probability": "85%",
      "advice": "焦らず、でも確実にチャンスを掴んでください"
    }
  ]
}
```

### 4. 運命の相手探し
```json
{
  "menu_id": "soulmate_search",
  "title": "運命の相手探し占い",
  "description": "あなたの運命の相手の特徴と出会いのタイミングを占います",
  "target_users": ["S値>70", "運命的な出会い志向"],
  "required_data": ["spiritual_beliefs", "ideal_partner", "past_relationships"],
  "resort_weights": {
    "spirit": 0.4,
    "romance": 0.3,
    "time": 0.3
  },
  "sample_results": [
    {
      "title": "魂の伴侶",
      "content": "あなたの運命の相手は、深い精神性を持ち、芸術的なセンスがある人です...",
      "partner_traits": [
        "優しくて包容力がある",
        "創造性豊か",
        "価値観が似ている"
      ],
      "meeting_place": "文化的なイベントや学びの場",
      "timing": "半年以内",
      "signs": "直感的に「この人だ」と感じる瞬間がある"
    }
  ]
}
```

### 5. 復縁可能性診断
```json
{
  "menu_id": "reconciliation", 
  "title": "復縁可能性診断",
  "description": "元恋人との復縁の可能性を詳しく占います",
  "target_users": ["過去の恋愛への執着", "E値変動大"],
  "required_data": ["breakup_reason", "post_breakup_contact", "mutual_feelings"],
  "resort_weights": {
    "emotion": 0.4,
    "romance": 0.3,
    "relationship": 0.3
  },
  "sample_results": [
    {
      "title": "希望の光",
      "content": "復縁の可能性は65%あります。相手もあなたのことを完全に忘れてはいません...",
      "success_rate": "65%",
      "current_ex_feelings": "複雑だが、良い思い出も残っている",
      "recommended_actions": [
        "まずは友人関係の修復から",
        "相手のペースを尊重する",
        "自分自身の成長をアピール"
      ],
      "timing": "3ヶ月後が転機",
      "warning": "焦りは禁物です"
    }
  ]
}
```

### 6. 人間関係修復
```json
{
  "menu_id": "relationship_repair",
  "title": "人間関係修復占い",
  "description": "こじれた人間関係を修復する方法を占います", 
  "target_users": ["R値<50", "対人関係の悩み深刻"],
  "required_data": ["conflict_details", "relationship_history", "desired_outcome"],
  "resort_weights": {
    "relationship": 0.4,
    "emotion": 0.3,
    "intelligence": 0.3
  },
  "sample_results": [
    {
      "title": "関係修復の道筋",
      "content": "この状況は修復可能です。相手も心の奥では関係を元に戻したいと思っています...",
      "repair_probability": "70%",
      "root_cause": "コミュニケーション不足による誤解",
      "action_steps": [
        "素直な謝罪から始める",
        "相手の立場を理解する努力",
        "時間をかけて信頼を回復"
      ],
      "timeline": "2-3ヶ月での段階的改善",
      "advice": "プライドより関係性を大切にしてください"
    }
  ]
}
```

### 7. 総合運勢・人生指針
```json
{
  "menu_id": "life_guidance",
  "title": "総合運勢・人生指針占い",
  "description": "あなたの総合運勢と人生の方向性をお示しします",
  "target_users": ["RESORT総合値>70", "人生全般への関心"],
  "required_data": ["life_goals", "current_challenges", "personal_growth_areas"],
  "resort_weights": {
    "relationship": 0.15,
    "emotion": 0.15,
    "spirit": 0.15,
    "occupation": 0.15,
    "romance": 0.15,
    "time": 0.15,
    "intelligence": 0.1
  },
  "sample_results": [
    {
      "title": "輝かしい未来への道標",
      "content": "あなたの人生は今、大きな転換点を迎えています。この変化は成長のための贈り物です...",
      "overall_fortune": "85%（非常に良好）",
      "life_phases": {
        "current": "変革期",
        "next_3_months": "基盤固めの時期", 
        "next_year": "飛躍の年"
      },
      "key_areas": [
        "キャリアでの大きな成功",
        "深い人間関係の構築",
        "内面的な成長と気づき"
      ],
      "life_mission": "多くの人に希望と癒しを与える存在になること",
      "advice": "直感を信じて、恐れずに前進してください"
    }
  ]
}
```

## 占いメニュー選択ロジック

### 自動推奨アルゴリズム
```javascript
function recommendFortune(userProfile, resortScores, detectedNeeds) {
  let menuScores = {};
  
  for (let menu of fortuneMenus) {
    let score = 0;
    
    // RESORT-TI適合度
    for (let dimension in menu.resort_weights) {
      score += resortScores[dimension] * menu.resort_weights[dimension];
    }
    
    // ニーズ適合度
    score += calculateNeedsMatch(detectedNeeds, menu.target_users);
    
    // データ充実度
    score += calculateDataCompleteness(userProfile, menu.required_data);
    
    menuScores[menu.menu_id] = score;
  }
  
  return Object.keys(menuScores).sort((a,b) => menuScores[b] - menuScores[a]);
}
```

### 表示用メニュー情報
```json
{
  "display_format": {
    "title_template": "🔮 {title}",
    "description_template": "{description}",
    "match_score_template": "マッチング度: {score}%",
    "button_template": "この占いを受ける"
  },
  "css_classes": {
    "high_match": "fortune-item-high",
    "medium_match": "fortune-item-medium", 
    "low_match": "fortune-item-low"
  }
}
```

## サンプル占い結果の使用ルール

### 適用条件
- データ不足時の補完
- AI生成結果の参考ベース
- 一貫性のあるトーン維持

### カスタマイズ要素  
- ユーザー名の挿入
- 具体的状況の反映
- RESORT-TI スコアによる調整
- 感情分析結果による語調調整