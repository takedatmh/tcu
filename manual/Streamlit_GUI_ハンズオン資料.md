# Streamlit GUIアプリケーション ハンズオン資料

StreamlitでリッチなGUIアプリケーションを作成・実行する方法と、入出力機能のTipsをまとめたハンズオン資料です。

## 目次

1. [Streamlitとは](#1-streamlitとは)
2. [環境構築と基本的な実行方法](#2-環境構築と基本的な実行方法)
3. [基本的なGUIコンポーネント](#3-基本的なguiコンポーネント)
4. [リッチなGUIの作成方法](#4-リッチなguiの作成方法)
5. [入出力機能の実装](#5-入出力機能の実装)
6. [レイアウトとデザイン](#6-レイアウトとデザイン)
7. [状態管理とセッション](#7-状態管理とセッション)
8. [実践的なTips集](#8-実践的なtips集)
9. [パフォーマンス最適化](#9-パフォーマンス最適化)
10. [デプロイ方法](#10-デプロイ方法)

---

## 1. Streamlitとは

### 概要

Streamlitは、Pythonで**数行のコードでWebアプリケーションを作成できる**オープンソースフレームワークです。

**主な特徴**:
- **HTMLやCSS不要**: Pythonだけでリッチなウェブアプリを作成
- **インタラクティブ**: リアルタイムでUIが更新される
- **データサイエンス向け**: Pandas、NumPy、Matplotlibなどとシームレスに統合
- **無料**: 完全オープンソース、商用利用も可能

### Streamlitが得意なこと

- データダッシュボード
- 機械学習モデルのデモ
- データ可視化ツール
- 社内ツールのプロトタイプ
- レポート生成ツール

### 比較: StreamlitとHTML/CSS/JavaScript

| 項目 | Streamlit | HTML/CSS/JS |
|------|-----------|-------------|
| 学習コスト | 低（Pythonのみ） | 高（3言語必要） |
| 開発速度 | 高速（数時間） | 遅い（数日～週） |
| カスタマイズ性 | 中（制約あり） | 高（自由度高い） |
| データ処理 | 得意 | 別途実装必要 |
| 適用範囲 | データアプリ | すべて |

---

## 2. 環境構築と基本的な実行方法

### ステップ2.1: Pythonのインストール確認

```bash
# Pythonバージョン確認（3.8以上が必要）
python3 --version
# 出力例: Python 3.11.5

# pipの確認
pip3 --version
```

### ステップ2.2: Streamlitのインストール

```bash
# 基本的なインストール
pip install streamlit

# データ可視化ライブラリも一緒にインストール
pip install streamlit pandas numpy matplotlib plotly

# インストール確認
streamlit --version
# 出力例: Streamlit, version 1.31.0
```

### ステップ2.3: 最初のアプリを作成

**hello_app.py**:
```python
import streamlit as st

# タイトル
st.title("Hello Streamlit!")

# テキスト
st.write("これは最初のStreamlitアプリです")

# ボタン
if st.button("クリックしてください"):
    st.balloons()  # 紙吹雪アニメーション
    st.success("ボタンがクリックされました！")
```

### ステップ2.4: アプリの実行

```bash
# アプリを起動
streamlit run hello_app.py

# 出力例:
#   Local URL: http://localhost:8501
#   Network URL: http://192.168.1.10:8501
```

ブラウザが自動的に開き、`http://localhost:8501`でアプリが表示されます。

### ステップ2.5: ホットリロード

Streamlitは**ファイルを保存すると自動的にリロード**されます。

1. `hello_app.py`を編集
2. ファイルを保存（Ctrl+S / Cmd+S）
3. ブラウザ右上に「Rerun」ボタンが表示
4. クリックするか、自動的に更新

---

## 3. 基本的なGUIコンポーネント

### 3.1 テキスト表示

```python
import streamlit as st

# タイトル（大見出し）
st.title("メインタイトル")

# ヘッダー（中見出し）
st.header("セクションヘッダー")

# サブヘッダー（小見出し）
st.subheader("サブセクション")

# テキスト
st.text("固定幅テキスト（プログラミングコード等）")

# Markdown
st.markdown("**太字** *斜体* `コード`")
st.markdown("### Markdownの見出し")
st.markdown("- リスト1\n- リスト2")

# 汎用的な書き込み（自動的に適切な表示形式を選択）
st.write("これは普通のテキスト")
st.write({"key": "value"})  # 辞書→JSON表示
st.write([1, 2, 3])  # リスト→テーブル表示

# キャプション（小さいテキスト）
st.caption("これは補足説明です")

# LaTeX数式
st.latex(r"\sum_{i=1}^{n} x_i^2")

# コードブロック
st.code("""
def hello():
    print("Hello World")
""", language="python")
```

### 3.2 入力ウィジェット

```python
import streamlit as st

# テキスト入力
name = st.text_input("お名前を入力", placeholder="山田太郎")

# テキストエリア（複数行）
message = st.text_area("メッセージ", height=150)

# 数値入力
age = st.number_input("年齢", min_value=0, max_value=120, value=25)

# スライダー
score = st.slider("スコア", 0, 100, 50)  # 最小、最大、初期値

# 範囲スライダー
price_range = st.select_slider(
    "価格帯",
    options=["安い", "普通", "高い", "非常に高い"],
    value=("普通", "高い")
)

# ボタン
if st.button("送信"):
    st.write(f"こんにちは、{name}さん！")

# チェックボックス
agree = st.checkbox("利用規約に同意する")
if agree:
    st.success("同意されました")

# ラジオボタン
choice = st.radio(
    "好きな色は？",
    ["赤", "青", "緑"]
)

# セレクトボックス（ドロップダウン）
option = st.selectbox(
    "都市を選択",
    ["東京", "大阪", "名古屋", "福岡"]
)

# マルチセレクト
options = st.multiselect(
    "好きな果物を選択（複数可）",
    ["りんご", "バナナ", "オレンジ", "ぶどう"],
    default=["りんご"]
)

# 日付入力
from datetime import date
birth_date = st.date_input("生年月日", date(2000, 1, 1))

# 時刻入力
from datetime import time
meeting_time = st.time_input("会議時間", time(10, 30))

# カラーピッカー
color = st.color_picker("テーマカラーを選択", "#FF0000")
```

### 3.3 データ表示

```python
import streamlit as st
import pandas as pd
import numpy as np

# データフレームの作成
df = pd.DataFrame({
    '商品名': ['りんご', 'バナナ', 'オレンジ'],
    '価格': [150, 100, 120],
    '在庫': [30, 45, 25]
})

# データフレーム表示（静的）
st.dataframe(df)

# データフレーム表示（インタラクティブ）
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "価格": st.column_config.NumberColumn(
            "価格（円）",
            format="¥%d"
        )
    }
)

# データテーブル（静的、小さいデータ向け）
st.table(df)

# メトリクス表示
col1, col2, col3 = st.columns(3)
col1.metric("売上", "¥1,234,567", "+12.3%")
col2.metric("訪問者", "45,678", "-5.2%", delta_color="inverse")
col3.metric("注文数", "890", "+8人")

# JSON表示
data = {"name": "太郎", "age": 25, "city": "東京"}
st.json(data)
```

### 3.4 メディア表示

```python
import streamlit as st

# 画像表示
st.image("image.png", caption="サンプル画像", width=300)

# URLから画像を表示
st.image("https://example.com/image.jpg")

# 複数画像を横並び
st.image(["image1.png", "image2.png", "image3.png"], width=200)

# 音声ファイル
st.audio("audio.mp3")

# 動画ファイル
st.video("video.mp4")

# YouTube動画
st.video("https://www.youtube.com/watch?v=VIDEO_ID")
```

### 3.5 グラフ・チャート

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# サンプルデータ
df = pd.DataFrame({
    '日付': pd.date_range('2024-01-01', periods=30),
    '売上': np.random.randint(100, 500, 30)
})

# 折れ線グラフ（Streamlit組み込み）
st.line_chart(df.set_index('日付')['売上'])

# 棒グラフ
st.bar_chart(df.set_index('日付')['売上'])

# エリアチャート
st.area_chart(df.set_index('日付')['売上'])

# 散布図（マップ）
map_df = pd.DataFrame({
    'lat': [35.6812, 34.6937, 35.0116],
    'lon': [139.7671, 135.5023, 135.7681]
})
st.map(map_df)

# Matplotlib
fig, ax = plt.subplots()
ax.plot(df['日付'], df['売上'])
ax.set_xlabel('日付')
ax.set_ylabel('売上')
st.pyplot(fig)

# Plotly（インタラクティブ）
fig = px.line(df, x='日付', y='売上', title='月次売上推移')
st.plotly_chart(fig, use_container_width=True)

# Altair
import altair as alt
chart = alt.Chart(df).mark_line().encode(
    x='日付',
    y='売上'
)
st.altair_chart(chart, use_container_width=True)
```

---

## 4. リッチなGUIの作成方法

### 4.1 ページ設定とテーマ

```python
import streamlit as st

# ページ設定（必ず最初に記述）
st.set_page_config(
    page_title="マイアプリ",
    page_icon="🚀",
    layout="wide",  # "centered" or "wide"
    initial_sidebar_state="expanded",  # "auto", "expanded", "collapsed"
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': 'https://www.example.com/bug',
        'About': "# これはサンプルアプリです\nバージョン1.0"
    }
)

# カスタムCSS
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)
```

### 4.2 サイドバーの活用

```python
import streamlit as st

# サイドバーにコンテンツを追加
with st.sidebar:
    st.title("設定")
    
    # ロゴ画像
    st.image("logo.png", width=200)
    
    # ナビゲーション
    page = st.radio(
        "ページを選択",
        ["ホーム", "データ分析", "設定"]
    )
    
    st.divider()  # 区切り線
    
    # フィルター
    st.subheader("フィルター")
    date_range = st.date_input("期間", [])
    category = st.multiselect("カテゴリ", ["A", "B", "C"])
    
    st.divider()
    
    # 情報
    st.info("Tip: サイドバーを使うとUIがスッキリします")

# メインコンテンツ
if page == "ホーム":
    st.title("ホーム")
    st.write("ようこそ！")
elif page == "データ分析":
    st.title("データ分析")
    st.write("データ分析画面")
else:
    st.title("設定")
    st.write("設定画面")
```

### 4.3 カラム（列）レイアウト

```python
import streamlit as st

# 等幅の2カラム
col1, col2 = st.columns(2)

with col1:
    st.header("左側")
    st.write("左側のコンテンツ")
    st.button("ボタン1")

with col2:
    st.header("右側")
    st.write("右側のコンテンツ")
    st.button("ボタン2")

# 異なる幅のカラム（1:2:1の比率）
col1, col2, col3 = st.columns([1, 2, 1])
col1.write("狭い")
col2.write("広い")
col3.write("狭い")

# 3カラムでメトリクス表示
col1, col2, col3 = st.columns(3)
col1.metric("ユーザー数", "1,234", "+12%")
col2.metric("売上", "¥5.6M", "+8%")
col3.metric("成約率", "23%", "-2%")
```

### 4.4 タブの使用

```python
import streamlit as st

tab1, tab2, tab3 = st.tabs(["グラフ", "データ", "設定"])

with tab1:
    st.header("グラフ表示")
    st.line_chart({"データ": [1, 5, 2, 6, 2, 1]})

with tab2:
    st.header("生データ")
    st.dataframe({"A": [1, 2, 3], "B": [4, 5, 6]})

with tab3:
    st.header("設定")
    st.checkbox("オプション1")
    st.checkbox("オプション2")
```

### 4.5 エクスパンダー（折りたたみ）

```python
import streamlit as st

# 基本的なエクスパンダー
with st.expander("詳細を表示"):
    st.write("ここに詳細な情報を記載")
    st.image("detail_image.png")

# デフォルトで展開
with st.expander("重要な情報", expanded=True):
    st.warning("この操作は取り消せません")

# 複数のエクスパンダー
with st.expander("セクション1"):
    st.write("セクション1の内容")

with st.expander("セクション2"):
    st.write("セクション2の内容")

with st.expander("セクション3"):
    st.write("セクション3の内容")
```

### 4.6 コンテナ

```python
import streamlit as st

# コンテナを使って動的に要素を追加
container = st.container()
container.write("これはコンテナ内です")

# 後から要素を追加できる
st.write("コンテナの外です")
container.write("後から追加しました")

# 枠線付きコンテナ
with st.container(border=True):
    st.write("枠線付きコンテナ")
    st.button("ボタン")

# emptyを使った動的更新
placeholder = st.empty()
placeholder.text("初期テキスト")
# 後から上書き
placeholder.text("更新されたテキスト")
```

### 4.7 ステータスメッセージ

```python
import streamlit as st
import time

# 成功メッセージ
st.success("処理が成功しました！")

# 情報メッセージ
st.info("参考情報です")

# 警告メッセージ
st.warning("注意してください")

# エラーメッセージ
st.error("エラーが発生しました")

# 例外表示
try:
    1 / 0
except Exception as e:
    st.exception(e)

# プログレスバー
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
st.success("完了！")

# スピナー（読み込み中表示）
with st.spinner("処理中..."):
    time.sleep(2)
st.success("完了！")

# ステータス表示（複数ステップ）
with st.status("データを処理中...", expanded=True) as status:
    st.write("データを読み込んでいます...")
    time.sleep(1)
    st.write("データを変換しています...")
    time.sleep(1)
    status.update(label="処理完了！", state="complete", expanded=False)
```

---

## 5. 入出力機能の実装

### 5.1 ファイルアップロード

```python
import streamlit as st
import pandas as pd
from PIL import Image

# 画像アップロード
uploaded_file = st.file_uploader("画像を選択", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)
    
    # ファイル情報
    st.write(f"ファイル名: {uploaded_file.name}")
    st.write(f"サイズ: {uploaded_file.size} bytes")

# CSVアップロード
uploaded_csv = st.file_uploader("CSVファイルをアップロード", type=["csv"])
if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)
    st.dataframe(df)
    
    # データ統計
    st.write("データの統計情報")
    st.write(df.describe())

# 複数ファイルアップロード
uploaded_files = st.file_uploader(
    "複数ファイルをアップロード",
    type=["jpg", "png"],
    accept_multiple_files=True
)
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.image(uploaded_file)

# Excelファイルのアップロード
uploaded_excel = st.file_uploader("Excelファイル", type=["xlsx", "xls"])
if uploaded_excel is not None:
    # 特定のシートを読み込み
    df = pd.read_excel(uploaded_excel, sheet_name="Sheet1")
    st.dataframe(df)
```

### 5.2 ファイルダウンロード

```python
import streamlit as st
import pandas as pd
import io

# CSVダウンロード
df = pd.DataFrame({
    '商品': ['りんご', 'バナナ', 'オレンジ'],
    '価格': [150, 100, 120]
})

# CSVに変換
csv = df.to_csv(index=False).encode('utf-8')

# ダウンロードボタン
st.download_button(
    label="CSVをダウンロード",
    data=csv,
    file_name='products.csv',
    mime='text/csv',
)

# Excelダウンロード
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Products', index=False)
    
st.download_button(
    label="Excelをダウンロード",
    data=buffer.getvalue(),
    file_name='products.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
)

# テキストファイルダウンロード
text_content = "これはサンプルテキストです。\n2行目です。"
st.download_button(
    label="テキストをダウンロード",
    data=text_content,
    file_name='sample.txt',
    mime='text/plain',
)

# JSONダウンロード
import json
data = {"name": "太郎", "age": 25}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
st.download_button(
    label="JSONをダウンロード",
    data=json_str,
    file_name='data.json',
    mime='application/json',
)

# 画像ダウンロード
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

# 画像をバイトに変換
buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)

st.download_button(
    label="グラフをダウンロード",
    data=buf,
    file_name='chart.png',
    mime='image/png',
)
```

### 5.3 カメラ入力

```python
import streamlit as st
from PIL import Image

# カメラで撮影
picture = st.camera_input("写真を撮影")

if picture:
    # 撮影した画像を表示
    st.image(picture)
    
    # 画像処理の例
    img = Image.open(picture)
    st.write(f"画像サイズ: {img.size}")
    
    # グレースケール変換
    gray_img = img.convert('L')
    st.image(gray_img, caption="グレースケール変換")
```

### 5.4 フォーム機能

```python
import streamlit as st

# フォームを使うと、一度に複数の入力をまとめて送信できる
with st.form("my_form"):
    st.write("お問い合わせフォーム")
    
    name = st.text_input("お名前")
    email = st.text_input("メールアドレス")
    message = st.text_area("メッセージ")
    
    # すべてのフォーム要素の後に送信ボタン
    submitted = st.form_submit_button("送信")
    
    if submitted:
        st.success(f"送信しました！")
        st.write(f"名前: {name}")
        st.write(f"メール: {email}")
        st.write(f"メッセージ: {message}")

# クリアボタン付きフォーム
with st.form("form_with_clear", clear_on_submit=True):
    st.write("送信後にフォームがクリアされます")
    
    input1 = st.text_input("入力1")
    input2 = st.text_input("入力2")
    
    submitted = st.form_submit_button("送信")
    if submitted:
        st.write(f"送信: {input1}, {input2}")
```

### 5.5 データエディタ

```python
import streamlit as st
import pandas as pd

# 編集可能なデータフレーム
df = pd.DataFrame({
    '商品': ['りんご', 'バナナ', 'オレンジ'],
    '価格': [150, 100, 120],
    '在庫': [30, 45, 25],
    '販売中': [True, True, False]
})

edited_df = st.data_editor(
    df,
    num_rows="dynamic",  # 行の追加・削除を許可
    use_container_width=True,
    column_config={
        "価格": st.column_config.NumberColumn(
            "価格（円）",
            min_value=0,
            max_value=10000,
            step=10,
            format="¥%d"
        ),
        "在庫": st.column_config.NumberColumn(
            "在庫数",
            min_value=0,
            max_value=1000
        ),
        "販売中": st.column_config.CheckboxColumn(
            "販売ステータス",
            help="販売中かどうか"
        )
    },
    hide_index=True
)

# 変更があったかチェック
if not df.equals(edited_df):
    st.write("データが変更されました")
    
    # 保存ボタン
    if st.button("変更を保存"):
        # ここでデータベースやファイルに保存
        st.success("保存しました！")
        st.write(edited_df)
```

---

## 6. レイアウトとデザイン

### 6.1 レスポンシブデザイン

```python
import streamlit as st

# ページ幅を最大化
st.set_page_config(layout="wide")

# 画面幅に応じて列数を変更
def get_column_count():
    # 画面幅に基づいて列数を決定（擬似的）
    return 3

cols = st.columns(get_column_count())

for i, col in enumerate(cols):
    with col:
        st.write(f"カラム {i+1}")
        st.image(f"https://via.placeholder.com/150?text=Image{i+1}")
```

### 6.2 カスタムHTMLとCSS

```python
import streamlit as st

# カスタムHTML
st.markdown("""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
    <h2 style="color: #0066cc;">カスタムヘッダー</h2>
    <p style="font-size: 16px;">これはHTMLで作成したカスタムコンテンツです。</p>
</div>
""", unsafe_allow_html=True)

# カスタムCSS（グローバル）
st.markdown("""
<style>
    /* ヘッダーのスタイル */
    h1 {
        color: #0066cc;
        font-family: 'Arial', sans-serif;
    }
    
    /* サイドバーの背景色 */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    
    /* ボタンのホバー効果 */
    .stButton>button:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# カスタムフォント
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
    }
</style>
""", unsafe_allow_html=True)
```

---

## 7. 状態管理とセッション

### 7.1 セッションステート（Session State）

```python
import streamlit as st

# セッションステートの初期化
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# カウンターアプリ
st.title("カウンターアプリ")
st.write(f"現在のカウント: {st.session_state.counter}")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("増やす"):
        st.session_state.counter += 1
        st.rerun()

with col2:
    if st.button("減らす"):
        st.session_state.counter -= 1
        st.rerun()

with col3:
    if st.button("リセット"):
        st.session_state.counter = 0
        st.rerun()
```

### 7.2 複雑な状態管理

```python
import streamlit as st

# 初期化
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': '',
        'age': 0,
        'interests': []
    }

if 'history' not in st.session_state:
    st.session_state.history = []

# フォーム
st.title("ユーザー情報管理")

name = st.text_input("名前", value=st.session_state.user_data['name'])
age = st.number_input("年齢", value=st.session_state.user_data['age'])
interests = st.multiselect(
    "興味",
    ["スポーツ", "音楽", "読書", "旅行"],
    default=st.session_state.user_data['interests']
)

if st.button("保存"):
    st.session_state.user_data = {
        'name': name,
        'age': age,
        'interests': interests
    }
    st.session_state.history.append(st.session_state.user_data.copy())
    st.success("保存しました！")

# 履歴表示
if st.session_state.history:
    st.subheader("変更履歴")
    for i, record in enumerate(st.session_state.history):
        st.write(f"{i+1}. {record}")
```

### 7.3 キャッシュ機能（@st.cache_data）

```python
import streamlit as st
import pandas as pd
import time

# データ読み込みをキャッシュ
@st.cache_data
def load_data():
    """データを読み込む（初回のみ実行、以降はキャッシュから取得）"""
    time.sleep(3)  # 重い処理を模擬
    return pd.DataFrame({
        '商品': ['A', 'B', 'C'],
        '売上': [100, 200, 150]
    })

st.title("キャッシュのデモ")
st.write("データを読み込んでいます...")

# 初回は3秒かかるが、2回目以降は即座に表示
df = load_data()
st.dataframe(df)

# キャッシュをクリア
if st.button("キャッシュをクリア"):
    st.cache_data.clear()
    st.rerun()
```

---

## 8. 実践的なTips集

### 8.1 動的なUIの更新

```python
import streamlit as st
import time

# プレースホルダーを使った動的更新
st.title("リアルタイム更新デモ")

placeholder = st.empty()

for i in range(10):
    placeholder.write(f"カウント: {i}")
    time.sleep(0.5)

placeholder.success("完了！")
```

### 8.2 条件付き表示

```python
import streamlit as st

# チェックボックスで表示を切り替え
show_details = st.checkbox("詳細を表示")

if show_details:
    st.write("これは詳細情報です")
    st.dataframe({"列1": [1, 2, 3], "列2": [4, 5, 6]})

# セレクトボックスで異なるコンテンツを表示
view_mode = st.selectbox("表示モード", ["シンプル", "詳細", "グラフ"])

if view_mode == "シンプル":
    st.write("シンプルビュー")
elif view_mode == "詳細":
    st.write("詳細ビュー")
    st.dataframe({"データ": [1, 2, 3]})
else:
    st.write("グラフビュー")
    st.line_chart([1, 3, 2, 4])
```

### 8.3 エラーハンドリング

```python
import streamlit as st

try:
    # 危険な操作
    number = st.number_input("数値を入力", value=1)
    result = 10 / number
    st.success(f"結果: {result}")
    
except ZeroDivisionError:
    st.error("ゼロで除算できません")
    
except Exception as e:
    st.error(f"エラーが発生しました: {str(e)}")
    st.exception(e)  # 詳細なスタックトレース

# ユーザー入力の検証
email = st.text_input("メールアドレス")

if email:
    if "@" not in email:
        st.warning("有効なメールアドレスを入力してください")
    else:
        st.success("有効なメールアドレスです")
```

### 8.4 検索・フィルタリング機能

```python
import streamlit as st
import pandas as pd

# サンプルデータ
df = pd.DataFrame({
    '商品名': ['りんご', 'バナナ', 'オレンジ', 'ぶどう', 'メロン'],
    'カテゴリ': ['果物', '果物', '果物', '果物', '果物'],
    '価格': [150, 100, 120, 300, 500],
    '在庫': [30, 45, 25, 15, 5]
})

st.title("商品検索")

# 検索ボックス
search_term = st.text_input("商品名で検索", "")

# フィルター
col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("最低価格", 0, 1000, 0)
with col2:
    max_price = st.number_input("最高価格", 0, 1000, 1000)

# データフィルタリング
filtered_df = df.copy()

if search_term:
    filtered_df = filtered_df[filtered_df['商品名'].str.contains(search_term)]

filtered_df = filtered_df[
    (filtered_df['価格'] >= min_price) & 
    (filtered_df['価格'] <= max_price)
]

# 結果表示
st.write(f"検索結果: {len(filtered_df)}件")
st.dataframe(filtered_df)
```

---

## 9. パフォーマンス最適化

### 9.1 データのキャッシュ

```python
import streamlit as st
import pandas as pd
import time

# 重い処理をキャッシュ
@st.cache_data(ttl=3600)  # 1時間キャッシュ
def load_large_dataset():
    """大きなデータセットを読み込む"""
    time.sleep(2)  # 重い処理を模擬
    return pd.DataFrame({
        'データ': range(10000)
    })

# キャッシュを使用
df = load_large_dataset()
st.write(f"データ件数: {len(df)}")
```

### 9.2 遅延読み込み

```python
import streamlit as st

# 初期表示は最小限に
st.title("データ分析ツール")

# 詳細はエクスパンダーに隠す
with st.expander("詳細データを表示"):
    # ここで重い処理を実行
    import pandas as pd
    import numpy as np
    
    df = pd.DataFrame(np.random.randn(1000, 10))
    st.dataframe(df)
```

---

## 10. デプロイ方法

### 10.1 Streamlit Community Cloud（無料）

#### ステップ1: GitHubリポジトリの準備

```bash
# プロジェクトをGitHubにプッシュ
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

#### ステップ2: requirements.txtの作成

```txt
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
plotly>=5.14.0
```

#### ステップ3: Streamlit Community Cloudでデプロイ

1. https://share.streamlit.io/ にアクセス
2. GitHubアカウントでサインイン
3. "New app"をクリック
4. リポジトリ、ブランチ、ファイルパスを指定
5. "Deploy!"をクリック

**URL**: `https://username-repo-main.streamlit.app`

### 10.2 Dockerでのデプロイ

#### Dockerfileの作成

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションをコピー
COPY . .

EXPOSE 8501

# Streamlitを起動
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

#### ビルドと実行

```bash
# イメージをビルド
docker build -t my-streamlit-app .

# コンテナを実行
docker run -p 8501:8501 my-streamlit-app

# ブラウザで http://localhost:8501 にアクセス
```

---

## まとめ

このハンズオン資料では、Streamlitを使った以下のトピックを網羅しました:

### 学習内容

1. **基本**: 環境構築、実行方法、基本コンポーネント
2. **リッチGUI**: レイアウト、デザイン、カスタマイズ
3. **入出力**: ファイルアップロード/ダウンロード、フォーム、カメラ
4. **高度な機能**: 状態管理、キャッシュ、パフォーマンス最適化
5. **実践**: 認証、ページネーション、検索、多言語対応
6. **デプロイ**: Community Cloud、Docker

### 次のステップ

1. **実践プロジェクトを作成**: 学んだ知識を使って実際のアプリを開発
2. **コミュニティに参加**: フォーラムで質問・回答、知見を共有
3. **高度な機能を学習**: カスタムコンポーネント、API統合
4. **デプロイして公開**: 作成したアプリを世界に公開

### 参考リソース

- **公式ドキュメント**: https://docs.streamlit.io/
- **APIリファレンス**: https://docs.streamlit.io/library/api-reference
- **フォーラム**: https://discuss.streamlit.io/
- **GitHub**: https://github.com/streamlit/streamlit
- **ギャラリー**: https://streamlit.io/gallery

---

**作成日**: 2025年11月30日  
**バージョン**: 1.0.0  
**ライセンス**: MIT License
