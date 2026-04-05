import streamlit as st
import pandas as pd
from datetime import datetime, date
from streamlit_calendar import calendar

# ページ設定
st.set_page_config(page_title="My Work App", layout="centered")

# --- データ保存 (擬似DB) ---
if 'db' not in st.session_state:
    st.session_state.db = []

# --- ユーザー名と売上表示 ---
st.markdown("<h2 style='text-align: center;'>👤 あなたの名前</h2>", unsafe_allow_html=True)

# 今月の売上計算
today = date.today()
this_month = today.strftime("%Y/%m")
total_sales = sum(item['合計'] for item in st.session_state.db if item['月'] == this_month)

st.markdown(f"<h3 style='text-align: center; border-bottom: 2px solid #333;'>{today.month}月：¥{total_sales:,}</h3>", unsafe_allow_html=True)

# --- カレンダーセクション ---
st.write("### 📅 カレンダー")
calendar_events = []
for item in st.session_state.db:
    calendar_events.append({
        "title": item['案件名'],
        "start": str(item['開始']),
        "end": str(item['納期']),
        "color": "#3D9970" if item.get('done') else "#FF4B4B"
    })

calendar_options = {
    "initialView": "dayGridMonth",
    "headerToolbar": {"left": "prev,next today", "center": "title", "right": ""},
}
calendar(events=calendar_events, options=calendar_options)

st.divider()

# --- 今月の仕事リスト ---
st.write("### ✅ 今月の仕事")
if st.session_state.db:
    for i, item in enumerate(st.session_state.db):
        if item['月'] == this_month:
            col1, col2 = st.columns([1, 4])
            with col1:
                # チェックボックス
                checked = st.checkbox("", value=item.get('done', False), key=f"check_{i}")
                st.session_state.db[i]['done'] = checked
            with col2:
                # 完了したら打ち消し線を入れる
                label = f"~~{item['案件名']}~~" if checked else item['案件名']
                st.markdown(f"**{label}** ({item['納期'].split('-')[-1]}日締 / 目標:{item['1日目標']:.1f}個)")
else:
    st.info("まだ案件がありません")

# --- 仕事の追加 (ポップアップ風にサイドバーを使用) ---
with st.sidebar:
    st.header("➕ 新規案件追加")
    with st.form("add_form", clear_on_submit=True):
        new_name = st.text_input("案件名")
        new_qty = st.number_input("総数", min_value=1)
        new_price = st.number_input("単価", min_value=0)
        new_start = st.date_input("開始日", date.today())
        new_end = st.date_input("納期", date.today())
        
        if st.form_submit_button("追加する"):
            days = (new_end - new_start).days + 1
            if days > 0:
                st.session_state.db.append({
                    "月": new_end.strftime("%Y/%m"),
                    "案件名": new_name,
                    "合計": new_qty * new_price,
                    "開始": new_start,
                    "納期": new_end,
                    "1日目標": new_qty / days,
                    "done": False
                })
                st.success("追加完了！")
                st.rerun()
            else:
                st.error("納期を確認してください")
