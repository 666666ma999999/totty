#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDファイル読み込みシステム - 統合版
MDファイル直接参照システムのコアモジュール
"""

import os
from typing import Dict, Optional
from datetime import datetime

class MDFileLoader:
    """MDファイル読み込み管理クラス（シングルトン）"""

    _instance = None
    _configs = {}
    _last_loaded = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load_md_file(self, file_path: str) -> str:
        """個別MDファイルを読み込み"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
            return ""
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return ""

    def load_system_configs(self, force_reload: bool = False) -> Dict[str, str]:
        """systemsフォルダからMDファイルを読み込み（キャッシュ付き）"""

        if self._configs and not force_reload:
            return self._configs

        # プロジェクトルートディレクトリを取得
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        systems_path = os.path.join(project_root, 'systems')

        md_files = {
            'needs_detection': 'needs_detection.md',
            'third_sentence_categories': 'third_sentence_categories.md',
            'category_selection': 'category_selection.md',
            'analysis_system': 'analysis_system.md',
            'data_collection': 'data_collection.md',
            'fortune_system': 'fortune_system.md',
            'fortune_menu_matching': 'fortune_menu_matching.md'
        }

        configs = {}
        for key, filename in md_files.items():
            file_path = os.path.join(systems_path, filename)
            configs[key] = self._load_md_file(file_path)

        # キャッシュ更新
        self._configs = configs
        self._last_loaded = datetime.now()

        print(f"MDファイル読み込み完了: {len([v for v in configs.values() if v])}個のファイル")

        return configs

    def load_character_config(self) -> str:
        """キャラクター設定をMDファイルから読み込み"""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        character_path = os.path.join(project_root, 'characters', 'psychic-character.md')

        content = self._load_md_file(character_path)
        if not content:
            # フォールバック設定
            content = """
            あなたは蒼司という名前のイケメン霊能師です。
            - 28歳、長身で整った顔立ち、神秘的な雰囲気
            - 優しく包容力があり、相談者を温かく受け入れる
            - 深い洞察力で相手の心の奥底を読み取る
            - 神秘性と誠実さを併せ持つ
            - 丁寧語を基調とした上品で穏やかな話し方
            """

        return content

    def get_config(self, key: str) -> Optional[str]:
        """特定のMD設定を取得"""
        if not self._configs:
            self.load_system_configs()
        return self._configs.get(key)

    def reload_configs(self) -> Dict[str, str]:
        """設定を強制再読み込み"""
        return self.load_system_configs(force_reload=True)


# シングルトンインスタンスを作成
md_loader = MDFileLoader()

def get_md_configs() -> Dict[str, str]:
    """依存関係注入用の設定取得関数"""
    return md_loader.load_system_configs()

def get_character_config() -> str:
    """キャラクター設定取得関数"""
    return md_loader.load_character_config()