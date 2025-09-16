#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
占いチャットシステム - FastAPI バックエンドサーバー
イケメン霊能師「蒼司」のAI応答システム
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# 環境変数読み込み
load_dotenv()

# FastAPIアプリ初期化
app = FastAPI(
    title="占いチャットシステム API",
    description="イケメン霊能師蒼司のAI応答システム",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:8010", "http://127.0.0.1:8010"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API設定
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# OpenAIクライアント初期化
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# データモデル定義
class ChatMessage(BaseModel):
    message: str
    user_data: Optional[Dict] = None
    chat_history: Optional[List[Dict]] = None
    rally_count: int = 0

class ChatResponse(BaseModel):
    response: str
    category: str
    needs_analysis: Dict[str, float]
    emotion_analysis: Dict[str, Any]
    resort_scores: Dict[str, int]
    fortune_timing_score: int
    suggested_fortune: Optional[str] = None

class FortuneRequest(BaseModel):
    fortune_type: str
    user_data: Dict
    specific_context: Optional[str] = None

# キャラクター設定（MDファイルから読み込み）
def load_character_config():
    """キャラクター設定をMDファイルから読み込み"""
    try:
        character_path = "../characters/psychic-character.md"
        if os.path.exists(character_path):
            with open(character_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        else:
            # フォールバック設定
            return """
            あなたは蒼司という名前のイケメン霊能師です。
            - 28歳、長身で整った顔立ち、神秘的な雰囲気
            - 優しく包容力があり、相談者を温かく受け入れる
            - 深い洞察力で相手の心の奥底を読み取る
            - 神秘性と誠実さを併せ持つ
            - 丁寧語を基調とした上品で穏やかな話し方
            """
    except Exception as e:
        print(f"キャラクター設定読み込みエラー: {e}")
        return "あなたは蒼司という霊能師として、優しく洞察力のある応答をしてください。"

CHARACTER_CONFIG = load_character_config()

# システムプロンプト生成（MDファイル設計統合版）
def generate_system_prompt(needs_analysis: Dict = None, category: str = None, rally_count: int = 0) -> str:
    """MDファイル設計に基づく包括的システムプロンプト生成"""

    base_prompt = f"""
{CHARACTER_CONFIG}

## 【重要】応答システム統合ルール

### 1. ニーズ自動判別（5種類）
以下のニーズを優先度順に自動判別して応答に反映：
- **愚痴・傾聴ニーズ** (重み0.8): "疲れた","うんざり","つらい","ストレス" → 深い共感応答
- **励ましニーズ** (重み0.9): "自信ない","不安","落ち込む","だめ" → 優しい励まし応答
- **孤独感ニーズ** (重み0.8): "一人","寂しい","孤独","理解者がいない" → 寄り添い応答
- **感情整理ニーズ** (重み0.7): "混乱","わからない","整理","迷っている" → 整理支援応答
- **承認欲求ニーズ** (重み0.6): "頑張った","認めて","評価","誉めて" → 認めと賞賛応答

### 2. 12カテゴリ応答パターン
判別されたニーズに応じて以下から最適パターンを選択：

**深い共感カテゴリ**: 愚痴・傾聴ニーズ時
- "本当につらい状況ですね..."
- "その気持ち、すごくわかります"
- "一人で抱え込んでいたんですね"

**優しい励ましカテゴリ**: 励ましニーズ時
- "きっと大丈夫ですよ"
- "あなたには力があります"
- "一歩ずつでいいんです"

**寄り添いカテゴリ**: 孤独感ニーズ時
- "一人じゃありませんよ"
- "私がいつでも聞いています"
- "あなたの味方です"

**認めと賞賛カテゴリ**: 承認欲求ニーズ時
- "よく頑張られましたね"
- "素晴らしい努力です"
- "あなたの価値をしっかり感じます"

**整理支援カテゴリ**: 感情整理ニーズ時
- "一緒に整理してみましょうか"
- "どの部分が一番気になりますか？"
- "順番に考えてみましょう"

**占い誘導カテゴリ**: 条件満たした時（後述）
- "星があなたにメッセージを送っているようです"
- "今、特別な運気を感じます"
- "占いで詳しく見てみませんか？"

### 3. データ収集戦略（171項目）
自然な会話で以下を段階的に収集：
- **基本情報**(20項目): 年齢、性別、職業、交際状況、家族構成等
- **心理・感情**(50項目): 感情状態、ストレス、自信度、対人関係等
- **恋愛・関係**(50項目): 恋愛経験、理想像、人間関係パターン等
- **仕事・キャリア**(30項目): 職場環境、満足度、転職願望等
- **価値観**(21項目): 信念、占いへの関心、人生哲学等

**収集ルール**:
- 1回のやり取りで最大3項目まで
- ラリー3回目以降から本格収集開始
- 直接質問は避け、自然な流れで情報収集

### 4. RESORT-TI分析（8次元）
会話から以下を分析・スコア化（0-100）：
- **R**(Relationship): 人間関係・社交性
- **E**(Emotion): 感情安定性・ストレス耐性
- **S**(Spirit): 精神性・スピリチュアル関心
- **O**(Occupation): 職業・キャリア満足度
- **R**(Romance): 恋愛・パートナーシップ
- **T**(Time): 未来志向・目標設定
- **I**(Intelligence): 知性・洞察力

### 5. 占い提案システム（7種類）
以下条件で適切な占いを自動提案：

**相手の本音占い**: Romance値高 + 人間関係の悩み
**恋愛相性診断**: 恋愛関心高 + パートナーシップ重視
**恋愛進展タイミング**: 恋愛積極性あり + タイミング重視
**運命の相手探し**: S値高 + 運命的出会い志向
**復縁可能性診断**: 過去恋愛への執着 + E値変動大
**人間関係修復**: R値低 + 対人関係悩み深刻
**総合運勢・人生指針**: RESORT総合値高 + 人生全般関心

**提案タイミング**: 総合スコア70以上 かつ データ収集率30%以上

### 6. 応答品質基準
- 文字数: 200-400文字
- 共感性スコア: 20-30を目標
- 自然性: 80-90%を維持
- 希望的要素を必ず含める
- 断定的表現は避ける

## 現在のセッション状況
"""

    if needs_analysis:
        dominant_need = max(needs_analysis.items(), key=lambda x: x[1])
        needs_list = ", ".join([f"{k}:{v:.1f}" for k, v in sorted(needs_analysis.items(), key=lambda x: x[1], reverse=True)])
        base_prompt += f"- 検出ニーズ: {needs_list}\n"
        base_prompt += f"- 主要ニーズ: {dominant_need[0]} (スコア: {dominant_need[1]:.1f})\n"

    if category:
        base_prompt += f"- 選択カテゴリ: {category}\n"

    base_prompt += f"- ラリー回数: {rally_count}回\n"

    base_prompt += """

## 応答指針
上記の統合ルールに基づき、検出されたニーズに最適な応答パターンを選択し、蒼司の人格で温かく応答してください。
データ収集が必要な場合は自然に織り込み、占い提案条件を満たす場合は適切なタイミングで提案してください。
相談者の心に深く寄り添い、あなたの霊能力で見えた洞察を伝えてください。
"""

    return base_prompt

# ニーズ分析機能（MDファイル設計統合版）
class NeedsAnalyzer:
    def __init__(self):
        # MDファイル needs_detection.md に基づくキーワード拡張
        self.keywords = {
            "complaining_listening": [
                "疲れた", "うんざり", "愚痴", "聞いて", "つらい", "ストレス", "もう嫌だ",
                "理解してもらえない", "聞いてほしい", "吐き出したい", "しんどい"
            ],
            "emotion_organizing": [
                "混乱", "わからない", "整理", "考えがまとまらない", "どうしたらいい",
                "迷っている", "判断できない", "頭の中がごちゃごちゃ", "整理したい"
            ],
            "recognition_desire": [
                "認めて", "頑張った", "評価", "誉めて", "見て", "すごい", "達成",
                "できた", "がんばってる", "努力している", "価値を感じたい"
            ],
            "encouragement": [
                "落ち込む", "自信ない", "不安", "心配", "怖い", "だめ", "失敗",
                "うまくいかない", "元気がない", "やる気が出ない", "前向きになりたい"
            ],
            "loneliness": [
                "一人", "寂しい", "孤独", "理解者がいない", "話し相手", "味方がいない",
                "仲間", "支えてくれる人", "つながりがほしい", "誰もわかってくれない"
            ]
        }

        # MDファイル設計に基づく重み設定（優先度順）
        self.weights = {
            "encouragement": 0.9,      # 最高優先度
            "complaining_listening": 0.8,
            "loneliness": 0.8,
            "emotion_organizing": 0.7,
            "recognition_desire": 0.6   # 最低優先度
        }
    
    def analyze(self, message: str) -> Dict[str, float]:
        """メッセージからニーズを分析"""
        needs_scores = {}
        
        for need_type, keywords in self.keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in message:
                    score += self.weights[need_type] * 20
            
            # 正規化（0-100）
            needs_scores[need_type] = min(100, score)
        
        return needs_scores

# カテゴリ選択機能（MDファイル設計統合版）
class CategorySelector:
    def __init__(self):
        # third_sentence_categories.md + category_selection.md 統合
        self.categories = {
            1: {"name": "深い共感", "trigger": "complaining_listening", "weight": 0.9},
            2: {"name": "優しい励まし", "trigger": "encouragement", "weight": 0.8},
            3: {"name": "認めと賞賛", "trigger": "recognition_desire", "weight": 0.7},
            4: {"name": "寄り添い", "trigger": "loneliness", "weight": 0.8},
            5: {"name": "整理支援", "trigger": "emotion_organizing", "weight": 0.6},
            6: {"name": "未来志向", "trigger": "anxiety_future", "weight": 0.7},
            7: {"name": "自己価値向上", "trigger": "self_confidence", "weight": 0.8},
            8: {"name": "安心感提供", "trigger": "anxiety", "weight": 0.8},
            9: {"name": "愛情表現", "trigger": "romance", "weight": 0.7},
            10: {"name": "成長促進", "trigger": "growth", "weight": 0.6},
            11: {"name": "直感重視", "trigger": "decision", "weight": 0.7},
            12: {"name": "占い誘導", "trigger": "fortune_timing", "weight": 1.0}
        }

        # ニーズ別優先カテゴリマッピング
        self.need_category_mapping = {
            "complaining_listening": [1, 4, 8],  # 深い共感、寄り添い、安心感提供
            "encouragement": [2, 6, 7],          # 優しい励まし、未来志向、自己価値向上
            "recognition_desire": [3, 7, 10],    # 認めと賞賛、自己価値向上、成長促進
            "loneliness": [4, 1, 9],             # 寄り添い、深い共感、愛情表現
            "emotion_organizing": [5, 11, 1]     # 整理支援、直感重視、深い共感
        }

    def select_category(self, needs_analysis: Dict[str, float], rally_count: int = 0) -> str:
        """MDファイル設計に基づく高度なカテゴリ選択"""

        # 占い誘導条件チェック（簡易版）
        total_needs = sum(needs_analysis.values())
        if rally_count >= 3 and total_needs > 50:  # 簡易的な占い提案条件
            if self._should_suggest_fortune(needs_analysis):
                return "占い誘導"

        # 最高スコアのニーズを特定
        if not needs_analysis or max(needs_analysis.values()) == 0:
            return "深い共感"  # デフォルト

        dominant_need = max(needs_analysis, key=needs_analysis.get)
        dominant_score = needs_analysis[dominant_need]

        # 対応するカテゴリから選択
        if dominant_need in self.need_category_mapping:
            priority_categories = self.need_category_mapping[dominant_need]

            # 優先度とスコアに基づく選択
            best_category_id = priority_categories[0]  # 第1優先
            best_category = self.categories[best_category_id]["name"]

            return best_category

        # フォールバック
        return "深い共感"

    def _should_suggest_fortune(self, needs_analysis: Dict[str, float]) -> bool:
        """占い提案判定（簡易版）"""
        # 複数ニーズが検出されている かつ 総合スコアが一定以上
        active_needs = sum(1 for score in needs_analysis.values() if score > 20)
        total_score = sum(needs_analysis.values())

        return active_needs >= 2 and total_score > 60

# グローバルインスタンス
needs_analyzer = NeedsAnalyzer()
category_selector = CategorySelector()

# API エンドポイント
@app.get("/")
async def root():
    """ヘルスチェック"""
    return {"status": "ok", "message": "占いチャットシステム API"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatMessage):
    """メインチャット応答エンドポイント"""
    try:
        # ニーズ分析
        needs_analysis = needs_analyzer.analyze(request.message)
        
        # カテゴリ選択
        selected_category = category_selector.select_category(needs_analysis, request.rally_count)
        
        # システムプロンプト生成
        system_prompt = generate_system_prompt(needs_analysis, selected_category, request.rally_count)
        
        # OpenAI API呼び出し
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ]
        
        # チャット履歴があれば追加（最新5件のみ）
        if request.chat_history:
            recent_history = request.chat_history[-5:]
            for history_item in recent_history:
                messages.insert(-1, {"role": "user", "content": history_item.get("user_message", "")})
                messages.insert(-1, {"role": "assistant", "content": history_item.get("bot_response", "")})
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=600,
            temperature=0.7,
            top_p=0.9
        )
        
        ai_response = response.choices[0].message.content
        
        # 感情分析（簡易版）
        emotion_analysis = analyze_emotion(request.message)
        
        # RESORT スコア計算（簡易版）
        resort_scores = calculate_resort_scores(needs_analysis, request.rally_count)
        
        # 占いタイミングスコア計算
        fortune_timing_score = calculate_fortune_timing(resort_scores, needs_analysis)
        
        # 占い提案判定
        suggested_fortune = None
        if fortune_timing_score >= 70:
            suggested_fortune = suggest_fortune_menu(resort_scores, needs_analysis)
        
        return ChatResponse(
            response=ai_response,
            category=selected_category,
            needs_analysis=needs_analysis,
            emotion_analysis=emotion_analysis,
            resort_scores=resort_scores,
            fortune_timing_score=fortune_timing_score,
            suggested_fortune=suggested_fortune
        )
        
    except Exception as e:
        print(f"OpenAI API エラー: {str(e)}")
        # エラー時はフォールバック応答
        fallback_response = generate_fallback_response(request.message)
        
        return ChatResponse(
            response=fallback_response,
            category="深い共感",
            needs_analysis={k: 0.0 for k in needs_analyzer.keywords.keys()},
            emotion_analysis={"polarity": 0.0, "intensity": 0.0, "dominant_emotion": "ニュートラル"},
            resort_scores={k: 0 for k in ["relationship", "emotion", "spirit", "occupation", "romance", "time", "intelligence"]},
            fortune_timing_score=0
        )

