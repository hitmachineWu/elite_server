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
new_chat_url="http://180.85.206.30:3000/chat/share?shareId=rrc0cvrtg9kl80bgl3mz9778"
agent1='http://180.85.206.30:3000/chat/share?shareId=ztwmryjyyn7a6zt6rtyl5pcg'

# 智能体数据
agents = [
    {
        "id": 1,
        "name": "定量工程设计",
        "description": "助你学习如何在工程设计过程中运用定量分析方法，作出更加科学的决策。",
        "url": agent1,
        "image_url": "/static/img/c0.png"
    },
    {
        "id": 2,
        "name": "编程助手",
        "description": "专注于帮助解决编程问题的智能体，支持多种编程语言。",
        "url": DEFAULT_EMBED_URL,
        "image_url": "/static/img/c1.png"
    },

]

agents_kd1=''

agents_kd = [
    {
        "id": 1,
        "name": "GPT-4",
        "description": "OpenAI的最先进模型，能够解决复杂任务，理解和生成自然语言。",
        "url": 'https://openai.com/gpt-4',
        "image_url": "/static/img/gpt4.png"
    },
    {
        "id": 2,
        "name": "LLaMA",
        "description": "Meta的开源大型语言模型，专为研究人员设计，具有强大的语言理解能力。",
        "url": 'https://ai.meta.com/llama/',
        "image_url": "/static/img/llama.png"
    },
    {
        "id": 3,
        "name": "Claude",
        "description": "Anthropic开发的AI助手，专注于安全性和有益的对话，减少有害输出。",
        "url": 'https://www.anthropic.com/claude',
        "image_url": "/static/img/cloude.png"
    },
    {
        "id": 4,
        "name": "BERT",
        "description": "Google的双向Transformer模型，专为自然语言理解而设计，在多种NLP任务中表现出色。",
        "url": 'https://github.com/google-research/bert',
        "image_url": "/static/img/bert.png"
    },
    {
        "id": 5,
        "name": "Gemini",
        "description": "Google的多模态AI系统，能够理解和生成文本、图像、音频等多种形式的内容。",
        "url": 'https://deepmind.google/technologies/gemini/',
        "image_url": "/static/img/gemin.png"
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
                          embed_url=new_chat_url,
                          username=session.get('username', '用户'))

@app.route('/dashboard/kd')
@login_required
def course_kd():
    # 参照course_agents传递完整智能体列表
    return render_template('dashboard/kd.html', 
                         agents=agents_kd,  # 关键修改点：传递列表而非单个URL
                         username=session.get('username', '用户'))

@app.route('/dashboard/kds/<int:agent_id>')
@login_required
def view_kd(agent_id):
    agent = next((a for a in agents_kd if a['id'] == agent_id), None)
    if not agent:
        flash('找不到该知识库智能体', 'error')
        return redirect(url_for('course_kd'))
    return render_template('dashboard/new_chat.html',
                         embed_url=agent['url'],
                         agent=agent,
                         username=session.get('username', '用户'))



@app.route('/dashboard/his')
@login_required
def his():
    return render_template('dashboard/his.html', 
                          embed_url=new_chat_url,
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