# YouTube頻道資訊系統 - API規格文件

## API基本資訊

**基礎URL**: `http://localhost:5000/api`  
**認證方式**: OAuth 2.0 (Google)  
**數據格式**: JSON  
**HTTP方法**: GET, POST  

## 認證端點

### 1. 初始化OAuth認證
**端點**: `GET /auth/login`  
**描述**: 重定向用戶到Google OAuth認證頁面  
**參數**: 無  
**響應**: 重定向到Google OAuth頁面  

### 2. OAuth回調處理
**端點**: `GET /auth/callback`  
**描述**: 處理Google OAuth回調並獲取access token  
**參數**: 
- `code` (query): OAuth授權碼
- `state` (query): CSRF保護狀態參數

**響應**:
```json
{
  "success": true,
  "message": "認證成功",
  "user": {
    "id": "string",
    "email": "string",
    "name": "string"
  }
}
```

### 3. 登出
**端點**: `POST /auth/logout`  
**描述**: 清除用戶認證狀態  
**響應**:
```json
{
  "success": true,
  "message": "已成功登出"
}
```

## 頻道資訊端點

### 1. 搜尋頻道
**端點**: `GET /channel/search`  
**描述**: 根據關鍵字搜尋YouTube頻道  
**參數**:
- `q` (query, required): 搜尋關鍵字
- `maxResults` (query, optional): 最大結果數量，預設10

**響應**:
```json
{
  "success": true,
  "data": {
    "channels": [
      {
        "channelId": "string",
        "title": "string",
        "description": "string",
        "thumbnails": {
          "default": "url",
          "medium": "url",
          "high": "url"
        },
        "subscriberCount": "number",
        "videoCount": "number"
      }
    ],
    "totalResults": "number"
  }
}
```

### 2. 獲取頻道基本資訊
**端點**: `GET /channel/{channelId}/basic`  
**描述**: 獲取指定頻道的基本資訊  
**參數**:
- `channelId` (path, required): YouTube頻道ID

**響應**:
```json
{
  "success": true,
  "data": {
    "channelId": "string",
    "title": "string",
    "description": "string",
    "customUrl": "string",
    "publishedAt": "2023-01-01T00:00:00Z",
    "thumbnails": {
      "default": "url",
      "medium": "url",
      "high": "url"
    },
    "statistics": {
      "viewCount": "number",
      "subscriberCount": "number",
      "videoCount": "number"
    },
    "contentDetails": {
      "uploadsPlaylistId": "string"
    },
    "brandingSettings": {
      "channel": {
        "title": "string",
        "description": "string",
        "keywords": "string",
        "country": "string"
      }
    }
  }
}
```

### 3. 獲取頻道統計數據
**端點**: `GET /channel/{channelId}/statistics`  
**描述**: 獲取頻道的詳細統計數據和趨勢分析  
**參數**:
- `channelId` (path, required): YouTube頻道ID
- `startDate` (query, optional): 開始日期 (YYYY-MM-DD)
- `endDate` (query, optional): 結束日期 (YYYY-MM-DD)
- `metrics` (query, optional): 指定要獲取的指標，預設為 "views,estimatedMinutesWatched,likes,comments"

**響應**:
```json
{
  "success": true,
  "data": {
    "period": {
      "startDate": "2023-01-01",
      "endDate": "2023-12-31"
    },
    "totalMetrics": {
      "views": "number",
      "estimatedMinutesWatched": "number",
      "likes": "number",
      "comments": "number",
      "shares": "number"
    },
    "dailyData": [
      {
        "date": "2023-01-01",
        "views": "number",
        "estimatedMinutesWatched": "number",
        "likes": "number",
        "comments": "number"
      }
    ],
    "growthRate": {
      "views": "percentage",
      "subscribers": "percentage",
      "estimatedMinutesWatched": "percentage"
    }
  }
}
```

### 4. 獲取受眾輪廓數據
**端點**: `GET /channel/{channelId}/demographics`  
**描述**: 獲取頻道的受眾輪廓分析數據  
**參數**:
- `channelId` (path, required): YouTube頻道ID
- `startDate` (query, optional): 開始日期 (YYYY-MM-DD)
- `endDate` (query, optional): 結束日期 (YYYY-MM-DD)

