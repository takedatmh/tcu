# 詳細セットアップガイド

このガイドでは、Streamlit PostgreSQL MCPアプリケーションをゼロから完全にセットアップする手順を説明します。

## 目次

1. [前提条件](#前提条件)
2. [PostgreSQLデータベースのセットアップ](#postgresqlデータベースのセットアップ)
3. [Groq APIキーの取得](#groq-apiキーの取得)
4. [アプリケーションのセットアップ](#アプリケーションのセットアップ)
5. [動作確認](#動作確認)
6. [トラブルシューティング](#トラブルシューティング)

## 前提条件

### 必要なソフトウェア

- **Node.js 18以上**
  - ダウンロード: https://nodejs.org/
  - インストール確認: `node -v`

- **Python 3.8以上**
  - ダウンロード: https://www.python.org/
  - インストール確認: `python3 --version`

- **PostgreSQL** (以下のいずれか)
  - ローカルPostgreSQL: https://www.postgresql.org/download/
  - Supabase無料プラン: https://supabase.com (推奨)
  - ElephantSQL無料プラン: https://www.elephantsql.com

## PostgreSQLデータベースのセットアップ

### オプション1: Supabase（推奨・最も簡単）

1. **Supabaseアカウント作成**
   - https://supabase.com にアクセス
   - "Start your project" をクリック
   - GitHubアカウントでサインアップ

2. **新しいプロジェクト作成**
   - "New project" をクリック
   - プロジェクト名、データベースパスワードを設定
   - リージョンを選択（Asia Northeast推奨）
   - "Create new project" をクリック

3. **接続情報を取得**
   - プロジェクトダッシュボードで "Settings" > "Database" を選択
   - 以下の情報をメモ:
     - Host: `db.xxxxxxxxxxxxx.supabase.co`
     - Port: `5432`
     - Database name: `postgres`
     - User: `postgres`
     - Password: 作成時に設定したパスワード

4. **サンプルデータの投入**
   - Supabaseダッシュボードで "SQL Editor" を選択
   - `sample_data.sql` の内容をコピー＆ペースト
   - "Run" をクリック

### オプション2: ローカルPostgreSQL

1. **PostgreSQLのインストール**
   ```bash
   # macOS (Homebrew)
   brew install postgresql@15
   brew services start postgresql@15
   
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   ```

2. **データベースとユーザーの作成**
   ```bash
   # postgresユーザーとして接続
   sudo -u postgres psql
   
   # データベースとユーザーを作成
   CREATE DATABASE testdb;
   CREATE USER testuser WITH PASSWORD 'testpassword';
   GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;
   \q
   ```

3. **サンプルデータの投入**
   ```bash
   psql -U testuser -d testdb -f sample_data.sql
   ```

## Groq APIキーの取得

1. **Groqアカウント作成**
   - https://console.groq.com にアクセス
   - "Sign Up" をクリック
   - メールアドレスで登録（Googleアカウントでも可）

2. **APIキーの生成**
   - ダッシュボードにログイン
   - 左メニューから "API Keys" を選択
   - "Create API Key" をクリック
   - キー名を入力（例: "streamlit-app"）
   - 生成されたAPIキーをコピー（後で確認できないので注意！）

3. **無料プランの制限**
   - 1日あたり14,400リクエスト
   - 1分あたり30リクエスト
   - 十分なクエリ数を実行可能

## アプリケーションのセットアップ

### 自動セットアップ（推奨）

```bash
cd streamlit-postgresql-mcp
chmod +x setup.sh
./setup.sh
```

### 手動セットアップ

#### 1. MCPサーバーのセットアップ

```bash
cd streamlit-postgresql-mcp/mcp-server

# 依存関係のインストール
npm install

# TypeScriptのコンパイル
npm run build

# ビルドの確認
ls -la build/index.js
```

#### 2. Streamlitアプリのセットアップ

```bash
cd ../streamlit-app

# 仮想環境の作成（推奨）
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存関係のインストール
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. 環境変数の設定

```bash
# .envファイルの作成
cp .env.example .env

# .envファイルを編集
nano .env  # または任意のエディタ
```

`.env` ファイルに以下を設定:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 動作確認

### 1. アプリケーションの起動

```bash
cd streamlit-postgresql-mcp/streamlit-app
source venv/bin/activate  # 仮想環境を使用している場合
streamlit run app.py
```

### 2. ブラウザでアクセス

- 自動的にブラウザが開きます
- または http://localhost:8501 にアクセス

### 3. データベース接続

1. サイドバーでデータベース接続情報を入力:
   - ホスト: Supabaseまたはローカルのホスト
   - ポート: `5432`
   - データベース名: `postgres`（Supabase）または `testdb`（ローカル）
   - ユーザー名: `postgres`または作成したユーザー名
   - パスワード: 設定したパスワード

2. "🔌 接続テスト" をクリック

3. "✅ 接続成功！" が表示されればOK

### 4. サンプルクエリの実行

以下のような自然言語クエリを試してください:

- "全てのテーブルを表示して"
- "顧客の一覧を表示"
- "売上トップ5の商品を表示"
- "東京の顧客を表示"
- "合計注文金額が50000円以上の注文を表示"

## トラブルシューティング

### Node.jsが見つからない

```bash
# Node.jsのインストール確認
node -v

# インストールされていない場合
# https://nodejs.org/ からダウンロードしてインストール
```

### MCPサーバーのビルドエラー

```bash
cd streamlit-postgresql-mcp/mcp-server

# node_modulesを削除して再インストール
rm -rf node_modules package-lock.json
npm install
npm run build
```

### PostgreSQL接続エラー

1. **接続情報の確認**
   - ホスト、ポート、データベース名が正しいか確認
   - パスワードが正しいか確認

2. **Supabaseの場合**
   - プロジェクトが起動しているか確認
   - IPアドレス制限がないか確認（Settings > Database > Connection Pooling）

3. **ローカルPostgreSQLの場合**
   ```bash
   # PostgreSQLが起動しているか確認
   brew services list  # macOS
   sudo systemctl status postgresql  # Linux
   
   # 接続テスト
   psql -U testuser -d testdb -h localhost
   ```

### Groq APIエラー

1. **APIキーの確認**
   ```bash
   # .envファイルの内容を確認
   cat streamlit-app/.env
   ```

2. **APIキーが有効か確認**
   - https://console.groq.com/keys でキーの状態を確認

3. **レート制限**
   - 1分に30リクエスト以上送信していないか確認
   - 少し時間をおいて再試行

### Pythonパッケージのインストールエラー

```bash
# pipを最新版にアップグレード
pip install --upgrade pip

# 特定のパッケージが問題の場合
pip install --upgrade <パッケージ名>

# 全て再インストール
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Streamlitが起動しない

```bash
# ポート8501が使用中か確認
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# 別のポートで起動
streamlit run app.py --server.port 8502
```

## 追加情報

### MCPサーバーのツール

このアプリケーションは以下のMCPツールを使用します:

1. **get_schema**: データベーススキーマ情報を取得
2. **execute_query**: SQLクエリを実行
3. **get_sample_data**: テーブルのサンプルデータを取得

### セキュリティのベストプラクティス

1. **環境変数の管理**
   - `.env` ファイルは絶対にGitにコミットしない
   - `.gitignore` に `.env` が含まれていることを確認

2. **データベースアクセス**
   - 本番環境では読み取り専用ユーザーを使用
   - 重要なデータには使用しない

3. **APIキー**
   - APIキーは定期的にローテーション
   - 不要になったキーは削除

## サポート

問題が解決しない場合:

1. エラーメッセージの全文をコピー
2. 使用している環境情報（OS、Node.jsバージョン、Pythonバージョン）を確認
3. GitHubのIssuesで質問

## ライセンス

MIT License
