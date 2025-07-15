from flask import Blueprint, jsonify
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

system_bp = Blueprint('system', __name__)

@system_bp.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return {'status': 'healthy'}

@system_bp.route('/quota/status', methods=['GET'])
def quota_status():
    """檢查API配額狀態"""
    try:
        # 這裡可以實作實際的配額檢查邏輯
        # 目前返回模擬數據
        return jsonify({
            'success': True,
            'data': {
                'quotaUsed': 1234,
                'quotaLimit': 10000,
                'quotaRemaining': 8766,
                'resetTime': (datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)).isoformat() + 'Z',
                'services': {
                    'youtubeDataAPI': {
                        'quotaUsed': 800,
                        'quotaLimit': 10000,
                        'quotaRemaining': 9200
                    },
                    'youtubeAnalyticsAPI': {
                        'quotaUsed': 434,
                        'quotaLimit': 10000,
                        'quotaRemaining': 9566
                    }
                }
            }
        })
    except Exception as e:
        logger.error(f"檢查配額狀態失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'QUOTA_CHECK_ERROR',
                'message': '檢查配額狀態時發生錯誤',
                'details': str(e)
            }
        }), 500

@system_bp.route('/config', methods=['GET'])
def get_config():
    """獲取系統配置資訊（不包含敏感資訊）"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'features': {
                    'youtubeDataAPI': bool(os.environ.get('YOUTUBE_API_KEY')),
                    'youtubeAnalyticsAPI': bool(os.environ.get('GOOGLE_CLIENT_ID')),
                    'oauth': bool(os.environ.get('GOOGLE_CLIENT_ID') and os.environ.get('GOOGLE_CLIENT_SECRET')),
                    'caching': True,
                    'rateLimit': True
                },
                'limits': {
                    'maxChannelsCompare': 5,
                    'maxSearchResults': 50,
                    'maxVideosPerChannel': 50,
                    'defaultDateRangeDays': 30
                },
                'cache': {
                    'channelBasicInfo': 3600,  # 1小時
                    'channelStatistics': 1800,  # 30分鐘
                    'audienceDemographics': 21600,  # 6小時
                    'videosList': 3600  # 1小時
                },
                'rateLimit': {
                    'requestsPerMinute': 100,
                    'requestsPerHour': 1000
                }
            }
        })
    except Exception as e:
        logger.error(f"獲取系統配置失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'CONFIG_ERROR',
                'message': '獲取系統配置時發生錯誤',
                'details': str(e)
            }
        }), 500

@system_bp.route('/stats', methods=['GET'])
def get_system_stats():
    """獲取系統統計資訊"""
    try:
        from src.models.channel import Channel, Video
        from src.models.user import User
        
        # 獲取數據庫統計
        total_channels = Channel.query.count()
        total_videos = Video.query.count()
        total_users = User.query.count()
        
        # 獲取最近活動
        recent_channels = Channel.query.order_by(Channel.last_updated.desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'database': {
                    'totalChannels': total_channels,
                    'totalVideos': total_videos,
                    'totalUsers': total_users
                },
                'recentActivity': {
                    'recentChannels': [
                        {
                            'channelId': channel.channel_id,
                            'title': channel.title,
                            'lastUpdated': channel.last_updated.isoformat()
                        }
                        for channel in recent_channels
                    ]
                },
                'systemInfo': {
                    'uptime': 'N/A',  # 可以實作實際的運行時間計算
                    'memoryUsage': 'N/A',  # 可以實作記憶體使用量監控
                    'diskUsage': 'N/A'  # 可以實作磁碟使用量監控
                }
            }
        })
    except Exception as e:
        logger.error(f"獲取系統統計失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'STATS_ERROR',
                'message': '獲取系統統計時發生錯誤',
                'details': str(e)
            }
        }), 500

