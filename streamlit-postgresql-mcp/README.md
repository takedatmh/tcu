# Streamlit PostgreSQL自然言語クエリアプリケーション

MCPサーバーを利用して、PostgreSQLに自然言語で問い合わせを行い、SQLに変換して実行するStreamlitアプリケーションです。

## 特徴

- 自然言語でPostgreSQLデータベースにクエリ可能
- MCPサーバー経由で安全にデータベース接続
- Groq API（無料）を使用したSQL生成
- コストゼロで運用可能

## 必要なもの

1. **PostgreSQL データベース** (以下のいずれか)
   - ローカルPostgreSQL
   - Supabase 無料プラン: https://supabase.com
   - ElephantSQL 無料プラン: https://www.elephantsql.com

2. **Groq API キー** (無料)
   - https://console.groq.com でアカウント作成
   - APIキーを取得

3. **Node.js** (MCPサーバー用)
   - バージョン 18 以上

## セットアップ

### 1. PostgreSQL MCPサーバーのセットアップ

```bash
cd mcp-server
npm install
npm run build
```

### 2. Streamlitアプリケーションのセットアップ

```bash
cd streamlit-app
pip install -r requirements.txt
```

### 3. 環境変数の設定

`.env`ファイルを作成:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. MCPサーバーの設定

Clineの設定ファイルにMCPサーバーを追加します（自動的に追加されます）。

### 5. アプリケーションの実行

```bash
cd streamlit-app
streamlit run app.py
```

## 使い方

1. アプリケーションを起動
2. データベース接続情報を入力（サイドバー）
3. 自然言語で質問を入力（例: "売上トップ10の商品を表示して"）
4. 自動的にSQLが生成され、実行結果が表示されます

## ディレクトリ構造

```
streamlit-postgresql-mcp/
├── README.md
├── mcp-server/           # PostgreSQL MCPサーバー
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       └── index.ts
└── streamlit-app/        # Streamlitアプリケーション
    ├── app.py
    ├── requirements.txt
    └── .env.example
```

## コスト

- PostgreSQL: $0 (Supabase無料プランまたはローカル)
- Groq API: $0 (無料プラン)
- Streamlit: $0 (ローカル実行)
- MCPサーバー: $0 (ローカル実行)

**総コスト: $0**

## 注意事項

- Groq無料プランには1日のリクエスト制限があります
- Supabase無料プランには500MBのストレージ制限があります
- 本番環境での使用には有料プランの検討をお勧めします
