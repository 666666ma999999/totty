#!/bin/bash

# 占いチャットシステム - バックエンドサーバー起動スクリプト
# FastAPI + OpenAI API統合

echo "🤖 AI統合バックエンドサーバーを起動します..."
echo "📁 プロジェクトディレクトリ: $(pwd)"
echo "🌐 バックエンドポート: 8011"
echo "🔑 OpenAI API: 統合済み"
echo ""

# Python仮想環境があれば有効化
if [ -d "venv" ]; then
    echo "🐍 Python仮想環境を有効化中..."
    source venv/bin/activate
fi

# 必要なパッケージインストール確認
echo "📦 依存パッケージを確認中..."
pip install -r requirements.txt

echo ""
echo "🚀 FastAPIサーバーを起動中..."
echo "📊 API Docs: http://localhost:8011/docs"
echo "🔮 メインアプリ: http://localhost:8010"
echo ""

# バックエンドディレクトリに移動して起動
cd backend
python main.py