**響應**:
```json
{
  "success": true,
  "data": {
    "period": {
      "startDate": "2023-01-01",
      "endDate": "2023-12-31"
    },
    "ageGroups": [
      {
        "ageGroup": "18-24",
        "viewsPercentage": "number",
        "watchTimePercentage": "number"
      },
      {
        "ageGroup": "25-34",
        "viewsPercentage": "number",
        "watchTimePercentage": "number"
      }
    ],
    "gender": {
      "male": {
        "viewsPercentage": "number",
        "watchTimePercentage": "number"
      },
      "female": {
        "viewsPercentage": "number",
        "watchTimePercentage": "number"
      }
    },
    "topCountries": [
      {
        "country": "US",
        "countryName": "United States",
        "viewsPercentage": "number",
        "watchTimePercentage": "number"
      }
    ],
    "deviceTypes": [
      {
        "deviceType": "mobile",
        "viewsPercentage": "number",
        "watchTimePercentage": "number"
      }
    ]
  }
}
```

### 5. 獲取熱門影片
**端點**: `GET /channel/{channelId}/videos`  
**描述**: 獲取頻道的熱門影片列表  
**參數**:
- `channelId` (path, required): YouTube頻道ID
- `maxResults` (query, optional): 最大結果數量，預設10
- `order` (query, optional): 排序方式 (date, rating, relevance, title, videoCount, viewCount)

**響應**:
```json
{
  "success": true,
  "data": {
    "videos": [
      {
        "videoId": "string",
        "title": "string",
        "description": "string",
        "publishedAt": "2023-01-01T00:00:00Z",
        "thumbnails": {
          "default": "url",
          "medium": "url",
          "high": "url"
        },
        "statistics": {
          "viewCount": "number",
          "likeCount": "number",
          "commentCount": "number"
        },
        "duration": "PT4M13S",
        "engagementRate": "percentage"
      }
    ],
    "totalResults": "number"
  }
}
```

### 6. 比較多個頻道
**端點**: `POST /channel/compare`  
**描述**: 比較多個頻道的統計數據  
**請求體**:
```json
{
  "channelIds": ["channelId1", "channelId2", "channelId3"],
  "metrics": ["views", "subscriberCount", "videoCount"],
  "startDate": "2023-01-01",
  "endDate": "2023-12-31"
}
```

**響應**:
```json
{
  "success": true,
  "data": {
    "comparison": [
      {
        "channelId": "string",
        "channelTitle": "string",
        "metrics": {
          "views": "number",
          "subscriberCount": "number",
          "videoCount": "number"
        }
      }
    ],
    "period": {
      "startDate": "2023-01-01",
      "endDate": "2023-12-31"
    }
  }
}
```

## 系統端點

### 1. 健康檢查
**端點**: `GET /health`  
**描述**: 檢查API服務狀態  
**響應**:
```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### 2. API配額狀態
**端點**: `GET /quota/status`  
**描述**: 檢查YouTube API配額使用狀況  
**響應**:
```json
{
  "success": true,
  "data": {
    "quotaUsed": "number",
    "quotaLimit": "number",
    "quotaRemaining": "number",
    "resetTime": "2023-01-02T00:00:00Z"
  }
}
```

## 錯誤響應格式

所有API端點在發生錯誤時都會返回統一的錯誤格式：

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "錯誤描述",
    "details": "詳細錯誤資訊（可選）"
  }
}
```

### 常見錯誤碼

| 錯誤碼 | HTTP狀態碼 | 描述 |
|--------|------------|------|
| INVALID_CHANNEL_ID | 400 | 無效的頻道ID |
| CHANNEL_NOT_FOUND | 404 | 找不到指定頻道 |
| UNAUTHORIZED | 401 | 未授權存取 |
| QUOTA_EXCEEDED | 429 | API配額超限 |
| INTERNAL_ERROR | 500 | 內部伺服器錯誤 |
| YOUTUBE_API_ERROR | 502 | YouTube API錯誤 |

## 速率限制

- 每個IP地址每分鐘最多100個請求
- 每個認證用戶每分鐘最多200個請求
- 超出限制時返回HTTP 429狀態碼

## 數據緩存

- 頻道基本資訊：緩存1小時
- 統計數據：緩存30分鐘
- 受眾輪廓數據：緩存6小時
- 影片列表：緩存1小時

## 版本控制

API使用URL路徑版本控制：
- 當前版本：`/api/v1/`
- 向後兼容性：至少支援前一個主要版本

這個API規格提供了完整的端點定義，確保前後端開發團隊能夠清楚了解每個API的功能、參數和響應格式。

