import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- データ保存・読み込み ---
DATA_FILE = "work_data.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["依頼日", "指図", "品番", "工程名", "No", "依頼数", "単価", "受取日", "完了"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

if 'page' not in st.session_state:
    st.session_state.page = "home"
df = load_data()

# --- デザイン（CSS）: 画像のデザインを強制適用 ---
st.markdown("""
<style>
    /* 明朝体フォントの読み込み */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');

    /* 全体の基本設定 */
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Noto Serif JP', serif !important;
        background-color: white !important;
        color: #333 !important;
    }

    /* ヘッダー部分（4月 ¥20000）のスタイル */
    .header-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-size: 40px;
        margin-top: -20px;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }

    /* カレンダーエリア（グレーの背景） */
    .calendar-box {
        background-color: #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
    }

    /* 完了項目のグレー背景 */
    .job-row {
        background-color: #cccccc;
        border-radius: 20px;
        padding: 10px 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        font-size: 14px;
    }

    /* ＋ボタンを右下に固定 */
    .stButton > button[kind="secondary"] {
        position: fixed;
        bottom: 30px;
        right: 30px;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 30px;
        background: white;
        border: 1px solid #ccc;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# --- ページ表示 ---

# 1. ロゴ（my work.）
st.markdown("<div style='font-size: 20px;'>📖<br>my work.</div>", unsafe_allow_html=True)

if st.session_state.page == "home":
    # 2. ヘッダー（月と金額）を横並びに
    sales = (df[df['完了']==True]['依頼数'].astype(float) * df[df['完了']==True]['単価'].astype(float)).sum()
    st.markdown(f"""
    <div class='header-container'>
        <div>{datetime.now().month}月</div>
        <div>¥{int(sales)}</div>
    </div>
    """, unsafe_allow_html=True)

    # 3. ナビゲーションアイコン
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1: st.markdown("<h1 style='text-align:center;'>🏠</h1>", unsafe_allow_html=True)
    with col_nav2:
        if st.button("📖🖋️", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()

    # 4. カレンダー（常に表示）
    st.markdown("<div class='calendar-box'>", unsafe_allow_html=True)
    # カレンダーのUIとして、常に表示される日付選択を表示
    st.date_input("カレンダー", datetime.now(), label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # 5. 現在作業中の内職
    st.markdown("### 現在作業中の内職")
    st.markdown("<small>依頼日 指図 品番 工程名 No. 依頼数 受取日</small>", unsafe_allow_html=True)
    
    active_jobs = df[df['完了'] == False]
    for idx, row in active_jobs.iterrows():
        cols = st.columns([1, 9])
        with cols[0]:
            if st.checkbox("", key=f"job_{idx}"):
                df.at[idx, '完了'] = True
                save_data(df)
                st.rerun()
        with cols[1]:
            st.markdown(f"""
            <div class='job-row'>
                {row['依頼日']} &nbsp; {row['指図']} &nbsp; {row['品番']} &nbsp; {row['工程名']} &nbsp; {row['No']} &nbsp; {row['依頼数']} &nbsp; {row['受取日']}
            </div>
            """, unsafe_allow_html=True)

    # 6. 作業終了した内職
    st.markdown("### 作業終了した内職")
    done_jobs = df[df['完了'] == True]
    for _, row in done_jobs.tail(5).iterrows():
        st.write(f"✅ {row['品番']} ({row['工程名']})")

    # 7. ＋ボタン（右下固定）
    if st.button("＋"):
        st.session_state.page = "add"
        st.rerun()

elif st.session_state.page == "add":
    st.subheader("新しい仕事の追加")
    # 追加画面のコード（省略せず、必要項目を配置）
    f_date = st.text_input("依頼日", datetime.now().strftime("%m/%d"))
    f_hin = st.text_input("品番")
    # ...（他の入力項目）
    if st.button("保存"):
        # 保存処理
        st.session_state.page = "home"
        st.rerun()
    if st.button("戻る"):
        st.session_state.page = "home"
        st.rerun()
