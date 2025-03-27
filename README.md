# UsingLocalOllama 專案

這是一個使用 Django 框架開發的專案，整合了本地 Ollama API 功能。

## 功能特點

- 整合本地 Ollama API
- 支援跨域請求 (CORS)
- RESTful API 設計

## 環境要求

- Python 3.9+
- Django 4.2.20
- Ollama 0.6.2+
- 其他依賴包（見 requirements.txt）

## 安裝步驟

1. 克隆專案並進入專案目錄：
```bash
git clone [your-repository-url]
cd [project-directory]
```

2. 創建並啟動虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安裝依賴包：
```bash
pip install -r requirements.txt
```

4. 確保 Ollama 服務已啟動：
```bash
# 檢查 Ollama 服務狀態
curl http://localhost:11434/api/version
```

5. 運行數據庫遷移：
```bash
python manage.py migrate
```

6. 啟動開發服務器：
```bash
python manage.py runserver
```

## API 使用說明

### Ollama API 端點

- URL: `http://localhost:8000/ollama/chat/`
- 方法: POST
- Content-Type: application/json

#### 請求格式
```json
{
    "prompt": "你的問題或提示",
    "model": "llama2"  // 可選，預設使用 llama2 模型
}
```

#### 回應格式
```json
{
    "status": "success",
    "response": "Ollama 的回應內容"
}
```

#### 使用示例
```bash
curl -X POST http://localhost:8000/ollama/chat/ \
     -H "Content-Type: application/json" \
     -d '{"prompt": "你好，請介紹一下你自己", "model": "llama2"}'
```

### 專案結構
```
.
├── manage.py
├── requirements.txt
├── myproject/          # 專案配置目錄
├── api/               # API 應用
└── ollama_api/        # Ollama API 整合應用
```

### 配置說明

- CORS 設置在 `myproject/settings.py` 中
- API 路由配置在 `myproject/urls.py` 中
- Ollama API 視圖在 `ollama_api/views.py` 中

## 注意事項

1. 確保 Ollama 服務在本地運行（預設端口：11434）
2. 開發環境中已啟用 CORS，允許所有來源
3. 生產環境部署時請適當配置 CORS 設置
4. 確保已下載所需的 Ollama 模型（如 llama2）
