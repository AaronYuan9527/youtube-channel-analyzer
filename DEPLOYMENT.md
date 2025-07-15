# 部署指南 🚀

本文檔說明如何將YouTube頻道分析器部署到各種平台。

## 📋 部署選項

### 1. Heroku部署

#### 準備工作
1. 註冊Heroku帳戶
2. 安裝Heroku CLI
3. 準備YouTube API金鑰

#### 部署步驟
```bash
# 登入Heroku
heroku login

# 建立Heroku應用程式
heroku create your-app-name

# 設置環境變數
heroku config:set YOUTUBE_API_KEY=your_api_key
heroku config:set SECRET_KEY=your_secret_key
heroku config:set FLASK_ENV=production

# 部署
git push heroku main
```

#### Procfile
建立`Procfile`檔案：
```
web: python src/main.py
```

### 2. Vercel部署

#### 準備工作
1. 註冊Vercel帳戶
2. 安裝Vercel CLI
3. 配置vercel.json

#### vercel.json配置
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "src/main.py"
    }
  ],
  "env": {
    "YOUTUBE_API_KEY": "@youtube_api_key",
    "SECRET_KEY": "@secret_key"
  }
}
```

#### 部署步驟
```bash
# 安裝Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

### 3. Docker部署

#### 本地Docker
```bash
# 建置映像
docker build -t youtube-analyzer .

# 運行容器
docker run -p 5000:5000 \
  -e YOUTUBE_API_KEY=your_api_key \
  -e SECRET_KEY=your_secret_key \
  youtube-analyzer
```

#### Docker Compose
```bash
# 啟動服務
docker-compose up -d

# 查看日誌
docker-compose logs -f

# 停止服務
docker-compose down
```

### 4. AWS部署

#### AWS Elastic Beanstalk
1. 安裝AWS CLI和EB CLI
2. 初始化Elastic Beanstalk應用程式
3. 配置環境變數
4. 部署應用程式

```bash
# 初始化
eb init

# 建立環境
eb create production

# 設置環境變數
eb setenv YOUTUBE_API_KEY=your_api_key

# 部署
eb deploy
```

#### AWS Lambda + API Gateway
使用Serverless框架部署：

```bash
# 安裝Serverless
npm install -g serverless

# 部署
serverless deploy
```

### 5. Google Cloud Platform

#### App Engine
建立`app.yaml`：
```yaml
runtime: python311

env_variables:
  YOUTUBE_API_KEY: "your_api_key"
  SECRET_KEY: "your_secret_key"
  FLASK_ENV: "production"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

部署：
```bash
gcloud app deploy
```

#### Cloud Run
```bash
# 建置並推送映像
gcloud builds submit --tag gcr.io/PROJECT_ID/youtube-analyzer

# 部署到Cloud Run
gcloud run deploy --image gcr.io/PROJECT_ID/youtube-analyzer \
  --platform managed \
  --set-env-vars YOUTUBE_API_KEY=your_api_key
```

## 🔧 環境變數配置

### 必需的環境變數
```env
YOUTUBE_API_KEY=your_youtube_api_key
SECRET_KEY=your_flask_secret_key
```

### 可選的環境變數
```env
FLASK_ENV=production
DATABASE_URL=your_database_url
JWT_SECRET_KEY=your_jwt_secret
CORS_ORIGINS=*
LOG_LEVEL=INFO
```

## 📊 監控和日誌

### 健康檢查
應用程式提供健康檢查端點：
```
GET /api/system/health
```

### 日誌配置
- 使用Python logging模組
- 支援不同日誌級別
- 可配置日誌輸出格式

### 監控建議
- 設置應用程式監控（如New Relic、DataDog）
- 配置錯誤追蹤（如Sentry）
- 監控API配額使用情況

## 🔒 安全考量

### API金鑰安全
- 使用環境變數存儲API金鑰
- 定期輪換API金鑰
- 限制API金鑰權限

### HTTPS配置
- 在生產環境中強制使用HTTPS
- 配置SSL證書
- 設置安全標頭

### CORS配置
- 根據需要限制CORS來源
- 避免使用通配符（*）在生產環境

## 🚀 性能優化

### 緩存策略
- 實施Redis緩存
- 緩存API響應
- 設置適當的緩存過期時間

### 數據庫優化
- 使用連接池
- 實施數據庫索引
- 定期清理舊數據

### CDN配置
- 使用CDN加速靜態資源
- 配置適當的緩存標頭
- 壓縮靜態資源

## 🔄 CI/CD流程

### GitHub Actions
專案已包含GitHub Actions工作流程：
- 自動測試
- 代碼品質檢查
- 自動部署

### 部署流程
1. 推送代碼到main分支
2. 自動運行測試
3. 建置前端資源
4. 部署到生產環境

## 📈 擴展性考量

### 水平擴展
- 使用負載均衡器
- 部署多個應用程式實例
- 實施會話存儲

### 數據庫擴展
- 使用數據庫讀寫分離
- 實施數據庫分片
- 考慮使用NoSQL數據庫

## 🆘 故障排除

### 常見問題
1. **API配額超限**
   - 檢查YouTube API配額
   - 實施請求限制
   - 使用緩存減少API調用

2. **靜態檔案404錯誤**
   - 檢查靜態檔案路徑
   - 確認建置過程正確
   - 驗證Flask靜態檔案配置

3. **CORS錯誤**
   - 檢查CORS配置
   - 確認前端URL在允許列表中
   - 驗證預檢請求處理

### 日誌分析
- 檢查應用程式日誌
- 監控錯誤率
- 分析性能指標

---

如有部署問題，請參考[故障排除指南](TROUBLESHOOTING.md)或提交Issue。

