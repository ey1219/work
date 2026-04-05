import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- データ保存設定 ---
DATA_FILE = "work_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["依頼日", "指図", "品番", "工程名", "No", "依頼数", "単価", "受取日", "完了"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# 初期化
if 'page' not in st.session_state:
    st.session_state.page = "home"
df = load_data()

def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- デザイン設定（画像そのままの再現） ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP&display=swap');
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Noto Serif JP', serif;
        background-color: #ffffff;
    }
    .job-card {
        background-color: #d3d3d3;
        border-radius: 25px;
        padding: 10px 20px;
        margin-bottom: 8px;
        color: #333;
    }
    .plus-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: white;
        border: 1px solid #ccc;
        border-radius: 50%;
        width: 60px; height: 60px;
        display: flex; justify-content: center; align-items: center;
        font-size: 30px; cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# --- 共通ロゴ ---
st.markdown("<div style='text-align: left;'><img src='https://img.icons8.com/ios/50/000000/open-book.png' width='30'><br><b>my work.</b></div>", unsafe_allow_html=True)

# --- ページ：ホーム ---
if st.session_state.page == "home":
    col_m, col_y = st.columns([1, 1])
    with col_m: st.markdown(f"## {datetime.now().month}月")
    with col_y:
        sales = (df[df['完了']==True]['依頼数'].astype(float) * df[df['完了']==True]['単価'].astype(float)).sum()
        st.markdown(f"## ¥{int(sales)}")

    nav1, nav2 = st.columns([1, 1])
    with nav1: st.button("🏠", on_click=go_to, args=("home",))
    with nav2: st.button("📖🖋️", on_click=go_to, args=("history",))
    
    st.divider()
    st.write("📅 カレンダー")
    st.date_input("", datetime.now(), label_visibility="collapsed")

    st.subheader("現在作業中の内職")
    st.markdown("<small>依頼日 指図 品番 工程名 No. 依頼数 受取日</small>", unsafe_allow_html=True)
    
    active = df[df['完了'] == False]
    for idx, row in active.iterrows():
        c1, c2 = st.columns([1, 8])
        with c1:
            if st.checkbox("", key=f"c_{idx}"):
                df.at[idx, '完了'] = True
                save_data(df)
                st.rerun()
        with c2:
            st.markdown(f"<div class='job-card'>{row['依頼日']} {row['指図']} {row['品番']} {row['工程名']} {row['No']} {row['依頼数']} {row['受取日']}</div>", unsafe_allow_html=True)

    st.subheader("作業終了した内職")
    for _, row in df[df['完了']==True].tail(3).iterrows():
        st.text(f"✅ {row['品番']} ({row['工程名']})")

    # 右下の＋ボタン
    if st.button("＋", key="add_p"): go_to("add")

# --- ページ：追加 ---
elif st.session_state.page == "add":
    st.markdown("### 手書き入力")
    with st.container():
        f_date = st.text_input("依頼日", "3/24")
        f_shizu = st.text_input("指図")
        f_hin = st.text_input("品番")
        f_kou = st.text_input("工程名")
        f_no = st.text_input("No")
        f_num = st.number_input("依頼数", min_value=0)
        f_price = st.number_input("単価", min_value=0)
        f_limit = st.text_input("受取日")
        
        if st.button("保存する", use_container_width=True):
            new_row = pd.DataFrame([[f_date, f_shizu, f_hin, f_kou, f_no, f_num, f_price, f_limit, False]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            go_to("home")
    
    st.button("📷 写真からスキャン", use_container_width=True)
    if st.button("戻る"): go_to("home")

# --- ページ：履歴 ---
elif st.session_state.page == "history":
    st.markdown("### 履歴一覧")
    df['売上'] = df['依頼数'].astype(float) * df['単価'].astype(float)
    st.dataframe(df[df['完了']==True][['依頼日', '品番', '売上']], hide_index=True)
    if st.button("戻る"): go_to("home")
