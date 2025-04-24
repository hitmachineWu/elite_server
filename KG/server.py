from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import uuid
from kg_json import KnowledgeGraphGenerator
from kg_json2graph import create_graph, load_json_data

app = Flask(__name__)
# 添加CORS支持，允许从任何域进行请求
CORS(app)

# 配置静态文件目录
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
OUTPUT_DIR = os.path.join(STATIC_DIR, 'output')

# 创建必要的目录
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    """主页路由"""
    return send_from_directory('.', 'nn_output_enhanced.html')

@app.route('/static/<path:path>')
def send_static(path):
    """提供静态文件服务"""
    return send_from_directory('static', path)

@app.route('/generate_kg', methods=['POST'])
def generate_kg():
    """处理生成知识图谱的请求"""
    # 获取请求数据
    data = request.json
    keyword = data.get('keyword')
    display_mode = data.get('display_mode', 'new_page')  # 默认为新页面打开，实则当前页面打开
    
    print(f"收到生成知识图谱请求：关键词 = {keyword}, 显示模式 = {display_mode}")
    
    if not keyword:
        print("错误：关键词为空")
        return jsonify({'error': '关键词不能为空'}), 400
    
    try:
        # 创建唯一文件名
        unique_id = str(uuid.uuid4())[:8]
        json_file = os.path.join(OUTPUT_DIR, f'kg_{keyword}_{unique_id}.json')
        html_file = os.path.join(OUTPUT_DIR, f'kg_{keyword}_{unique_id}.html')
        
        print(f"将生成JSON文件：{json_file}")
        print(f"将生成HTML文件：{html_file}")
        
        # 在每次请求中重新创建KnowledgeGraphGenerator实例
        # 这样可以避免多线程问题
        kg_generator = KnowledgeGraphGenerator()
        json_result = kg_generator.generate_knowledge_graph(keyword=keyword, output_file=json_file)
        
        if not json_result:
            print(f"知识图谱生成失败：无返回结果")
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
            'json_path': f'/static/output/{os.path.basename(json_file)}',
            'html_path': f'/static/output/{os.path.basename(html_file)}',
            'nodes': nodes,
            'links': links,
            'display_mode': display_mode
        }
        print(f"知识图谱生成成功：{result}")
        
        # 返回结果
        return jsonify(result)
    
    except Exception as e:
        error_msg = f"生成知识图谱时出错: {str(e)}"
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    """添加响应头，禁止缓存"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=7000) 
