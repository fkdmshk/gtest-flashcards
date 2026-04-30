import streamlit as st
import pandas as pd
import random

# --------------------
# ページ設定
# --------------------
st.set_page_config(page_title="G検定フラッシュカード", layout="centered")
st.title("📚 G検定フラッシュカード")

# --------------------
# Excel 読み込み
# --------------------
file_path = "フラッシュカード_Ver01.xlsx"
xls = pd.ExcelFile(file_path)

# --------------------
# UI：章選択
# --------------------
chapter = st.selectbox("章を選択してください", xls.sheet_names)

# --------------------
# UI：難易度選択
# --------------------
level = st.selectbox(
    "難易度を選択してください",
    ["初級", "中級", "上級"]
)

# --------------------
# データ読み込み
# --------------------
df = pd.read_excel(xls, sheet_name=chapter)

# --------------------
# 難易度フィルタ関数
# --------------------
def filter_by_level(df, level):
    """
    ID例: 4-021 → 後半の数値で難易度判定
    """
    def id_to_num(id_str):
        try:
            return int(str(id_str).split("-")[1])
        except:
            return None

    df = df.copy()
    df["ID_num"] = df["ID"].apply(id_to_num)

    if level == "初級":
        return df[df["ID_num"].between(1, 20)]
    elif level == "中級":
        return df[df["ID_num"].between(21, 30)]
    elif level == "上級":
        return df[df["ID_num"].between(31, 41)]
    return df

df_level = filter_by_level(df, level)

# --------------------
# 問題抽出
# --------------------
questions = list(
    zip(
        df_level["Question"].dropna(),
        df_level["Answer"].dropna()
    )
)

# --------------------
# セッション管理
# --------------------
if "current_question" not in st.session_state:
    st.session_state.current_question = None
    st.session_state.show_answer = False

# --------------------
# ボタン
# --------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("次の質問"):
        if len(questions) == 0:
            st.warning("この章・難易度には問題がありません。")
            st.session_state.current_question = None
        else:
            st.session_state.current_question = random.choice(questions)
            st.session_state.show_answer = False

with col2:
    if st.button("答えを見る"):
        st.session_state.show_answer = True

# --------------------
# 表示
# --------------------
if st.session_state.current_question:
    st.markdown("### ❓ 質問")
    st.write(st.session_state.current_question[0])

    if st.session_state.show_answer:
        st.markdown("### ✅ 答え")
        st.write(st.session_state.current_question[1])
