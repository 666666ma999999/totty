# レスポンスパターン完全定義

## 3文構成システム

### 第1文（共感カテゴリ）
```yaml
deep_empathy:
  patterns:
    - "その気持ち、痛いほどわかる..."
    - "本当につらい状況ですね..."
    - "一人で抱え込んでいたんですね..."
  conditions:
    - emotion_intensity > 70
    - primary_emotion: ["悲しみ", "不安", "絶望"]
  weight: 0.9

emotional_acceptance:
  patterns:
    - "その気持ちって本当に辛いよね"
    - "そんな風に感じるのは自然なことだよ"
    - "心が重くなるのも当たり前だよ"
  conditions:
    - emotion_intensity: 40-70
    - empathy_level >= 3
  weight: 0.8

gentle_support:
  patterns:
    - "その気持ち、一人で抱えないで"
    - "あなたの想いを聞かせてくれてありがとう"
    - "今はそう感じても仕方ないよ"
  conditions:
    - emotion_intensity < 40
    - consultation_type: "軽い相談"
  weight: 0.7
```

### 第2文（橋渡しカテゴリ）
```yaml
self_worth_confirmation:
  patterns:
    - "でもね、あなたは十分素敵な人だから"
    - "あなたには価値があること、忘れないで"
    - "あなたらしさが、とても大切なんだよ"
  conditions:
    - deep_emotion: "愛されたい・認められたい"
    - resort_scores.resource < 5
  weight: 0.9

emotion_validation:
  patterns:
    - "その気持ち、我慢しなくていいんだよ"
    - "感じることに、良いも悪いもないから"
    - "あなたの感情は、すべて大切なもの"
  conditions:
    - emotion_layers.middle: "不安・恐れ"
    - consultation_type: "自己肯定感の問題"
  weight: 0.8

gentle_reality_check:
  patterns:
    - "彼にも事情があるかもしれないけど"
    - "状況は複雑だけれど"
    - "今は見えないけれど"
  conditions:
    - consultation_type: "関係性の迷い"
    - resort_scores.relationship > 6
  weight: 0.7
```

