#!/bin/bash

# 占いチャットシステム - 停止スクリプト

echo "🛑 占いチャットシステムを停止しています..."

# PIDファイルから停止
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "✅ バックエンドサーバーを停止 (PID: $BACKEND_PID)"
    fi
    rm -f logs/backend.pid
fi

if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✅ フロントエンドサーバーを停止 (PID: $FRONTEND_PID)"
    fi
    rm -f logs/frontend.pid
fi

# ポート強制終了（確実に停止）
if lsof -ti:8010 > /dev/null 2>&1; then
    lsof -ti:8010 | xargs kill -9 2>/dev/null
    echo "✅ ポート8010を解放"
fi

if lsof -ti:8011 > /dev/null 2>&1; then
    lsof -ti:8011 | xargs kill -9 2>/dev/null
    echo "✅ ポート8011を解放"
fi

echo "✨ すべてのサーバーが停止しました"