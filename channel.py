from datetime import datetime
from src.models.user import db

class Channel(db.Model):
    """YouTube頻道模型"""
    __tablename__ = 'channels'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    custom_url = db.Column(db.String(255))
    published_at = db.Column(db.DateTime)
    thumbnail_default = db.Column(db.Text)
    thumbnail_medium = db.Column(db.Text)
    thumbnail_high = db.Column(db.Text)
    country = db.Column(db.String(2))
    view_count = db.Column(db.BigInteger, default=0)
    subscriber_count = db.Column(db.BigInteger, default=0)
    video_count = db.Column(db.Integer, default=0)
    uploads_playlist_id = db.Column(db.String(255))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'channelId': self.channel_id,
            'title': self.title,
            'description': self.description,
            'customUrl': self.custom_url,
            'publishedAt': self.published_at.isoformat() if self.published_at else None,
            'thumbnails': {
                'default': self.thumbnail_default,
                'medium': self.thumbnail_medium,
                'high': self.thumbnail_high
            },
            'country': self.country,
            'statistics': {
                'viewCount': self.view_count,
                'subscriberCount': self.subscriber_count,
                'videoCount': self.video_count
            },
            'contentDetails': {
                'uploadsPlaylistId': self.uploads_playlist_id
            },
            'lastUpdated': self.last_updated.isoformat() if self.last_updated else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_youtube_data(cls, youtube_data):
        """從YouTube API數據建立頻道物件"""
        snippet = youtube_data.get('snippet', {})
        statistics = youtube_data.get('statistics', {})
        content_details = youtube_data.get('contentDetails', {})
        thumbnails = snippet.get('thumbnails', {})
        
        return cls(
            channel_id=youtube_data.get('id'),
            title=snippet.get('title'),
            description=snippet.get('description'),
            custom_url=snippet.get('customUrl'),
            published_at=datetime.fromisoformat(snippet.get('publishedAt', '').replace('Z', '+00:00')) if snippet.get('publishedAt') else None,
            thumbnail_default=thumbnails.get('default', {}).get('url'),
            thumbnail_medium=thumbnails.get('medium', {}).get('url'),
            thumbnail_high=thumbnails.get('high', {}).get('url'),
            country=snippet.get('country'),
            view_count=int(statistics.get('viewCount', 0)),
            subscriber_count=int(statistics.get('subscriberCount', 0)),
            video_count=int(statistics.get('videoCount', 0)),
            uploads_playlist_id=content_details.get('relatedPlaylists', {}).get('uploads')
        )

class ChannelStatisticsHistory(db.Model):
    """頻道統計歷史記錄模型"""
    __tablename__ = 'channel_statistics_history'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(255), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    view_count = db.Column(db.BigInteger, default=0)
    subscriber_count = db.Column(db.BigInteger, default=0)
    video_count = db.Column(db.Integer, default=0)
    estimated_minutes_watched = db.Column(db.BigInteger, default=0)
    average_view_duration = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('channel_id', 'date', name='_channel_date_uc'),)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'channelId': self.channel_id,
            'date': self.date.isoformat(),
            'viewCount': self.view_count,
            'subscriberCount': self.subscriber_count,
            'videoCount': self.video_count,
            'estimatedMinutesWatched': self.estimated_minutes_watched,
            'averageViewDuration': self.average_view_duration,
            'createdAt': self.created_at.isoformat()
        }

class AudienceDemographics(db.Model):
    """受眾輪廓模型"""
    __tablename__ = 'audience_demographics'
    
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(255), nullable=False, index=True)
    date_range_start = db.Column(db.Date, nullable=False, index=True)
    date_range_end = db.Column(db.Date, nullable=False, index=True)
    dimension_type = db.Column(db.String(50), nullable=False)  # 'ageGroup', 'gender', 'country', 'deviceType'
    dimension_value = db.Column(db.String(100), nullable=False)
    views_percentage = db.Column(db.Numeric(5, 2), default=0)
    watch_time_percentage = db.Column(db.Numeric(5, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('channel_id', 'date_range_start', 'date_range_end', 'dimension_type', 'dimension_value', 
                          name='_demographics_unique'),
        db.Index('idx_demographics_channel_type', 'channel_id', 'dimension_type'),
        db.Index('idx_demographics_date_range', 'date_range_start', 'date_range_end')
    )
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'channelId': self.channel_id,
            'dateRangeStart': self.date_range_start.isoformat(),
            'dateRangeEnd': self.date_range_end.isoformat(),
            'dimensionType': self.dimension_type,
            'dimensionValue': self.dimension_value,
            'viewsPercentage': float(self.views_percentage),
            'watchTimePercentage': float(self.watch_time_percentage),
            'createdAt': self.created_at.isoformat()
        }

class Video(db.Model):
    """影片模型"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    channel_id = db.Column(db.String(255), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    published_at = db.Column(db.DateTime, index=True)
    duration = db.Column(db.String(20))  # ISO 8601 duration format
    thumbnail_default = db.Column(db.Text)
    thumbnail_medium = db.Column(db.Text)
    thumbnail_high = db.Column(db.Text)
    view_count = db.Column(db.BigInteger, default=0, index=True)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Numeric(5, 2), default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            'videoId': self.video_id,
            'channelId': self.channel_id,
            'title': self.title,
            'description': self.description,
            'publishedAt': self.published_at.isoformat() if self.published_at else None,
            'duration': self.duration,
            'thumbnails': {
                'default': self.thumbnail_default,
                'medium': self.thumbnail_medium,
                'high': self.thumbnail_high
            },
            'statistics': {
                'viewCount': self.view_count,
                'likeCount': self.like_count,
                'commentCount': self.comment_count
            },
            'engagementRate': float(self.engagement_rate),
            'lastUpdated': self.last_updated.isoformat(),
            'createdAt': self.created_at.isoformat()
        }
    
    @classmethod
    def from_youtube_data(cls, youtube_data, channel_id):
        """從YouTube API數據建立影片物件"""
        snippet = youtube_data.get('snippet', {})
        statistics = youtube_data.get('statistics', {})
        content_details = youtube_data.get('contentDetails', {})
        thumbnails = snippet.get('thumbnails', {})
        
        view_count = int(statistics.get('viewCount', 0))
        like_count = int(statistics.get('likeCount', 0))
        comment_count = int(statistics.get('commentCount', 0))
        
        # 計算互動率 (按讚數 + 留言數) / 觀看數 * 100
        engagement_rate = 0
        if view_count > 0:
            engagement_rate = ((like_count + comment_count) / view_count) * 100
        
        return cls(
            video_id=youtube_data.get('id'),
            channel_id=channel_id,
            title=snippet.get('title'),
            description=snippet.get('description'),
            published_at=datetime.fromisoformat(snippet.get('publishedAt', '').replace('Z', '+00:00')) if snippet.get('publishedAt') else None,
            duration=content_details.get('duration'),
            thumbnail_default=thumbnails.get('default', {}).get('url'),
            thumbnail_medium=thumbnails.get('medium', {}).get('url'),
            thumbnail_high=thumbnails.get('high', {}).get('url'),
            view_count=view_count,
            like_count=like_count,
            comment_count=comment_count,
            engagement_rate=engagement_rate
        )

