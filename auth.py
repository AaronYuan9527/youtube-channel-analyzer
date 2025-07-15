from flask import Blueprint, request, jsonify, session, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.services.youtube_service import YouTubeOAuthService
from src.models.user import User, db
import logging
import os

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login():
    """初始化OAuth認證"""
    try:
        oauth_service = YouTubeOAuthService()
        authorization_url, state = oauth_service.get_authorization_url()
        
        # 將state儲存在session中用於驗證
        session['oauth_state'] = state
        
        return jsonify({
            'success': True,
            'authorizationUrl': authorization_url,
            'state': state
        })
    except Exception as e:
        logger.error(f"OAuth登入初始化失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'OAUTH_INIT_ERROR',
                'message': '無法初始化OAuth認證',
                'details': str(e)
            }
        }), 500

@auth_bp.route('/callback', methods=['GET'])
def oauth_callback():
    """處理OAuth回調"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'OAUTH_ERROR',
                    'message': f'OAuth認證失敗: {error}'
                }
            }), 400
        
        if not code or not state:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_PARAMETERS',
                    'message': '缺少必要的OAuth參數'
                }
            }), 400
        
        # 驗證state參數
        if session.get('oauth_state') != state:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_STATE',
                    'message': '無效的OAuth狀態參數'
                }
            }), 400
        
        # 交換授權碼獲取存取令牌
        oauth_service = YouTubeOAuthService()
        credentials = oauth_service.exchange_code_for_token(code, state)
        
        # 獲取用戶資訊
        from googleapiclient.discovery import build
        oauth2_service = build('oauth2', 'v2', credentials=credentials)
        user_info = oauth2_service.userinfo().get().execute()
        
        # 查找或建立用戶
        user = User.query.filter_by(google_id=user_info['id']).first()
        if not user:
            user = User(
                google_id=user_info['id'],
                email=user_info['email'],
                name=user_info['name'],
                picture_url=user_info.get('picture')
            )
            db.session.add(user)
        else:
            # 更新用戶資訊
            user.email = user_info['email']
            user.name = user_info['name']
            user.picture_url = user_info.get('picture')
        
        # 儲存OAuth令牌
        user.access_token = credentials.token
        user.refresh_token = credentials.refresh_token
        user.token_expires_at = credentials.expiry
        
        db.session.commit()
        
        # 建立JWT令牌
        access_token = create_access_token(identity=user.id)
        
        # 清除session中的state
        session.pop('oauth_state', None)
        
        return jsonify({
            'success': True,
            'message': '認證成功',
            'accessToken': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'pictureUrl': user.picture_url
            }
        })
    except Exception as e:
        logger.error(f"OAuth回調處理失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'OAUTH_CALLBACK_ERROR',
                'message': '處理OAuth回調時發生錯誤',
                'details': str(e)
            }
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """登出"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user:
            # 清除OAuth令牌
            user.access_token = None
            user.refresh_token = None
            user.token_expires_at = None
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '已成功登出'
        })
    except Exception as e:
        logger.error(f"登出失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'LOGOUT_ERROR',
                'message': '登出時發生錯誤',
                'details': str(e)
            }
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """獲取當前用戶資訊"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'USER_NOT_FOUND',
                    'message': '找不到用戶'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'pictureUrl': user.picture_url,
                'hasValidToken': user.access_token is not None
            }
        })
    except Exception as e:
        logger.error(f"獲取用戶資訊失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'GET_USER_ERROR',
                'message': '獲取用戶資訊時發生錯誤',
                'details': str(e)
            }
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_oauth_token():
    """刷新OAuth令牌"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or not user.refresh_token:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NO_REFRESH_TOKEN',
                    'message': '沒有可用的刷新令牌'
                }
            }), 400
        
        # 建立認證憑證物件
        from google.oauth2.credentials import Credentials
        credentials = Credentials(
            token=user.access_token,
            refresh_token=user.refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.environ.get('GOOGLE_CLIENT_ID'),
            client_secret=os.environ.get('GOOGLE_CLIENT_SECRET')
        )
        
        # 刷新令牌
        oauth_service = YouTubeOAuthService()
        refreshed_credentials = oauth_service.refresh_token(credentials)
        
        # 更新用戶的令牌資訊
        user.access_token = refreshed_credentials.token
        user.token_expires_at = refreshed_credentials.expiry
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '令牌已成功刷新'
        })
    except Exception as e:
        logger.error(f"刷新OAuth令牌失敗: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'TOKEN_REFRESH_ERROR',
                'message': '刷新令牌時發生錯誤',
                'details': str(e)
            }
        }), 500

