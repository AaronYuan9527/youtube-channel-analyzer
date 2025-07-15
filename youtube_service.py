import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    """YouTube API服務類"""
    
    def __init__(self, api_key=None, credentials=None):
        """
        初始化YouTube服務
        
        Args:
            api_key: YouTube Data API金鑰（用於公開數據）
            credentials: OAuth2認證憑證（用於私人數據）
        """
        self.api_key = api_key or os.environ.get('YOUTUBE_API_KEY')
        self.credentials = credentials
        
        # 建立YouTube Data API服務
        if self.credentials:
            self.youtube = build('youtube', 'v3', credentials=self.credentials)
        elif self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        else:
            raise ValueError("需要提供API金鑰或OAuth2認證憑證")
        
        # 建立YouTube Analytics API服務（需要OAuth2認證）
        self.youtube_analytics = None
        if self.credentials:
            try:
                self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=self.credentials)
            except Exception as e:
                logger.warning(f"無法建立YouTube Analytics API服務: {e}")
    
    def search_channels(self, query, max_results=10):
        """
        搜尋YouTube頻道
        
        Args:
            query: 搜尋關鍵字
            max_results: 最大結果數量
            
        Returns:
            list: 頻道列表
        """
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='channel',
                maxResults=max_results
            )
            response = request.execute()
            
            channels = []
            for item in response.get('items', []):
                channel_id = item['id']['channelId']
                # 獲取頻道的詳細統計資訊
                channel_details = self.get_channel_details(channel_id)
                if channel_details:
                    channels.append(channel_details)
            
            return channels
        except Exception as e:
            logger.error(f"搜尋頻道時發生錯誤: {e}")
            raise
    
    def get_channel_details(self, channel_id):
        """
        獲取頻道詳細資訊
        
        Args:
            channel_id: YouTube頻道ID
            
        Returns:
            dict: 頻道詳細資訊
        """
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics,contentDetails,brandingSettings',
                id=channel_id
            )
            response = request.execute()
            
            if not response.get('items'):
                return None
            
            return response['items'][0]
        except Exception as e:
            logger.error(f"獲取頻道詳細資訊時發生錯誤: {e}")
            raise
    
    def get_channel_by_username(self, username):
        """
        透過用戶名獲取頻道資訊
        
        Args:
            username: YouTube用戶名
            
        Returns:
            dict: 頻道資訊
        """
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics,contentDetails,brandingSettings',
                forUsername=username
            )
            response = request.execute()
            
            if not response.get('items'):
                return None
            
            return response['items'][0]
        except Exception as e:
            logger.error(f"透過用戶名獲取頻道資訊時發生錯誤: {e}")
            raise
    
    def get_channel_videos(self, channel_id, max_results=10, order='viewCount'):
        """
        獲取頻道的影片列表
        
        Args:
            channel_id: YouTube頻道ID
            max_results: 最大結果數量
            order: 排序方式 (date, rating, relevance, title, videoCount, viewCount)
            
        Returns:
            list: 影片列表
        """
        try:
            # 首先獲取頻道的上傳播放列表ID
            channel_details = self.get_channel_details(channel_id)
            if not channel_details:
                return []
            
            uploads_playlist_id = channel_details.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
            if not uploads_playlist_id:
                return []
            
            # 獲取播放列表中的影片
            request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=max_results
            )
            response = request.execute()
            
            video_ids = []
            for item in response.get('items', []):
                video_id = item['snippet']['resourceId']['videoId']
                video_ids.append(video_id)
            
            if not video_ids:
                return []
            
            # 獲取影片的詳細統計資訊
            videos_request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()
            
            videos = videos_response.get('items', [])
            
            # 根據指定的順序排序
            if order == 'viewCount':
                videos.sort(key=lambda x: int(x.get('statistics', {}).get('viewCount', 0)), reverse=True)
            elif order == 'date':
                videos.sort(key=lambda x: x.get('snippet', {}).get('publishedAt', ''), reverse=True)
            
            return videos
        except Exception as e:
            logger.error(f"獲取頻道影片時發生錯誤: {e}")
            raise
    
    def get_channel_analytics(self, channel_id, start_date, end_date, metrics='views,estimatedMinutesWatched', dimensions=None):
        """
        獲取頻道的分析數據（需要OAuth2認證）
        
        Args:
            channel_id: YouTube頻道ID
            start_date: 開始日期 (YYYY-MM-DD)
            end_date: 結束日期 (YYYY-MM-DD)
            metrics: 指標列表
            dimensions: 維度列表
            
        Returns:
            dict: 分析數據
        """
        if not self.youtube_analytics:
            raise ValueError("YouTube Analytics API需要OAuth2認證")
        
        try:
            params = {
                'ids': f'channel=={channel_id}',
                'startDate': start_date,
                'endDate': end_date,
                'metrics': metrics
            }
            
            if dimensions:
                params['dimensions'] = dimensions
            
            request = self.youtube_analytics.reports().query(**params)
            response = request.execute()
            
            return response
        except Exception as e:
            logger.error(f"獲取頻道分析數據時發生錯誤: {e}")
            raise
    
    def get_audience_demographics(self, channel_id, start_date, end_date):
        """
        獲取受眾輪廓數據
        
        Args:
            channel_id: YouTube頻道ID
            start_date: 開始日期 (YYYY-MM-DD)
            end_date: 結束日期 (YYYY-MM-DD)
            
        Returns:
            dict: 受眾輪廓數據
        """
        if not self.youtube_analytics:
            raise ValueError("YouTube Analytics API需要OAuth2認證")
        
        demographics_data = {}
        
        try:
            # 獲取年齡組數據
            age_groups = self.get_channel_analytics(
                channel_id, start_date, end_date,
                metrics='views,estimatedMinutesWatched',
                dimensions='ageGroup'
            )
            demographics_data['ageGroups'] = age_groups
            
            # 獲取性別數據
            gender = self.get_channel_analytics(
                channel_id, start_date, end_date,
                metrics='views,estimatedMinutesWatched',
                dimensions='gender'
            )
            demographics_data['gender'] = gender
            
            # 獲取國家數據
            countries = self.get_channel_analytics(
                channel_id, start_date, end_date,
                metrics='views,estimatedMinutesWatched',
                dimensions='country'
            )
            demographics_data['countries'] = countries
            
            return demographics_data
        except Exception as e:
            logger.error(f"獲取受眾輪廓數據時發生錯誤: {e}")
            raise

class YouTubeOAuthService:
    """YouTube OAuth認證服務"""
    
    def __init__(self):
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID')
        self.client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        self.redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
        
        if not all([self.client_id, self.client_secret, self.redirect_uri]):
            raise ValueError("缺少Google OAuth配置")
        
        self.scopes = [
            'https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/yt-analytics.readonly'
        ]
    
    def get_authorization_url(self):
        """
        獲取OAuth授權URL
        
        Returns:
            str: 授權URL
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return authorization_url, state
    
    def exchange_code_for_token(self, code, state):
        """
        交換授權碼獲取存取令牌
        
        Args:
            code: 授權碼
            state: 狀態參數
            
        Returns:
            Credentials: OAuth2認證憑證
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes,
            state=state
        )
        flow.redirect_uri = self.redirect_uri
        
        flow.fetch_token(code=code)
        
        return flow.credentials
    
    def refresh_token(self, credentials):
        """
        刷新存取令牌
        
        Args:
            credentials: OAuth2認證憑證
            
        Returns:
            Credentials: 刷新後的認證憑證
        """
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        
        return credentials

