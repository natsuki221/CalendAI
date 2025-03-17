import React, { useState, useEffect, useRef } from "react";
import { connectWebSocket } from "./api";
import ReactMarkdown from "react-markdown";
import {
  TextField,
  Button,
  CircularProgress,
  Alert,
  Container,
  Typography,
  Box,
  Fade
} from "@mui/material";

const SchedulePlanner = () => {
  const [activities, setActivities] = useState("");
  const [schedule, setSchedule] = useState("");
  const [socket, setSocket] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const reconnectAttemptsRef = useRef(0);
  const MAX_RECONNECT_ATTEMPTS = 5;

  useEffect(() => {
    let ws;

    const connect = () => {
      ws = connectWebSocket((message) => {
        if (message !== "PING") {
          setSchedule(message);
          setLoading(false);
        }
      });

      ws.onerror = () => {
        setError("⚠️ WebSocket 連線失敗，請檢查伺服器狀態。");
        setLoading(false);
      };

      ws.onclose = () => {
        setError("⚠️ 伺服器已斷開連線，正在嘗試重新連線...");
        setTimeout(() => {
          if (reconnectAttemptsRef.current < MAX_RECONNECT_ATTEMPTS) {
            reconnectAttemptsRef.current++;
            console.log(`♻️ WebSocket 重連嘗試 ${reconnectAttemptsRef.current}/${MAX_RECONNECT_ATTEMPTS}`);
            connect();
          } else {
            setError("❌ 無法連線至 WebSocket 伺服器，請稍後再試。");
          }
        }, 5000);
      };

      setSocket(ws);
    };

    connect();

    return () => {
      if (ws) {
        console.log("🛑 清理 WebSocket 連線");
        ws.close();
      }
    };
  }, []); // 只在組件掛載時運行一次

  const handleGenerate = () => {
    if (socket && socket.readyState === WebSocket.OPEN && activities.trim()) {
      setLoading(true);
      setError(""); // 清除舊錯誤
      try {
        socket.send(activities);
      } catch (err) {
        setError("⚠️ 發送請求時發生錯誤，請稍後再試。");
        setLoading(false);
      }
    } else {
      setError("⚠️ 連線異常，請重新整理頁面或稍後再試。");
    }
  };

  return (
    <Container maxWidth="sm" sx={{ textAlign: "center", py: 4 }}>
      <Typography variant="h4" gutterBottom>
        行程規劃助手 (WebSocket)
      </Typography>

      {/* 多行文字輸入框 */}
      <TextField
        label="輸入你的活動清單"
        multiline
        rows={5}
        fullWidth
        value={activities}
        onChange={(e) => setActivities(e.target.value)}
        sx={{ my: 2 }}
      />

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Button
        variant="contained"
        color="primary"
        onClick={handleGenerate}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? "生成中..." : "生成行程"}
      </Button>

      {loading && (
        <Box sx={{ display: "flex", justifyContent: "center", my: 2 }}>
          <CircularProgress />
        </Box>
      )}

      {schedule && (
        <Fade in={true}>
          <Box
            sx={{
              mt: 3,
              p: 2,
              border: "1px solid #ddd",
              borderRadius: "8px",
              bgcolor: "#f9f9f9",
            }}
          >
            <Typography variant="h6">📅 你的行程：</Typography>
            <ReactMarkdown>{schedule}</ReactMarkdown>
          </Box>
        </Fade>
      )}
    </Container>
  );
};

export default SchedulePlanner;