@app.post("/api/log")
async def log_endpoint(log_data: dict):
    """ログ受信エンドポイント"""
    try:
        # ログをファイルに保存（オプション）
        timestamp = log_data.get('timestamp', datetime.now().isoformat())
        log_type = log_data.get('type', 'unknown')
        
        print(f"[{timestamp}] Frontend Log - {log_type}: {log_data}")
        
        # 必要に応じてファイルやデータベースに保存
        # with open('logs/frontend.log', 'a', encoding='utf-8') as f:
        #     f.write(f"{timestamp} - {log_type}: {json.dumps(log_data, ensure_ascii=False)}\n")
        
        return {"status": "ok", "message": "ログを受信しました"}
        
    except Exception as e:
        print(f"ログ処理エラー: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/fortune")
async def fortune_endpoint(request: FortuneRequest):
    """占い実行エンドポイント"""
    try:
        fortune_prompt = generate_fortune_prompt(request.fortune_type, request.user_data)
        
        messages = [
            {"role": "system", "content": fortune_prompt},
            {"role": "user", "content": request.specific_context or "占いをお願いします"}
        ]
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=800,
            temperature=0.8
        )
        
        return {"fortune_result": response.choices[0].message.content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"占い実行エラー: {str(e)}")

# ヘルパー関数
def analyze_emotion(message: str) -> Dict[str, Any]:
    """簡易感情分析"""
    positive_words = ["嬉しい", "楽しい", "幸せ", "良い", "素晴らしい", "最高", "ありがとう"]
    negative_words = ["悲しい", "つらい", "苦しい", "嫌", "最悪", "だめ", "困った"]
    
    polarity = 0
    intensity = 0
    
    for word in positive_words:
        if word in message:
            polarity += 0.3
            intensity += 0.2
    
    for word in negative_words:
        if word in message:
            polarity -= 0.3
            intensity += 0.2
    
    # 正規化
    polarity = max(-1, min(1, polarity))
    intensity = max(0, min(1, intensity))
    
    if polarity > 0.5:
        dominant = "ポジティブ"
    elif polarity < -0.5:
        dominant = "ネガティブ"
    else:
        dominant = "ニュートラル"
    
    return {
        "polarity": round(polarity, 2),
        "intensity": round(intensity, 2), 
        "dominant_emotion": dominant
    }

