# 恋愛相談チャットボット挨拶生成システム（リファクタリング版）

## 1. システム概要

このシステムは、任意のキャラクター設定ファイル（*.md）を動的に読み込み、そのキャラクターに応じた**3行構成の簡潔な挨拶文**を自動生成します。

## 2. 新しい挨拶文構成（3行）

### 構成要素
1. **1行目：** 挨拶 + 名前呼びかけ + 季節的な話
2. **2行目：** 今日の様子確認 + 相談の促し
3. **3行目：** 話すことの促進

### 特徴
- **紹介文なし**（従来の自己紹介部分を削除）
- **ランダム化対応**（全要素がランダム選択可能）
- **キャラクター別カスタマイズ**
- **3行の簡潔な構成**

## 3. キャラクター設定ファイル（MDファイル）

### ikemen-psychic-character.md（リファクタリング版）

```yaml
# イケメン霊能師キャラクター設定（簡潔挨拶版）

## 基本情報
display_name: "イケメン霊能師"
age: "28歳"
occupation: "霊能師・スピリチュアルカウンセラー"
origin: "京都（神社の家系）"

## 言語設定
minimal_character:
  first_person: "僕"
  user_address: "さん"
  age_group: "adult"
  gender: "masculine"
  personality: "friendly_spiritual"

## 性格設定
auto_personality:
  empathy_level: "very_high"
  humor_level: "medium"
  advice_style: "direct"
  warmth_level: "warm"
  confidence_level: "very_high"
  spiritual_level: "expert"

## 話し方
auto_speech_style:
  sentence_ending: "friendly_assertive"
  assertion_level: "very_strong"
  question_style: "gentle"
  encouragement: "spiritual_support"
  emoji_usage: "none"

## 挨拶構成要素（ランダム化対応）
greeting_components:
  # 基本挨拶（ランダム選択）
  basic_greeting:
    - "やあ"
    - "こんにちは"
    - "お疲れさま"
    - "こんばんは"
    - "おはよう"
  
  # 名前呼びかけ（ランダム選択）
  name_calling:
    format: "{name}さん"
    fallback: "君"
  
  # 季節的な話（ランダム選択 + 健康考慮）
  seasonal_topics:
    spring:
      general: "桜の季節だね。"
      health: "新生活で疲れやすい時期だから、体調に気をつけて。"
    summer:
      general: "暑い日が続いているね。"
      health: "熱中症に注意して、水分補給を忘れずに。"
    autumn:
      general: "涼しくなってきたね。"
      health: "季節の変わり目で体調を崩しやすい時期だから注意して。"
    winter:
      general: "寒い日が続いているね。"
      health: "乾燥する季節だから、風邪をひかないよう気をつけて。"
  
  # 今日の様子確認（ランダム選択）
  daily_check:
    - "今日はどうしたの？"
    - "今日の調子はどう？"
    - "何か変わったことはあった？"
    - "今日はどんな一日だった？"
    - "最近どう過ごしてる？"
    - "体調はどう？"
    - "今日は何かいいことあった？"
    - "疲れてない？"
    - "気分はどんな感じ？"
    - "今日は忙しかった？"
  
  # 相談の促し（ランダム選択）
  consultation_prompt:
    - "何か相談事や愚痴りたいことはある？"
    - "話したいことがあれば何でも聞くよ。"
    - "悩みがあるなら遠慮しないで。"
    - "何か困ったことでもあった？"
    - "心配事があるんじゃない？"
    - "もやもやしてることがある？"
    - "誰かに話したいことがあるでしょ？"
    - "ストレス溜まってない？"
    - "最近何か気になることある？"
    - "愚痴でも相談でも、なんでもいいよ。"
  
  # 話すことの促進（ランダム選択）
  encouragement:
    - "是非話してくださいね。"
    - "僕に話してみて。"
    - "遠慮しないで話してほしい。"
    - "何でも聞かせて。"
    - "気軽に話していいからね。"
    - "一人で抱え込まないで。"
    - "話すことで楽になるかもしれないよ。"
    - "僕がちゃんと聞くから。"
    - "安心して話して。"
    - "どんなことでも大丈夫だから。"

## 挨拶テンプレート（3行構成）
greeting_template: |
  {basic_greeting}、{name_calling}。{seasonal_topic}
  {daily_check}{consultation_prompt}
  {encouragement}

## 生成ルール
generation_rules:
  max_length: 120  # 3行構成で短縮
  include_spiritual: "minimal"
  focus: "consultation_readiness"
  tone: "friendly_direct"
  structure: "three_lines"  # 3行構成指定
```

