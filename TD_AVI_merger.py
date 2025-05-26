import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

# 語言切換
lang = st.sidebar.selectbox("Language / 語言", ["English", "中文"])

def t(en, zh):
    return zh if lang == "中文" else en

st.title(t("TD + AVI Map Merger", "TD + AVI 缺陷地圖合併工具"))

# 說明與圖片
st.markdown(t(
    "**This tool analyzes the relationship between AVI defect distribution and Touch Down (TD) order.** "
    "Before running the program, please make sure the probing map and AVI defect map are both aligned to the same origin (top-left corner).",
    "**本工具用於分析 AVI 缺陷分布與 Touch Down（TD）順序之間的關係。** "
    "執行程式前，請先確認 Probing Map 與 AVI Map 的零點座標均已對齊至左上角。"
))
image = Image.open("origin_alignment_example.png")
st.image(image, caption=t("Example of top-left (0,0) alignment", "零點對齊示意圖（左上角為 (0,0)）"), width=500)

st.markdown("---")

# 上傳
td_file = st.file_uploader(t("Upload TD map", "上傳 TD map"), type=["xlsx"])
avi_file = st.file_uploader(t("Upload AVI map", "上傳 AVI map"), type=["xlsx"])

if td_file and avi_file:
    try:
        # 處理 TD
        td_df = pd.read_excel(td_file, sheet_name=0)
        td_long = td_df.drop(columns=['Unnamed: 0']).stack().reset_index()
        td_long.columns = ['row', 'column', 'TD']
        td_long_clean = td_long.dropna().astype({'row': int, 'column': int})

        # 處理 AVI
        avi_df = pd.read_excel(avi_file, sheet_name=0)
        avi_long = avi_df.drop(columns=['Unnamed: 0']).stack().reset_index()
        avi_long.columns = ['row', 'column', 'AVI defect']
        avi_long_clean = avi_long.dropna().astype({'row': int, 'column': int})

        # 合併
        merged_df = pd.merge(td_long_clean, avi_long_clean, on=['row', 'column'], how='left')
        st.success(t("Successfully merged TD and AVI maps!", "成功合併 TD 與 AVI 地圖！"))
        st.dataframe(merged_df)

        # 下載
        csv = merged_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=t("Download CSV", "下載 CSV"),
            data=csv,
            file_name="merged_td_avi_map.csv",
            mime="text/csv"
        )

        # 缺陷分析
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

        # 圖表視覺化
fig, ax = plt.subplots(figsize=(14, 4))
ax.bar(td_summary_sorted["TD"].astype(str), td_summary_sorted["Defect Qty"], color="skyblue")
ax.set_title(t("Defect Quantity by TD", "各 TD 缺陷數量"))
ax.set_xlabel("TD")
ax.set_ylabel(t("Defect Qty", "缺陷數量"))
plt.xticks(rotation=90, fontsize=8)
st.pyplot(fig)

    except Exception as e:
        st.error(t(f"An error occurred: {e}", f"處理過程發生錯誤：{e}"))
