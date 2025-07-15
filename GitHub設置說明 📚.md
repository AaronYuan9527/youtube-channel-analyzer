# GitHub設置說明 📚

本文檔說明如何將YouTube頻道分析器專案設置到您的GitHub帳戶。

## 🚀 快速開始

### 1. 建立GitHub Repository

#### 方法一：通過GitHub網站
1. 登入您的GitHub帳戶
2. 點擊右上角的「+」按鈕，選擇「New repository」
3. 填寫repository資訊：
   - **Repository name**: `youtube-channel-analyzer`
   - **Description**: `一個功能強大的YouTube頻道數據分析工具`
   - **Visibility**: Public（推薦）或Private
   - **不要**勾選「Initialize this repository with a README」
4. 點擊「Create repository」

#### 方法二：使用GitHub CLI
```bash
# 安裝GitHub CLI（如果尚未安裝）
# macOS: brew install gh
# Windows: winget install GitHub.cli
# Linux: 參考官方文檔

# 登入GitHub
gh auth login

# 建立repository
gh repo create youtube-channel-analyzer --public --description "一個功能強大的YouTube頻道數據分析工具"
```

### 2. 推送代碼到GitHub

在您的本地專案目錄中執行：

```bash
# 添加GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/youtube-channel-analyzer.git

# 推送代碼
git branch -M main
git push -u origin main
```

**注意**: 將`YOUR_USERNAME`替換為您的GitHub用戶名。

### 3. 設置GitHub Pages（可選）

如果您想使用GitHub Pages託管靜態版本：

1. 進入您的repository設置
2. 滾動到「Pages」部分
3. 在「Source」下選擇「Deploy from a branch」
4. 選擇「main」分支和「/ (root)」資料夾
5. 點擊「Save」

## 🔧 配置GitHub Secrets

為了使GitHub Actions正常工作，您需要設置一些secrets：

1. 進入您的repository
2. 點擊「Settings」標籤
3. 在左側選單中選擇「Secrets and variables」→「Actions」
4. 點擊「New repository secret」
5. 添加以下secrets：

### 必需的Secrets
- `YOUTUBE_API_KEY`: 您的YouTube Data API金鑰
- `SECRET_KEY`: Flask應用程式的密鑰（隨機字符串）

### 可選的Secrets
- `DATABASE_URL`: 數據庫連接URL（如果使用外部數據庫）
- `JWT_SECRET_KEY`: JWT令牌密鑰

## 📋 Repository設置建議

### 1. 啟用Issues
- 進入「Settings」→「General」
- 確保「Issues」已勾選
- 這允許用戶報告錯誤和提出功能請求

### 2. 設置Branch Protection Rules
- 進入「Settings」→「Branches」
- 點擊「Add rule」
- 設置以下規則：
  - Branch name pattern: `main`
  - ✅ Require a pull request before merging
  - ✅ Require status checks to pass before merging
  - ✅ Require branches to be up to date before merging

### 3. 配置Labels
建議添加以下labels來組織issues和PRs：
- `bug` - 錯誤報告
- `enhancement` - 功能增強
- `documentation` - 文檔相關
- `good first issue` - 適合新貢獻者
- `help wanted` - 需要幫助

## 🤖 GitHub Actions設置

專案已包含GitHub Actions工作流程檔案（`.github/workflows/deploy.yml`），它會：

1. **自動測試**: 在每次push和PR時運行測試
2. **代碼品質檢查**: 使用flake8進行Python代碼檢查
3. **前端建置**: 自動建置React前端（如果需要）
4. **部署準備**: 準備部署所需的檔案

### 自定義工作流程
您可以根據需要修改`.github/workflows/deploy.yml`檔案：

```yaml
# 添加更多測試步驟
- name: Run additional tests
  run: |
    python -m pytest tests/ -v
    python -m coverage run -m pytest
    python -m coverage report

# 添加安全掃描
- name: Security scan
  run: |
    pip install safety
    safety check
```

## 📊 設置Repository Insights

### 1. 啟用Discussions（可選）
- 進入「Settings」→「General」
- 勾選「Discussions」
- 這提供了一個社區討論的平台

### 2. 添加Topics
在repository主頁：
1. 點擊設置圖標（齒輪）
2. 在「Topics」欄位添加相關標籤：
   - `youtube-api`
   - `data-analysis`
   - `flask`
   - `react`
   - `python`
   - `web-application`

### 3. 設置Repository Description
確保repository有清晰的描述和網站URL（如果有部署的話）。

## 🔗 連接外部服務

### 1. 連接到部署平台
- **Heroku**: 連接GitHub repository進行自動部署
- **Vercel**: 導入GitHub repository
- **Netlify**: 連接repository進行前端部署

### 2. 設置監控
- **CodeClimate**: 代碼品質監控
- **Codecov**: 測試覆蓋率報告
- **Dependabot**: 自動依賴更新

## 📝 維護最佳實踐

### 1. 定期更新
- 定期更新依賴項
- 保持README.md最新
- 更新文檔

### 2. 社區管理
- 及時回應issues和PRs
- 提供清晰的貢獻指南
- 感謝貢獻者

### 3. 版本管理
- 使用語義化版本控制
- 建立releases和tags
- 維護CHANGELOG.md

## 🆘 常見問題

### Q: 推送時出現權限錯誤
A: 確保您有repository的寫入權限，或使用personal access token。

### Q: GitHub Actions失敗
A: 檢查secrets是否正確設置，查看Actions日誌了解具體錯誤。

### Q: 如何邀請協作者？
A: 進入「Settings」→「Manage access」→「Invite a collaborator」

---

完成這些設置後，您的YouTube頻道分析器專案就可以在GitHub上正常運作了！🎉

