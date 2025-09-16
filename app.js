// 占いチャットシステム - メインアプリケーション

class FortuneChat {
    constructor() {
        // システム状態
        this.rallyCount = 0;
        this.userData = this.initUserData();
        this.chatHistory = [];
        this.currentCharacter = 'psychic';
        
        // UI要素
        this.initializeElements();
        this.attachEventListeners();
        
        // システム初期化
        this.loadSystemConfigs();
        this.startRealtimeUpdates();
        
        console.log('占いチャットシステム初期化完了');
    }
    
    // ユーザーデータ初期化
    initUserData() {
        return {
            basic_info: {},
            psychology_emotion: {},
            love_relationships: {},
            work_career: {},
            spiritual_values: {},
            analysis_results: {
                resort_ti_scores: {
                    relationship: 0, emotion: 0, spirit: 0, occupation: 0,
                    romance: 0, time: 0, intelligence: 0, total: 0
                },
                detected_needs: {
                    complaining_listening: 0, emotion_organizing: 0,
                    recognition_desire: 0, encouragement: 0, loneliness: 0
                },
                emotional_analysis: { polarity: 0.0, intensity: 0.0, dominant_emotion: null },
                fortune_suggestion: { timing_score: 0, recommended_menu: null, confidence: 0 },
                data_completeness: {
                    basic_info: 0, psychology_emotion: 0, love_relationships: 0,
                    work_career: 0, spiritual_values: 0, total: 0
                }
            }
        };
    }
    
    // UI要素初期化
    initializeElements() {
        try {
            // ログ管理要素
        this.logControls = document.getElementById('logControls');
        this.downloadLogsBtn = document.getElementById('downloadLogsBtn');
        this.clearLogsBtn = document.getElementById('clearLogsBtn');
        this.toggleLogViewBtn = document.getElementById('toggleLogViewBtn');
        this.logViewer = document.getElementById('logViewer');
        this.logViewerContent = document.getElementById('logViewerContent');
        this.closeLogViewer = document.getElementById('closeLogViewer');
        this.logCount = document.getElementById('logCount');
        this.sessionIdDisplay = document.getElementById('sessionId');
        
        // 既存要素
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.fortuneSuggestions = document.getElementById('fortuneSuggestions');
        this.suggestionsContainer = document.getElementById('suggestionsContainer');
        this.fortuneModal = document.getElementById('fortuneModal');
        this.closeModal = document.getElementById('closeModal');
        
        // リアルタイム表示要素
        this.rallyCountElement = document.getElementById('rallyCount');
        this.iValueElement = document.getElementById('iValue');
        this.iValueBar = document.getElementById('iValueBar');
        
        // データ収集進捗要素
        this.basicInfoProgress = document.getElementById('basicInfoProgress');
        this.emotionProgress = document.getElementById('emotionProgress');
        this.loveProgress = document.getElementById('loveProgress');
        this.careerProgress = document.getElementById('careerProgress');
        this.spiritualProgress = document.getElementById('spiritualProgress');
        this.totalDataProgress = document.getElementById('totalDataProgress');
        
        // ニーズ表示要素
        this.complaintBar = document.getElementById('complaintBar');
        this.complaintScore = document.getElementById('complaintScore');
        this.emotionOrgBar = document.getElementById('emotionOrgBar');
        this.emotionOrgScore = document.getElementById('emotionOrgScore');
        this.recognitionBar = document.getElementById('recognitionBar');
        this.recognitionScore = document.getElementById('recognitionScore');
        this.encouragementBar = document.getElementById('encouragementBar');
        this.encouragementScore = document.getElementById('encouragementScore');
        this.lonelinessBar = document.getElementById('lonelinessBar');
        this.lonelinessScore = document.getElementById('lonelinessScore');
        
        // RESORT-TI要素
        this.relationshipScore = document.getElementById('relationshipScore');
        this.emotionScore = document.getElementById('emotionScore');
        this.spiritScore = document.getElementById('spiritScore');
        this.occupationScore = document.getElementById('occupationScore');
        this.romanceScore = document.getElementById('romanceScore');
        this.timeScore = document.getElementById('timeScore');
        this.intelligenceScore = document.getElementById('intelligenceScore');
        this.resortTotal = document.getElementById('resortTotal');
        
        // 感情分析要素
        this.emotionPolarity = document.getElementById('emotionPolarity');
        this.emotionIntensity = document.getElementById('emotionIntensity');
        this.dominantEmotion = document.getElementById('dominantEmotion');
        
        // 占いタイミング要素
        this.fortuneTimingScore = document.getElementById('fortuneTimingScore');
        this.fortuneTimingBar = document.getElementById('fortuneTimingBar');
        this.timingStatus = document.getElementById('timingStatus');
        
            // カテゴリ要素
            this.selectedCategory = document.getElementById('selectedCategory');
            this.categoryScore = document.getElementById('categoryScore');
            this.algorithmType = document.getElementById('algorithmType');

        } catch (error) {
            console.error('UI要素の初期化でエラーが発生しました:', error);
        }
    }
    