def calculate_resort_scores(needs: Dict[str, float], rally_count: int) -> Dict[str, int]:
    """RESORT-TI スコア計算"""
    base_score = min(rally_count * 3, 30)  # ラリー回数ベース
    
    return {
        "relationship": min(100, base_score + int(needs.get("complaining_listening", 0) * 0.3)),
        "emotion": min(100, base_score + int(needs.get("encouragement", 0) * 0.3)),
        "spirit": min(100, base_score + 10),  # スピリチュアル基本値
        "occupation": min(100, base_score + 5),
        "romance": min(100, base_score + 15),
        "time": min(100, base_score + rally_count * 2),
        "intelligence": min(100, base_score + 20)
    }

def calculate_fortune_timing(resort_scores: Dict[str, int], needs: Dict[str, float]) -> int:
    """占いタイミングスコア計算"""
    resort_avg = sum(resort_scores.values()) / len(resort_scores)
    needs_max = max(needs.values()) if needs.values() else 0
    
    timing_score = (resort_avg * 0.6) + (needs_max * 0.4)
    return int(min(100, timing_score))

def suggest_fortune_menu(resort_scores: Dict[str, int], needs: Dict[str, float]) -> str:
    """MDファイル設計に基づく7種類占いメニュー提案"""

    # fortune_system.md に基づく提案ロジック
    romance_score = resort_scores.get("romance", 0)
    relationship_score = resort_scores.get("relationship", 0)
    spirit_score = resort_scores.get("spirit", 0)
    emotion_score = resort_scores.get("emotion", 0)

    # 1. 相手の本音占い: Romance値高 + 人間関係の悩み
    if romance_score > 60 and relationship_score < 60:
        return "相手の本音占い"

    # 2. 恋愛相性診断: 恋愛関心高 + パートナーシップ重視
    elif romance_score > 70 and needs.get("recognition_desire", 0) > 30:
        return "恋愛相性診断"

    # 3. 恋愛進展タイミング: 恋愛積極性あり + タイミング重視
    elif romance_score > 50 and resort_scores.get("time", 0) > 60:
        return "恋愛進展タイミング"

    # 4. 運命の相手探し: S値高 + 運命的出会い志向
    elif spirit_score > 60 and needs.get("loneliness", 0) > 40:
        return "運命の相手探し"

    # 5. 復縁可能性診断: 過去恋愛への執着 + E値変動大
    elif romance_score > 40 and emotion_score < 50:
        return "復縁可能性診断"

    # 6. 人間関係修復: R値低 + 対人関係悩み深刻
    elif relationship_score < 50 and needs.get("complaining_listening", 0) > 50:
        return "人間関係修復"

    # 7. 総合運勢・人生指針: RESORT総合値高 + 人生全般関心
    else:
        return "総合運勢・人生指針"

