#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
占いサービス - 統合版
占い実行とメニュー提案の専用サービスモジュール
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.md_loader import get_md_configs
from core.openai_client import get_openai_manager
from shared.config import AppConfig

# 占い用のルーター
fortune_router = APIRouter()

# データモデル
class FortuneRequest(BaseModel):
    fortune_type: str
    user_data: Dict[str, Any]
    specific_context: Optional[str] = None

class FortuneResponse(BaseModel):
    fortune_type: str
    result: str
    guidance: str
    timing_advice: str
    confidence_score: float

class FortuneMenuRequest(BaseModel):
    user_profile: Dict[str, Any]
    resort_scores: Dict[str, int]
    current_needs: Dict[str, float]

class FortuneMenuResponse(BaseModel):
    recommended_menus: list
    match_reasons: Dict[str, str]
    timing_scores: Dict[str, float]

# 占いシステムクラス
class FortuneSystem:
    def __init__(self, md_configs: Dict[str, str]):
        self.md_configs = md_configs
        self._load_fortune_configs()

    def _load_fortune_configs(self):
        """MDファイルから占い設定を読み込み"""
        fortune_md = self.md_configs.get('fortune_system', '')

        # 7種類の占いメニュー定義
        self.fortune_menus = {
            "相手の本音占い": {
                "target_resort": ["romance"],
                "description": "気になる相手の心理と本音を霊視で読み解きます",
                "keywords": ["恋愛", "相手", "気持ち", "本音"]
            },
            "恋愛相性診断": {
                "target_resort": ["romance", "relationship"],
                "description": "お二人の性格と価値観の相性を深く分析します",
                "keywords": ["相性", "恋愛", "関係性"]
            },
            "恋愛進展タイミング": {
                "target_resort": ["time", "romance"],
                "description": "最適なアプローチタイミングを星の配置から読み取ります",
                "keywords": ["タイミング", "進展", "アプローチ"]
            },
            "運命の相手探し": {
                "target_resort": ["spirit", "romance"],
                "description": "スピリチュアル的観点から運命の出会いを予測します",
                "keywords": ["運命", "出会い", "相手"]
            },
            "復縁可能性診断": {
                "target_resort": ["emotion", "romance"],
                "description": "復縁の可能性と成功への道筋を霊視で探ります",
                "keywords": ["復縁", "元彼", "元カノ", "戻る"]
            },
            "人間関係修復": {
                "target_resort": ["relationship"],
                "description": "職場や友人関係の修復方法を導きます",
                "keywords": ["人間関係", "修復", "職場", "友人"]
            },
            "総合運勢・人生指針": {
                "target_resort": ["spirit", "intelligence", "time"],
                "description": "全人生領域を包括的に占い、進むべき道を示します",
                "keywords": ["運勢", "人生", "全般", "指針"]
            }
        }

    def match_fortune_menu(
        self,
        resort_scores: Dict[str, int],
        needs_analysis: Dict[str, float],
        user_context: str = ""
    ) -> Dict[str, Any]:
        """最適な占いメニューをマッチング"""

        menu_scores = {}

        for menu_name, menu_config in self.fortune_menus.items():
            score = 0.0

            # RESORT値との適合度
            for target_resort in menu_config["target_resort"]:
                if target_resort in resort_scores:
                    score += resort_scores[target_resort] / 100.0

            # キーワードマッチング
            for keyword in menu_config["keywords"]:
                if keyword in user_context.lower():
                    score += 0.3

            # ニーズとの相関
            if "romance" in menu_config["target_resort"]:
                score += sum(needs_analysis.values()) * 0.2

            menu_scores[menu_name] = min(1.0, score)

        # トップ3を選択
        sorted_menus = sorted(menu_scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "recommended_menus": [menu[0] for menu in sorted_menus[:3]],
            "scores": dict(sorted_menus[:3]),
            "match_reasons": {
                menu: f"適合度: {score:.1%}"
                for menu, score in sorted_menus[:3]
            }
        }

    async def execute_fortune(
        self,
        fortune_type: str,
        user_data: Dict[str, Any],
        openai_manager,
        context: str = ""
    ) -> Dict[str, str]:
        """占い実行"""

        if fortune_type not in self.fortune_menus:
            raise ValueError(f"未対応の占いタイプ: {fortune_type}")

        menu_config = self.fortune_menus[fortune_type]

        # 占い専用プロンプト構築
        fortune_prompt = f"""
あなたは霊能師「蒼司」として、以下の占いを実行してください：

占いタイプ: {fortune_type}
占い内容: {menu_config['description']}

ユーザー情報:
{user_data}

追加コンテキスト: {context}

以下の形式で占い結果を生成してください：

【占い結果】
具体的で的確な洞察を3-4文で

【ガイダンス】
実践的なアドバイスを2-3文で

【タイミング】
最適な行動時期について1-2文で

神秘的で魅力的な表現を使い、前向きで建設的な内容にしてください。
"""

        try:
            # OpenAI API呼び出し
            result = await openai_manager.generate_fortune_reading(
                fortune_prompt, user_data, fortune_type
            )

            # 結果をパース（簡易版）
            parts = result.split("【")

            fortune_result = ""
            guidance = ""
            timing = ""

            for part in parts:
                if part.startswith("占い結果】"):
                    fortune_result = part.replace("占い結果】", "").strip()
                elif part.startswith("ガイダンス】"):
                    guidance = part.replace("ガイダンス】", "").strip()
                elif part.startswith("タイミング】"):
                    timing = part.replace("タイミング】", "").strip()

            # フォールバック
            if not fortune_result:
                fortune_result = result[:200] + "..." if len(result) > 200 else result
            if not guidance:
                guidance = "あなたの直感を信じて、前向きに行動することをお勧めします。"
            if not timing:
                timing = "今この時が、新しい一歩を踏み出すのに適した時期です。"

            return {
                "result": fortune_result,
                "guidance": guidance,
                "timing": timing
            }

        except Exception as e:
            print(f"占い実行エラー: {e}")
            return {
                "result": "星の導きが一時的に見えません。少し時間をおいてからもう一度お試しください。",
                "guidance": "焦らずに、心の声に耳を傾けてみてください。",
                "timing": "適切な時期が必ず訪れます。"
            }

