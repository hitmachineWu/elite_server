from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session加密

# 用内存存储用户信息，实际应用中应使用数据库
users = {
    'junyuan': '11'
}

# 卓工院大模型数据
models = [
    {
        'id': 1,
        'name': 'GPT-4',
        'description': 'OpenAI的最先进模型，能够解决复杂任务，理解和生成自然语言。',
        'image_path': 'img/models/gpt4.jpg',
        'detail_url': 'gpt4',
        'external_url': 'https://openai.com/gpt-4'
    },
    {
        'id': 2,
        'name': 'LLaMA',
        'description': 'Meta的开源大型语言模型，专为研究人员设计，具有强大的语言理解能力。',
        'image_path': 'img/models/llama.jpg',
        'detail_url': 'llama',
        'external_url': 'https://ai.meta.com/llama/'
    },
    {
        'id': 3,
        'name': 'Claude',
        'description': 'Anthropic开发的AI助手，专注于安全性和有益的对话，减少有害输出。',
        'image_path': 'img/models/claude.jpg',
        'detail_url': 'claude',
        'external_url': 'https://www.anthropic.com/claude'
    },
    {
        'id': 4,
        'name': 'BERT',
        'description': 'Google的双向Transformer模型，专为自然语言理解而设计，在多种NLP任务中表现出色。',
        'image_path': 'img/models/bert.jpg',
        'detail_url': 'bert',
        'external_url': 'https://github.com/google-research/bert'
    },
    {
        'id': 5,
        'name': 'Gemini',
        'description': 'Google的多模态AI系统，能够理解和生成文本、图像、音频等多种形式的内容。',
        'image_path': 'img/models/gemini.jpg',
        'detail_url': 'gemini',
        'external_url': 'https://deepmind.google/technologies/gemini/'
    }
]

