from flask import Blueprint, send_from_directory, current_app
import os

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def index():
    """提供前端主頁"""
    return send_from_directory(current_app.static_folder, 'index.html')

@frontend_bp.route('/<path:path>')
def static_files(path):
    """提供靜態檔案"""
    try:
        return send_from_directory(current_app.static_folder, path)
    except:
        # 如果檔案不存在，返回index.html（用於SPA路由）
        return send_from_directory(current_app.static_folder, 'index.html')

