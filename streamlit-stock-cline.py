import streamlit as st
import yfinance as yf
import pandas as pd

# ページ設定
st.set_page_config(page_title="株価確認アプリ", layout="wide")

# タイトル
st.title("株価確認アプリ")

# サイドバーで銘柄コードを入力
with st.sidebar:
    ticker_symbol = st.text_input("銘柄コード（例：7203.T）", "7203.T")
    st.caption("※日本株の場合は末尾に .T を付けてください")

# メイン処理
if ticker_symbol:
    try:
        # 株価データの取得
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="1y")
        
        if not hist.empty:
            # 会社情報の表示
            info = ticker.info
            company_name = info.get('longName', 'データなし')
            st.header(f"{company_name} ({ticker_symbol})")
            
            # 株価情報の表示
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("現在値", f"¥{hist['Close'][-1]:,.0f}", 
                         f"{((hist['Close'][-1] - hist['Close'][-2])/hist['Close'][-2]*100):,.2f}%")
            with col2:
                st.metric("始値", f"¥{hist['Open'][-1]:,.0f}")
            with col3:
                st.metric("出来高", f"{hist['Volume'][-1]:,.0f}")
            
            # チャートの表示
            st.subheader("株価チャート（1年間）")
            st.line_chart(hist['Close'])
            
            # 詳細データの表示
            st.subheader("株価詳細データ")
            st.dataframe(hist.tail())
            
        else:
            st.error("データを取得できませんでした。銘柄コードを確認してください。")
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.error("正しい銘柄コードを入力してください。")
