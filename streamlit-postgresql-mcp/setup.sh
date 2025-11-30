#!/bin/bash

# Streamlit PostgreSQL MCP アプリケーション セットアップスクリプト

set -e

echo "🚀 Streamlit PostgreSQL MCP アプリケーションのセットアップを開始します..."

# 色の定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Node.jsのバージョンチェック
echo -e "\n${YELLOW}📦 Node.jsのバージョンを確認中...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✓ Node.js ${NODE_VERSION} が見つかりました${NC}"
else
    echo -e "${RED}✗ Node.jsがインストールされていません${NC}"
    echo "Node.js 18以上をインストールしてください: https://nodejs.org/"
    exit 1
fi

# Python 3のバージョンチェック
echo -e "\n${YELLOW}🐍 Python 3のバージョンを確認中...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ ${PYTHON_VERSION} が見つかりました${NC}"
else
    echo -e "${RED}✗ Python 3がインストールされていません${NC}"
    exit 1
fi

# MCPサーバーのセットアップ
echo -e "\n${YELLOW}🔧 MCPサーバーのセットアップ中...${NC}"
cd mcp-server

if [ ! -d "node_modules" ]; then
    echo "npm install を実行中..."
    npm install
else
    echo -e "${GREEN}✓ node_modules は既に存在します${NC}"
fi

echo "TypeScriptをコンパイル中..."
npm run build

if [ -f "build/index.js" ]; then
    echo -e "${GREEN}✓ MCPサーバーのビルドが完了しました${NC}"
else
    echo -e "${RED}✗ MCPサーバーのビルドに失敗しました${NC}"
    exit 1
fi

cd ..

# Streamlitアプリのセットアップ
echo -e "\n${YELLOW}🎨 Streamlitアプリケーションのセットアップ中...${NC}"
cd streamlit-app

# 仮想環境の作成（オプション）
if [ ! -d "venv" ]; then
    echo "Python仮想環境を作成中..."
    python3 -m venv venv
fi

echo "仮想環境をアクティベート中..."
source venv/bin/activate

echo "Pythonパッケージをインストール中..."
pip install --upgrade pip
pip install -r requirements.txt

# .envファイルのチェック
if [ ! -f ".env" ]; then
    echo -e "\n${YELLOW}⚠️  .envファイルが見つかりません${NC}"
    echo ".env.exampleを.envにコピーしています..."
    cp .env.example .env
    echo -e "${YELLOW}📝 .envファイルを編集してGroq APIキーを設定してください${NC}"
fi

cd ..

# 完了メッセージ
echo -e "\n${GREEN}✅ セットアップが完了しました！${NC}"
echo -e "\n📖 次のステップ:"
echo -e "  1. Groq APIキーを取得: ${YELLOW}https://console.groq.com${NC}"
echo -e "  2. streamlit-app/.env ファイルにAPIキーを設定"
echo -e "  3. PostgreSQLデータベースを準備（ローカルまたはSupabase）"
echo -e "  4. アプリケーションを起動:"
echo -e "     ${GREEN}cd streamlit-app${NC}"
echo -e "     ${GREEN}source venv/bin/activate${NC}"
echo -e "     ${GREEN}streamlit run app.py${NC}"
echo ""