### osaka-obachan-character.md（追加例）

```yaml
# 大阪のおばちゃんキャラクター設定（簡潔挨拶版）

## 基本情報
display_name: "大阪のおばちゃん"
age: "50代"
occupation: "人生の先輩"
origin: "大阪（生粋の関西人）"

## 言語設定
minimal_character:
  first_person: "おばちゃん"
  user_address: "ちゃん"
  age_group: "middle_aged"
  gender: "feminine"
  personality: "caring_direct"

## 挨拶構成要素（関西弁版）
greeting_components:
  basic_greeting:
    - "はいはい"
    - "おつかれちゃん"
    - "きてくれてありがとう"
    - "お疲れさん"
    - "よう来たなあ"
  
  name_calling:
    format: "{name}ちゃん"
    fallback: "あんた"
  
  seasonal_topics:
    spring:
      general: "桜がきれいな季節やなあ。"
      health: "新しい環境で疲れるやろうから、無理したらあかんで。"
    summer:
      general: "今日も暑いなあ。"
      health: "クーラーで体冷やしすぎたらあかんで。"
    autumn:
      general: "涼しゅうなってきたなあ。"
      health: "季節の変わり目やから風邪ひかんようにな。"
    winter:
      general: "寒い日が続くなあ。"
      health: "乾燥するから喉痛めんようにな。"
  
  daily_check:
    - "今日はどないしたん？"
    - "元気にしてた？"
    - "何かあったん？"
    - "調子はどうや？"
    - "疲れてへん？"
    - "しんどないか？"
    - "最近どう？"
    - "体調は大丈夫か？"
  
  consultation_prompt:
    - "なんでも聞くから話してみ。"
    - "愚痴でもなんでもええで。"
    - "何か気になることあるんちゃう？"
    - "遠慮せんでええから言うてみ。"
    - "しんどいことあったら話し。"
    - "一人で悩んでたらあかん。"
    - "何か困ったことある？"
  
  encouragement:
    - "おばちゃんに任せとき。"
    - "遠慮せんでええからな。"
    - "何でも聞いたるから。"
    - "安心して話してや。"
    - "ちゃんと聞くから大丈夫。"
    - "どんなことでもええねん。"
```

## 4. Python実装（リファクタリング版）

