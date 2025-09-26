# Python 3.11ベースイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# システムパッケージを更新し、必要な依存関係をインストール
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーし、Python依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# ポート8011を露出
EXPOSE 8011

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8011/ || exit 1

# 統合サーバーを起動
CMD ["python3", "backend/main_integrated.py"]