# 占い実行エンドポイント
@fortune_router.post("/fortune/execute", response_model=FortuneResponse)
async def execute_fortune_endpoint(
    request: FortuneRequest,
    md_configs: Dict[str, str] = Depends(get_md_configs),
    openai_manager = Depends(get_openai_manager)
):
    """占い実行エンドポイント"""
    try:
        fortune_system = FortuneSystem(md_configs)

        result = await fortune_system.execute_fortune(
            request.fortune_type,
            request.user_data,
            openai_manager,
            request.specific_context or ""
        )

        return FortuneResponse(
            fortune_type=request.fortune_type,
            result=result["result"],
            guidance=result["guidance"],
            timing_advice=result["timing"],
            confidence_score=0.85  # 固定値（今後改善予定）
        )

    except Exception as e:
        print(f"占い実行エンドポイントエラー: {str(e)}")
        raise HTTPException(status_code=500, detail="占い実行エラー")

# 占いメニュー提案エンドポイント
@fortune_router.post("/fortune/recommend", response_model=FortuneMenuResponse)
async def recommend_fortune_menu(
    request: FortuneMenuRequest,
    md_configs: Dict[str, str] = Depends(get_md_configs)
):
    """占いメニュー推奨エンドポイント"""
    try:
        fortune_system = FortuneSystem(md_configs)

        # ユーザーコンテキストを構築
        context = str(request.user_profile) + str(request.current_needs)

        match_result = fortune_system.match_fortune_menu(
            request.resort_scores,
            request.current_needs,
            context
        )

        return FortuneMenuResponse(
            recommended_menus=match_result["recommended_menus"],
            match_reasons=match_result["match_reasons"],
            timing_scores=match_result["scores"]
        )

    except Exception as e:
        print(f"占いメニュー推奨エラー: {str(e)}")
        raise HTTPException(status_code=500, detail="メニュー推奨エラー")

# 利用可能な占いメニュー一覧
@fortune_router.get("/fortune/menus")
async def get_fortune_menus(
    md_configs: Dict[str, str] = Depends(get_md_configs)
):
    """占いメニュー一覧取得"""
    try:
        fortune_system = FortuneSystem(md_configs)

        menus = []
        for name, config in fortune_system.fortune_menus.items():
            menus.append({
                "name": name,
                "description": config["description"],
                "target_areas": config["target_resort"],
                "keywords": config["keywords"]
            })

        return {
            "menus": menus,
            "total_count": len(menus)
        }

    except Exception as e:
        print(f"メニュー一覧取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail="メニュー取得エラー")