import pymysql
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, send_from_directory
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid

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
DEFAULT_EMBED_URL = "http://180.85.206.30:3000/chat/share?shareId=cc1greng47slrl6ivb6ik03p"
new_chat_url="http://180.85.206.30:3000/chat/share?shareId=cc1greng47slrl6ivb6ik03p" # 默认
agent1='http://180.85.206.30:3000/chat/share?shareId=ztwmryjyyn7a6zt6rtyl5pcg' # 不用
agent_class_url = "http://180.85.206.30:3000/chat/share?shareId=zci1ditlgimgguu13dz5ra5n&studentUid="
agent_develop_url = "http://180.85.206.21:3000/chat/share?shareId=3b2pdqik1odzyy3egy0n5o3a&studentUid="

# 智能体数据
agents = [
    { 
        "id": 1,
        "name": "定量工程设计",
        "description": "助你学习如何在工程设计过程中运用定量分析方法，作出更加科学的决策。",
        "url": agent_class_url,
        "image_url": "/static/img/c0.png"
    },
    { 
        "id": 2,
        "name": "课程",
        "description": "助你学习如何在工程设计过程中运用定量分析方法，作出更加科学的决策。",
        "url": agent_class_url,
        "image_url": "/static/img/c0.png"
    },
    {
        "id": 3,
        "name": "Agent内部开发自测",
        "description": "开发团队内部自测",
        "url": agent_develop_url,
        "image_url": "/static/img/c1.png"
    }
]

agents_kd1=''

agents_kd = [
    {
        "id": 2,
        "name": "编程助手",
        "description": "专注于帮助解决编程问题的智能体，支持多种编程语言。",
        "url": 0,
        "image_url": "/static/img/c1.png"
    }
]

# 定义KG服务相关的常量
KG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'KG')

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

        # 判断注册资格 先判断学号是否存在 再判断账号是否注册（邮箱是否为空）
        cursor.execute("SELECT sid, email FROM student WHERE sid = %s", username)
        result = cursor.fetchone()
        if result is None:
            flash('非法学号')
            return redirect(url_for('register'))
        elif result[1] is not None:
            flash('账号已被注册')
            return redirect(url_for('register'))

        cursor.execute("SELECT email FROM student WHERE email = %s", email)
        result = cursor.fetchone()
        if result is not None:
            flash('邮箱已被注册')
            return redirect(url_for('register'))
            
        cursor.execute("UPDATE student SET password = %s, email = %s WHERE sid = %s",
                       (password, email, username))
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
    embed_url = agent['url']
    username=session.get('username', '用户')
    # if agent_id == 3:  # 仅对 id 为 3 的智能体进行特殊处理
    #     # 使用预先定义的包含 studentUid 参数的 URL
    print(f"username = {username}")
    embed_url = embed_url + username
    print(f"embed_url  = {embed_url} ")
    return render_template('dashboard/new_chat.html',
                           embed_url=embed_url,
                           agent=agent,
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


# 知识图谱相关路由
@app.route('/kg')
def kg_index():
    """显示知识图谱主页"""
    return send_from_directory(KG_FOLDER, 'nn_output_enhanced.html')

@app.route('/js/<path:filename>')
def kg_js(filename):
    """提供JavaScript文件服务"""
    return send_from_directory(KG_FOLDER, filename)

@app.route('/generate_kg', methods=['POST'])
def proxy_generate_kg():
    """处理生成知识图谱的请求"""
    try:
        # 从请求中获取数据
        data = request.json
        
        # 直接导入KG服务中的相关模块
        try:
            from KG.kg_json import KnowledgeGraphGenerator
            from KG.kg_json2graph import create_graph, load_json_data
            
            keyword = data.get('keyword')
            display_mode = data.get('display_mode', 'new_page')
            
            print(f"收到生成知识图谱请求：关键词 = {keyword}, 显示模式 = {display_mode}")
            
            if not keyword:
                print("错误：关键词为空")
                return jsonify({'error': '关键词不能为空'}), 400
            
            # 创建目录
            KG_STATIC_DIR = os.path.join(KG_FOLDER, 'static')
            KG_OUTPUT_DIR = os.path.join(KG_STATIC_DIR, 'output')
            os.makedirs(KG_STATIC_DIR, exist_ok=True)
            os.makedirs(KG_OUTPUT_DIR, exist_ok=True)
            
            # 创建唯一文件名
            unique_id = str(uuid.uuid4())[:8]
            json_file = os.path.join(KG_OUTPUT_DIR, f'kg_{keyword}_{unique_id}.json')
            html_file = os.path.join(KG_OUTPUT_DIR, f'kg_{keyword}_{unique_id}.html')
            
            print(f"将生成JSON文件：{json_file}")
            print(f"将生成HTML文件：{html_file}")
            
            # 生成知识图谱
            kg_generator = KnowledgeGraphGenerator()
            json_result = kg_generator.generate_knowledge_graph(keyword=keyword, output_file=json_file)
            
            if not json_result:
                print("知识图谱生成失败：无返回结果")
                return jsonify({'error': '知识图谱生成失败'}), 500
            
            # 加载生成的JSON数据
            nodes, links = load_json_data(json_file)
            
            if not nodes or not links:
                print(f"知识图谱数据为空：nodes={nodes}, links={links}")
                return jsonify({'error': '知识图谱数据为空'}), 500
            
            # 创建图表
            c = create_graph(nodes, links)
            
            # 渲染HTML文件
            c.render(html_file)
            
            result = {
                'success': True,
                'keyword': keyword,
                'json_path': f'/KG/static/output/{os.path.basename(json_file)}',
                'html_path': f'/KG/static/output/{os.path.basename(html_file)}',
                'nodes': nodes,
                'links': links,
                'display_mode': display_mode
            }
            
            print(f"知识图谱生成成功：{result}")
            return jsonify(result)
            
        except Exception as e:
            import traceback
            print(f"处理请求时出错: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': f'处理请求时出错: {str(e)}'}), 500
            
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")
        return jsonify({'error': f'处理请求时出错: {str(e)}'}), 500

@app.route('/KG/static/output/<path:filename>')
def kg_output_files(filename):
    """提供KG生成的输出文件"""
    output_dir = os.path.join(KG_FOLDER, 'static', 'output')
    return send_from_directory(output_dir, filename)


# 应用启动前初始化
create_sample_images()

# 预加载KG模块，确保可以正常导入
try:
    from KG.kg_json import KnowledgeGraphGenerator
    from KG.kg_json2graph import create_graph, load_json_data
    print("KG模块加载成功")
except Exception as e:
    print(f"KG模块加载失败: {str(e)}")

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
    app.run(debug=True, host='0.0.0.0', port=5000)