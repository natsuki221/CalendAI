# CalendAI 專案

此專案結合 **FastAPI**（後端）與 **React**（前端），提供一個行程規劃與排程的系統。使用者可在前端輸入想要進行的活動、需求時間、地點等，後端會透過 Hugging Face API（大型語言模型）來協助生成合理的行程安排，並以 WebSocket 進行即時互動。

## 功能特色

1. **多元排程**：可根據使用者提供的活動，包含開始/結束時間、地點與需求，生成全天時程。
2. **Hugging Face API 整合**：透過 `HUGGINGFACE_KEYs.json` 中的有效金鑰，連線 Hugging Face 大型語言模型進行行程生成。
3. **WebSocket 即時互動**：使用者可在前端即時傳遞活動內容，伺服器即時回應完整行程安排。
4. **前後端獨立運行**：前端使用 React 建置，後端使用 FastAPI 建置，可分別部署與維護。

---

## 專案結構

```
natsuki221-calendai_server_side/
├── api.py                   # FastAPI 主程式 (後端 API)
├── api_test.py              # 測試 API Key 狀態用的腳本
├── calender.md              # 範例行程 Markdown
├── requirements.txt         # Python 相依套件列表
├── schedule_assistant_system_prompt.txt  # 後端行程助理使用的 System Prompt
└── frontend/
    ├── audit-report.json    # 依賴套件安全性檢測報告
    └── calendai/
        ├── README.md        # React App 預設生成的 README
        ├── package.json     # 前端 NPM 相依套件資訊
        ├── package-lock.json
        ├── public/          # 前端靜態檔案
        └── src/             # React App 原始碼
            ├── App.js
            ├── SchedulePlanner.js
            └── ... (其他 React 組件)
```

---

## 環境需求

- Python 3.8+  
- Node.js 14+（建議 16 或更高）
- 可用的 Hugging Face API Key（儲存在 `HUGGINGFACE_KEYs.json`，並將 status 設為 `"valid"`）

---

## 安裝與執行

### 1. 後端 (FastAPI)

1. **安裝套件**

   ```bash
   cd natsuki221-calendai_server_side
   pip install -r requirements.txt
   ```
   
2. **設置 Hugging Face API 金鑰**

   - 在 `HUGGINGFACE_KEYs.json` 新增或維護可用金鑰，並將 `"status"` 設為 `"valid"`。
   - 例如：
     ```json
     [
       {
         "id": "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
         "status": "valid"
       }
     ]
     ```

3. **啟動後端伺服器**

   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   預設情況下，你可以在瀏覽器開啟 `http://localhost:8000/docs` 檢視自動生成的 API 文件。

### 2. 前端 (React)

1. **安裝相依套件**

   ```bash
   cd frontend/calendai
   npm install
   ```

2. **本地開發運行**

   ```bash
   npm start
   ```
   - 伺服器預設使用連接埠 3000（可在瀏覽器中開啟 `http://localhost:3000` 查看）。
   - 修改程式碼時，頁面會自動重新載入。

3. **打包部署**

   ```bash
   npm run build
   ```
   - 產出檔案預設會放在 `build/` 資料夾，可上傳至任意靜態網站伺服器或整合至後端。

---

## 後端 API 說明

1. **POST /schedule/**  
   - **說明**：接收使用者活動資訊，並呼叫 Hugging Face API 生成行程安排。  
   - **參數格式**（JSON）：
     ```json
     {
       "activities": "想要進行的活動描述"
     }
     ```
   - **成功回應**（JSON）：
     ```json
     {
       "schedule": "生成的行程文字"
     }
     ```

2. **WebSocket /ws**  
   - **說明**：透過 WebSocket 實現即時互動的行程生成。  
   - **用法**：
     - 客戶端與 `/ws` 建立連線後，傳入文字訊息即可獲得行程回應。
     - 若連線超時，伺服器會定時回傳 `"PING"`，客戶端須回傳 `"PONG"` 以保持連線。

---

## 其他檔案說明

- **`api_test.py`**  
  提供測試所有 `HUGGINGFACE_KEYs.json` 內金鑰可用性的功能，並自動更新每支金鑰的狀態（`valid`, `invalid`, `quota_exceeded`, `rate_limited` 等）。

- **`calender.md`**  
  展示範例的行程安排 Markdown 檔。可參考其格式了解行程生成的最終呈現方式。

- **`audit-report.json`**  
  前端使用 `npm audit` 進行安全性檢測的報告檔案。

---

## 注意事項

- 若有多組 Hugging Face API Key，程式會隨機選擇 **status** 為 `"valid"` 的一支來執行行程生成。若無可用金鑰，將拋出錯誤。
- WebSocket 在前端可能需要自行撰寫相對應的邏輯（`PING`/`PONG`）以維持連線穩定。

---

## 授權條款

本專案程式碼採用 **MIT License** 。

---

## 未來規劃

- 增加使用者認證（如 OAuth）以便個人化行程保存與查詢。
- 提供更多行程優化選項（如：移動距離最短、優先重要事項、支援多時區等）。
- 開放更多模型選擇（如 GPT、Llama 等）以增強行程建議的多樣化。
