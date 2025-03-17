import json
import random
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from openai import OpenAI
import asyncio
from starlette.websockets import WebSocketState

# 設定檔案路徑
API_KEYS_FILE = "HUGGINGFACE_KEYs.json"
PROMPT_FILE = "schedule_assistant_system_prompt.txt"

def load_valid_api_key():
    """從 JSON 檔案載入可用的 API Key（status 為 'valid'）。"""
    try:
        with open(API_KEYS_FILE, "r", encoding="utf-8") as f:
            api_data = json.load(f)

        # 過濾出所有 status = "valid" 的金鑰
        valid_keys = [entry["id"] for entry in api_data if entry.get("status") == "valid"]

        if not valid_keys:
            raise ValueError("No valid API keys available.")

        # 隨機選擇一個 API Key（如果有多個）
        return random.choice(valid_keys)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load API keys: {str(e)}")

def load_system_prompt():
    """從文本檔案載入 System Prompt。"""
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load system prompt: {str(e)}")

# 讀取 API Key 和 System Prompt
API_KEY = load_valid_api_key()
SYSTEM_PROMPT = load_system_prompt()

# 初始化 FastAPI
app = FastAPI()

# 設定 Hugging Face API 客戶端
client = OpenAI(
    base_url="https://router.huggingface.co/hf-inference/v1",
    api_key=API_KEY
)

# 定義請求格式
class ChatRequest(BaseModel):
    activities: str  # 使用者輸入的活動

@app.post("/schedule/")
async def generate_schedule(request: ChatRequest):
    """接收使用者的活動內容，並透過 Hugging Face API 生成行程安排。"""
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.activities}
        ]

        completion = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=messages,
            max_tokens=1024
        )

        return {"schedule": completion.choices[0].message.content}  # ✅ 修正 `.content`

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 連線，用於即時處理活動並回應行程"""
    await websocket.accept()
    print(f"✅ WebSocket 連線已建立: {websocket.client}")

    try:
        while True:
            try:
                # 增加超時時間，避免 WebSocket 過快被關閉
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)

                # 如果客戶端回應 "PONG"，則繼續保持連線
                if data == "PONG":
                    print("🔄 客戶端回應 PONG，保持 WebSocket 連線")
                    continue  

            except asyncio.TimeoutError:
                print("🔄 WebSocket 保持活躍，發送 PING")
                await websocket.send_text("PING")
                continue

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": data}
            ]

            completion = client.chat.completions.create(
                model="microsoft/Phi-3.5-mini-instruct",
                messages=messages,
                max_tokens=4096
            )
            await websocket.send_text(completion.choices[0].message.content)

    except WebSocketDisconnect:
        print("⚠️ WebSocket 連線已斷開")
    except Exception as e:
        print(f"❌ WebSocket 錯誤: {e}")
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
            print("🔴 WebSocket 連線已安全關閉")
        
# 啟動方式（執行以下指令）
# uvicorn api_test:app --host 0.0.0.0 --port 8000 --reload