import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Search, Youtube, Users, Eye, ThumbsUp, MessageCircle, TrendingUp, Globe, Calendar, BarChart3 } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts'
import './App.css'

// 模擬數據
const mockChannelData = {
  channelId: 'UC_x5XG1OV2P6uZZ5FSM9Ttw',
  title: 'Google Developers',
  description: 'The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.',
  customUrl: '@GoogleDevelopers',
  thumbnails: {
    high: 'https://yt3.ggpht.com/ytc/AIdro_mNLKQO2VaOy_Qi2Qg8pJQhNOC_6QM8QzQQQQQQQQ=s800-c-k-c0x00ffffff-no-rj'