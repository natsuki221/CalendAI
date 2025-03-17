import json
import requests

# JSON 檔案路徑
json_file = "HUGGINGFACE_KEYs.json"

# Hugging Face API 端點 (Messages API)
API_URL = "https://api-inference.huggingface.co/v1/chat/completions"

def load_api_keys(file_path):
    """從 JSON 檔案載入 API Key。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_api_keys(file_path, data):
    """將 API Key 狀態儲存回 JSON 檔案。"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def check_api_key(api_key):
    """使用 POST 請求測試 API Key 是否有效。"""
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # 測試訊息
    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [{"role": "user", "content": "What is the capital of France?"}],
        "max_tokens": 10
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    status_code = response.status_code

    if status_code == 200:
        return "valid", status_code
    elif status_code == 401:
        return "invalid", status_code
    elif status_code == 403:
        return "quota_exceeded", status_code
    elif status_code == 429:
        return "rate_limited", status_code
    else:
        return f"unknown (HTTP {status_code})", status_code

def test_and_update_keys(file_path):
    """測試每個 API Key 並更新 JSON 狀態。"""
    api_data = load_api_keys(file_path)

    for entry in api_data:
        api_key = entry.get("id")
        if api_key and api_key.startswith("hf_"):
            status, status_code = check_api_key(api_key)
            entry["status"] = status
            print(f"Checked {api_key}: {status} (HTTP {status_code})")

    save_api_keys(file_path, api_data)
    print("API Key 狀態已更新！")

# 執行測試
test_and_update_keys(json_file)