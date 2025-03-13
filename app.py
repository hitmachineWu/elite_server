from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from models import db, UserInfo, Course, Favorite
from routes.auth import auth_bp
from routes.content import content_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化登录管理器
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return UserInfo.query.get(int(id))
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(content_bp)
    
    # 重定向根URL到content_bp的index
    @app.route('/')
    def home():
        return redirect(url_for('content.index'))
    
    # 创建数据库表和初始数据
    with app.app_context():
        db.create_all()
        
        # 添加测试用户 (如果不存在)
        if not UserInfo.query.filter_by(UID='test001').first():
            from werkzeug.security import generate_password_hash
            test_user = UserInfo(
                UID='test001',
                UName='测试用户',
                password=generate_password_hash('password123')
            )
            db.session.add(test_user)
            db.session.commit()
            print("创建测试用户: test001 (密码: password123)")
        
        # 添加初始课程数据
        if Course.query.count() == 0:
            default_courses = [
                Course(
                    title="通用对话模型",
                    description="支持多种场景的通用对话AI模型，能够理解和回应各种问题，适合日常学习和研究使用。",
                    url="http://180.85.206.30:3000/chat/share?shareId=rrc0cvrtg9kl80bgl3mz9778",
                    image_url="/static/images/general-chat.jpg"
                ),
                Course(
                    title="专业课程辅导模型",
                    description="针对工程专业课程设计的AI辅导模型，深入理解专业知识，提供详细的解答和指导。",
                    url="http://180.85.206.30:3000/chat/share?shareId=ztwmryjyyn7a6zt6rtyl5pcg",
                    image_url="/static/images/course-assistant.jpg"
                ),
                Course(
                    title="编程助手",
                    description="帮助解决编程问题和代码优化的AI模型，支持多种编程语言，提供代码示例和解释。",
                    url="http://180.85.206.30:3000/chat/share?shareId=ztwmryjyyn7a6zt6rtyl5pcg",
                    image_url="/static/images/code-assistant.jpg"
                )
            ]
            db.session.add_all(default_courses)
            db.session.commit()
            print("创建默认课程数据")
            
            # 为测试用户添加一个收藏
            test_user = UserInfo.query.filter_by(UID='test001').first()
            if test_user:
                favorite = Favorite(
                    user_id=test_user.id,
                    course_id=1  # 收藏第一个课程
                )
                db.session.add(favorite)
                db.session.commit()
                print("为测试用户添加收藏")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)