#!/bin/bash

# 占いチャットシステム - サーバー起動スクリプト
# ポート番号: 8010

echo "🔮 占いチャットシステムを起動します..."
echo "📁 プロジェクトディレクトリ: $(pwd)"
echo "🌐 ポート番号: 8010"
echo ""

# Pythonでローカルサーバーを起動
echo "🚀 サーバーを起動中..."
python3 -m http.server 8010

# 自動的にブラウザを開く場合は以下を追加
# open http://localhost:8010