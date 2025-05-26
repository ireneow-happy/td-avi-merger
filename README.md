# TD + AVI Map Merger

A Streamlit web application to merge TD and AVI defect maps based on (row, column) position.

一個基於 Streamlit 的網頁應用程式，可根據 (row, column) 座標合併 TD map 與 AVI 缺陷地圖。

---

## 🌟 Features / 功能

- ✅ Upload TD and AVI maps in Excel format  
  上傳 TD 與 AVI 的 Excel 檔案  
- ✅ Merge data based on row and column coordinates  
  根據行列座標進行資料合併  
- ✅ Multi-language support (English / 中文)  
  支援多語言（英文 / 中文）  
- ✅ Preview and download merged results in CSV  
  預覽並下載合併後的結果（CSV 格式）

---

## 🚀 How to Run / 執行方式

### 🔹 English

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:

   ```bash
   streamlit run app.py
   ```

3. Open your browser to `http://localhost:8501`

---

### 🔹 中文說明

1. 安裝所需套件：

   ```bash
   pip install -r requirements.txt
   ```

2. 執行應用程式：

   ```bash
   streamlit run app.py
   ```

3. 開啟瀏覽器並前往 `http://localhost:8501`

---

## 📦 Deploy Online / 線上部署

You can also deploy this app for free using [Streamlit Community Cloud](https://streamlit.io/cloud). After pushing this project to GitHub:

你也可以使用 [Streamlit Cloud](https://streamlit.io/cloud) 免費部署此應用程式。將專案上傳到 GitHub 後：

1. 登入 Streamlit Cloud
2. 點選「New app」
3. 選擇你的 GitHub repo
4. 設定 `app.py` 為主程式
5. 點選「Deploy」

---

## 📂 File Structure / 檔案結構

```
td-avi-merger/
├── app.py              # 主程式
├── requirements.txt    # 套件需求
└── README.md           # 專案說明
```

---

## 📬 Feedback / 回饋

If you have suggestions or feature requests, feel free to open an [Issue](https://github.com/your-repo/issues).  
如果你有建議或想新增功能，歡迎建立 GitHub 的 [Issue](https://github.com/your-repo/issues)。
