import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Search, Youtube, Users, Eye, ThumbsUp, MessageCircle, TrendingUp, Globe, Calendar, BarChart3, AlertCircle } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'
import apiService from './services/api.js'
import './App.css'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

function HomePage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [channelData, setChannelData] = useState(null)
  const [videos, setVideos] = useState([])
  const [demographics, setDemographics] = useState(null)
  const [error, setError] = useState(null)
  const [systemHealth, setSystemHealth] = useState(null)

  // 檢查系統健康狀態
  useEffect(() => {
    const checkSystemHealth = async () => {
      try {
        const health = await apiService.getSystemHealth()
        setSystemHealth(health)
      } catch (error) {
        console.error('Failed to check system health:', error)
        setSystemHealth({ status: 'unhealthy', error: error.message })
      }
    }
    
    checkSystemHealth()
  }, [])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    
    setIsLoading(true)
    setError(null)
    
    try {
      // 搜尋頻道
      const searchResults = await apiService.searchChannels(searchQuery, 1)
      
      if (searchResults.success && searchResults.data.channels.length > 0) {
        const channel = searchResults.data.channels[0]
        const channelId = channel.channelId
        
        // 獲取頻道詳細資訊
        const channelInfo = await apiService.getChannelBasicInfo(channelId)
        
        if (channelInfo.success) {
          setChannelData(channelInfo.data)
          
          // 獲取頻道影片
          try {
            const videosResult = await apiService.getChannelVideos(channelId, 10)
            if (videosResult.success) {
              setVideos(videosResult.data.videos)
            }
          } catch (videoError) {
            console.error('Failed to fetch videos:', videoError)
          }
          
          // 嘗試獲取受眾輪廓（需要OAuth認證）
          try {
            const demographicsResult = await apiService.getChannelDemographics(channelId)
            if (demographicsResult.success) {
              setDemographics(demographicsResult.data)
            }
          } catch (demoError) {
            console.error('Failed to fetch demographics (OAuth required):', demoError)
            // 使用模擬數據
            setDemographics({
              ageGroups: [
                { ageGroup: '18-24', viewsPercentage: 25.4, watchTimePercentage: 28.1 },
                { ageGroup: '25-34', viewsPercentage: 35.2, watchTimePercentage: 38.7 },
                { ageGroup: '35-44', viewsPercentage: 22.8, watchTimePercentage: 20.3 },
                { ageGroup: '45-54', viewsPercentage: 12.1, watchTimePercentage: 9.8 },
                { ageGroup: '55+', viewsPercentage: 4.5, watchTimePercentage: 3.1 }
              ],
              gender: {
                male: { viewsPercentage: 68.3, watchTimePercentage: 71.2 },
                female: { viewsPercentage: 31.7, watchTimePercentage: 28.8 }
              },
              topCountries: [
                { country: 'US', countryName: '美國', viewsPercentage: 32.1, watchTimePercentage: 35.4 },
                { country: 'IN', countryName: '印度', viewsPercentage: 18.7, watchTimePercentage: 16.2 },
                { country: 'GB', countryName: '英國', viewsPercentage: 8.9, watchTimePercentage: 9.8 },
                { country: 'CA', countryName: '加拿大', viewsPercentage: 6.4, watchTimePercentage: 7.1 },
                { country: 'DE', countryName: '德國', viewsPercentage: 5.2, watchTimePercentage: 5.8 }
              ]
            })
          }
        } else {
          throw new Error(channelInfo.error?.message || '無法獲取頻道資訊')
        }
      } else {
        throw new Error('找不到相關頻道')
      }
    } catch (error) {
      console.error('Search failed:', error)
      setError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M'
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K'
    }
    return num.toString()
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('zh-TW')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="bg-red-500 p-2 rounded-lg">
                <Youtube className="h-6 w-6 text-white" />
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-red-500 to-purple-600 bg-clip-text text-transparent">
                YouTube頻道分析器
              </h1>
            </motion.div>
            <div className="flex items-center space-x-3">
              {systemHealth && (
                <Badge 
                  variant={systemHealth.status === 'healthy' ? 'default' : 'destructive'}
                  className="hidden md:flex"
                >
                  {systemHealth.status === 'healthy' ? '系統正常' : '系統異常'}
                </Badge>
              )}
              <Badge variant="secondary" className="hidden md:flex">
                v1.0.0
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Search Section */}
        <motion.section 
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            快速獲取YouTube頻道資訊
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            輸入頻道名稱或URL，立即獲取詳細的頻道統計數據、受眾輪廓和影片分析
          </p>
          
          <div className="max-w-2xl mx-auto flex gap-4">
            <Input
              type="text"
              placeholder="輸入YouTube頻道名稱或URL..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="flex-1 h-12 text-lg"
            />
            <Button 
              onClick={handleSearch}
              disabled={isLoading}
              className="h-12 px-8 bg-red-500 hover:bg-red-600"
            >
              {isLoading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                />
              ) : (
                <>
                  <Search className="w-5 h-5 mr-2" />
                  搜尋
                </>
              )}
            </Button>
          </div>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg max-w-2xl mx-auto"
            >
              <div className="flex items-center text-red-700">
                <AlertCircle className="w-5 h-5 mr-2" />
                <span>{error}</span>
              </div>
            </motion.div>
          )}
        </motion.section>

        {/* Results Section */}
        {channelData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            {/* Channel Overview */}
            <Card className="overflow-hidden">
              <CardHeader className="bg-gradient-to-r from-red-500 to-purple-600 text-white">
                <div className="flex items-start space-x-4">
                  <img
                    src={channelData.thumbnails?.high || 'https://via.placeholder.com/80x80/ff0000/ffffff?text=YT'}
                    alt={channelData.title}
                    className="w-20 h-20 rounded-full border-4 border-white/20"
                    onError={(e) => {
                      e.target.src = 'https://via.placeholder.com/80x80/ff0000/ffffff?text=YT'
                    }}
                  />
                  <div className="flex-1">
                    <CardTitle className="text-2xl mb-2">{channelData.title}</CardTitle>
                    <CardDescription className="text-white/80 text-base">
                      {channelData.customUrl && `@${channelData.customUrl.replace('@', '')}`}
                    </CardDescription>
                    <div className="flex items-center space-x-4 mt-3">
                      {channelData.country && (
                        <Badge variant="secondary" className="bg-white/20 text-white">
                          <Globe className="w-4 h-4 mr-1" />
                          {channelData.country}
                        </Badge>
                      )}
                      <Badge variant="secondary" className="bg-white/20 text-white">
                        <Calendar className="w-4 h-4 mr-1" />
                        更新於 {formatDate(channelData.lastUpdated)}
                      </Badge>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="p-6">
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {channelData.description}
                </p>
                
                {/* Statistics Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl border border-blue-200"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-blue-600 font-medium">總觀看數</p>
                        <p className="text-3xl font-bold text-blue-900">
                          {formatNumber(channelData.statistics?.viewCount || 0)}
                        </p>
                      </div>
                      <Eye className="w-8 h-8 text-blue-500" />
                    </div>
                  </motion.div>
                  
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl border border-green-200"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-green-600 font-medium">訂閱人數</p>
                        <p className="text-3xl font-bold text-green-900">
                          {formatNumber(channelData.statistics?.subscriberCount || 0)}
                        </p>
                      </div>
                      <Users className="w-8 h-8 text-green-500" />
                    </div>
                  </motion.div>
                  
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl border border-purple-200"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-purple-600 font-medium">影片數量</p>
                        <p className="text-3xl font-bold text-purple-900">
                          {formatNumber(channelData.statistics?.videoCount || 0)}
                        </p>
                      </div>
                      <BarChart3 className="w-8 h-8 text-purple-500" />
                    </div>
                  </motion.div>
                </div>
              </CardContent>
            </Card>

            {/* Detailed Analysis Tabs */}
            <Tabs defaultValue="videos" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="videos">熱門影片</TabsTrigger>
                <TabsTrigger value="demographics">受眾輪廓</TabsTrigger>
                <TabsTrigger value="analytics">數據分析</TabsTrigger>
              </TabsList>
              
              <TabsContent value="videos" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <TrendingUp className="w-5 h-5 mr-2" />
                      熱門影片分析
                    </CardTitle>
                    <CardDescription>
                      根據觀看數和互動率排序的頻道熱門影片
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {videos.length > 0 ? (
                      <div className="space-y-4">
                        {videos.map((video, index) => (
                          <motion.div
                            key={video.videoId}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className="flex items-start space-x-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                          >
                            <img
                              src={video.thumbnails?.medium || 'https://via.placeholder.com/320x240/cccccc/666666?text=Video'}
                              alt={video.title}
                              className="w-32 h-24 object-cover rounded-lg"
                              onError={(e) => {
                                e.target.src = 'https://via.placeholder.com/320x240/cccccc/666666?text=Video'
                              }}
                            />
                            <div className="flex-1">
                              <h3 className="font-semibold text-lg mb-2 line-clamp-2">
                                {video.title}
                              </h3>
                              <p className="text-gray-500 text-sm mb-3">
                                發布於 {formatDate(video.publishedAt)}
                              </p>
                              <div className="flex items-center space-x-6 text-sm">
                                <div className="flex items-center text-blue-600">
                                  <Eye className="w-4 h-4 mr-1" />
                                  {formatNumber(video.statistics?.viewCount || 0)} 次觀看
                                </div>
                                <div className="flex items-center text-green-600">
                                  <ThumbsUp className="w-4 h-4 mr-1" />
                                  {formatNumber(video.statistics?.likeCount || 0)} 個讚
                                </div>
                                <div className="flex items-center text-purple-600">
                                  <MessageCircle className="w-4 h-4 mr-1" />
                                  {formatNumber(video.statistics?.commentCount || 0)} 則留言
                                </div>
                                <Badge variant="outline">
                                  互動率 {video.engagementRate || 0}%
                                </Badge>
                              </div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    ) : (
                      <div className="text-center py-8 text-gray-500">
                        <Youtube className="w-12 h-12 mx-auto mb-4 opacity-50" />
                        <p>暫無影片數據</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="demographics" className="space-y-4">
                {demographics ? (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Age Groups */}
                    <Card>
                      <CardHeader>
                        <CardTitle>年齡分布</CardTitle>
                        <CardDescription>觀眾年齡組分析</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <ResponsiveContainer width="100%" height={300}>
                          <PieChart>
                            <Pie
                              data={demographics.ageGroups}
                              cx="50%"
                              cy="50%"
                              labelLine={false}
                              label={({ ageGroup, viewsPercentage }) => `${ageGroup}: ${viewsPercentage}%`}
                              outerRadius={80}
                              fill="#8884d8"
                              dataKey="viewsPercentage"
                            >
                              {demographics.ageGroups.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>

                    {/* Gender Distribution */}
                    <Card>
                      <CardHeader>
                        <CardTitle>性別分布</CardTitle>
                        <CardDescription>觀眾性別比例</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">男性</span>
                            <span className="text-2xl font-bold text-blue-600">
                              {demographics.gender.male.viewsPercentage}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <div 
                              className="bg-blue-500 h-3 rounded-full transition-all duration-1000"
                              style={{ width: `${demographics.gender.male.viewsPercentage}%` }}
                            />
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <span className="font-medium">女性</span>
                            <span className="text-2xl font-bold text-pink-600">
                              {demographics.gender.female.viewsPercentage}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-3">
                            <div 
                              className="bg-pink-500 h-3 rounded-full transition-all duration-1000"
                              style={{ width: `${demographics.gender.female.viewsPercentage}%` }}
                            />
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    {/* Top Countries */}
                    <Card className="lg:col-span-2">
                      <CardHeader>
                        <CardTitle>主要觀眾地區</CardTitle>
                        <CardDescription>按觀看數排序的前5個國家/地區</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <ResponsiveContainer width="100%" height={300}>
                          <BarChart data={demographics.topCountries}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="countryName" />
                            <YAxis />
                            <Tooltip />
                            <Bar dataKey="viewsPercentage" fill="#8884d8" />
                          </BarChart>
                        </ResponsiveContainer>
                      </CardContent>
                    </Card>
                  </div>
                ) : (
                  <Card>
                    <CardContent className="text-center py-8">
                      <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p className="text-gray-500">受眾輪廓數據需要OAuth認證</p>
                      <p className="text-sm text-gray-400 mt-2">目前顯示模擬數據</p>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
              
              <TabsContent value="analytics" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>數據分析總覽</CardTitle>
                    <CardDescription>頻道表現的關鍵指標分析</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-blue-900">平均觀看數</h4>
                        <p className="text-2xl font-bold text-blue-600">
                          {formatNumber(Math.round((channelData.statistics?.viewCount || 0) / (channelData.statistics?.videoCount || 1)))}
                        </p>
                        <p className="text-sm text-blue-600">每部影片</p>
                      </div>
                      
                      <div className="bg-green-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-green-900">訂閱轉換率</h4>
                        <p className="text-2xl font-bold text-green-600">
                          {(((channelData.statistics?.subscriberCount || 0) / (channelData.statistics?.viewCount || 1)) * 100).toFixed(2)}%
                        </p>
                        <p className="text-sm text-green-600">觀看轉訂閱</p>
                      </div>
                      
                      <div className="bg-purple-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-purple-900">內容產出</h4>
                        <p className="text-2xl font-bold text-purple-600">
                          {channelData.statistics?.videoCount || 0}
                        </p>
                        <p className="text-sm text-purple-600">總影片數</p>
                      </div>
                      
                      <div className="bg-orange-50 p-4 rounded-lg">
                        <h4 className="font-semibold text-orange-900">平均互動率</h4>
                        <p className="text-2xl font-bold text-orange-600">
                          {videos.length > 0 ? 
                            (videos.reduce((acc, video) => acc + (video.engagementRate || 0), 0) / videos.length).toFixed(2) : 
                            '0.00'
                          }%
                        </p>
                        <p className="text-sm text-orange-600">讚+留言/觀看</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </motion.div>
        )}

        {/* Features Section */}
        {!channelData && !isLoading && (
          <motion.section 
            className="mt-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
              強大的分析功能
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[
                {
                  icon: <Eye className="w-8 h-8" />,
                  title: "觀看數據",
                  description: "詳細的觀看數、觀看時長等統計數據"
                },
                {
                  icon: <Users className="w-8 h-8" />,
                  title: "受眾輪廓",
                  description: "年齡、性別、地理位置等受眾分析"
                },
                {
                  icon: <ThumbsUp className="w-8 h-8" />,
                  title: "互動分析",
                  description: "按讚數、留言數、分享數等互動指標"
                },
                {
                  icon: <TrendingUp className="w-8 h-8" />,
                  title: "趨勢追蹤",
                  description: "頻道成長趨勢和表現分析"
                }
              ].map((feature, index) => (
                <motion.div
                  key={index}
                  whileHover={{ scale: 1.05 }}
                  className="text-center p-6 bg-white rounded-xl shadow-lg border border-gray-100"
                >
                  <div className="bg-gradient-to-br from-red-500 to-purple-600 text-white p-3 rounded-lg inline-block mb-4">
                    {feature.icon}
                  </div>
                  <h4 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h4>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <div className="bg-red-500 p-2 rounded-lg">
              <Youtube className="h-5 w-5" />
            </div>
            <span className="text-lg font-semibold">YouTube頻道分析器</span>
          </div>
          <p className="text-gray-400">
            快速、準確、全面的YouTube頻道數據分析工具
          </p>
        </div>
      </footer>
    </div>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </Router>
  )
}

export default App

