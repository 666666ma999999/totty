#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI API接続テストスクリプト
占いチャットシステム用OpenAI機能の動作確認
"""

import os
import sys
import json
import asyncio
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# プロジェクトルートに移動
sys.path.append('/Users/masaaki/Desktop/prm/totty2')

# 環境変数読み込み
load_dotenv('/Users/masaaki/Desktop/prm/totty2/.env')

def test_environment_setup():
    """環境設定テスト"""
    print("🔧 環境設定テスト")
    print("-" * 50)

    # API Key確認
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print(f"✅ OPENAI_API_KEY: 設定済み ({openai_key[:15]}...)")
    else:
        print("❌ OPENAI_API_KEY: 未設定")
        return False

    # OpenAIライブラリバージョン確認
    try:
        import openai
        print(f"✅ OpenAIライブラリ: v{openai.__version__}")
    except ImportError:
        print("❌ OpenAIライブラリ: インストール未確認")
        return False

    print()
    return True

def test_openai_client_initialization():
    """OpenAIクライアント初期化テスト"""
    print("🤖 OpenAIクライアント初期化テスト")
    print("-" * 50)

    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print("✅ OpenAIクライアント初期化成功")
        print()
        return client
    except Exception as e:
        print(f"❌ OpenAIクライアント初期化失敗: {e}")
        print()
        return None

def test_simple_completion(client):
    """シンプルな完了APIテスト"""
    print("💬 シンプルなChat Completion APIテスト")
    print("-" * 50)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは簡潔に回答するアシスタントです。"},
                {"role": "user", "content": "こんにちは。元気ですか？"}
            ],
            max_tokens=100,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content
        print(f"✅ API呼び出し成功")
        print(f"📝 応答: {ai_response}")
        print(f"🎯 モデル: {response.model}")
        print(f"📊 使用トークン: {response.usage.total_tokens}")
        print()
        return True

    except Exception as e:
        print(f"❌ API呼び出し失敗: {e}")
        print()
        return False

def test_character_response(client):
    """キャラクター応答テスト"""
    print("👤 キャラクター応答テスト（蒼司）")
    print("-" * 50)

    system_prompt = """
あなたは蒼司という名前のイケメン霊能師です。
- 28歳、長身で整った顔立ち、神秘的な雰囲気
- 優しく包容力があり、相談者を温かく受け入れる
- 深い洞察力で相手の心の奥底を読み取る
- 丁寧語を基調とした上品で穏やかな話し方
- 300文字程度の応答をしてください
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "最近仕事がうまくいかなくて悩んでいます..."}
            ],
            max_tokens=400,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content
        print(f"✅ キャラクター応答成功")
        print(f"📝 蒼司の応答:")
        print(f"「{ai_response}」")
        print(f"📊 使用トークン: {response.usage.total_tokens}")
        print()
        return True

    except Exception as e:
        print(f"❌ キャラクター応答失敗: {e}")
        print()
        return False

def test_backend_api_integration():
    """バックエンドAPI統合テスト"""
    print("🔌 バックエンドAPI統合テスト")
    print("-" * 50)

    # サーバー状態確認
    try:
        health_response = requests.get("http://127.0.0.1:8011/", timeout=5)
        if health_response.status_code == 200:
            print("✅ バックエンドサーバー: 稼働中")
        else:
            print(f"⚠️  バックエンドサーバー: 応答異常 (status: {health_response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ バックエンドサーバー: 接続失敗")
        print("   サーバーを起動してください: python3 backend/main.py")
        print()
        return False
    except Exception as e:
        print(f"❌ サーバー確認エラー: {e}")
        print()
        return False

    # チャットAPI テスト
    try:
        chat_payload = {
            "message": "こんにちは、占いをお願いします",
            "user_data": {},
            "chat_history": [],
            "rally_count": 1
        }

        chat_response = requests.post(
            "http://127.0.0.1:8011/api/chat",
            json=chat_payload,
            timeout=30
        )

        if chat_response.status_code == 200:
            data = chat_response.json()
            print("✅ チャットAPI: 正常動作")
            print(f"📝 応答: {data['response'][:100]}...")
            print(f"🏷️  カテゴリ: {data['category']}")
            print(f"📊 占いタイミングスコア: {data['fortune_timing_score']}")
        else:
            print(f"❌ チャットAPI: エラー (status: {chat_response.status_code})")
            print(f"   エラー詳細: {chat_response.text}")

    except Exception as e:
        print(f"❌ チャットAPI テスト失敗: {e}")
        print()
        return False

    print()
    return True

