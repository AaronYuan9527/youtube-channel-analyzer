import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.channel import channel_bp
from src.routes.system import system_bp
from src.config import config
import logging

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

def create_app(config_name='default'):
    """應用程式工廠函數"""
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, static_folder=static_folder)
    
    # 載入配置
    app.config.from_object(config[config_name])
    
    # 啟用CORS
    CORS(app, origins="*")
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 註冊藍圖
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(channel_bp, url_prefix='/api/channel')
    app.register_blueprint(system_bp, url_prefix='/api/system')
    
    # 初始化數據庫
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404
    
    # 錯誤處理
    @app.errorhandler(404)
    def not_found(error):
        return {
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': '找不到請求的資源'
            }
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': '內部伺服器錯誤'
            }
        }, 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)
