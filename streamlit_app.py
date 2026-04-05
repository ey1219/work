import streamlit as st
import pandas as pd
from datetime import datetime, date

# ページ設定
st.set_page_config(page_title="Work Manager", layout="centered")

st.title("📱 お仕事・売上管理")

# タブ分け
tab1, tab2 = st.tabs(["📊 目標計算", "💰 売上管理"])

with tab1:
    st.subheader("案件シミュレーション")
    name = st.text_input("案件名", value="新規案件")
    
    col1, col2 = st.columns(2)
    with col1:
        total_qty = st.number_input("総納品数", min_value=1, value=100)
        unit_price = st.number_input("単価 (円)", min_value=0, value=500)
    with col2:
        start_d = st.date_input("開始日", date.today())
        end_d = st.date_input("納期", date.today())

    days = (end_d - start_d).days + 1
    
    if days > 0:
        daily_target = total_qty / days
        total_amount = total_qty * unit_price
        
        st.metric("1日の目標", f"{daily_target:.1f} 個")
        st.metric("合計金額", f"¥{total_amount:,}")
        
        if st.button("記録する", use_container_width=True):
            if 'db' not in st.session_state: st.session_state.db = []
            st.session_state.db.append({"月": end_d.strftime("%Y/%m"), "名": name, "合計": total_amount})
            st.success("保存しました！")
    else:
        st.warning("納期を正しく設定してください")

with tab2:
    if 'db' in st.session_state:
        df = pd.DataFrame(st.session_state.db)
        st.write(df)
    else:
        st.info("データがありません")
