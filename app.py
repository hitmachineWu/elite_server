import pymysql
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
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
        if 'username' not in session:
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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        sql = "select password from student where sid = " + username
        # 执行 SQL 查询
        cursor.execute(sql)
        # 获取单条结果
        result = cursor.fetchone()
        if result and result[0] == password:
            session['username'] = username
            return redirect(url_for('new_chat'))
        else:
            print("error")
            flash('用户名或密码错误，请重试！', 'danger')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if 'user_email' in session:
    #     return redirect(url_for('new_chat'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        sql = "select password from student where sid = " + username
        # 执行 SQL 查询
        cursor.execute(sql)
        # 获取单条结果
        result = cursor.fetchone()
        if result and result[0] == username:
            flash('该学号已被注册')
            return redirect(url_for('register'))

        e = "\"" + email + "\""
        sql = "select email from student where email = " + e
        # 执行 SQL 查询
        cursor.execute(sql)
        # 获取单条结果
        result = cursor.fetchone()
        if result and result[0] == email:
            flash('该邮箱已被注册')
            return redirect(url_for('register'))

        cursor.execute("INSERT INTO student (sid, password, email) VALUES (%s, %s, %s)",
                       (username, password, email))
        conn.commit()
        flash('注册成功，请登录')
        return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/change_password')
def change_password():
    if request.method == 'POST':
        p1 = request.form.get('p1')
        p2 = request.form.get('p2')
        if p1 == p2:
            cursor.execute("UPDATE student SET password = %s WHERE sid = %s", (p1, session["username"]))
        else:
            flash('两次输入的密码不相同，请重新修改')
    return redirect(url_for('new_chat'))


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        sid = request.form.get('username')
        email = request.form.get('email')

        # 查询数据库，检查学号和邮箱是否匹配
        # e = "\"" + email + "\""
        cursor.execute("SELECT password FROM student WHERE sid = %s AND email = %s", (sid, email))
        user = cursor.fetchone()

        if not user:  # 数据库中找不到匹配的记录
            flash('输入学号或邮箱错误')
            return redirect(url_for('forget_password'))
        cursor.execute("UPDATE student SET password = %s WHERE sid = %s", (sid, sid))
        conn.commit()
        return redirect(url_for('login'))

    return render_template('auth/forget_password.html')


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


@app.route("/get_session")
def get_session():
    username = session.get("username", "1111")  # 获取 session 数据
    return jsonify({"username": username})


# 应用启动前初始化
create_sample_images()

if __name__ == '__main__':
    # 用户表名称——student
    # 如下4个字段
    # id
    # sid 学号
    # password 密码
    # email 邮箱
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="zgllm",
        charset="utf8mb4"

    )
    cursor = conn.cursor()
    app.run(debug=True)