# YouTube頻道資訊系統 - 數據庫設計

## 數據庫選擇

考慮到系統的需求和複雜度，我們選擇使用 **SQLite** 作為開發和小規模部署的數據庫，並支援遷移到 **PostgreSQL** 用於生產環境。

### SQLite vs PostgreSQL

| 特性 | SQLite | PostgreSQL |
|------|--------|------------|
| 部署複雜度 | 簡單 | 中等 |
| 並發支援 | 有限 | 優秀 |
| 數據類型 | 基本 | 豐富 |
| 擴展性 | 有限 | 優秀 |
| 適用場景 | 開發/小規模 | 生產環境 |

## 數據庫結構設計

### 1. 用戶表 (users)

儲存OAuth認證用戶的基本資訊。

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    picture_url TEXT,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**欄位說明**:
- `google_id`: Google OAuth用戶唯一識別碼
- `access_token`: YouTube API存取令牌
- `refresh_token`: 用於刷新access_token
- `token_expires_at`: 令牌過期時間

### 2. 頻道表 (channels)

儲存YouTube頻道的基本資訊，用於緩存和快速查詢。

```sql
CREATE TABLE channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    custom_url VARCHAR(255),
    published_at DATETIME,
    thumbnail_default TEXT,
    thumbnail_medium TEXT,
    thumbnail_high TEXT,
    country VARCHAR(2),
    view_count BIGINT DEFAULT 0,
    subscriber_count BIGINT DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    uploads_playlist_id VARCHAR(255),
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**索引**:
```sql
CREATE INDEX idx_channels_channel_id ON channels(channel_id);
CREATE INDEX idx_channels_last_updated ON channels(last_updated);
```

### 3. 頻道統計歷史表 (channel_statistics_history)

儲存頻道統計數據的歷史記錄，用於趨勢分析。

```sql
CREATE TABLE channel_statistics_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    view_count BIGINT DEFAULT 0,
    subscriber_count BIGINT DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    estimated_minutes_watched BIGINT DEFAULT 0,
    average_view_duration INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    UNIQUE(channel_id, date)
);
```

**索引**:
```sql
CREATE INDEX idx_channel_stats_channel_date ON channel_statistics_history(channel_id, date);
```

### 4. 受眾輪廓表 (audience_demographics)

儲存頻道的受眾輪廓數據。

```sql
CREATE TABLE audience_demographics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id VARCHAR(255) NOT NULL,
    date_range_start DATE NOT NULL,
    date_range_end DATE NOT NULL,
    dimension_type VARCHAR(50) NOT NULL, -- 'ageGroup', 'gender', 'country', 'deviceType'
    dimension_value VARCHAR(100) NOT NULL,
    views_percentage DECIMAL(5,2) DEFAULT 0,
    watch_time_percentage DECIMAL(5,2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id),
    UNIQUE(channel_id, date_range_start, date_range_end, dimension_type, dimension_value)
);
```

**索引**:
```sql
CREATE INDEX idx_demographics_channel_type ON audience_demographics(channel_id, dimension_type);
CREATE INDEX idx_demographics_date_range ON audience_demographics(date_range_start, date_range_end);
```

### 5. 影片表 (videos)

儲存頻道影片的基本資訊和統計數據。

```sql
CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id VARCHAR(255) UNIQUE NOT NULL,
    channel_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    published_at DATETIME,
    duration VARCHAR(20), -- ISO 8601 duration format
    thumbnail_default TEXT,
    thumbnail_medium TEXT,
    thumbnail_high TEXT,
    view_count BIGINT DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2) DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);
```

**索引**:
```sql
CREATE INDEX idx_videos_channel_id ON videos(channel_id);
CREATE INDEX idx_videos_published_at ON videos(published_at);
CREATE INDEX idx_videos_view_count ON videos(view_count DESC);
```

### 6. 查詢歷史表 (query_history)

記錄用戶的查詢歷史，用於分析和優化。

```sql
CREATE TABLE query_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    channel_id VARCHAR(255),
    query_type VARCHAR(50) NOT NULL, -- 'basic', 'statistics', 'demographics', 'videos'
    query_parameters TEXT, -- JSON格式儲存查詢參數
    response_time_ms INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);
```

**索引**:
```sql
CREATE INDEX idx_query_history_user_id ON query_history(user_id);
CREATE INDEX idx_query_history_created_at ON query_history(created_at);
```

### 7. API配額使用表 (api_quota_usage)

追蹤YouTube API配額的使用情況。

```sql
CREATE TABLE api_quota_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    api_type VARCHAR(50) NOT NULL, -- 'data_api', 'analytics_api'
    quota_used INTEGER DEFAULT 0,
    quota_limit INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date, api_type)
);
```

### 8. 系統設定表 (system_settings)

儲存系統配置參數。

```sql
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**預設設定**:
```sql
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('cache_duration_channel_basic', '3600', '頻道基本資訊緩存時間（秒）'),
('cache_duration_statistics', '1800', '統計數據緩存時間（秒）'),
('cache_duration_demographics', '21600', '受眾輪廓緩存時間（秒）'),
('max_channels_compare', '5', '最大比較頻道數量'),
('default_date_range_days', '30', '預設查詢日期範圍（天）');
```

## 數據關係圖

```
users (1) ←→ (N) query_history
channels (1) ←→ (N) channel_statistics_history
channels (1) ←→ (N) audience_demographics
channels (1) ←→ (N) videos
channels (1) ←→ (N) query_history
```

## 數據遷移策略

### 1. 版本控制

使用Flask-Migrate進行數據庫版本控制：

```python
# migrations/versions/001_initial_schema.py
def upgrade():
    # 建立所有表格
    pass

def downgrade():
    # 回滾操作
    pass
```

### 2. 數據備份

定期備份策略：
- 每日自動備份
- 重要操作前手動備份
- 保留最近30天的備份

### 3. 效能優化

#### 查詢優化
- 使用適當的索引
- 避免N+1查詢問題
- 實施查詢結果緩存

#### 數據清理
- 定期清理過期的緩存數據
- 壓縮歷史統計數據
- 清理無效的查詢歷史

## 緩存策略

### 1. 應用層緩存

使用Redis進行應用層緩存：

```python
# 緩存鍵命名規範
CACHE_KEYS = {
    'channel_basic': 'channel:basic:{channel_id}',
    'channel_stats': 'channel:stats:{channel_id}:{start_date}:{end_date}',
    'demographics': 'channel:demographics:{channel_id}:{start_date}:{end_date}',
    'videos': 'channel:videos:{channel_id}:{order}:{max_results}'
}
```

### 2. 數據庫層緩存

- 查詢結果緩存
- 連接池優化
- 預編譯語句

## 安全性考量

### 1. 數據加密
- 敏感資料（access_token, refresh_token）使用AES加密
- 密碼雜湊使用bcrypt
- 數據庫連接使用SSL

### 2. 存取控制
- 用戶只能存取自己的查詢歷史
- API令牌定期輪換
- 實施SQL注入防護

### 3. 數據隱私
- 遵循GDPR規範
- 實施數據保留政策
- 提供數據刪除功能

## 監控和維護

### 1. 效能監控
- 查詢執行時間監控
- 數據庫連接數監控
- 緩存命中率監控

### 2. 數據完整性
- 定期檢查外鍵約束
- 驗證數據一致性
- 監控數據增長趨勢

這個數據庫設計提供了完整的數據儲存解決方案，支援系統的所有功能需求，同時考慮了效能、安全性和可維護性。

