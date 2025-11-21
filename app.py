import streamlit as st
import pandas as pd
import random

# ▼ ページ設定
st.set_page_config(page_title="G検定フラッシュカード", layout="centered")

st.title("📚 G検定フラッシュカード")

# ▼ Excelファイル読み込み
file_path = "フラッシュカード.xlsx"  # 同じフォルダに配置
xls = pd.ExcelFile(file_path)

# ▼ 章選択
chapter = st.selectbox("章を選択してください", xls.sheet_names)

# ▼ データ読み込み
df = pd.read_excel(xls, sheet_name=chapter)
questions = list(zip(df['Question'].dropna(), df['Answer'].dropna()))

# ▼ セッション状態管理
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# ▼ 次の質問ボタン
if st.button("次の質問"):
    st.session_state.current_question = random.choice(questions)
    st.session_state.show_answer = False

# ▼ 質問表示
if st.session_state.current_question:
    st.write(f"**質問:** {st.session_state.current_question[0]}")

    # ▼ 回答ボタン
    if st.button("回答"):
        st.session_state.show_answer = True

    # ▼ 答え表示
    if st.session_state.show_answer:
        st.success(f"答え: {st.session_state.current_question[1]}")