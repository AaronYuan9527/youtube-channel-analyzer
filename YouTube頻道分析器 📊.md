# YouTube頻道分析器 📊

一個功能強大的YouTube頻道數據分析工具，可以快速獲取頻道資訊，包含觀看數、留言、按讚、受眾輪廓等詳細數據分析。

## 🌟 功能特色

### 📈 核心分析功能
- **頻道基本資訊**: 頻道名稱、描述、訂閱數、影片數量
- **觀看數據**: 總觀看數、平均觀看數、觀看趨勢
- **互動分析**: 按讚數、留言數、互動率計算
- **受眾輪廓**: 年齡分布、性別比例、地理位置分析
- **熱門影片**: 影片列表、表現指標、發布時間

### 🎨 用戶體驗
- **現代化介面**: 使用React + Tailwind CSS設計
- **響應式設計**: 完美支援桌面和行動裝置
- **數據視覺化**: 豐富的圖表和統計卡片
- **流暢動畫**: 使用Framer Motion提供優雅的過渡效果

## 🚀 線上演示

**網站地址**: [https://j6h5i7c0gxzp.manussite.space](https://j6h5i7c0gxzp.manussite.space)

## 🛠️ 技術棧

### 後端
- **Flask**: Python Web框架
- **YouTube Data API v3**: 獲取頻道和影片數據
- **YouTube Analytics API**: 獲取詳細分析數據
- **Flask-CORS**: 跨域請求支援
- **SQLAlchemy**: 數據庫ORM

### 前端
- **React 18**: 現代化前端框架
- **Vite**: 快速建置工具
- **Tailwind CSS**: 實用優先的CSS框架
- **shadcn/ui**: 高品質UI組件庫
- **Framer Motion**: 動畫庫
- **Recharts**: 數據視覺化圖表庫
- **Lucide React**: 圖標庫

## 📦 安裝與運行

### 環境要求
- Python 3.8+
- Node.js 16+
- YouTube Data API金鑰

### 後端設置

1. **克隆專案**
```bash
git clone https://github.com/your-username/youtube-channel-analyzer.git
cd youtube-channel-analyzer
```

2. **建立虛擬環境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. **安裝依賴**
```bash
pip install -r requirements.txt
```

4. **配置環境變數**
```bash
# 建立 .env 檔案
cp .env.example .env

# 編輯 .env 檔案，添加您的YouTube API金鑰
YOUTUBE_API_KEY=your_youtube_api_key_here
```

5. **啟動後端服務**
```bash
python src/main.py
```

### 前端設置

1. **進入前端目錄**
```bash
cd frontend  # 如果有獨立的前端目錄
```

2. **安裝依賴**
```bash
npm install
```

3. **啟動開發服務器**
```bash
npm run dev
```

4. **建置生產版本**
```bash
npm run build
```

## 🔧 配置說明

### YouTube API設置

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用YouTube Data API v3
4. 建立API金鑰
5. 將API金鑰添加到環境變數中

### 環境變數

建立 `.env` 檔案並配置以下變數：

```env
# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key

# 數據庫
DATABASE_URL=sqlite:///app.db

# JWT
JWT_SECRET_KEY=your_jwt_secret_key
```

## 📖 API文檔

### 頻道相關API

#### 搜尋頻道
```http
GET /api/channel/search?q=頻道名稱&maxResults=10
```

#### 獲取頻道基本資訊
```http
GET /api/channel/{channelId}/basic
```

#### 獲取頻道統計數據
```http
GET /api/channel/{channelId}/statistics
```

#### 獲取頻道受眾輪廓
```http
GET /api/channel/{channelId}/demographics
```

#### 獲取頻道影片列表
```http
GET /api/channel/{channelId}/videos?maxResults=10&order=viewCount
```

### 系統相關API

#### 健康檢查
```http
GET /api/system/health
```

#### 系統配置
```http
GET /api/system/config
```

## 🎯 使用方法

1. **訪問網站**: 打開瀏覽器訪問部署的網站
2. **搜尋頻道**: 在搜尋框中輸入YouTube頻道名稱或URL
3. **查看分析**: 點擊搜尋按鈕，查看詳細的頻道分析報告
4. **探索數據**: 使用不同的標籤頁查看影片、受眾輪廓和數據分析

## 📊 功能截圖

### 主頁面
- 簡潔的搜尋介面
- 功能特色展示

### 頻道分析
- 頻道基本資訊卡片
- 統計數據視覺化
- 熱門影片列表

### 受眾輪廓
- 年齡分布圓餅圖
- 性別比例條形圖
- 地理位置分析

### 數據分析
- 關鍵指標總覽
- 趨勢分析圖表

## 🤝 貢獻指南

歡迎貢獻代碼！請遵循以下步驟：

1. Fork 這個專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 開發計劃

### 即將推出的功能
- [ ] 頻道比較功能
- [ ] 數據導出（CSV/PDF）
- [ ] 用戶帳戶系統
- [ ] 數據緩存機制
- [ ] 更多視覺化選項
- [ ] 移動應用程式

### 已知問題
- 受眾輪廓數據需要OAuth認證
- API配額限制可能影響大量請求
- 某些私人頻道無法獲取完整數據

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

- [YouTube Data API](https://developers.google.com/youtube/v3) - 提供數據來源
- [React](https://reactjs.org/) - 前端框架
- [Flask](https://flask.palletsprojects.com/) - 後端框架
- [Tailwind CSS](https://tailwindcss.com/) - CSS框架
- [shadcn/ui](https://ui.shadcn.com/) - UI組件庫

## 📞 聯絡方式

如有問題或建議，請通過以下方式聯絡：

- 開啟 [GitHub Issue](https://github.com/your-username/youtube-channel-analyzer/issues)
- 發送郵件至：your-email@example.com

---

⭐ 如果這個專案對您有幫助，請給我們一個星星！

