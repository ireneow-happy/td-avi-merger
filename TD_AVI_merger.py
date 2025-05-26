import streamlit as st
import pandas as pd

# 語言切換
lang = st.sidebar.selectbox("Language / 語言", ["English", "中文"])

def t(en, zh):
    return zh if lang == "中文" else en

st.title(t("TD + AVI Map Merger", "TD + AVI 缺陷地圖合併工具"))
st.markdown(t(
    "Upload TD map and AVI map (both in Excel format with row index in the first column).",
    "請上傳 TD map 與 AVI map（Excel 格式，第一欄為 row index）。"
))

# 檔案上傳
td_file = st.file_uploader(t("Upload TD map", "上傳 TD map"), type=["xlsx"])
avi_file = st.file_uploader(t("Upload AVI map", "上傳 AVI map"), type=["xlsx"])

if td_file and avi_file:
    try:
        # 讀取 TD map
        td_df = pd.read_excel(td_file, sheet_name=0)
        td_long = td_df.drop(columns=['Unnamed: 0']).stack().reset_index()
        td_long.columns = ['row', 'column', 'TD']
        td_long_clean = td_long.dropna().astype({'row': int, 'column': int})

        # 讀取 AVI map
        avi_df = pd.read_excel(avi_file, sheet_name=0)
        avi_long = avi_df.drop(columns=['Unnamed: 0']).stack().reset_index()
        avi_long.columns = ['row', 'column', 'AVI defect']
        avi_long_clean = avi_long.dropna().astype({'row': int, 'column': int})

        # 合併資料
        merged_df = pd.merge(td_long_clean, avi_long_clean, on=['row', 'column'], how='left')

        # 顯示結果
        st.success(t("Successfully merged TD and AVI maps!", "成功合併 TD 與 AVI 地圖！"))
        st.dataframe(merged_df)

        # 下載 CSV
        csv = merged_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=t("Download CSV", "下載 CSV"),
            data=csv,
            file_name="merged_td_avi_map.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(t(f"An error occurred: {e}", f"處理過程發生錯誤：{e}"))
