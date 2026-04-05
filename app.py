import streamlit as st
import pandas as pd

st.title("💼 お仕事管理アプリ")

# 簡易的な入力フォーム
task = st.text_input("新しいタスクを入力してください")
if st.button("追加"):
    st.write(f"「{task}」を登録しました！（テスト動作中）")