### 第3文（締めカテゴリ）- 優先順位付き
```yaml
self_affirmation_boost:
  priority: 1
  patterns:
    - "あなたは愛される価値がある人だよ"
    - "あなたの存在そのものが大切なんだから"
    - "ありのままのあなたが美しいよ"
  conditions:
    - deep_emotion: "愛されたい"
    - consultation_type: "自己肯定感の問題"
  weight: 1.0

empowerment:
  priority: 2
  patterns:
    - "あなたの優しさは必ず伝わるから"
    - "あなたには乗り越える力があるよ"
    - "あなたの想いはきっと届くから"
  conditions:
    - emotion_intensity > 50
    - resort_scores.resource >= 5
  weight: 0.9

accompaniment:
  priority: 3
  patterns:
    - "私はここにいるから、一人じゃないよ"
    - "いつでも話を聞くから、安心して"
    - "あなたの味方がここにいるからね"
  conditions:
    - primary_emotion: "孤独"
    - consultation_type: ["深い悲しみ", "慢性的な悩み"]
  weight: 0.9

emotional_release:
  priority: 4
  patterns:
    - "泣いてもいいし、ゆっくりでいいからね"
    - "無理しないで、自分のペースで大丈夫"
    - "今は休むことも大切だよ"
  conditions:
    - emotion_intensity > 80
    - resort_scores.resource < 4
  weight: 0.8

conversation_continuation:
  priority: 6
  patterns:
    - "よかったら、もう少し詳しく聞かせてもらえる？"
    - "その時の気持ち、どんな感じだった？"
    - "その後はどうなったの？"
    - "他にも何か気になることはある？"
    - "詳しいことは無理しなくていいけど、話したいことがあったら聞かせてね"
  conditions:
    - rally_count < 3
    - emotion_intensity < 60
  weight: 0.7

# ユーザー提案の7つのカテゴリ（第3文パターン）
exploratory_empathy:
  priority: 1
  patterns:
    - "その気持ち、もう少し聞かせてくれる？"
    - "どんな風に感じているか、教えてもらえる？"
    - "もう少し詳しく聞かせてもらえたら嬉しい"
  conditions:
    - rally_count < 3
    - emotion_intensity: 30-70
  weight: 0.9

small_insight_promotion:
  priority: 2
  patterns:
    - "でも、こうして話してくれるあなたの強さ、感じるよ"
    - "そうやって自分の気持ちに向き合えるのって、すごいことだと思う"
    - "話してくれることで、何か変化を感じられるかな"
  conditions:
    - rally_count >= 2
    - emotion_intensity: 40-80
  weight: 0.8

emotion_verbalization:
  priority: 3
  patterns:
    - "寂しさと不安が入り混じってる感じかな"
    - "もやもやした気持ちと、ちょっとした心配が一緒になってる？"
    - "複雑な気持ちが重なり合ってるんだね"
  conditions:
    - emotion_intensity: 50-85
    - empathy_level >= 3
  weight: 0.8

collaborative_exploration:
  priority: 4
  patterns:
    - "この気持ち、一緒に少しずつ整理してみようか"
    - "一緒に考えてみましょうか"
    - "お互いに探っていけたらいいね"
  conditions:
    - rally_count >= 2
    - emotion_intensity: 40-70
  weight: 0.7

resource_discovery:
  priority: 5
  patterns:
    - "今まで辛い時、何が支えになってた？"
    - "これまでも乗り越えてきた力、きっとあると思うんだ"
    - "あなたなりの対処法とか、何かある？"
  conditions:
    - rally_count >= 3
    - resort_scores.resource >= 4
  weight: 0.7

normalization_acceptance:
  priority: 7
  patterns:
    - "その気持ち、すごく自然なことだよ"
    - "そう感じるのは、当たり前のことだと思う"
    - "誰でも感じる気持ちだから、大丈夫"
  conditions:
    - emotion_intensity: 20-60
    - crisis_level < 3
  weight: 0.8

possibility_presentation:
  priority: 8
  patterns:
    - "もしかしたら、違う見方もできるかもね"
    - "別の角度から見ると、何か見えてくるかも"
    - "時間が経つと、また違って見えることもあるよね"
  conditions:
    - rally_count >= 4
    - emotion_intensity < 70
    - resort_scores.resource >= 5
  weight: 0.6
```

## 動的パターン選択ルール

### 選択アルゴリズム
```yaml
pattern_selection:
  step1_emotion_matching:
    - 感情強度による第1文選択
    - 相談タイプによる重み調整

  step2_context_analysis:
    - RESORT分析結果との適合性
    - 多層感情との一貫性チェック

  step3_priority_application:
    - 第3文は優先順位順で評価
    - 条件マッチ + 重み値で最終決定

combination_rules:
  avoid_conflicts:
    - 第1文が「深い共感」なら第2文は「感情正当化」推奨
    - 第2文が「現実認識」なら第3文は「エンパワーメント」避ける

  ensure_flow:
    - 感情の流れ：共感→理解→希望
    - トーンの統一：一貫した温かさ
```

## カスタマイズポイント

### A. 感情強度別調整
```yaml
intensity_adjustments:
  high_intensity(80+):
    first_sentence: "深い共感型必須"
    tone: "より優しく、時間をかけて"
    avoid: "解決提案、前向き過ぎる表現"

  medium_intensity(40-80):
    first_sentence: "感情受容型推奨"
    tone: "理解と温かさのバランス"
    allow: "軽い視点転換"

  low_intensity(40-):
    first_sentence: "優しい支援型"
    tone: "親しみやすく、希望的"
    allow: "前向きな提案"
```

### B. 相談タイプ別カスタマイズ
```yaml
consultation_customization:
  急性の不安:
    first_focus: "即座の安心感"
    second_focus: "感情の正当化"
    third_focus: "支え・同伴感"
    avoid_patterns: ["現実的慰め", "選択肢提示"]

  深い悲しみ:
    first_focus: "深い共感・理解"
    second_focus: "自己価値確認"
    third_focus: "自己肯定促進・支え"
    avoid_patterns: ["軽い表現", "急かす表現"]

  関係性の迷い:
    first_focus: "複雑さへの理解"
    second_focus: "現実認識"
    third_focus: "エンパワーメント"
    allow_patterns: ["整理提案", "視点転換"]
```