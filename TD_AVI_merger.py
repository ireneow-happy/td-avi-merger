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

        # 合併
        merged_df = pd.merge(td_long_clean, avi_long_clean, on=['row', 'column'], how='left')

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

        # ===== 分析功能 =====
        st.header(t("Defect Analysis", "缺陷分析"))

        available_defects = merged_df["AVI defect"].dropna().unique()
        selected_defect = st.selectbox(t("Select AVI defect", "選擇 AVI 缺陷代碼"), sorted(available_defects))

        sort_option = st.radio(
            t("Sort by", "排序方式"),
            options=[t("TD order", "依 TD 順序"), t("Defect Qty descending", "依缺陷數量降冪")],
            horizontal=True
        )

        filtered = merged_df[merged_df["AVI defect"] == selected_defect]
        td_summary = filtered.groupby("TD").size().reset_index(name="Defect Qty")

        if sort_option == "TD order" or sort_option == "依 TD 順序":
            td_summary_sorted = td_summary.sort_values(by="TD", ascending=True)
        else:
            td_summary_sorted = td_summary.sort_values(by="Defect Qty", ascending=False)

        st.markdown(t(
            f"Defect count for: **{selected_defect}**",
            f"缺陷代碼 **{selected_defect}** 對應各 TD 數量如下："
        ))
        st.dataframe(td_summary_sorted)

    except Exception as e:
        st.error(t(f"An error occurred: {e}", f"處理過程發生錯誤：{e}"))
