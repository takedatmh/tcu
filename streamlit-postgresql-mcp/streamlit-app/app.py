import streamlit as st
import json
import os
from groq import Groq
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
from contextlib import asynccontextmanager

# ページ設定
st.set_page_config(
    page_title="PostgreSQL 自然言語クエリ",
    page_icon="🗄️",
    layout="wide"
)

# セッション状態の初期化
if 'mcp_session' not in st.session_state:
    st.session_state.mcp_session = None
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'schema_info' not in st.session_state:
    st.session_state.schema_info = None

# Groqクライアントの初期化
@st.cache_resource
def get_groq_client():
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        st.error("GROQ_API_KEY環境変数が設定されていません")
        return None
    return Groq(api_key=api_key)

# MCPサーバーへの接続
@asynccontextmanager
async def get_mcp_session(db_config):
    """MCPサーバーセッションを作成"""
    server_params = StdioServerParameters(
        command="node",
        args=[os.path.join(os.path.dirname(__file__), "..", "mcp-server", "build", "index.js")],
        env={
            "POSTGRES_HOST": db_config['host'],
            "POSTGRES_PORT": str(db_config['port']),
            "POSTGRES_DB": db_config['database'],
            "POSTGRES_USER": db_config['user'],
            "POSTGRES_PASSWORD": db_config['password'],
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

# スキーマ情報の取得
async def get_database_schema(session):
    """データベースのスキーマ情報を取得"""
    try:
        result = await session.call_tool("get_schema", {})
        schema_data = json.loads(result.content[0].text)
        return schema_data
    except Exception as e:
        st.error(f"スキーマ取得エラー: {str(e)}")
        return None

# SQLクエリの実行
async def execute_sql_query(session, sql):
    """SQLクエリを実行"""
    try:
        result = await session.call_tool("execute_query", {"sql": sql})
        return json.loads(result.content[0].text)
    except Exception as e:
        return {"error": str(e)}

# 自然言語からSQLへの変換
def natural_language_to_sql(client, nl_query, schema_info):
    """自然言語をSQLに変換"""
    # スキーマ情報を整形
    schema_text = "データベーススキーマ:\n"
    if schema_info and 'tables' in schema_info:
        for table in schema_info['tables']:
            schema_text += f"- {table['table_name']}\n"
    
    prompt = f"""あなたはPostgreSQLのエキスパートです。以下のデータベーススキーマに基づいて、ユーザーの自然言語クエリをSQLに変換してください。

{schema_text}

ユーザーの質問: {nl_query}

要件:
1. PostgreSQL互換のSQLを生成してください
2. SELECTクエリのみを生成してください（UPDATE、DELETE、DROPなどは禁止）
3. SQLのみを返してください（説明文は不要）
4. クエリは1つだけ生成してください

SQL:"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "あなたはPostgreSQLのエキスパートです。自然言語をSQLに変換します。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",  # Groqの無料モデル
            temperature=0.1,
            max_tokens=500,
        )
        
        sql = chat_completion.choices[0].message.content.strip()
        # コードブロックのマークダウンを削除
        sql = sql.replace("```sql", "").replace("```", "").strip()
        return sql
    except Exception as e:
        st.error(f"SQL生成エラー: {str(e)}")
        return None

# メインアプリケーション
def main():
    st.title("🗄️ PostgreSQL 自然言語クエリアプリ")
    st.markdown("MCPサーバーを利用してPostgreSQLに自然言語でクエリを実行")
    
    # サイドバー - データベース接続設定
    with st.sidebar:
        st.header("⚙️ データベース設定")
        
        db_host = st.text_input("ホスト", value="localhost")
        db_port = st.number_input("ポート", value=5432, min_value=1, max_value=65535)
        db_name = st.text_input("データベース名", value="postgres")
        db_user = st.text_input("ユーザー名", value="postgres")
        db_password = st.text_input("パスワード", type="password")
        
        db_config = {
            'host': db_host,
            'port': db_port,
            'database': db_name,
            'user': db_user,
            'password': db_password
        }
        
        if st.button("🔌 接続テスト", use_container_width=True):
            with st.spinner("接続中..."):
                try:
                    async def test_connection():
                        async with get_mcp_session(db_config) as session:
                            schema = await get_database_schema(session)
                            return schema
                    
                    schema = asyncio.run(test_connection())
                    if schema:
                        st.session_state.schema_info = schema
                        st.success("✅ 接続成功！")
                        if 'tables' in schema:
                            st.write(f"テーブル数: {len(schema['tables'])}")
                    else:
                        st.error("❌ 接続失敗")
                except Exception as e:
                    st.error(f"❌ 接続エラー: {str(e)}")
        
        # スキーマ情報の表示
        if st.session_state.schema_info:
            st.divider()
            st.subheader("📋 テーブル一覧")
            if 'tables' in st.session_state.schema_info:
                for table in st.session_state.schema_info['tables']:
                    st.write(f"- {table['table_name']}")
    
    # メインエリア
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 自然言語クエリ")
        nl_query = st.text_area(
            "質問を入力してください",
            placeholder="例: 全てのユーザーの名前とメールアドレスを表示して",
            height=100
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            execute_button = st.button("🚀 実行", use_container_width=True, type="primary")
        with col_btn2:
            generate_sql_only = st.button("📝 SQLのみ生成", use_container_width=True)
    
    with col2:
        st.subheader("💡 サンプルクエリ")
        st.code("全てのテーブルを表示", language="text")
        st.code("ユーザー数をカウント", language="text")
        st.code("最新の10件を取得", language="text")
    
    # Groqクライアントの取得
    groq_client = get_groq_client()
    if not groq_client:
        st.warning("⚠️ Groq APIキーを設定してください（.envファイル）")
        return
    
    # SQLのみ生成
    if generate_sql_only and nl_query:
        if not st.session_state.schema_info:
            st.warning("⚠️ まずデータベースに接続してください")
        else:
            with st.spinner("SQLを生成中..."):
                sql = natural_language_to_sql(groq_client, nl_query, st.session_state.schema_info)
                if sql:
                    st.subheader("📄 生成されたSQL")
                    st.code(sql, language="sql")
    
    # クエリ実行
    if execute_button and nl_query:
        if not st.session_state.schema_info:
            st.warning("⚠️ まずデータベースに接続してください")
        else:
            with st.spinner("処理中..."):
                # SQL生成
                sql = natural_language_to_sql(groq_client, nl_query, st.session_state.schema_info)
                
                if sql:
                    st.subheader("📄 生成されたSQL")
                    st.code(sql, language="sql")
                    
                    # SQL実行
                    async def run_query():
                        async with get_mcp_session(db_config) as session:
                            result = await execute_sql_query(session, sql)
                            return result
                    
                    result = asyncio.run(run_query())
                    
                    if 'error' in result:
                        st.error(f"❌ エラー: {result['error']}")
                    else:
                        st.subheader("📊 実行結果")
                        st.write(f"取得行数: {result.get('rowCount', 0)}")
                        
                        if result.get('rows'):
                            st.dataframe(result['rows'], use_container_width=True)
                        else:
                            st.info("結果がありません")
                        
                        # 履歴に追加
                        st.session_state.query_history.append({
                            'query': nl_query,
                            'sql': sql,
                            'result_count': result.get('rowCount', 0)
                        })
    
    # クエリ履歴
    if st.session_state.query_history:
        st.divider()
        st.subheader("📜 クエリ履歴")
        for i, hist in enumerate(reversed(st.session_state.query_history[-5:])):
            with st.expander(f"#{len(st.session_state.query_history) - i}: {hist['query'][:50]}..."):
                st.write(f"**質問:** {hist['query']}")
                st.code(hist['sql'], language="sql")
                st.write(f"**結果行数:** {hist['result_count']}")

if __name__ == "__main__":
    main()
