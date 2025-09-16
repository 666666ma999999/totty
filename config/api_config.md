# API設定ファイル

## 設定済みAPI KEY

### OpenAI API
- **サービス**: ChatGPT-4o
- **用途**: メイン応答生成、分析処理
- **環境変数**: OPENAI_API_KEY
- **設定状況**: ✅ 設定済み

### Anthropic API  
- **サービス**: Claude Sonnet
- **用途**: バックアップ応答、複雑な分析
- **環境変数**: ANTHROPIC_API_KEY  
- **設定状況**: ✅ 設定済み

## API統合実装計画

### 現在の状況
- **フロントエンド**: 完成（静的応答）
- **バックエンド**: 未実装
- **API統合**: 未実装

### 統合手順（将来実装）

#### 1. バックエンドAPI作成
```python
# FastAPI実装例
from fastapi import FastAPI
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat_endpoint(message: str):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content
```

#### 2. フロントエンド改修
```javascript
// app.js内のgenerateResponse関数を改修
async generateResponse(message) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        const data = await response.json();
        return data.response;
    } catch (error) {
        // フォールバック: 既存の静的応答
        return this.generateStaticResponse(message);
    }
}
```

#### 3. キャラクター応答の統合
```python
# システムプロンプト例
PSYCHIC_SYSTEM_PROMPT = """
あなたは蒼司という名前のイケメン霊能師です。
- 優しく包容力のある話し方
- 神秘的で洞察力のある応答
- 相談者の心に寄り添う共感的な対応
- 適切なタイミングでの占い提案
"""
```

## セキュリティ設定

### API KEY保護
- ✅ .envファイルに格納
- ✅ .gitignoreに.env追加済み
- ❌ サーバーサイド実装（要実装）

### 推奨セキュリティ対策
- API KEYをフロントエンドに露出させない
- CORS設定でドメイン制限
- レート制限の実装
- API使用量監視

## 使用量管理

### OpenAI API制限
- **トークン制限**: プロジェクト毎の上限確認
- **レート制限**: 1分間のリクエスト数制限
- **コスト管理**: 使用量アラート設定推奨

### 最適化戦略
- キャッシュ機能（同一質問の応答保存）
- トークン数削減（簡潔なプロンプト）
- フォールバック機能（API障害時の静的応答）

## 実装優先度

### Phase 1 (高優先度)
- [ ] FastAPI バックエンド構築
- [ ] OpenAI API統合
- [ ] 基本的なチャット応答

### Phase 2 (中優先度)  
- [ ] RESORT-TI分析のAI化
- [ ] ニーズ検出精度向上
- [ ] 占い結果の動的生成

### Phase 3 (低優先度)
- [ ] Claude API統合（バックアップ）
- [ ] 多言語対応
- [ ] 高度な感情分析

## 設定確認コマンド

```bash
# API KEY確認
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# 設定ファイル確認
cat .env
```

**⚠️ 注意**: API KEYは機密情報です。外部に共有しないでください。