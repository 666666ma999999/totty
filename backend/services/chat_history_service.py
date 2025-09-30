#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
チャット履歴サービス - 統合版
チャット履歴の保存・管理・表示機能
"""

import os
import json
import glob
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# チャット履歴用のルーター
chat_history_router = APIRouter()

# データモデル
class ChatMessage(BaseModel):
    message_id: str
    type: str  # "user" or "ai"
    content: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

class ChatSession(BaseModel):
    session_id: str
    session_name: str
    start_time: str
    end_time: str
    message_count: int
    duration_minutes: float
    messages: List[ChatMessage]

class ChatHistoryManager:
    """チャット履歴管理クラス"""

    def __init__(self):
        self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "chat_logs")
        os.makedirs(self.logs_dir, exist_ok=True)

    def save_chat_message(
        self,
        session_id: str,
        message_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """チャットメッセージを保存"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()

            # セッションファイルパス
            session_file = self._get_session_filepath(session_id)

            # 既存セッションデータを読み込み
            session_data = self._load_session_data(session_file)

            # 新しいメッセージを追加
            message = {
                "message_id": f"{session_id}_{len(session_data['messages'])}",
                "type": message_type,
                "content": content,
                "timestamp": timestamp,
                "metadata": metadata or {}
            }

            session_data['messages'].append(message)
            session_data['end_time'] = timestamp
            session_data['message_count'] = len(session_data['messages'])

            # 期間計算
            if session_data['start_time']:
                start_time = datetime.fromisoformat(session_data['start_time'].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                duration = (end_time - start_time).total_seconds() / 60
                session_data['duration_minutes'] = round(duration, 2)

            # ファイルに保存
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)

            return True

        except Exception as e:
            print(f"チャット履歴保存エラー: {e}")
            return False

    def _get_session_filepath(self, session_id: str) -> str:
        """セッションファイルパスを取得"""
        # 日時ベースのファイル名
        today = datetime.now().strftime('%Y%m%d')
        filename = f"chat_{today}_{session_id}.json"
        return os.path.join(self.logs_dir, filename)

    def _load_session_data(self, session_file: str) -> Dict[str, Any]:
        """セッションデータを読み込み"""
        if os.path.exists(session_file):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"セッションファイル読み込みエラー: {e}")

        # 新しいセッション
        session_id = os.path.basename(session_file).replace('.json', '')
        timestamp = datetime.now(timezone.utc).isoformat()

        return {
            "session_id": session_id,
            "session_name": f"チャットセッション {datetime.now().strftime('%Y/%m/%d %H:%M')}",
            "start_time": timestamp,
            "end_time": timestamp,
            "message_count": 0,
            "duration_minutes": 0.0,
            "messages": []
        }

    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """全セッション一覧を取得"""
        sessions = []

        try:
            # chat_logs/*.json ファイルを検索
            pattern = os.path.join(self.logs_dir, "chat_*.json")
            files = glob.glob(pattern)

            for file_path in sorted(files, key=os.path.getmtime, reverse=True):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)

                    # サマリー情報のみ抽出
                    sessions.append({
                        "session_id": session_data.get('session_id', ''),
                        "session_name": session_data.get('session_name', ''),
                        "start_time": session_data.get('start_time', ''),
                        "end_time": session_data.get('end_time', ''),
                        "message_count": session_data.get('message_count', 0),
                        "duration_minutes": session_data.get('duration_minutes', 0.0),
                        "file_path": file_path
                    })

                except Exception as e:
                    print(f"セッションファイル読み込みエラー: {file_path} - {e}")

        except Exception as e:
            print(f"セッション一覧取得エラー: {e}")

        return sessions

    def get_session_detail(self, session_id: str) -> Optional[Dict[str, Any]]:
        """特定セッションの詳細を取得"""
        try:
            # セッションファイルを検索
            pattern = os.path.join(self.logs_dir, f"*{session_id}.json")
            files = glob.glob(pattern)

            if not files:
                return None

            session_file = files[0]  # 最初のマッチファイル

            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            print(f"セッション詳細取得エラー: {e}")
            return None

    def get_active_session_id(self) -> Optional[str]:
        """アクティブなセッションIDを取得（30分以内の最新セッション）"""
        if not os.path.exists(self.logs_dir):
            return None

        chat_files = [f for f in os.listdir(self.logs_dir) if f.startswith('chat_') and f.endswith('.json')]

        if not chat_files:
            return None

        # 最新のセッションファイルを取得
        latest_file = None
        latest_time = None

        for file in chat_files:
            try:
                file_path = os.path.join(self.logs_dir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)

                # 最後のメッセージの時刻を確認
                if session_data.get('messages'):
                    last_message_time = datetime.fromisoformat(session_data['messages'][-1]['timestamp'].replace('Z', '+00:00'))

                    if latest_time is None or last_message_time > latest_time:
                        latest_time = last_message_time
                        latest_file = file

            except Exception as e:
                print(f"セッションファイル読み込みエラー ({file}): {str(e)}")
                continue

        if latest_file and latest_time:
            # 30分以内のセッションかチェック
            time_diff = datetime.now(timezone.utc) - latest_time
            if time_diff <= timedelta(minutes=30):
                # ファイル名からセッションIDを抽出
                session_id = latest_file.replace('chat_', '').replace('.json', '')
                return session_id

        return None

