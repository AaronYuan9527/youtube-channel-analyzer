import streamlit as st

st.set_page_config(page_title="YouTube Channel Analyzer", layout="centered")

st.title("📊 YouTube Channel Analyzer")
st.write(
    """
    輸入一個 YouTube 頻道的 ID 或 URL，我們會幫你分析該頻道的基本數據。
    """
)

channel_input = st.text_input("請輸入 YouTube 頻道 ID 或 URL")

if st.button("開始分析"):
    if not channel_input.strip():
        st.error("請輸入一個有效的頻道 ID 或 URL")
    else:
        with st.spinner("分析中..."):
            st.success("這是測試結果！")
            st.json({
                "channel": channel_input,
                "subscribers": 12345,
                "videos": 67,
                "views": 890123
            })