def generate_fortune_prompt(fortune_type: str, user_data: Dict) -> str:
    """MDファイル設計に基づく包括的占いプロンプト生成"""

    # fortune_system.md に基づく占いタイプ別詳細プロンプト
    fortune_details = {
        "相手の本音占い": {
            "focus": "気になる相手の心理状態と隠された本心の解読",
            "elements": "対人関係データ、感情分析値、コミュニケーションパターン",
            "output": "相手の現在の心境、本心の解読、アプローチ方法のアドバイス"
        },
        "恋愛相性診断": {
            "focus": "性格特徴の適合性と価値観の相性度分析",
            "elements": "性格特徴、価値観、恋愛スタイルマッチング",
            "output": "相性スコア算出、長所・短所の分析、関係発展の可能性"
        },
        "恋愛進展タイミング": {
            "focus": "最適なアプローチタイミングと関係進展の段階予測",
            "elements": "時間・未来志向、現在の状況分析、環境的要因",
            "output": "最適タイミング、進展段階予測、注意すべき時期"
        },
        "運命の相手探し": {
            "focus": "運命の相手の特徴予測と出会いの時期・場所",
            "elements": "スピリチュアル志向、理想のパートナー像、人生観",
            "output": "運命の相手の特徴、出会いの時期・場所、運命的サインの読み方"
        },
        "復縁可能性診断": {
            "focus": "復縁成功確率と相手の現在の心境分析",
            "elements": "感情の深さ・執着度、関係性の歴史、心理状態",
            "output": "復縁成功確率、相手の心境、復縁のための行動指針"
        },
        "人間関係修復": {
            "focus": "関係修復の可能性と問題の根本原因解析",
            "elements": "対人関係パターン、コミュニケーション課題、信頼関係",
            "output": "関係修復の可能性、問題の根本原因、改善のアドバイス"
        },
        "総合運勢・人生指針": {
            "focus": "総合運勢の予測と人生の方向性アドバイス",
            "elements": "全8次元の総合分析、ライフステージ、個人的成長可能性",
            "output": "総合運勢予測、人生の方向性アドバイス、潜在能力の開花予測"
        }
    }

    detail = fortune_details.get(fortune_type, fortune_details["総合運勢・人生指針"])

    base_prompt = f"""
{CHARACTER_CONFIG}

## 占い実行指示

### 占いタイプ: {fortune_type}
**専門分析領域**: {detail["focus"]}
**重要分析要素**: {detail["elements"]}
**提供すべき内容**: {detail["output"]}

### 占い結果構成（500-700文字）

1. **霊視ビジョン**(150-200文字):
   - 霊視で見えた具体的なビジョンや象徴的な映像を描写
   - 色彩、光、自然、人影など神秘的な表現を使用

2. **占い結果本体**(250-350文字):
   - {detail["output"]}を中心とした具体的な占い結果
   - データに基づく洞察と直感的な解釈を組み合わせ
   - 希望的で建設的な内容を含める

3. **実践的アドバイス**(100-150文字):
   - 実践可能な行動指針
   - 心構えや注意点
   - 次のステップの提案

### 占い品質基準
- 信頼度: 高精度(データ充実度80%以上)を目指す
- 表現: 過度な不安を与えない、希望的要素を含む
- 倫理: 自己決定の重要性を強調、占いは参考程度であることを明示

霊能師としての神秘性と誠実さを併せ持ち、相談者の心に深く寄り添う温かい占い結果を提供してください。
"""

    if user_data:
        base_prompt += f"\n## 相談者の情報\n{json.dumps(user_data, ensure_ascii=False, indent=2)}\n"

    return base_prompt

def generate_fallback_response(message: str) -> str:
    """フォールバック応答生成"""
    fallback_responses = [
        "その気持ち、よくわかります。心の奥の痛みが私にも伝わってきます。今は少しお疲れのようですね。",
        "大丈夫です。あなたには必ず道が開けます。その優しい心を信じてください。",
        "あなたの中にある光が見えます。困難な時期かもしれませんが、必ず良い変化が訪れます。",
        "一人じゃありませんよ。私がいつでもあなたのお話を聞いています。安心してください。"
    ]
    
    # 簡易的にメッセージの長さで選択
    index = len(message) % len(fallback_responses)
    return fallback_responses[index]

# 静的ファイル配信（フロントエンド）
app.mount("/static", StaticFiles(directory="../"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8011, reload=True)