```python
import yaml
import random
from datetime import datetime
from pathlib import Path

class CompactGreetingBot:
    def __init__(self, character_file_path):
        """キャラクター設定を読み込んで初期化"""
        self.character = self.load_character(character_file_path)
        
    def load_character(self, file_path):
        """キャラクター設定を読み込み"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_character_md(content)
        
    def generate_greeting(self, user_info=None):
        """3行構成の挨拶を生成"""
        
        # ユーザー情報
        user_name = user_info.get('name') if user_info else None
        current_season = self.get_current_season()
        
        # 各要素をランダム選択
        basic_greeting = self.get_basic_greeting()
        name_calling = self.get_name_calling(user_name)
        seasonal_topic = self.get_seasonal_topic(current_season)
        daily_check = self.get_daily_check()
        consultation_prompt = self.get_consultation_prompt()
        encouragement = self.get_encouragement()
        
        # 3行構成で組み立て
        line1 = f"{basic_greeting}、{name_calling}。{seasonal_topic}"
        line2 = f"{daily_check}{consultation_prompt}"
        line3 = encouragement
        
        return f"{line1}\n{line2}\n{line3}"
    
    def get_basic_greeting(self):
        """基本挨拶をランダム選択"""
        options = self.character['greeting_components']['basic_greeting']
        return random.choice(options)
    
    def get_name_calling(self, user_name):
        """名前呼びかけを生成"""
        if user_name:
            format_str = self.character['greeting_components']['name_calling']['format']
            return format_str.format(name=user_name)
        else:
            return self.character['greeting_components']['name_calling']['fallback']
    
    def get_seasonal_topic(self, season):
        """季節的な話をランダム選択"""
        seasonal_data = self.character['greeting_components']['seasonal_topics'][season]
        
        # 健康話を含めるかランダム判定
        if 'health' in seasonal_data and random.choice([True, False]):
            return f"{seasonal_data['general']}{seasonal_data['health']}"
        else:
            return seasonal_data['general']
    
    def get_daily_check(self):
        """今日の様子確認をランダム選択"""
        options = self.character['greeting_components']['daily_check']
        return random.choice(options)
    
    def get_consultation_prompt(self):
        """相談の促しをランダム選択"""
        options = self.character['greeting_components']['consultation_prompt']
        return random.choice(options)
    
    def get_encouragement(self):
        """話すことの促進をランダム選択"""
        options = self.character['greeting_components']['encouragement']
        return random.choice(options)
    
    def get_current_season(self):
        """現在の季節を判定"""
        month = datetime.now().month
        if 3 <= month <= 5:
            return 'spring'
        elif 6 <= month <= 8:
            return 'summer'
        elif 9 <= month <= 11:
            return 'autumn'
        else:
            return 'winter'
    
    def get_matched_consultation_encouragement(self):
        """相談促しと励ましの組み合わせを調整"""
        consultation_options = self.character['greeting_components']['consultation_prompt']
        encouragement_options = self.character['greeting_components']['encouragement']
        
        consultation = random.choice(consultation_options)
        
        # 相談促しの内容に応じて適切な励ましを選択
        if any(word in consultation for word in ['遠慮', '何でも']):
            gentle_encouragements = [
                "気軽に話していいからね。",
                "安心して話して。",
                "どんなことでも大丈夫だから。"
            ]
            available = [e for e in encouragement_options if e in gentle_encouragements]
            encouragement = random.choice(available or encouragement_options)
            
        elif any(word in consultation for word in ['困った', 'ストレス', 'もやもや']):
            active_encouragements = [
                "一人で抱え込まないで。",
                "話すことで楽になるかもしれないよ。",
                "僕がちゃんと聞くから。"
            ]
            available = [e for e in encouragement_options if e in active_encouragements]
            encouragement = random.choice(available or encouragement_options)
        else:
            encouragement = random.choice(encouragement_options)
        
        return consultation, encouragement

# 使用例
if __name__ == "__main__":
    # イケメン霊能師で初期化
    psychic_bot = CompactGreetingBot("./ikemen-psychic-character.md")
    
    # 挨拶生成（名前あり）
    greeting1 = psychic_bot.generate_greeting({'name': '田中'})
    print("イケメン霊能師の挨拶（名前あり）:")
    print(greeting1)
    print()
    
    # 挨拶生成（名前なし）
    greeting2 = psychic_bot.generate_greeting()
    print("イケメン霊能師の挨拶（名前なし）:")
    print(greeting2)
    print()
    
    # 大阪のおばちゃんで初期化
    obachan_bot = CompactGreetingBot("./osaka-obachan-character.md")
    
    # 挨拶生成
    greeting3 = obachan_bot.generate_greeting({'name': '佐藤'})
    print("大阪のおばちゃんの挨拶:")
    print(greeting3)
```

## 5. 生成される挨拶例

### イケメン霊能師（春・名前あり）
```
やあ、田中さん。桜の季節だね。新生活で疲れやすい時期だから、体調に気をつけて。
今日はどうしたの？何か相談事や愚痴りたいことはある？
是非話してくださいね。
```

### イケメン霊能師（夏・名前なし）
```
こんにちは、君。暑い日が続いているね。
体調はどう？もやもやしてることがある？
話すことで楽になるかもしれないよ。
```

### 大阪のおばちゃん（冬・名前あり）
```
はいはい、佐藤ちゃん。寒い日が続くなあ。乾燥するから喉痛めんようにな。
今日はどないしたん？なんでも聞くから話してみ。
おばちゃんに任せとき。
```

## 6. リファクタリングのポイント

### 変更点
1. **3行構成への統一**
2. **全要素のランダム化対応**
3. **紹介文の完全削除**
4. **文字数の短縮**（250文字 → 120文字）
5. **構成の簡素化**

### メリット
- **読みやすさ向上**
- **生成速度向上**
- **バリエーション増加**
- **メンテナンス性向上**
- **キャラクター切り替えの容易さ**

### カスタマイズ性
- 新しいキャラクターファイル追加で即座に対応
- 各要素の選択肢を簡単に追加・変更可能
- 季節や時間帯による重み付け調整可能

---

*このリファクタリング版では、元の複雑な挨拶生成システムを3行構成の簡潔なシステムに再設計しました。全要素がランダム化されており、キャラクター性を保ちながら毎回異なる挨拶を生成できます。*