def test_fortune_api(client):
    """占いAPI専用テスト"""
    print("🔮 占いAPI テスト")
    print("-" * 50)

    try:
        fortune_payload = {
            "fortune_type": "相手の本音占い",
            "user_data": {
                "analysis_results": {
                    "resort_ti_scores": {
                        "romance": 75,
                        "relationship": 60
                    }
                }
            },
            "specific_context": "気になる人がいるのですが、相手の気持ちが知りたいです"
        }

        fortune_response = requests.post(
            "http://127.0.0.1:8011/api/fortune",
            json=fortune_payload,
            timeout=30
        )

        if fortune_response.status_code == 200:
            data = fortune_response.json()
            print("✅ 占いAPI: 正常動作")
            print(f"🔮 占い結果:")
            print(f"「{data['fortune_result'][:200]}...」")
        else:
            print(f"❌ 占いAPI: エラー (status: {fortune_response.status_code})")
            print(f"   エラー詳細: {fortune_response.text}")
            return False

    except Exception as e:
        print(f"❌ 占いAPI テスト失敗: {e}")
        return False

    print()
    return True

def test_error_handling():
    """エラーハンドリングテスト"""
    print("🛡️  エラーハンドリングテスト")
    print("-" * 50)

    try:
        # 不正なAPIキーでテスト
        bad_client = OpenAI(api_key="invalid-key")

        response = bad_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10
        )

        print("❌ 不正なAPIキーが受け入れられました（想定外）")
        return False

    except Exception as e:
        print(f"✅ 不正なAPIキーによるエラーハンドリング正常: {type(e).__name__}")

    # バックエンドでのフォールバック応答テスト
    try:
        # 無効なペイロードでテスト
        invalid_payload = {"invalid": "data"}

        response = requests.post(
            "http://127.0.0.1:8011/api/chat",
            json=invalid_payload,
            timeout=10
        )

        if response.status_code >= 400:
            print("✅ 無効なリクエストに対する適切なエラーレスポンス")
        else:
            print("⚠️  無効なリクエストが処理されました")

    except Exception as e:
        print(f"✅ ネットワークエラーハンドリング: {type(e).__name__}")

    print()
    return True

def generate_test_report(results):
    """テスト結果レポート生成"""
    print("=" * 60)
    print("📋 OpenAI API 動作確認テスト結果レポート")
    print("=" * 60)

    passed_tests = sum(results.values())
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100

    print(f"📊 総合結果: {passed_tests}/{total_tests} テスト合格 ({success_rate:.1f}%)")
    print()

    print("📋 詳細結果:")
    test_names = {
        "environment": "環境設定",
        "client_init": "クライアント初期化",
        "simple_completion": "基本API呼び出し",
        "character_response": "キャラクター応答",
        "backend_integration": "バックエンド統合",
        "fortune_api": "占いAPI",
        "error_handling": "エラーハンドリング"
    }

    for test_key, test_name in test_names.items():
        status = "✅ 合格" if results.get(test_key, False) else "❌ 不合格"
        print(f"  {test_name}: {status}")

    print()

    if success_rate >= 85:
        print("🎉 総合評価: 優秀 - OpenAI統合は正常に動作しています")
    elif success_rate >= 70:
        print("✅ 総合評価: 良好 - 一部機能に改善の余地があります")
    else:
        print("⚠️  総合評価: 要改善 - 重要な問題が検出されました")

    print()
    print(f"🕐 テスト実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def main():
    """メインテスト実行"""
    print("🚀 OpenAI API 動作確認テスト開始")
    print("=" * 60)

    results = {}

    # 1. 環境設定テスト
    results["environment"] = test_environment_setup()
    if not results["environment"]:
        print("❌ 環境設定に問題があります。テストを中止します。")
        return

    # 2. OpenAIクライアント初期化
    client = test_openai_client_initialization()
    results["client_init"] = client is not None

    if not client:
        print("❌ OpenAIクライアントの初期化に失敗しました。")
        generate_test_report(results)
        return

    # 3. 基本API呼び出しテスト
    results["simple_completion"] = test_simple_completion(client)

    # 4. キャラクター応答テスト
    results["character_response"] = test_character_response(client)

    # 5. バックエンドAPI統合テスト
    results["backend_integration"] = test_backend_api_integration()

    # 6. 占いAPIテスト
    results["fortune_api"] = test_fortune_api(client)

    # 7. エラーハンドリングテスト
    results["error_handling"] = test_error_handling()

    # 8. 結果レポート生成
    generate_test_report(results)

if __name__ == "__main__":
    main()