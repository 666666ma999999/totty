#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
柔軟レスポンス生成エンジン
MDファイル設定に基づく完全外部化システム
"""

import yaml
import re
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import os

@dataclass
class ResponseCandidate:
    """レスポンス候補データクラス"""
    first_sentence: str
    second_sentence: str
    third_sentence: str
    pattern_combination: str
    match_score: float
    reasoning: str

class FlexibleResponseEngine:
    """MDファイルベース柔軟レスポンス生成エンジン"""

    def __init__(self, systems_path: str):
        self.systems_path = systems_path
        self.response_patterns = {}
        self.consultation_types = {}
        self.evaluation_criteria = {}
        self.timing_rules = {}
        self._load_all_configs()

    def _load_all_configs(self):
        """全設定ファイルを読み込み"""
        try:
            # レスポンスパターン読み込み
            self._load_response_patterns()
            # 相談タイプ読み込み
            self._load_consultation_types()
            # 評価基準読み込み（将来実装）
            # self._load_evaluation_criteria()
        except Exception as e:
            print(f"設定読み込みエラー: {e}")

    def _load_response_patterns(self):
        """レスポンスパターンをMDファイルから読み込み"""
        # v3.2仕様：柔軟レスポンスシステムは無効化、バックエンドで直接計算
        print("v3.2: レスポンスパターンファイルは使用されません（バックエンド直接計算）")
        return

    def _load_consultation_types(self):
        """相談タイプをMDファイルから読み込み"""
        # v3.2仕様：相談タイプファイルも使用されません
        print("v3.2: 相談タイプファイルは使用されません（バックエンド直接計算）")
        return

    def detect_consultation_type(self,
                                message: str,
                                emotion_analysis: Dict,
                                resort_scores: Dict) -> str:
        """相談タイプを動的検出"""

        best_match = "軽い相談"
        best_score = 0.0

        for type_name, type_config in self.consultation_types.items():
            if not isinstance(type_config, dict):
                continue

            score = 0.0
            detection = type_config.get('detection_patterns', {})

            # キーワード検出
            keywords = detection.get('keywords', [])
            for keyword in keywords:
                if keyword in message:
                    score += 2.0

            # 感情強度チェック
            intensity_condition = detection.get('emotion_intensity', '')
            if intensity_condition:
                intensity = emotion_analysis.get('emotion_intensity', 0)
                if self._check_condition(intensity, intensity_condition):
                    score += 3.0

            # RESORT スコアチェック
            if 'resort_scores.resource' in detection:
                condition = detection['resort_scores.resource']
                resource_score = resort_scores.get('resource', 5)
                if self._check_condition(resource_score, condition):
                    score += 2.0

            # 主要感情マッチング
            key_emotions = type_config.get('key_emotions', [])
            primary_emotion = emotion_analysis.get('primary_emotion', '')
            if primary_emotion in key_emotions:
                score += 4.0

            if score > best_score:
                best_score = score
                best_match = type_name

        return best_match

    def _check_condition(self, value: float, condition: str) -> bool:
        """条件文字列をチェック"""
        if condition.startswith('> '):
            return value > float(condition[2:])
        elif condition.startswith('< '):
            return value < float(condition[2:])
        elif '-' in condition:
            min_val, max_val = map(float, condition.split('-'))
            return min_val <= value <= max_val
        return False

    def generate_response_candidates(self,
                                   message: str,
                                   emotion_analysis: Dict,
                                   resort_scores: Dict,
                                   rally_count: int) -> List[ResponseCandidate]:
        """複数のレスポンス候補を生成"""

        # 相談タイプ検出
        consultation_type = self.detect_consultation_type(message, emotion_analysis, resort_scores)

        # 候補生成
        candidates = []

        # 戦略的組み合わせを生成
        strategies = self._get_response_strategies(consultation_type, emotion_analysis, resort_scores)

        for strategy in strategies[:5]:  # 上位5候補
            candidate = self._build_response_candidate(strategy, emotion_analysis, resort_scores)
            if candidate:
                candidates.append(candidate)

        return sorted(candidates, key=lambda x: x.match_score, reverse=True)

    def _get_response_strategies(self,
                               consultation_type: str,
                               emotion_analysis: Dict,
                               resort_scores: Dict) -> List[Dict]:
        """レスポンス戦略を取得"""

        strategies = []

        # 基本戦略（相談タイプベース）
        if consultation_type in self.consultation_types:
            type_config = self.consultation_types[consultation_type]
            if isinstance(type_config, dict) and 'response_strategy' in type_config:
                strategy = type_config['response_strategy'].copy()
                strategy['consultation_type'] = consultation_type
                strategy['priority_score'] = 10.0
                strategies.append(strategy)

        # 感情強度ベース戦略
        emotion_intensity = emotion_analysis.get('emotion_intensity', 0)

        if emotion_intensity > 80:
            strategies.append({
                'first_sentence': 'deep_empathy',
                'second_sentence': 'emotion_validation',
                'third_sentence': 'accompaniment',
                'priority_score': 9.0,
                'reasoning': '高強度感情対応'
            })
        elif emotion_intensity > 50:
            strategies.append({
                'first_sentence': 'emotional_acceptance',
                'second_sentence': 'self_worth_confirmation',
                'third_sentence': 'empowerment',
                'priority_score': 7.0,
                'reasoning': '中強度感情対応'
            })
        else:
            strategies.append({
                'first_sentence': 'gentle_support',
                'second_sentence': 'gentle_reality_check',
                'third_sentence': 'empowerment',
                'priority_score': 5.0,
                'reasoning': '軽度感情対応'
            })

        # リソースベース戦略
        resource_score = resort_scores.get('resource', 5)
        if resource_score < 4:
            strategies.append({
                'first_sentence': 'deep_empathy',
                'second_sentence': 'self_worth_confirmation',
                'third_sentence': 'self_affirmation_boost',
                'priority_score': 8.0,
                'reasoning': '低リソース対応'
            })

        return sorted(strategies, key=lambda x: x.get('priority_score', 0), reverse=True)

    def _build_response_candidate(self, strategy: Dict, emotion_analysis: Dict, resort_scores: Dict) -> Optional[ResponseCandidate]:
        """戦略からレスポンス候補を構築"""

        try:
            # 各文のパターンを取得
            first_pattern = strategy.get('first_sentence', 'gentle_support')
            second_pattern = strategy.get('second_sentence', 'emotion_validation')
            third_pattern = strategy.get('third_sentence', 'empowerment')

            # パターンから具体的な文を選択
            first_sentence = self._select_sentence(first_pattern, emotion_analysis, resort_scores)
            second_sentence = self._select_sentence(second_pattern, emotion_analysis, resort_scores)
            third_sentence = self._select_sentence(third_pattern, emotion_analysis, resort_scores)

            if not all([first_sentence, second_sentence, third_sentence]):
                return None

            # マッチスコア計算
            match_score = self._calculate_match_score(strategy, emotion_analysis, resort_scores)

            return ResponseCandidate(
                first_sentence=first_sentence,
                second_sentence=second_sentence,
                third_sentence=third_sentence,
                pattern_combination=f"{first_pattern}→{second_pattern}→{third_pattern}",
                match_score=match_score,
                reasoning=strategy.get('reasoning', '標準的な対応')
            )

        except Exception as e:
            print(f"レスポンス候補構築エラー: {e}")
            return None

    def _select_sentence(self, pattern_name: str, emotion_analysis: Dict, resort_scores: Dict) -> str:
        """パターンから具体的な文を選択"""

        if pattern_name not in self.response_patterns:
            return f"[{pattern_name}パターンが見つかりません]"

        pattern_config = self.response_patterns[pattern_name]
        patterns = pattern_config.get('patterns', [])

        if not patterns:
            return f"[{pattern_name}の文例が見つかりません]"

        # 条件チェック（将来実装）
        # conditions = pattern_config.get('conditions', [])
        # if not self._check_pattern_conditions(conditions, emotion_analysis, resort_scores):
        #     return patterns[0]  # デフォルト

        # ランダム選択（または重み付き選択）
        return random.choice(patterns)

    def _calculate_match_score(self, strategy: Dict, emotion_analysis: Dict, resort_scores: Dict) -> float:
        """マッチスコアを計算"""

        base_score = strategy.get('priority_score', 5.0)

        # 感情強度適合性
        emotion_intensity = emotion_analysis.get('emotion_intensity', 0)
        if emotion_intensity > 80 and 'deep_empathy' in strategy.get('first_sentence', ''):
            base_score += 2.0

        # リソース適合性
        resource_score = resort_scores.get('resource', 5)
        if resource_score < 4 and 'self_worth_confirmation' in strategy.get('second_sentence', ''):
            base_score += 1.5

        # 共感レベル適合性
        empathy_level = emotion_analysis.get('empathy_level', 1)
        if empathy_level >= 4:
            base_score += 1.0

        return min(10.0, base_score)  # 最大10点

    async def get_best_response(self,
                         message: str,
                         emotion_analysis: Dict,
                         resort_scores: Dict,
                         rally_count: int,
                         openai_manager=None) -> Dict:
        """最適なレスポンスを取得"""

        candidates = self.generate_response_candidates(message, emotion_analysis, resort_scores, rally_count)

        if not candidates:
            return {
                'response': '申し訳ございません。適切な応答を生成できませんでした。',
                'pattern': 'fallback',
                'score': 0.0,
                'reasoning': 'エラー時フォールバック'
            }

        best_candidate = candidates[0]

        # OpenAI APIを使用して自然なレスポンスを生成
        if openai_manager:
            try:
                # プロンプトテンプレートを読み込み
                prompt_template = self._load_openai_prompt_template()

                # テンプレートを具体的な値で置換
                system_prompt = self._build_openai_prompt(
                    prompt_template,
                    message,
                    emotion_analysis,
                    resort_scores,
                    best_candidate
                )

                # OpenAI APIで自然な応答を生成
                full_response = await openai_manager.generate_chat_response(system_prompt, message)

            except Exception as e:
                print(f"OpenAI生成エラー: {e}")
                # フォールバック：パターン結合
                full_response = f"{best_candidate.first_sentence} {best_candidate.second_sentence} {best_candidate.third_sentence}"
        else:
            # OpenAI未使用時：パターン結合
            full_response = f"{best_candidate.first_sentence} {best_candidate.second_sentence} {best_candidate.third_sentence}"

        # 第3文パターンをわかりやすいカテゴリ名に変換
        third_pattern = best_candidate.pattern_combination.split('→')[-1]  # 最後の要素
        category_display_name = self._get_category_display_name(third_pattern)

        return {
            'response': full_response,
            'pattern': category_display_name,
            'score': best_candidate.match_score,
            'reasoning': best_candidate.reasoning,
            'candidates': [
                {
                    'response': f"{c.first_sentence} {c.second_sentence} {c.third_sentence}",
                    'pattern': self._get_category_display_name(c.pattern_combination.split('→')[-1]),
                    'score': c.match_score,
                    'reasoning': c.reasoning
                }
                for c in candidates[:3]  # 上位3候補
            ]
        }

    def _load_openai_prompt_template(self) -> str:
        """OpenAIプロンプトテンプレートを読み込み"""
        prompt_file = os.path.join(self.systems_path, "response_generation", "openai_prompts.md")

        if not os.path.exists(prompt_file):
            return "あなたは世界最高の恋愛カウンセラーです。以下の指示に従って、3センテンス以内で温かく共感的な返答をしてください。"

        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # base_system_prompt を抽出
        yaml_blocks = re.findall(r'```yaml\\n(.*?)\\n```', content, re.DOTALL)
        for block in yaml_blocks:
            try:
                data = yaml.safe_load(block)
                if data and 'base_system_prompt' in data:
                    return data['base_system_prompt']
            except yaml.YAMLError:
                continue

        # フォールバック
        return "あなたは世界最高の恋愛カウンセラーです。以下の指示に従って、3センテンス以内で温かく共感的な返答をしてください。"

    def _build_openai_prompt(self, template: str, message: str, emotion_analysis: Dict, resort_scores: Dict, candidate) -> str:
        """OpenAIプロンプトを構築"""

        # テンプレート変数を置換
        prompt = template.replace("{{primary_emotion}}", emotion_analysis.get('primary_emotion', 'ニュートラル'))
        prompt = prompt.replace("{{emotion_intensity}}", str(emotion_analysis.get('emotion_intensity', 0)))
        prompt = prompt.replace("{{deep_emotion}}", emotion_analysis.get('emotion_layers', {}).get('deep', '不明'))
        prompt = prompt.replace("{{pattern_combination}}", candidate.pattern_combination)
        prompt = prompt.replace("{{reasoning}}", candidate.reasoning)
        prompt = prompt.replace("{{first_sentence}}", candidate.first_sentence)
        prompt = prompt.replace("{{second_sentence}}", candidate.second_sentence)
        prompt = prompt.replace("{{third_sentence}}", candidate.third_sentence)
        prompt = prompt.replace("{{user_message}}", message)

        return prompt

    def _get_category_display_name(self, pattern_name: str) -> str:
        """パターン名を表示用カテゴリ名に変換"""
        pattern_to_category = {
            # ユーザー提案の7つのカテゴリ
            'exploratory_empathy': '探索的共感型',
            'small_insight_promotion': '小さな気づき促進型',
            'emotion_verbalization': '感情の言語化型',
            'collaborative_exploration': '共同探求型',
            'resource_discovery': 'リソース発見型',
            'normalization_acceptance': '正常化と受容型',
            'possibility_presentation': '可能性の提示型',

            # 既存のパターン
            'conversation_continuation': '探索的共感型',
            'empowerment': '励まし・希望提示型',
            'accompaniment': '寄り添い型',
            'self_affirmation_boost': '認めと賞賛型',
            'emotion_validation': '感情受容型',
            'gentle_reality_check': '現実認識型',
            'emotional_release': '感情解放型'
        }

        return pattern_to_category.get(pattern_name, pattern_name)

    def reload_configs(self):
        """設定の再読み込み（開発時便利機能）"""
        self.response_patterns = {}
        self.consultation_types = {}
        self._load_all_configs()
        print("設定を再読み込みしました")

# 使用例・テスト関数
def test_response_engine():
    """レスポンスエンジンのテスト"""

    # テストデータ
    systems_path = "/Users/masaaki/Desktop/prm/totty2/systems"

    engine = FlexibleResponseEngine(systems_path)

    test_message = "彼からの連絡が急に減って、とても不安です..."
    test_emotion = {
        'primary_emotion': '不安',
        'emotion_intensity': 75,
        'empathy_level': 4,
        'emotion_layers': {
            'surface': '不安',
            'middle': '愛情欲求',
            'deep': '愛されたい'
        }
    }
    test_resort = {
        'relationship': 7,
        'emotion': 8,
        'resource': 4
    }

    result = engine.get_best_response(test_message, test_emotion, test_resort, 2)

    print("=== レスポンス生成テスト ===")
    print(f"入力: {test_message}")
    print(f"応答: {result['response']}")
    print(f"パターン: {result['pattern']}")
    print(f"スコア: {result['score']}")
    print(f"理由: {result['reasoning']}")

    if 'candidates' in result:
        print("\n--- 他の候補 ---")
        for i, candidate in enumerate(result['candidates'][1:], 2):
            print(f"{i}. {candidate['response']} (スコア: {candidate['score']})")

if __name__ == "__main__":
    test_response_engine()