# 模型详情
model_details = {
    'gpt4': {
        'name': 'GPT-4',
        'full_description': '''
        GPT-4是OpenAI开发的最先进的大型语言模型，相比前代产品有显著提升。它能够生成更自然、更精确的文本，
        理解和处理复杂指令，并展现出更强的推理能力。GPT-4在各种专业考试和基准测试中表现出色，
        接近人类表现水平。它支持更长的上下文窗口，允许用户提供更详细的提示和处理更长的对话。
        ''',
        'image_path': 'img/models/gpt4.jpg',
        'features': [
            '强大的自然语言理解和生成能力',
            '多语言支持，包括中英文等多种语言',
            '上下文窗口更大，可处理更长对话',
            '理解和执行复杂指令的能力增强'
        ],
        'use_cases': [
            '内容创作和编辑',
            '代码生成与调试',
            '复杂问题解答',
            '语言翻译'
        ],
        'specs': {
            'params': '1.76万亿参数',
            'training_data': '截至2025年4月的互联网文本、书籍、代码等',
            'languages': '支持多种语言',
            'release_date': '2025年3月'
        },
        'external_url': 'https://openai.com/gpt-4'
    },
    'llama': {
        'name': 'LLaMA',
        'full_description': '''
        LLaMA (Large Language Model Meta AI) 是由Meta AI研发的开源大型语言模型系列。
        它在相对较小的参数规模下展现出了与更卓工院大模型相媲美的性能，这得益于其在更大规模和更高质量的数据集上的训练。
        LLaMA模型有多种规格，从7B到70B参数不等，使其适用于不同的硬件环境和应用场景。
        ''',
        'image_path': 'img/models/llama.jpg',
        'features': [
            '开源可用，便于研究人员和开发者使用',
            '参数规模相对较小但性能强大',
            '可在消费级硬件上运行的版本',
            '支持微调以适应特定任务'
        ],
        'use_cases': [
            '学术研究',
            '自定义AI应用开发',
            '文本生成和理解',
            '对话系统构建'
        ],
        'specs': {
            'params': '7B-70B参数',
            'training_data': '互联网文本、科学论文、代码等',
            'languages': '主要为英语，但支持其他语言',
            'release_date': '2025年2月'
        },
        'external_url': 'https://ai.meta.com/llama/'
    },
    'claude': {
        'name': 'Claude',
        'full_description': '''
        Claude是由Anthropic开发的AI助手，专注于有益、无害和诚实的对话。
        它采用了"宪法AI"方法训练，旨在减少有害输出，增强安全性。
        Claude能够理解复杂指令，生成连贯文本，并在各种任务中表现出色，包括创意写作、编程辅助和知识问答。
        ''',
        'image_path': 'img/models/claude.jpg',
        'features': [
            '强调安全性和减少有害输出',
            '长上下文窗口，可处理大量文本',
            '自然的对话能力',
            '遵循复杂指令的能力'
        ],
        'use_cases': [
            '客户服务',
            '内容审核',
            '教育辅助',
            '创意写作'
        ],
        'specs': {
            'params': '未公开具体参数',
            'training_data': '多样化的文本数据',
            'languages': '主要为英语',
            'release_date': '2022年'
        },
        'external_url': 'https://www.anthropic.com/claude'
    },
    'bert': {
        'name': 'BERT',
        'full_description': '''
        BERT (Bidirectional Encoder Representations from Transformers) 是由Google开发的预训练语言表示模型。
        它的创新之处在于应用了双向训练的Transformer模型，使其能够同时考虑文本的左右上下文，从而更好地理解语言。
        BERT在多种自然语言处理任务中都取得了突破性的成果，包括问答、语言推理、命名实体识别等。
        ''',
        'image_path': 'img/models/bert.jpg',
        'features': [
            '双向上下文理解',
            '强大的语言表示能力',
            '适用于多种NLP任务',
            '可微调以适应特定领域'
        ],
        'use_cases': [
            '搜索引擎优化',
            '情感分析',
            '问答系统',
            '文本分类'
        ],
        'specs': {
            'params': '110M-340M参数',
            'training_data': '维基百科和图书语料库',
            'languages': '初始为英语，后扩展到多语言',
            'release_date': '2018年'
        },
        'external_url': 'https://github.com/google-research/bert'
    },
    'gemini': {
        'name': 'Gemini',
        'full_description': '''
        Gemini是Google DeepMind开发的多模态AI系统，被设计为能够理解和处理文本、图像、音频、视频等多种形式的信息。
        它在各种基准测试中表现出色，尤其是在需要复杂推理的任务上。
        Gemini有多个版本，包括Ultra、Pro和Nano，分别适用于不同的计算环境和应用场景。
        ''',
        'image_path': 'img/models/gemini.jpg',
        'features': [
            '多模态能力，可处理文本、图像等多种形式的输入',
            '强大的推理和问题解决能力',
            '不同规模的版本适应不同需求',
            '与Google生态系统的深度集成'
        ],
        'use_cases': [
            '多模态内容生成',
            '复杂问题解答',
            '编程辅助',
            '教育应用'
        ],
        'specs': {
            'params': '未公开具体参数',
            'training_data': '多模态数据集，包括文本、图像、视频等',
            'languages': '支持多种语言',
            'release_date': '2025年12月'
        },
        'external_url': 'https://deepmind.google/technologies/gemini/'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误，请重试！', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验证用户名是否已存在
        if username in users:
            flash('该用户名已被使用，请选择其他用户名！', 'danger')
            return render_template('register.html')
        
        # 验证密码是否一致
        if password != confirm_password:
            flash('两次输入的密码不一致！', 'danger')
            return render_template('register.html')
        
        # 验证用户名格式
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            flash('用户名只能包含字母、数字和下划线，长度为3-20个字符！', 'danger')
            return render_template('register.html')
        
        # 创建新用户
        users[username] = password
        
        flash('账号创建成功！请登录。', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('请先登录！', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', models=models)

@app.route('/model/<model_url>')
def model_detail(model_url):
    if 'username' not in session:
        flash('请先登录！', 'danger')
        return redirect(url_for('login'))
    
    if model_url not in model_details:
        flash('模型不存在！', 'danger')
        return redirect(url_for('dashboard'))
    
    model = model_details[model_url]
    return render_template('model_detail.html', model=model)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('您已成功退出登录！', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
