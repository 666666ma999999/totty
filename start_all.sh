#!/bin/bash

# 占いチャットシステム - 統合起動スクリプト
# フロントエンド + バックエンド同時起動

echo "🚀 占いチャットシステム（AI統合版）を起動します..."
echo ""

# 既存のプロセスをクリーンアップ
echo "📋 既存プロセスをチェック中..."
if lsof -ti:8010 > /dev/null 2>&1; then
    echo "⚠️  ポート8010使用中のプロセスを終了"
    lsof -ti:8010 | xargs kill -9 2>/dev/null || true
fi

if lsof -ti:8011 > /dev/null 2>&1; then
    echo "⚠️  ポート8011使用中のプロセスを終了"
    lsof -ti:8011 | xargs kill -9 2>/dev/null || true
fi

# Python依存パッケージのインストール確認
echo "📦 Python依存パッケージを確認中..."
pip3 install -q -r requirements.txt

echo ""
echo "🤖 バックエンド（AI統合）サーバーを起動中..."
echo "   ポート: 8011"
echo "   OpenAI API: 有効"

# バックエンドをバックグラウンドで起動
cd backend
python3 main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# バックエンドの起動を少し待つ
sleep 3

# バックエンドの起動確認
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ バックエンドサーバー起動完了 (PID: $BACKEND_PID)"
else
    echo "❌ バックエンド起動エラー"
    echo "📋 ログを確認: tail logs/backend.log"
    exit 1
fi

echo ""
echo "🌐 フロントエンドサーバーを起動中..."
echo "   ポート: 8010"

# フロントエンドをバックグラウンドで起動
python3 -m http.server 8010 > logs/frontend.log 2>&1 &
FRONTEND_PID=$!

# フロントエンドの起動を少し待つ
sleep 2

# フロントエンドの起動確認
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "✅ フロントエンドサーバー起動完了 (PID: $FRONTEND_PID)"
else
    echo "❌ フロントエンド起動エラー"
    exit 1
fi

echo ""
echo "🎉 すべてのサーバーが正常に起動しました！"
echo ""
echo "📊 アクセス情報:"
echo "   🔮 メインアプリ: http://localhost:8010"
echo "   📚 API文書:     http://localhost:8011/docs"
echo ""
echo "💡 使用方法:"
echo "   1. ブラウザで http://localhost:8010 を開く"
echo "   2. チャットで悩みを入力"
echo "   3. AI（蒼司）がリアルタイムで応答"
echo "   4. 占い提案が表示されたらクリック"
echo ""
echo "🔧 サーバー管理:"
echo "   停止: Ctrl+C または ./stop_all.sh"
echo "   ログ確認: tail -f logs/backend.log"
echo ""

# PIDファイル保存（停止スクリプト用）
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo "⏳ サーバーは実行中です... （Ctrl+C で停止）"

# 自動でブラウザを開く
sleep 2
if command -v open > /dev/null 2>&1; then
    echo "🌐 ブラウザを自動で開きます..."
    open http://localhost:8010
elif command -v xdg-open > /dev/null 2>&1; then
    echo "🌐 ブラウザを自動で開きます..."
    xdg-open http://localhost:8010
fi

# フォアグラウンドで待機（Ctrl+Cで停止可能）
trap 'echo ""; echo "🛑 サーバーを停止中..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit' INT

while true; do
    sleep 1
done