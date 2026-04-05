import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- データ保存・読み込み ---
DATA_FILE = "work_records.csv"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            return df
        except:
            pass
    return pd.DataFrame(columns=["依頼日", "指図", "品番", "工程名", "No", "依頼数", "単価", "受取日", "完了"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# 初期化
if 'page' not in st.session_state:
    st.session_state.page = "home"
df = load_data()

# --- デザイン（CSS）: 画像のデザインを忠実に再現 ---
st.markdown("""
<style>
    /* 明朝体フォントの読み込み */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stApp {
        font-family: 'Noto Serif JP', serif !important;
        background-color: white !important;
        color: #333333 !important;
    }

    /* ロゴ部分 (指定画像) */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
        margin-top: -30px;
    }
    .logo-img {
        width: 100px;
        height: auto;
    }
    .logo-text {
        font-size: 24px;
        line-height: 1.2;
        margin-top: -10px;
        font-weight: bold;
    }

    /* カレンダーエリア（画面上部・グレー背景） */
    .calendar-container {
        background-color: #e0e0e0;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* Streamlit標準の入力枠を消してカレンダーっぽく見せる */
    div[data-testid="stDateInput"] > div {
        background-color: transparent !important;
        border: none !important;
    }

    /* 4月 ¥20000 の横並び */
    .summary-header {
        display: flex;
        justify-content: space-around;
        font-size: 35px;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }

    /* ナビゲーションアイコン */
    .nav-col {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .nav-img {
        width: 60px;
        height: auto;
        cursor: pointer;
    }

    /* 作業中アイテムのグレー背景 */
    .job-item {
        background-color: #d3d3d3;
        border-radius: 20px;
        padding: 8px 15px;
        margin-bottom: 5px;
        font-size: 13px;
        display: flex;
        align-items: center;
        width: 100%;
        color: #333333 !important;
    }

    /* タイトル部分 */
    h3 {
        font-size: 20px !important;
        margin-bottom: 10px !important;
    }

    /* ＋ボタン（右下固定） */
    div.stButton > button:first-child[kind="secondary"] {
        position: fixed;
        bottom: 30px;
        right: 30px;
        border-radius: 50%;
        width: 60px; height: 60px;
        font-size: 30px;
        z-index: 1000;
        background: white;
        border: 1px solid #ccc;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# --- ロゴ表示（my work.） ---
st.markdown("""
<div class='logo-container'>
    <img src='https://loosedrawing.com/illust/1847/' class='logo-img'><br>
    <div class='logo-text'>my work.</div>
</div>
""", unsafe_allow_html=True)

# --- 共通ページ切り替え関数 ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 1枚目：ホーム画面 ---
if st.session_state.page == "home":
    # 1. カレンダーを最上部に配置
    st.markdown("<div class='calendar-container'>", unsafe_allow_html=True)
    st.date_input("calendar", datetime.now(), label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 月と売上
    done_df = df[df['完了'] == True]
    total_sales = (done_df['依頼数'].astype(float) * done_df['単価'].astype(float)).sum()
    st.markdown(f"""
    <div class='summary-header'>
        <div>{datetime.now().month}月</div>
        <div>¥{int(total_sales)}</div>
    </div>
    """, unsafe_allow_html=True)

    # 3. ナビゲーションアイコン
    c1, c2 = st.columns(2)
    with c1: st.markdown("<h1 style='text-align:center; margin:0;'>🏠</h1>", unsafe_allow_html=True)
    with c2:
        if st.button("📖🖋️履歴", key="to_hist", use_container_width=True):
            go_to("history")

    st.divider()

    # 4. 作業中の仕事
    st.markdown("<h3>現在作業中の内職</h3>", unsafe_allow_html=True)
    st.markdown("<small style='margin-left:25px;'>依頼日 指図 品番 工程名 No. 依頼数 受取日</small>", unsafe_allow_html=True)
    
    active_df = df[df['完了'] == False]
    for idx, row in active_df.iterrows():
        cols = st.columns([1, 9])
        with cols[0]:
            if st.checkbox("", key=f"cb_{idx}"):
                df.at[idx, '完了'] = True
                save_data(df)
                st.rerun()
        with cols[1]:
            st.markdown(f"<div class='job-item'>{row['依頼日']} {row['指図']} {row['品番']} {row['工程名']} {row['No']} {row['依頼数']} {row['受取日']}</div>", unsafe_allow_html=True)

    # 5. 終了した仕事（直近3件）
    st.markdown("<br><h3>作業終了した内職</h3>", unsafe_allow_html=True)
    if not done_df.empty:
        for _, row in done_df.tail(3).iterrows():
            st.markdown(f"✅ {row['品番']} - {row['工程名']} (¥{int(row['依頼数']*row['単価'])})", unsafe_allow_html=True)
    else:
        st.info("データがありません")

    # 6. ＋ボタン
    if st.button("＋", key="main_add"):
        go_to("add")

# --- 2枚目：仕事の追加 ---
elif st.session_state.page == "add":
    st.markdown("<h2 style='text-align: center;'>手書き入力</h2>", unsafe_allow_html=True)
    
    # 手書き入力エリア
    f_date = st.text_input("依頼日", datetime.now().strftime("%m/%d"))
    f_hin = st.text_input("品番")
    f_kou = st.text_input("工程名")
    f_num = st.number_input("依頼数", min_value=0)
    f_price = st.number_input("単価", min_value=0)
    
    # 画像にある他の項目も追加
    f_shizu = st.text_input("指図")
    f_no = st.text_input("No")
    f_limit = st.text_input("受取日")

    if st.button("保存する", use_container_width=True):
        new_data = pd.DataFrame([[f_date, f_shizu, f_hin, f_kou, f_no, f_num, f_price, f_limit, False]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        go_to("home")
    
    if st.button("戻る"):
        go_to("home")

# --- 3枚目：履歴一覧 ---
elif st.session_state.page == "history":
    st.markdown("<h2 style='text-align: center;'>売上履歴</h2>", unsafe_allow_html=True)
    
    done_jobs = df[df['完了'] == True]
    if not done_jobs.empty:
        done_jobs['売上'] = done_jobs['依頼数'].astype(float) * done_jobs['単価'].astype(float)
        st.dataframe(done_jobs[['依頼日', '品番', '売上']], hide_index=True)
    else:
        st.write("履歴がありません")
        
    if st.button("ホームに戻る"):
        go_to("home")
