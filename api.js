// API服務模組 - 連接後端API
const API_BASE_URL = 'http://localhost:5003/api'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error?.message || `HTTP error! status: ${response.status}`)
      }
      
      return data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // 系統相關API
  async getSystemHealth() {
    return this.request('/system/health')
  }

  async getSystemConfig() {
    return this.request('/system/config')
  }

  async getSystemStats() {
    return this.request('/system/stats')
  }

  // 頻道相關API
  async searchChannels(query, maxResults = 10) {
    const params = new URLSearchParams({
      q: query,
      maxResults: maxResults.toString()
    })
    return this.request(`/channel/search?${params}`)
  }

  async getChannelBasicInfo(channelId) {
    return this.request(`/channel/${channelId}/basic`)
  }

  async getChannelStatistics(channelId, startDate, endDate, metrics) {
    const params = new URLSearchParams()
    if (startDate) params.append('startDate', startDate)
    if (endDate) params.append('endDate', endDate)
    if (metrics) params.append('metrics', metrics)
    
    return this.request(`/channel/${channelId}/statistics?${params}`)
  }

  async getChannelDemographics(channelId, startDate, endDate) {
    const params = new URLSearchParams()
    if (startDate) params.append('startDate', startDate)
    if (endDate) params.append('endDate', endDate)
    
    return this.request(`/channel/${channelId}/demographics?${params}`)
  }

  async getChannelVideos(channelId, maxResults = 10, order = 'viewCount') {
    const params = new URLSearchParams({
      maxResults: maxResults.toString(),
      order
    })
    return this.request(`/channel/${channelId}/videos?${params}`)
  }

  async compareChannels(channelIds, metrics, startDate, endDate) {
    return this.request('/channel/compare', {
      method: 'POST',
      body: JSON.stringify({
        channelIds,
        metrics,
        startDate,
        endDate
      })
    })
  }

  // 認證相關API
  async login() {
    return this.request('/auth/login')
  }

  async logout() {
    return this.request('/auth/logout', { method: 'POST' })
  }

  async getCurrentUser() {
    return this.request('/auth/me')
  }

  async refreshToken() {
    return this.request('/auth/refresh', { method: 'POST' })
  }
}

// 建立單例實例
const apiService = new ApiService()

export default apiService

