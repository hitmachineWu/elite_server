from flask import Flask, render_template, redirect, url_for, flash, request, session
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-replace-in-production'

# 内存中存储用户数据
users = {
    "admin@example.com": {
        "username": "admin",
        "password": generate_password_hash("password"),
        "favorites": []
    }
}
# 默认的嵌入URL
DEFAULT_EMBED_URL = "http://180.85.206.30:3000/chat/share?shareId=rrc0cvrtg9kl80bgl3mz9778"

# 智能体数据
agents = [
    {
        "id": 1,
        "name": "DeepSeek Chat",
        "description": "DeepSeek的官方聊天模型，支持多轮对话和复杂任务处理。",
        "url": DEFAULT_EMBED_URL,
        "image_url": "/static/img/deepseek.png"
    },
    {
        "id": 2,
        "name": "编程助手",
        "description": "专注于帮助解决编程问题的智能体，支持多种编程语言。",
        "url": DEFAULT_EMBED_URL,
        "image_url": "/static/img/coding.png"
    },
    {
        "id": 3,
        "name": "数学导师",
        "description": "数学问题解答专家，可以帮助解决从基础到高等数学的各类问题。",
        "url": DEFAULT_EMBED_URL,
        "image_url": "/static/img/math.png"
    },
    {
        "id": 4,
        "name": "论文写作助手",
        "description": "帮助用户进行学术论文写作、润色和参考文献管理。",
        "url": DEFAULT_EMBED_URL,
        "image_url": "/static/img/academic.png"
    }
]


# 登录验证装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('请先登录')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 创建必要的目录
os.makedirs('static/img', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('templates/auth', exist_ok=True)
os.makedirs('templates/dashboard', exist_ok=True)

# 创建示例图片文件
def create_sample_images():
    # 创建一些简单的空图片文件作为占位符
    placeholder_images = [
        'static/img/deepseek.png',
        'static/img/coding.png',
        'static/img/math.png',
        'static/img/academic.png'
    ]
    
    for img_path in placeholder_images:
        if not os.path.exists(img_path):
            with open(img_path, 'w') as f:
                f.write('placeholder')

# 路由
@app.route('/')
def index():
    if 'user_email' in session:
        return redirect(url_for('new_chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_email' in session:
        return redirect(url_for('new_chat'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users and check_password_hash(users[email]['password'], password):
            session['user_email'] = email
            session['username'] = users[email]['username']
            return redirect(url_for('new_chat'))
        else:
            flash('邮箱或密码不正确')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_email' in session:
        return redirect(url_for('new_chat'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users:
            flash('该邮箱已被注册')
            return redirect(url_for('register'))
        
        # 创建新用户
        users[email] = {
            "username": username,
            "password": generate_password_hash(password),
            "favorites": []
        }
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard/new-chat')
@login_required
def new_chat():
    return render_template('dashboard/new_chat.html', 
                          embed_url=DEFAULT_EMBED_URL,
                          username=session.get('username', '用户'))

@app.route('/dashboard/agents')
@login_required
def course_agents():
    return render_template('dashboard/agents.html', 
                          agents=agents, 
                          username=session.get('username', '用户'))

@app.route('/dashboard/agent/<int:agent_id>')
@login_required
def view_agent(agent_id):
    agent = next((a for a in agents if a['id'] == agent_id), None)
    if not agent:
        flash('找不到该智能体')
        return redirect(url_for('course_agents'))
    
    return render_template('dashboard/new_chat.html', 
                          embed_url=agent['url'],
                          agent=agent,
                          username=session.get('username', '用户'))

@app.route('/dashboard/favorites')
@login_required
def favorites():
    user_email = session.get('user_email')
    if not user_email or user_email not in users:
        return redirect(url_for('logout'))
        
    user_favorites = users[user_email]['favorites']
    favorite_agents = [agent for agent in agents if agent['id'] in user_favorites]
    
    return render_template('dashboard/favorites.html', 
                          agents=favorite_agents, 
                          username=session.get('username', '用户'))

@app.route('/api/toggle-favorite/<int:agent_id>', methods=['POST'])
@login_required
def toggle_favorite(agent_id):
    user_email = session.get('user_email')
    if not user_email or user_email not in users:
        return {'error': 'User not found'}, 404
        
    user_favorites = users[user_email]['favorites']
    
    if agent_id in user_favorites:
        user_favorites.remove(agent_id)
        return {'status': 'removed'}
    else:
        user_favorites.append(agent_id)
        return {'status': 'added'}

# 应用启动前初始化
create_sample_images()

if __name__ == '__main__':
    app.run(debug=True)