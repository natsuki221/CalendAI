const API_WS_URL = "ws://192.168.0.162:8000/ws";

export const connectWebSocket = (onMessageCallback) => {
    let socket = new WebSocket(API_WS_URL);

    socket.onopen = () => {
        console.log("✅ WebSocket 已連線");
    };

    socket.onmessage = (event) => {
        if (event.data === "PING") {
            console.log("🔄 收到 PING，回應 PONG");
            socket.send("PONG");
            return;
        }
        onMessageCallback(event.data);
    };

    socket.onerror = (error) => {
        console.error("❌ WebSocket 錯誤:", error);
    };

    socket.onclose = () => {
        console.log("🔴 WebSocket 連線已關閉");
    };

    return socket;
};