# グローバルインスタンス
chat_history_manager = ChatHistoryManager()

# API エンドポイント

@chat_history_router.post("/chat/save")
async def save_chat_message(
    session_id: str,
    message_type: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
):
    """チャットメッセージ保存API"""
    try:
        success = chat_history_manager.save_chat_message(
            session_id, message_type, content, metadata
        )

        if success:
            return {"status": "ok", "message": "チャットメッセージを保存しました"}
        else:
            raise HTTPException(status_code=500, detail="保存に失敗しました")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存エラー: {str(e)}")

@chat_history_router.get("/chat/sessions")
async def get_chat_sessions():
    """チャットセッション一覧取得API"""
    try:
        sessions = chat_history_manager.get_all_sessions()
        return {
            "sessions": sessions,
            "total_count": len(sessions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション取得エラー: {str(e)}")

@chat_history_router.get("/chat/sessions/{session_id}")
async def get_session_detail(session_id: str):
    """特定セッション詳細取得API"""
    try:
        session = chat_history_manager.get_session_detail(session_id)

        if session:
            return session
        else:
            raise HTTPException(status_code=404, detail="セッションが見つかりません")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"セッション詳細取得エラー: {str(e)}")

@chat_history_router.get("/chat_history/", response_class=HTMLResponse)
async def chat_history_page():
    """チャット履歴一覧HTMLページ"""

    html_content = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>チャット履歴 - 蒼司の占い館</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans JP', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
            user-select: text;
            -webkit-user-select: text;
            -moz-user-select: text;
            -ms-user-select: text;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .sessions-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .loading {
            text-align: center;
            padding: 50px;
            font-size: 1.2rem;
            color: #666;
        }

        .session-item {
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            margin-bottom: 15px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .session-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-color: #2a5298;
        }

        .session-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 10px;
        }

        .session-name {
            font-size: 1.3rem;
            font-weight: bold;
            color: #2a5298;
        }

        .session-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }

        .info-item {
            display: flex;
            align-items: center;
            font-size: 0.9rem;
            color: #666;
        }

        .info-label {
            font-weight: bold;
            margin-right: 8px;
            min-width: 80px;
        }

        .detail-view {
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #2a5298;
        }

        .message-list {
            max-height: none;
            overflow-y: visible;
        }

        .message-item {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
        }

        .message-user {
            background: #e3f2fd;
            text-align: right;
        }

        .message-ai {
            background: #f3e5f5;
        }

        .message-content {
            font-size: 1rem;
            margin-bottom: 5px;
            user-select: text !important;
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            cursor: text;
        }

        /* すべてのテキスト要素に対する包括的な設定 */
        .message-item * {
            user-select: text !important;
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
        }

        .session-detail * {
            user-select: text !important;
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
        }

        .expand-icon {
            float: right;
            font-size: 0.9rem;
            transition: transform 0.2s;
        }

        .session-header:hover {
            background: rgba(0, 0, 0, 0.05);
        }

        .detail-view {
            border-top: 1px solid #ddd;
            padding: 15px;
            margin-top: 10px;
        }

        .message-timestamp {
            font-size: 0.8rem;
            color: #666;
        }

        .message-metadata {
            margin-top: 10px;
            padding: 8px;
            background: rgba(255,255,255,0.7);
            border-radius: 4px;
            font-size: 0.85rem;
        }

        .metadata-item {
            margin-bottom: 3px;
        }

        .back-button {
            display: inline-block;
            margin-bottom: 20px;
            padding: 10px 20px;
            background: #2a5298;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s ease;
        }

        .back-button:hover {
            background: #1e3c72;
        }

        .no-sessions {
            text-align: center;
            padding: 50px;
            color: #666;
            font-size: 1.1rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔮 チャット履歴</h1>
            <p>蒼司との過去の会話履歴をご覧いただけます</p>
            <a href="/" class="back-button">メインページに戻る</a>
        </div>

        <div class="sessions-container">
            <div id="loading" class="loading">
                履歴を読み込み中...
            </div>

            <div id="sessions-list" style="display: none;">
                <!-- セッション一覧がここに動的に挿入される -->
            </div>

            <div id="no-sessions" class="no-sessions" style="display: none;">
                チャット履歴がありません<br>
                メインページでチャットを始めてみましょう
            </div>
        </div>
    </div>

    <script>
        class ChatHistoryViewer {
            constructor() {
                this.loadSessions();
            }

            async loadSessions() {
                try {
                    console.log('Loading sessions...');
                    const response = await fetch('/chat/sessions');
                    const data = await response.json();
                    console.log('Response data:', data);
                    console.log('Sessions count:', data.sessions.length);

                    document.getElementById('loading').style.display = 'none';

                    if (data.sessions.length === 0) {
                        console.log('No sessions found');
                        document.getElementById('no-sessions').style.display = 'block';
                        return;
                    }

                    console.log('Rendering sessions...');
                    this.renderSessions(data.sessions);
                    document.getElementById('sessions-list').style.display = 'block';
                    console.log('Sessions list displayed');

                } catch (error) {
                    console.error('セッション読み込みエラー:', error);
                    document.getElementById('loading').innerHTML = 'エラーが発生しました';
                }
            }

            renderSessions(sessions) {
                console.log('renderSessions called with', sessions.length, 'sessions');
                const container = document.getElementById('sessions-list');
                console.log('Container found:', container);

                const html = sessions.map(session => `
                    <div class="session-item">
                        <div class="session-header" onclick="chatHistory.toggleSessionDetail('${session.session_id}')" style="cursor: pointer;">
                            <div class="session-name">${session.session_name}</div>
                            <div class="expand-icon">▼</div>
                        </div>

                        <div class="session-info">
                            <div class="info-item">
                                <span class="info-label">メッセージ数:</span>
                                <span>${session.message_count}件</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">開始時刻:</span>
                                <span>${this.formatDateTime(session.start_time)}</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">継続時間:</span>
                                <span>${session.duration_minutes}分</span>
                            </div>
                            <div class="info-item">
                                <span class="info-label">セッションID:</span>
                                <span>${session.session_id}</span>
                            </div>
                        </div>

                        <div id="detail-${session.session_id}" class="detail-view" style="display: none;" onclick="event.stopPropagation();">
                            <div class="loading">詳細を読み込み中...</div>
                        </div>
                    </div>
                `).join('');

                console.log('Generated HTML:', html);
                container.innerHTML = html;
                console.log('HTML set to container');
            }

            async toggleSessionDetail(sessionId) {
                const detailDiv = document.getElementById(`detail-${sessionId}`);

                if (detailDiv.style.display === 'block') {
                    detailDiv.style.display = 'none';
                    return;
                }

                detailDiv.style.display = 'block';

                try {
                    const response = await fetch(`/chat/sessions/${sessionId}`);
                    const session = await response.json();

                    this.renderSessionDetail(detailDiv, session);

                } catch (error) {
                    console.error('セッション詳細取得エラー:', error);
                    detailDiv.innerHTML = '<div class="loading">詳細の読み込みに失敗しました</div>';
                }
            }

            renderSessionDetail(container, session) {
                console.log('Rendering session detail:', session);
                console.log('Messages count:', session.messages.length);
                const messagesHtml = session.messages.map(message => {
                    const messageClass = message.type === 'user' ? 'message-user' : 'message-ai';
                    const typeLabel = message.type === 'user' ? 'あなた' : '蒼司';

                    let metadataHtml = '';
                    if (message.type === 'ai' && message.metadata) {
                        const meta = message.metadata;
                        metadataHtml = `
                            <div class="message-metadata">
                                ${meta.category ? `<div class="metadata-item"><strong>第3文カテゴリ:</strong> ${meta.category}</div>` : ''}
                                ${meta.emotion_analysis ? `
                                    <div class="metadata-item">
                                        <strong>感情分析:</strong>
                                        極性: ${meta.emotion_analysis.polarity},
                                        強度: ${meta.emotion_analysis.intensity},
                                        主要感情: ${meta.emotion_analysis.dominant_emotion}
                                    </div>
                                ` : ''}
                                ${meta.needs_analysis ? `
                                    <div class="metadata-item">
                                        <strong>ニーズ分析:</strong>
                                        ${Object.entries(meta.needs_analysis)
                                            .filter(([key, value]) => value > 0)
                                            .map(([key, value]) => `${key}: ${value}`)
                                            .join(', ')}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }

                    return `
                        <div class="message-item ${messageClass}">
                            <div class="message-content">
                                <strong>${typeLabel}:</strong> ${message.content}
                            </div>
                            <div class="message-timestamp">
                                ${this.formatDateTime(message.timestamp)}
                            </div>
                            ${metadataHtml}
                        </div>
                    `;
                }).join('');

                const finalHtml = `
                    <h4>会話詳細 (${session.message_count}件のメッセージ)</h4>
                    <div class="message-list">
                        ${messagesHtml}
                    </div>
                `;
                console.log('Final HTML:', finalHtml);
                container.innerHTML = finalHtml;
            }

            formatDateTime(isoString) {
                const date = new Date(isoString);
                return date.toLocaleString('ja-JP', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
            }
        }

        // グローバルインスタンス
        const chatHistory = new ChatHistoryViewer();
    </script>
</body>
</html>
    """

    return HTMLResponse(content=html_content)

# チャット履歴保存関数（他のサービスから呼び出し用）
def save_chat_interaction(
    session_id: str,
    user_message: str,
    ai_response: str,
    analysis_data: Dict[str, Any]
):
    """チャットのやり取りを一括保存"""
    # セッション継続判定
    if not session_id:
        # セッションIDが未指定の場合、アクティブセッションを検索
        active_session = chat_history_manager.get_active_session_id()
        if active_session:
            session_id = active_session
            print(f"継続セッションを使用: {session_id}")
        else:
            # 新しいセッションを作成
            from uuid import uuid4
            session_id = str(uuid4())[:8]
            print(f"新しいセッションを作成: {session_id}")

    # ユーザーメッセージを保存
    chat_history_manager.save_chat_message(
        session_id=session_id,
        message_type="user",
        content=user_message
    )

    # AI応答を分析データ付きで保存
    chat_history_manager.save_chat_message(
        session_id=session_id,
        message_type="ai",
        content=ai_response,
        metadata=analysis_data
    )

    return session_id