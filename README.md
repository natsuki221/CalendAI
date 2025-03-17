![CalendAI Brand](Brand_CalendAI_Rounded.png)
# CalendAI 🗓️

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

CalendAI 是一個結合 **FastAPI**（後端）與 **React**（前端）的行程規劃系統。使用者只需在前端輸入想進行的活動與需求，後端即會透過 Hugging Face API（大型語言模型）產生合宜的行程建議，並藉由 **WebSocket** 實現即時互動。

---

## 📋 目錄
- [CalendAI 🗓️](#calendai-️)
  - [📋 目錄](#-目錄)
  - [✨ 功能特色](#-功能特色)
  - [📂 專案結構](#-專案結構)
  - [🔧 環境需求](#-環境需求)
  - [⚙️ 安裝與執行](#️-安裝與執行)
    - [1. 後端 (FastAPI)](#1-後端-fastapi)
    - [2. 前端 (React)](#2-前端-react)
  - [🌐 後端 API 說明](#-後端-api-說明)
  - [📑 其他檔案說明](#-其他檔案說明)
  - [⚠️ 注意事項](#️-注意事項)
  - [📝 授權條款](#-授權條款)
  - [🔮 未來規劃](#-未來規劃)

---

## ✨ 功能特色
1. **多元排程**  
   - 使用者可輸入活動開始／結束時間、地點、需求等，系統自動產生全天行程。  

2. **Hugging Face API 整合**  
   - 運用 `HUGGINGFACE_KEYs.json` 內的有效金鑰，連線至大型語言模型生成個人化行程。  

3. **WebSocket 即時互動**  
   - 前端與伺服器雙向傳遞訊息，享受無縫的即時行程更新體驗。  

4. **前後端獨立運行**  
   - 前端採用 React、後端使用 FastAPI，可分別部署、測試與維護。  

---

## 📂 專案結構
```
natsuki221-calendai_server_side/
├── api.py                   # FastAPI 主程式 (後端 API)
├── api_test.py              # 測試 API Key 狀態用的腳本
├── calender.md              # 範例行程 Markdown
├── requirements.txt         # Python 相依套件列表
├── schedule_assistant_system_prompt.txt  # 後端行程助理的 System Prompt
└── frontend/
    ├── audit-report.json    # 依賴套件安全性檢測報告
    └── calendai/
        ├── README.md        # React App 預設生成的 README
        ├── package.json     # 前端 NPM 相依套件資訊
        ├── package-lock.json
        ├── public/          # 前端靜態檔案
        └── src/             # React 原始碼 (主要程式邏輯)
            ├── App.js
            ├── SchedulePlanner.js
            └── ... (其他 React 組件)
```

---

## 🔧 環境需求
- **Python** 3.8+  
- **Node.js** 14+（建議 16 或更新版本）  
- 可用的 **Hugging Face API Key**（存放於 `HUGGINGFACE_KEYs.json`，並將 `"status"` 設為 `"valid"`）

---

## ⚙️ 安裝與執行

### 1. 後端 (FastAPI)

1. **安裝套件**  
   ```bash
   cd natsuki221-calendai_server_side
   pip install -r requirements.txt
   ```

2. **設定 Hugging Face API 金鑰**  
   - 在 `HUGGINGFACE_KEYs.json` 中，新增或維護可用金鑰，並將 `"status"` 設為 `"valid"`：
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
   - 在瀏覽器開啟 [http://localhost:8000/docs](http://localhost:8000/docs) 以查看自動生成的 API 文件。

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
   - 預設服務埠為 [http://localhost:3000](http://localhost:3000)  
   - 編輯程式碼時，頁面會自動重新載入。

3. **打包部署**  
   ```bash
   npm run build
   ```
   - 產生的檔案放置於 `build/`，可直接使用靜態伺服器或整合後端進行部署。

---

## 🌐 後端 API 說明

1. **POST /schedule/**  
   - **說明**：接收使用者活動資訊，並透過 Hugging Face API 生成行程安排。  
   - **參數格式 (JSON)**：
     ```json
     {
       "activities": "想要進行的活動描述"
     }
     ```
   - **成功回應 (JSON)**：
     ```json
     {
       "schedule": "生成的行程文字"
     }
     ```

2. **WebSocket /ws**  
   - **說明**：讓客戶端能即時傳送活動描述並獲得行程回饋。  
   - **用法**：
     - 與 `/ws` 建立 WebSocket 連線後，即可傳送訊息並接收行程。  
     - 伺服器會定時發送 `"PING"`，請客戶端回傳 `"PONG"` 以保持連線。  

---

## 📑 其他檔案說明
- **`api_test.py`**  
  測試所有 `HUGGINGFACE_KEYs.json` 內金鑰可用性，並自動更新金鑰狀態（`valid`, `invalid`, `quota_exceeded`, `rate_limited` 等）。  
- **`calender.md`**  
  範例行程的 Markdown 文件，可參考其排版與呈現方式。  
- **`audit-report.json`**  
  前端使用 `npm audit` 產生的安全性檢測報告。  

---

## ⚠️ 注意事項
- 如有多組 Hugging Face API Key，系統會隨機選擇 status 為 `"valid"` 的金鑰進行行程生成。若無可用金鑰，將拋出錯誤。  
- WebSocket 模式下，前端需自行維護 `PING`/`PONG` 邏輯以防連線中斷。  

---

## 📝 授權條款
本專案程式碼採用 **MIT License**。

---

## 🔮 未來規劃
- **使用者認證**：如 OAuth，以便個人化行程保存與查詢。  
- **更多行程優化策略**：提供移動距離最短、優先重要事項、或支援多時區等自訂參數。  
- **支援更多模型**：如 GPT、Llama 等，以增強行程建議的多樣化。  
