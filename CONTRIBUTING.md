# 貢獻指南

感謝您對YouTube頻道分析器專案的興趣！我們歡迎所有形式的貢獻。

## 🤝 如何貢獻

### 報告問題
- 使用GitHub Issues報告錯誤
- 提供詳細的錯誤描述和重現步驟
- 包含您的環境資訊（作業系統、Python版本等）

### 提出功能建議
- 在Issues中描述您的功能想法
- 解釋為什麼這個功能會有用
- 提供可能的實現方案

### 提交代碼
1. Fork這個repository
2. 建立功能分支：`git checkout -b feature/amazing-feature`
3. 提交您的更改：`git commit -m 'Add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 開啟Pull Request

## 📋 開發設置

### 環境要求
- Python 3.8+
- Node.js 16+
- Git

### 本地開發
```bash
# 克隆repository
git clone https://github.com/your-username/youtube-channel-analyzer.git
cd youtube-channel-analyzer

# 設置Python環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 設置環境變數
cp .env.example .env
# 編輯.env檔案添加您的API金鑰

# 啟動開發服務器
python src/main.py
```

## 🎯 代碼標準

### Python代碼
- 遵循PEP 8風格指南
- 使用有意義的變數和函數名稱
- 添加適當的註釋和文檔字符串
- 編寫單元測試

### JavaScript/React代碼
- 使用ES6+語法
- 遵循React最佳實踐
- 使用有意義的組件和變數名稱
- 保持組件小而專注

### 提交訊息
- 使用清晰、描述性的提交訊息
- 格式：`類型: 簡短描述`
- 類型：feat, fix, docs, style, refactor, test, chore

範例：
```
feat: 添加頻道比較功能
fix: 修復API配額超限問題
docs: 更新安裝說明
```

## 🧪 測試

### 運行測試
```bash
# Python測試
python -m pytest tests/

# 前端測試（如果有）
npm test
```

### 測試覆蓋率
- 新功能應該包含測試
- 維持良好的測試覆蓋率
- 測試應該清晰且可維護

## 📖 文檔

### 更新文檔
- 新功能需要更新README.md
- API變更需要更新API文檔
- 重要變更需要更新CHANGELOG.md

### 代碼註釋
- 複雜邏輯需要註釋說明
- 公共API需要完整的文檔字符串
- 使用中文或英文，保持一致性

## 🔍 代碼審查

### Pull Request要求
- 清晰的PR描述
- 相關的Issue連結
- 通過所有測試
- 代碼審查通過

### 審查標準
- 代碼品質和可讀性
- 功能正確性
- 性能考量
- 安全性檢查

## 🚀 發布流程

### 版本號
- 遵循語義化版本控制（Semantic Versioning）
- 格式：MAJOR.MINOR.PATCH
- 重大變更增加MAJOR版本

### 發布檢查清單
- [ ] 所有測試通過
- [ ] 文檔已更新
- [ ] CHANGELOG.md已更新
- [ ] 版本號已更新

## 📞 聯絡方式

如有問題，請通過以下方式聯絡：
- GitHub Issues
- 電子郵件：your-email@example.com

## 📄 授權

通過貢獻代碼，您同意您的貢獻將在MIT授權條款下發布。

---

再次感謝您的貢獻！🎉

