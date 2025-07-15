# YouTube Data API 研究結果

## 頻道資訊獲取

YouTube Data API v3 提供了 `channels.list` 方法來獲取頻道資訊。透過設定不同的參數，可以獲取到觀看數、留言數、按讚數（影片的按讚數，非頻道整體按讚數）、訂閱者數以及部分受眾輪廓相關的數據。

### 關鍵參數：

*   **`part`**: 此參數用於指定要獲取的頻道資源部分。對於獲取頻道統計數據，需要包含 `statistics`。其他有用的部分包括 `snippet` (基本資訊)、`contentDetails` (內容相關資訊，如上傳影片的播放列表ID) 和 `brandingSettings` (品牌設定)。
    *   `snippet`: 包含頻道標題、描述、自訂URL、發布日期等基本資訊。
    *   `contentDetails`: 包含頻道內容相關資訊，例如包含頻道上傳影片的播放列表ID。
    *   `statistics`: 包含觀看次數、留言次數、訂閱者人數和影片數量。這些數據對於了解受眾輪廓非常重要。
    *   `brandingSettings`: 包含品牌相關資訊。

*   **頻道識別方式 (以下三選一)：**
    *   **`mine=true`**: 獲取當前已驗證用戶的YouTube頻道資訊。需要OAuth 2.0授權。
    *   **`forUsername`**: 透過YouTube用戶名獲取頻道資訊。例如：`forUsername=Google`。
    *   **`id`**: 透過YouTube頻道ID獲取頻道資訊。例如：`id=UCK8sQmJBp8GCxrOtXWBpyEA` (Google官方頻道ID)。

### 獲取受眾輪廓：

YouTube Data API v3 的 `channels.list` 方法的 `statistics` 部分提供了訂閱者人數，這可以作為受眾輪廓的一個重要指標。然而，更詳細的受眾輪廓（例如年齡、性別、地理位置等）通常需要使用 **YouTube Analytics API**。我將在後續研究中探討 YouTube Analytics API。

### 範例 API 呼叫 (使用 `id` 和 `part=snippet,contentDetails,statistics`)：

```
GET https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=CHANNEL_ID&key=YOUR_API_KEY
```

### 授權：

對於需要用戶特定數據的請求（例如 `mine=true`），需要OAuth 2.0 授權。對於公開頻道數據，可以使用API Key。

## 後續研究方向：

*   **YouTube Analytics API**: 深入研究如何使用 YouTube Analytics API 獲取更詳細的受眾輪廓數據（例如年齡、性別、地理位置、觀看時間等）。
*   **API 配額**: 了解 YouTube Data API 的配額限制，以便在設計應用程式時考慮。
*   **Python 客戶端函式庫**: 尋找並評估適合用於 Python 開發的 YouTube Data API 客戶端函式庫。




## YouTube Analytics API 研究結果

YouTube Analytics API 提供了更詳細的數據，特別是受眾輪廓相關的數據。它使用 **dimensions** 和 **metrics** 來聚合數據和測量用戶活動。

### 關鍵參數：

*   **`metrics`**: 指定報告中包含的測量數據，例如 `views` (觀看次數)、`estimatedMinutesWatched` (預計觀看時長)。
*   **`dimensions`**: 解釋指標如何分組，例如 `ageGroup` (年齡組)、`gender` (性別)、`country` (國家)。
*   **`startDate` 和 `endDate`**: 指定報告的時間範圍。
*   **`filters`**: 用於過濾數據，例如只獲取特定國家或影片的數據。

### 受眾輪廓相關的 Dimensions：

*   **`ageGroup`**: 用戶的年齡組。
*   **`gender`**: 用戶的性別。
*   **`country`**: 用戶所在的國家。
*   `province`: 美國州或地區。
*   `dma`: 指定市場區域 (DMA)。
*   `city`: 城市。

### 授權：

YouTube Analytics API 的請求也需要 OAuth 2.0 授權。

### 範例 API 呼叫 (獲取年齡組和性別的觀看數據)：

```
GET https://youtubeanalytics.googleapis.com/v2/reports?metrics=views&dimensions=ageGroup%2Cgender&startDate=2024-01-01&endDate=2024-12-31&ids=channel%3D%3DCHANNEL_ID
```

## API 配額：

YouTube Data API 和 YouTube Analytics API 都有配額限制。在開發應用程式時，需要考慮這些限制，並實施適當的緩存機制或優化請求策略，以避免超出配額。

## Python 客戶端函式庫：

Google 提供了官方的 Python 客戶端函式庫，可以簡化與 YouTube Data API 和 YouTube Analytics API 的互動。這將是我們開發網頁程式的首選工具。