    // イベントリスナー設定
    attachEventListeners() {
        try {
            if (this.sendButton) {
                this.sendButton.addEventListener('click', () => this.sendMessage());
            } else {
                console.error('sendButton要素が見つかりません');
            }

            if (this.userInput) {
                this.userInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        this.sendMessage();
                    }
                });
            }

            if (this.closeModal) {
                this.closeModal.addEventListener('click', () => {
                    this.fortuneModal.style.display = 'none';
                });
            }

            window.addEventListener('click', (e) => {
                if (e.target === this.fortuneModal) {
                    this.fortuneModal.style.display = 'none';
                }
            });

            // ログ管理イベントリスナー
            if (this.downloadLogsBtn) this.downloadLogsBtn.addEventListener('click', () => this.downloadLogs());
            if (this.clearLogsBtn) this.clearLogsBtn.addEventListener('click', () => this.clearLogs());
            if (this.toggleLogViewBtn) this.toggleLogViewBtn.addEventListener('click', () => this.toggleLogViewer());
            if (this.closeLogViewer) this.closeLogViewer.addEventListener('click', () => this.hideLogViewer());

            // ログステータス更新
            this.updateLogStatus();
            setInterval(() => this.updateLogStatus(), 5000); // 5秒ごとに更新

        } catch (error) {
            console.error('イベントリスナー設定でエラーが発生しました:', error);
        }
    }
    
    // システム設定読み込み
    loadSystemConfigs() {
        // 実際の実装では、MDファイルから設定を読み込み
        this.needsDetectionConfig = {
            keywords: {
                complaining_listening: ["疲れた", "うんざり", "愚痴", "聞いて", "つらい", "ストレス"],
                emotion_organizing: ["混乱", "わからない", "整理", "考えがまとまらない", "どうしたらいい"],
                recognition_desire: ["認めて", "頑張った", "評価", "誉めて", "見て", "すごい"],
                encouragement: ["落ち込む", "自信ない", "不安", "心配", "怖い", "だめ"],
                loneliness: ["一人", "寂しい", "孤独", "理解者がいない", "話し相手", "味方がいない"]
            },
            weights: {
                complaining_listening: 0.8,
                emotion_organizing: 0.7,
                recognition_desire: 0.6,
                encouragement: 0.9,
                loneliness: 0.8
            }
        };
        
        this.categoryConfig = {
            categories: [
                { id: 1, name: "深い共感", trigger: "complaining_listening", weight: 0.9 },
                { id: 2, name: "優しい励まし", trigger: "encouragement", weight: 0.8 },
                { id: 3, name: "認めと賞賛", trigger: "recognition_desire", weight: 0.7 },
                { id: 4, name: "寄り添い", trigger: "loneliness", weight: 0.8 },
                { id: 5, name: "整理支援", trigger: "emotion_organizing", weight: 0.6 },
                { id: 12, name: "占い誘導", trigger: "fortune_timing", weight: 1.0 }
            ]
        };
        
        this.fortuneMenus = [
            {
                id: "honesty_reading",
                title: "相手の本音占い",
                description: "気になるあの人の本当の気持ちを占います",
                match_conditions: ["Romance値>50", "R値>60"]
            },
            {
                id: "love_compatibility", 
                title: "恋愛相性診断",
                description: "お二人の恋愛相性を詳しく分析します",
                match_conditions: ["Romance値>70"]
            },
            {
                id: "love_timing",
                title: "恋愛進展タイミング占い",
                description: "関係を進展させる最適なタイミングを占います",
                match_conditions: ["T値>65", "Romance値>60"]
            }
        ];
    }
    
    // メッセージ送信
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message) return;
        
        try {
            // ユーザーアクションログ
            this.logUserAction('send_message', { message: message.substring(0, 100) + '...' });
            
            // ユーザーメッセージ表示
            this.displayMessage(message, 'user');
            this.userInput.value = '';
            
            // ラリー回数増加
            this.rallyCount++;
            this.updateRallyCount();
            
            // メッセージ分析
            const analysis = await this.analyzeMessage(message);
            
            // AI応答生成
            const response = await this.generateResponse(message);
            
            // 応答表示
            this.displayMessage(response, 'bot');
            
            // チャット履歴保存
            this.chatHistory.push({
                turn: this.rallyCount,
                user_message: message,
                bot_response: response,
                timestamp: new Date().toISOString()
            });
            
            // チャット履歴ログ
            this.logChatMessage(message, response, analysis);
            
            // リアルタイム更新
            this.updateAllDisplays();
            
            // 占い提案チェック
            this.checkFortuneProposal();
            
        } catch (error) {
            console.error('メッセージ送信エラー:', error);
            this.logError(error, 'sendMessage');
            this.displayMessage('エラーが発生しました。もう一度お試しください。', 'bot');
        }
    }
    
    // メッセージ表示
    displayMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = message.replace(/\\n/g, '<br>');
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        // スクロール調整
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    // メッセージ分析
    async analyzeMessage(message) {
        // ニーズ検出
        this.detectNeeds(message);
        
        // 感情分析
        this.analyzeEmotion(message);
        
        // データ収集
        this.collectData(message);
        
        // RESORT-TI分析更新
        this.updateResortScores();
        
        // 分析結果を返す
        return {
            detectedNeeds: { ...this.userData.analysis_results.detected_needs },
            emotionalAnalysis: { ...this.userData.analysis_results.emotional_analysis },
            resortScores: { ...this.userData.analysis_results.resort_ti_scores },
            dataCompleteness: { ...this.userData.analysis_results.data_completeness }
        };
    }
    
    // ニーズ検出
    detectNeeds(message) {
        const needs = this.userData.analysis_results.detected_needs;
        
        Object.keys(this.needsDetectionConfig.keywords).forEach(needType => {
            const keywords = this.needsDetectionConfig.keywords[needType];
            const weight = this.needsDetectionConfig.weights[needType];
            
            let score = 0;
            keywords.forEach(keyword => {
                if (message.includes(keyword)) {
                    score += weight * 20; // 基本スコア20を重み付け
                }
            });
            
            // 既存スコアとの平均化
            needs[needType] = Math.min(100, (needs[needType] + score) / 2);
        });
    }
    
    // 感情分析
    analyzeEmotion(message) {
        const emotionalAnalysis = this.userData.analysis_results.emotional_analysis;
        
        // 簡単な感情極性分析
        const positiveWords = ["嬉しい", "楽しい", "幸せ", "良い", "素晴らしい", "最高"];
        const negativeWords = ["悲しい", "つらい", "苦しい", "嫌", "最悪", "ダメ"];
        
        let polarity = 0;
        let intensity = 0;
        
        positiveWords.forEach(word => {
            if (message.includes(word)) {
                polarity += 0.3;
                intensity += 0.2;
            }
        });
        
        negativeWords.forEach(word => {
            if (message.includes(word)) {
                polarity -= 0.3;
                intensity += 0.2;
            }
        });
        
        // 範囲制限
        emotionalAnalysis.polarity = Math.max(-1, Math.min(1, polarity));
        emotionalAnalysis.intensity = Math.max(0, Math.min(1, intensity));
        
        // 主要感情判定
        if (polarity > 0.5) emotionalAnalysis.dominant_emotion = "ポジティブ";
        else if (polarity < -0.5) emotionalAnalysis.dominant_emotion = "ネガティブ";
        else emotionalAnalysis.dominant_emotion = "ニュートラル";
    }
    
    // データ収集
    collectData(message) {
        const completeness = this.userData.analysis_results.data_completeness;
        
        // 基本情報の推測収集
        if (message.includes("歳") || message.includes("年")) {
            completeness.basic_info = Math.min(100, completeness.basic_info + 15);
        }
        
        if (message.includes("仕事") || message.includes("会社")) {
            completeness.work_career = Math.min(100, completeness.work_career + 20);
        }
        
        if (message.includes("恋人") || message.includes("好きな人") || message.includes("彼")) {
            completeness.love_relationships = Math.min(100, completeness.love_relationships + 25);
        }
        
        if (message.includes("占い") || message.includes("運命") || message.includes("スピリチュアル")) {
            completeness.spiritual_values = Math.min(100, completeness.spiritual_values + 20);
        }
        
        // 心理・感情データは常に更新
        completeness.psychology_emotion = Math.min(100, completeness.psychology_emotion + 10);
        
        // 総合データ完成度計算
        completeness.total = (
            completeness.basic_info + completeness.psychology_emotion +
            completeness.love_relationships + completeness.work_career +
            completeness.spiritual_values
        ) / 5;
    }
    
    // RESORT-TI分析更新
    updateResortScores() {
        const scores = this.userData.analysis_results.resort_ti_scores;
        const completeness = this.userData.analysis_results.data_completeness;
        const needs = this.userData.analysis_results.detected_needs;
        
        // 関係性(R)
        scores.relationship = Math.min(100, scores.relationship + needs.complaining_listening * 0.1);
        
        // 感情(E)
        scores.emotion = Math.min(100, scores.emotion + (needs.encouragement + needs.emotion_organizing) * 0.05);
        
        // 精神性(S)
        scores.spirit = Math.min(100, scores.spirit + completeness.spiritual_values * 0.3);
        
        // 職業(O)
        scores.occupation = Math.min(100, scores.occupation + completeness.work_career * 0.2);
        
        // 恋愛(Romance)
        scores.romance = Math.min(100, scores.romance + completeness.love_relationships * 0.3);
        
        // 時間(T)
        scores.time = Math.min(100, scores.time + this.rallyCount * 2);
        
        // 知性(I)
        scores.intelligence = Math.min(100, scores.intelligence + completeness.total * 0.2);
        
        // 総合スコア
        scores.total = Math.round((scores.relationship + scores.emotion + scores.spirit + 
                                 scores.occupation + scores.romance + scores.time + scores.intelligence) / 7);
    }
    
    // AI応答生成
    async generateResponse(message) {
        try {
            // AIバックエンドAPI呼び出し
            const requestData = {
                message: message,
                user_data: this.userData,
                chat_history: this.chatHistory.slice(-5), // 最新5件の履歴
                rally_count: this.rallyCount
            };

            const response = await fetch('http://127.0.0.1:8011/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (response.ok) {
                const data = await response.json();
                
                // AI分析結果をユーザーデータに反映
                if (data.needs_analysis) {
                    Object.assign(this.userData.analysis_results.detected_needs, data.needs_analysis);
                }
                
                if (data.emotion_analysis) {
                    Object.assign(this.userData.analysis_results.emotional_analysis, data.emotion_analysis);
                }
                
                if (data.resort_scores) {
                    Object.assign(this.userData.analysis_results.resort_ti_scores, data.resort_scores);
                    // 総合スコア計算
                    const total = Object.values(data.resort_scores).reduce((sum, val) => sum + val, 0) / 7;
                    this.userData.analysis_results.resort_ti_scores.total = Math.round(total);
                }
                
                if (data.fortune_timing_score !== undefined) {
                    this.userData.analysis_results.fortune_suggestion.timing_score = data.fortune_timing_score;
                }
                
                // カテゴリ情報更新
                if (data.category) {
                    this.updateCategoryDisplay({
                        id: this.getCategoryIdFromName(data.category),
                        name: data.category,
                        score: 90 // AI分析による高スコア
                    });
                }
                
                // 占い提案があれば表示
                if (data.suggested_fortune) {
                    this.showAIFortuneSuggestion(data.suggested_fortune);
                }
                
                return data.response;
            } else {
                throw new Error('API応答エラー');
            }
        } catch (error) {
            console.warn('AI API呼び出しエラー、フォールバック応答に切り替え:', error);
            return this.generateFallbackResponse(message);
        }
    }
    
    // フォールバック応答生成（AI API失敗時）
    generateFallbackResponse(message) {
        // 第3文カテゴリ選択
        const selectedCategory = this.selectThirdSentenceCategory();
        
        // 既存の静的応答
        const responses = {
            1: [ // 深い共感
                "その気持ち、本当によくわかります。とてもつらい状況ですね...",
                "心の奥の痛みが私にも伝わってきます。一人で抱え込まれていたんですね。",
                "その重さを感じています。よく今まで頑張ってこられましたね。"
            ],
            2: [ // 優しい励まし
                "大丈夫です。あなたには必ず道が開けます。その優しい心を信じてください。",
                "きっと素晴らしい未来が待っています。今の困難は成長のための試練なのです。",
                "あなたの中にある光が見えます。その強さを信じて前に進んでください。"
            ],
            3: [ // 認めと賞賛
                "よく頑張られましたね。その努力は必ず報われます。",
                "素晴らしい行動力ですね。あなたの価値をしっかりと感じています。",
                "その積極性、とても素敵です。自分を誇りに思ってください。"
            ],
            4: [ // 寄り添い
                "一人じゃありませんよ。私がいつでもあなたのお話を聞いています。",
                "あなたの味方です。どんな時でもあなたを見守っています。",
                "心の支えになりたいと思っています。安心してお話しください。"
            ],
            5: [ // 整理支援
                "一緒に整理してみましょうか。どの部分が一番気になりますか？",
                "順番に考えてみましょう。まず、何が最も大切でしょうか？",
                "心の中を整理するお手伝いをさせてください。"
            ]
        };
        
        // ランダムに応答を選択
        const categoryResponses = responses[selectedCategory.id] || responses[1];
        const response = categoryResponses[Math.floor(Math.random() * categoryResponses.length)];
        
        // カテゴリ情報更新
        this.updateCategoryDisplay(selectedCategory);
        
        return response;
    }
    
    // カテゴリ名からIDを取得
    getCategoryIdFromName(categoryName) {
        const categoryMap = {
            "深い共感": 1,
            "優しい励まし": 2,
            "認めと賞賛": 3,
            "寄り添い": 4,
            "整理支援": 5,
            "占い誘導": 12
        };
        return categoryMap[categoryName] || 1;
    }
    
    // AI占い提案表示
    showAIFortuneSuggestion(fortuneType) {
        const suggestionDiv = document.createElement('div');
        suggestionDiv.className = 'suggestion-item ai-suggested';
        suggestionDiv.innerHTML = `
            <h4>🤖 AIが提案: ${fortuneType}</h4>
            <p>あなたの状況を分析した結果、この占いがおすすめです</p>
            <span class="match-score ai-match">AI分析: 95%</span>
        `;
        
        suggestionDiv.addEventListener('click', () => {
            this.executeAIFortune(fortuneType);
        });
        
        // 占い提案エリアを表示
        this.suggestionsContainer.innerHTML = '';
        this.suggestionsContainer.appendChild(suggestionDiv);
        this.fortuneSuggestions.style.display = 'block';
    }
    
    // 第3文カテゴリ選択
    selectThirdSentenceCategory() {
        const needs = this.userData.analysis_results.detected_needs;
        let bestCategory = { id: 1, name: "深い共感", score: 0 };
        
        this.categoryConfig.categories.forEach(category => {
            let score = 0;
            
            if (category.trigger === "complaining_listening") {
                score = needs.complaining_listening * category.weight;
            } else if (category.trigger === "encouragement") {
                score = needs.encouragement * category.weight;
            } else if (category.trigger === "recognition_desire") {
                score = needs.recognition_desire * category.weight;
            } else if (category.trigger === "loneliness") {
                score = needs.loneliness * category.weight;
            } else if (category.trigger === "emotion_organizing") {
                score = needs.emotion_organizing * category.weight;
            }
            
            if (score > bestCategory.score) {
                bestCategory = { id: category.id, name: category.name, score: score };
            }
        });
        
        return bestCategory;
    }
    
    // 占い提案チェック
    checkFortuneProposal() {
        const timingScore = this.calculateFortuneTimingScore();
        this.userData.analysis_results.fortune_suggestion.timing_score = timingScore;
        
        if (timingScore >= 70) {
            this.showFortuneSuggestions();
        }
    }
    
    // 占い提案タイミングスコア計算
    calculateFortuneTimingScore() {
        const resortTotal = this.userData.analysis_results.resort_ti_scores.total;
        const dataCompleteness = this.userData.analysis_results.data_completeness.total;
        const needsClarity = Math.max(...Object.values(this.userData.analysis_results.detected_needs));
        
        const score = (resortTotal * 0.4) + (dataCompleteness * 0.3) + (needsClarity * 0.3);
        return Math.round(score);
    }
    
    // 占い提案表示
    showFortuneSuggestions() {
        const recommendations = this.recommendFortuneMenus();
        
        this.suggestionsContainer.innerHTML = '';
        
        recommendations.slice(0, 3).forEach(menu => {
            const suggestionDiv = document.createElement('div');
            suggestionDiv.className = 'suggestion-item';
            suggestionDiv.innerHTML = `
                <h4>🔮 ${menu.title}</h4>
                <p>${menu.description}</p>
                <span class="match-score">マッチング度: ${menu.matchScore}%</span>
            `;
            
            suggestionDiv.addEventListener('click', () => {
                this.executeFortune(menu.id);
            });
            
            this.suggestionsContainer.appendChild(suggestionDiv);
        });
        
        this.fortuneSuggestions.style.display = 'block';
    }
    
    // 占いメニュー推奨
    recommendFortuneMenus() {
        const resortScores = this.userData.analysis_results.resort_ti_scores;
        const needs = this.userData.analysis_results.detected_needs;
        
        return this.fortuneMenus.map(menu => {
            let matchScore = 50; // ベーススコア
            
            // メニューごとのマッチング計算
            if (menu.id === "honesty_reading") {
                matchScore += (resortScores.romance * 0.3) + (resortScores.relationship * 0.3);
            } else if (menu.id === "love_compatibility") {
                matchScore += (resortScores.romance * 0.4) + (resortScores.spirit * 0.2);
            } else if (menu.id === "love_timing") {
                matchScore += (resortScores.time * 0.4) + (resortScores.romance * 0.3);
            }
            
            return {
                ...menu,
                matchScore: Math.min(100, Math.round(matchScore))
            };
        }).sort((a, b) => b.matchScore - a.matchScore);
    }
    
    // AI占い実行
    async executeAIFortune(fortuneType) {
        try {
            const requestData = {
                fortune_type: fortuneType,
                user_data: this.userData,
                specific_context: `${fortuneType}について詳しく占ってください`
            };

            const response = await fetch('http://127.0.0.1:8011/api/fortune', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (response.ok) {
                const data = await response.json();
                this.displayFortuneResult({
                    title: `${fortuneType} - AI占い結果`,
                    content: data.fortune_result,
                    keyPoints: ["AI分析による洞察", "霊能力で見えたビジョン", "具体的なアドバイス"],
                    advice: "AIが分析した結果に基づいています"
                });
            } else {
                throw new Error('AI占いAPI呼び出しエラー');
            }
        } catch (error) {
            console.warn('AI占い実行エラー、フォールバック占いに切り替え:', error);
            // 既存の静的占いにフォールバック
            const fortuneId = this.getFortuneIdFromType(fortuneType);
            this.executeFortune(fortuneId);
        }
    }
    
    // 占い名からIDを取得
    getFortuneIdFromType(fortuneType) {
        const typeMap = {
            "相手の本音占い": "honesty_reading",
            "恋愛相性診断": "love_compatibility",
            "恋愛進展タイミング": "love_timing",
            "運命の相手探し": "soulmate_search",
            "復縁可能性診断": "reconciliation",
            "人間関係修復": "relationship_repair",
            "総合運勢・人生指針": "life_guidance"
        };
        return typeMap[fortuneType] || "honesty_reading";
    }
    
    // 占い実行（フォールバック用）
    executeFortune(fortuneId) {
        const fortuneResults = {
            "honesty_reading": {
                title: "相手の本音占い結果",
                content: "霊視の結果をお伝えします。あの人はあなたに対して、表面的には見せていない深い関心を抱いています。普段はクールに振る舞っていますが、心の奥では特別な存在として感じています。",
                keyPoints: [
                    "相手はあなたを特別視している",
                    "照れ隠しで素っ気ない態度を取っている", 
                    "今後アプローチのチャンスがある"
                ],
                advice: "相手からの小さなサインを見逃さないでください。直感を信じて行動することで、良い変化が訪れるでしょう。"
            },
            "love_compatibility": {
                title: "恋愛相性診断結果", 
                content: "お二人の相性を詳しく占わせていただきました。総合的な相性は89%と非常に高い数値を示しています。特に精神的な繋がりが深く、お互いを成長させる関係性です。",
                keyPoints: [
                    "価値観の高い一致度",
                    "お互いを高め合える関係",
                    "深い精神的な結びつき"
                ],
                advice: "この相性の良さを大切にして、お互いの個性を尊重しながら関係を深めていってください。"
            },
            "love_timing": {
                title: "恋愛進展タイミング占い結果",
                content: "星の配置から見ると、今月下旬から来月上旬にかけて、恋愛運が最高潮に達します。特に自然な流れでの関係進展に絶好のタイミングです。",
                keyPoints: [
                    "今月23日頃がベストタイミング",
                    "自然な流れでのアプローチが効果的",
                    "成功確率85%の高い数値"
                ],
                advice: "焦らず、でも確実にチャンスを掴んでください。あなたの直感を信じることが成功の鍵です。"
            }
        };
        
        const result = fortuneResults[fortuneId];
        if (result) {
            this.displayFortuneResult(result);
        }
    }
    
    // 占い結果表示
    displayFortuneResult(result) {
        const resultHTML = `
            <h2>${result.title}</h2>
            <div class="content">
                <p>${result.content}</p>
            </div>
            <div class="key-points">
                <h4>📍 重要なポイント</h4>
                <ul>
                    ${result.keyPoints.map(point => `<li>${point}</li>`).join('')}
                </ul>
            </div>
            <div class="advice">
                <h4>💡 アドバイス</h4>
                <p>${result.advice}</p>
            </div>
        `;
        
        document.getElementById('fortuneResult').innerHTML = resultHTML;
        this.fortuneModal.style.display = 'block';
    }
    
    // すべての表示を更新
    updateAllDisplays() {
        try {
            this.updateDataProgress();
            this.updateNeedsDisplay();
            this.updateResortDisplay();
            this.updateEmotionDisplay();
            this.updateFortuneTimingDisplay();
        } catch (error) {
            console.error('Display update error (prevented):', error);
            // エラーを無視して続行
        }
    }
    
    // ラリー回数更新
    updateRallyCount() {
        if (this.rallyCountElement) this.rallyCountElement.textContent = this.rallyCount;
    }
    
    // データ進捗更新
    updateDataProgress() {
        const completeness = this.userData.analysis_results.data_completeness;

        // DOM要素の存在確認
        if (this.basicInfoProgress) this.basicInfoProgress.textContent = `${Math.round(completeness.basic_info)}%`;
        if (this.emotionProgress) this.emotionProgress.textContent = `${Math.round(completeness.psychology_emotion)}%`;
        if (this.loveProgress) this.loveProgress.textContent = `${Math.round(completeness.love_relationships)}%`;
        if (this.careerProgress) this.careerProgress.textContent = `${Math.round(completeness.work_career)}%`;
        if (this.spiritualProgress) this.spiritualProgress.textContent = `${Math.round(completeness.spiritual_values)}%`;
        if (this.totalDataProgress) this.totalDataProgress.textContent = `${Math.round(completeness.total)}%`;
    }
    
    // ニーズ表示更新
    updateNeedsDisplay() {
        const needs = this.userData.analysis_results.detected_needs;
        
        this.updateNeedBar(this.complaintBar, this.complaintScore, needs.complaining_listening);
        this.updateNeedBar(this.emotionOrgBar, this.emotionOrgScore, needs.emotion_organizing);
        this.updateNeedBar(this.recognitionBar, this.recognitionScore, needs.recognition_desire);
        this.updateNeedBar(this.encouragementBar, this.encouragementScore, needs.encouragement);
        this.updateNeedBar(this.lonelinessBar, this.lonelinessScore, needs.loneliness);
    }
    
    // 個別ニーズバー更新
    updateNeedBar(barElement, scoreElement, value) {
        const percentage = Math.round(value);
        if (barElement) barElement.style.width = `${percentage}%`;
        if (scoreElement) scoreElement.textContent = `${percentage}%`;
    }
    
    // RESORT表示更新
    updateResortDisplay() {
        const scores = this.userData.analysis_results.resort_ti_scores;

        // DOM要素の存在確認
        if (this.relationshipScore) this.relationshipScore.textContent = Math.round(scores.relationship);
        if (this.emotionScore) this.emotionScore.textContent = Math.round(scores.emotion);
        if (this.spiritScore) this.spiritScore.textContent = Math.round(scores.spirit);
        if (this.occupationScore) this.occupationScore.textContent = Math.round(scores.occupation);
        if (this.romanceScore) this.romanceScore.textContent = Math.round(scores.romance);
        if (this.timeScore) this.timeScore.textContent = Math.round(scores.time);
        if (this.intelligenceScore) this.intelligenceScore.textContent = Math.round(scores.intelligence);
        if (this.resortTotal) this.resortTotal.textContent = Math.round(scores.total);

        // I値更新
        if (this.iValue) this.iValue.textContent = Math.round(scores.intelligence);
        if (this.iValueBar) this.iValueBar.style.width = `${scores.intelligence}%`;
    }
    
    // 感情分析表示更新
    updateEmotionDisplay() {
        const emotion = this.userData.analysis_results.emotional_analysis;

        // DOM要素の存在確認
        if (this.emotionPolarity) this.emotionPolarity.textContent = emotion.polarity.toFixed(2);
        if (this.emotionIntensity) this.emotionIntensity.textContent = emotion.intensity.toFixed(2);
        if (this.dominantEmotion) this.dominantEmotion.textContent = emotion.dominant_emotion || '-';
    }
    
    // 占いタイミング表示更新
    updateFortuneTimingDisplay() {
        const timingScore = this.userData.analysis_results.fortune_suggestion.timing_score;

        // DOM要素の存在確認
        if (this.fortuneTimingScore) this.fortuneTimingScore.textContent = timingScore;
        if (this.fortuneTimingBar) this.fortuneTimingBar.style.width = `${timingScore}%`;

        if (this.timingStatus) {
            if (timingScore >= 70) {
                this.timingStatus.textContent = '提案準備完了';
                this.timingStatus.className = 'timing-status ready';
            } else if (timingScore >= 50) {
                this.timingStatus.textContent = 'もう少し';
                this.timingStatus.className = 'timing-status';
            } else {
                this.timingStatus.textContent = '準備中';
                this.timingStatus.className = 'timing-status';
            }
        }
    }
    
    // カテゴリ表示更新
    updateCategoryDisplay(category) {
        if (this.selectedCategory) this.selectedCategory.textContent = category.name;
        if (this.categoryScore) this.categoryScore.textContent = `${Math.round(category.score)}%`;
    }
    
    // リアルタイム更新開始
    startRealtimeUpdates() {
        // リアルタイム更新を一時的に無効化（エラー回避のため）
        // setInterval(() => {
        //     this.updateAllDisplays();
        // }, 1000);
        console.log('リアルタイム更新は一時停止中です');
    }
    
    // ログ保存機能
    saveLog(type, data) {
        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            type,
            data,
            rallyCount: this.rallyCount,
            userData: this.userData,
            sessionId: this.getSessionId()
        };
        
        // localStorageに保存
        this.saveToLocalStorage(logEntry);
        
        // コンソールにも出力
        console.log(`[${timestamp}] ${type}:`, data);
        
        // バックエンドにも送信（オプション）
        this.sendLogToBackend(logEntry);
    }
    
    // セッションID取得・生成
    getSessionId() {
        let sessionId = localStorage.getItem('fortuneChat_sessionId');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('fortuneChat_sessionId', sessionId);
        }
        return sessionId;
    }
    
    // localStorageに保存
    saveToLocalStorage(logEntry) {
        try {
            const logs = JSON.parse(localStorage.getItem('fortuneChat_logs') || '[]');
            logs.push(logEntry);
            
            // 最新100件のみ保持
            if (logs.length > 100) {
                logs.splice(0, logs.length - 100);
            }
            
            localStorage.setItem('fortuneChat_logs', JSON.stringify(logs));
        } catch (error) {
            console.error('ログ保存エラー:', error);
        }
    }
    
    // バックエンドにログ送信
    async sendLogToBackend(logEntry) {
        try {
            await fetch('http://127.0.0.1:8011/api/log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(logEntry)
            });
        } catch (error) {
            console.warn('バックエンドログ送信失敗:', error);
        }
    }
    
    // ログダウンロード機能
    downloadLogs() {
        try {
            const logs = JSON.parse(localStorage.getItem('fortuneChat_logs') || '[]');
            const dataStr = JSON.stringify(logs, null, 2);
            const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
            
            const exportFileDefaultName = `fortuneChat_logs_${new Date().toISOString().split('T')[0]}.json`;
            
            const linkElement = document.createElement('a');
            linkElement.setAttribute('href', dataUri);
            linkElement.setAttribute('download', exportFileDefaultName);
            linkElement.click();
        } catch (error) {
            console.error('ログダウンロードエラー:', error);
        }
    }
    
    // チャット履歴ログ
    logChatMessage(userMessage, botResponse, analysis) {
        this.saveLog('chat_message', {
            userMessage,
            botResponse,
            analysis,
            rallyCount: this.rallyCount
        });
    }
    
    // ユーザーアクションログ
    logUserAction(action, details) {
        this.saveLog('user_action', {
            action,
            details
        });
    }
    
    // システムエラー ログ
    logError(error, context) {
        this.saveLog('error', {
            error: error.toString(),
            stack: error.stack,
            context
        });
    }
    
    // ログクリア
    clearLogs() {
        if (confirm('全てのログを削除しますか？この操作は取り消せません。')) {
            localStorage.removeItem('fortuneChat_logs');
            this.updateLogStatus();
            this.hideLogViewer();
            alert('ログをクリアしました。');
        }
    }
    
    // ログビューアー表示切替
    toggleLogViewer() {
        if (this.logViewer.style.display === 'none' || !this.logViewer.style.display) {
            this.showLogViewer();
        } else {
            this.hideLogViewer();
        }
    }
    
    // ログビューアー表示
    showLogViewer() {
        this.logViewer.style.display = 'flex';
        this.refreshLogViewer();
    }
    
    // ログビューアー非表示
    hideLogViewer() {
        this.logViewer.style.display = 'none';
    }
    
    // ログビューアー内容更新
    refreshLogViewer() {
        try {
            const logs = JSON.parse(localStorage.getItem('fortuneChat_logs') || '[]');
            
            if (logs.length === 0) {
                this.logViewerContent.innerHTML = '<p style="text-align: center; color: #a0aec0;">ログが見つかりません</p>';
                return;
            }
            
            // 最新のログから表示
            const recentLogs = logs.slice(-20).reverse();
            
            this.logViewerContent.innerHTML = recentLogs.map(log => {
                return `
                    <div class="log-entry ${log.type}">
                        <div class="log-entry-header">
                            <span class="log-type">${this.getLogTypeLabel(log.type)}</span>
                            <span class="log-timestamp">${this.formatTimestamp(log.timestamp)}</span>
                        </div>
                        <div class="log-data">${this.formatLogData(log.data)}</div>
                    </div>
                `;
            }).join('');
        } catch (error) {
            this.logViewerContent.innerHTML = '<p style="color: red;">ログの読み込みに失敗しました</p>';
        }
    }
    
    // ログタイプのラベル取得
    getLogTypeLabel(type) {
        const labels = {
            chat_message: '💬 チャットメッセージ',
            user_action: '👤 ユーザーアクション',
            error: '❌ エラー'
        };
        return labels[type] || type;
    }
    
    // タイムスタンプ フォーマット
    formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('ja-JP', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    
    // ログデータフォーマット
    formatLogData(data) {
        if (typeof data === 'object') {
            return JSON.stringify(data, null, 2);
        }
        return String(data);
    }
    
    // ログステータス更新
    updateLogStatus() {
        try {
            const logs = JSON.parse(localStorage.getItem('fortuneChat_logs') || '[]');
            this.logCount.textContent = logs.length;
            this.sessionIdDisplay.textContent = this.getSessionId().substring(0, 12) + '...';
        } catch (error) {
            this.logCount.textContent = '0';
            this.sessionIdDisplay.textContent = 'エラー';
        }
    }
}

// アプリケーション初期化
document.addEventListener('DOMContentLoaded', () => {
    window.fortuneChat = new FortuneChat();
});