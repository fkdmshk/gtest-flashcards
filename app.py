import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="G検定フラッシュカード", layout="centered")
st.title("📚 G検定フラッシュカード")

# -------------------
# Excel 読み込み
# -------------------
df_all = pd.ExcelFile("フラッシュカード_Ver01.xlsx")

# -------------------
# UI：章選択
# -------------------
chapter = st.selectbox(
    "章を選択してください",
    df_all.sheet_names,
    key="chapter"
)

# -------------------
# UI：難易度選択（★追加）
# -------------------
level = st.selectbox(
    "難易度を選択してください",
    ["初級", "中級", "上級"],
    key="level"
)

# -------------------
# 状態リセット（★最重要）
# -------------------
if "prev_chapter" not in st.session_state:
    st.session_state.prev_chapter = chapter
    st.session_state.prev_level = level

if (
    chapter != st.session_state.prev_chapter
    or level != st.session_state.prev_level
):
    st.session_state.current_q = None
    st.session_state.used = []
    st.session_state.prev_chapter = chapter
    st.session_state.prev_level = level

# -------------------
# データ読み込み
# -------------------
df = pd.read_excel(df_all, sheet_name=chapter)

def extract_level(num):
    if 1 <= num <= 20:
        return "初級"
    elif 21 <= num <= 30:
        return "中級"
    elif 31 <= num <= 41:
        return "上級"
    return None

df["ID_num"] = df["ID"].str.split("-").str[1].astype(int)
df["Level"] = df["ID_num"].apply(extract_level)

df = df[df["Level"] == level]

qa_list = list(zip(df["Question"], df["Answer"]))

# -------------------
# ボタン
# -------------------
if st.button("▶ 次の問題"):
    remain = [
        q for q in qa_list
        if q not in st.session_state.get("used", [])
    ]
    if not remain:
        st.info("この難易度の問題はすべて出題しました")
    else:
        q = random.choice(remain)
        st.session_state.current_q = q
        st.session_state.used.append(q)

# -------------------
# 表示
# -------------------
if st.session_state.get("current_q"):
    st.markdown("### ❓ 問題")
    st.write(st.session_state.current_q[0])

    with st.expander("✅ 答えを見る"):
        st.write(st.session_state.current_q[1])
