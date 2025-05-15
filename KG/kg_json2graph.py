from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType
import json
import webbrowser
import os
import re

def create_graph(categories=None, nodes=None, links=None):
    """
    创建关系图
    :param nodes: 节点数据
    :param links: 连接数据
    :return: 图表对象
    """
    # 定义节点类别
    # categories = [
    #     {"name": "Neural Center"},
    #     {"name": "工程技术"},
       
       
    # ]

    # 如果没有提供数据，加载示例数据
    if nodes is None or links is None:
        print("未提供节点或连接数据，使用示例数据")
        categories , nodes, links = load_example_data()
    else:
        print(f"使用提供的数据: {len(nodes)} 个节点和 {len(links)} 个连接")
        
    # 打印前几个节点和链接以便调试
    # if nodes and len(nodes) > 0:
    #     print(f"使用的第一个节点: {nodes[0]}")
    # if links and len(links) > 0:
    #     print(f"使用的第一个连接: {links[0]}")

    # 创建图表
    c = (
        Graph(init_opts=opts.InitOpts(
            width="1000px", 
            height="800px", 
            theme=ThemeType.LIGHT,
            js_host="../js/",  # 使用相对路径
            # js_host=None,
            animation_opts=opts.AnimationOpts(animation=True)
        ))
        .add(
            series_name="",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="force",
            is_roam=True,
            is_draggable=True,
            edge_symbol=["circle", "arrow"],
            edge_symbol_size=[2, 10],
            edge_label=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(
                width=2,
                color="#4b565b",
                opacity=0.5,
            ),
            label_opts=opts.LabelOpts(is_show=True),
        )
        # 在.add()方法外单独设置力导向图的配置
        .set_global_opts(
            title_opts=opts.TitleOpts(title="工程原理设计"),
            tooltip_opts=opts.TooltipOpts(
                formatter="{b}"  # 简化tooltip显示
            ),
            legend_opts=opts.LegendOpts(
                is_show=True,
            ),
            toolbox_opts=opts.ToolboxOpts(
                is_show=False,
                feature={
                    "mark": {"show": True},
                    "restore": {"show": True},
                    "saveAsImage": {"show": True}
                }
            )
        )
    )
    
    # 单独设置力导向图参数
    c.options.get('series')[0]['force'] = {
        "repulsion": 2500,
        "edgeLength": 50
    }

    return c

def load_json_data(file_path):
    """
    从JSON文件加载数据
    :param file_path: JSON文件路径
    :return: 节点和连接数据
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"加载 JSON 成功: 找到 {len(data.get('nodes', []))} 个节点和 {len(data.get('links', []))} 个连接")
            # 打印前几个节点和连接以检查格式
            if data.get('nodes'):
                print(f"节点示例: {data['nodes'][0]}")
            if data.get('links'):
                print(f"连接示例: {data['links'][0]}")
            return data.get('categories', []), data.get('nodes', []), data.get('links', [])
    except Exception as e:
        print(f"加载JSON文件时出错: {e}")
        return None, None, None

def load_example_data():
    """
    加载示例数据
    :return: 节点和连接数据
    """
    # 示例节点数据
    categories = [
        {"name": "Neural Center"},
        {"name": "工程技术"},
        {"name": "艺术设计"},
        {"name": "数理逻辑"},
        {"name": "视野"},
        {"name": "人文社科"},
        {"name": "沟通表达"},
        {"name": "FCL"}
    ]
    
    nodes = [
        {"name": "中心节点", "symbolSize": 70, "category": 0, "des": "这是中心节点的详细描述"},
        {"name": "工程节点1", "symbolSize": 50, "category": 1, "des": "工程技术节点1"},
        {"name": "工程节点2", "symbolSize": 50, "category": 1, "des": "工程技术节点2"},
        {"name": "艺术节点", "symbolSize": 50, "category": 2, "des": "艺术设计节点"},
        {"name": "数理节点", "symbolSize": 50, "category": 3, "des": "数理逻辑节点"},
        {"name": "视野节点", "symbolSize": 50, "category": 4, "des": "视野节点"},
        {"name": "人文节点", "symbolSize": 50, "category": 5, "des": "人文社科节点"},
        {"name": "沟通节点", "symbolSize": 50, "category": 6, "des": "沟通表达节点"},
        {"name": "FCL节点", "symbolSize": 50, "category": 7, "des": "FCL节点"},
        {"name": "非线性拟合", "symbolSize": 50, "category": 8, "des": "非线性拟合节点"}
    ]
    
    # 示例连接数据
    links = [
        {"source": "中心节点", "target": "工程节点1"},
        {"source": "中心节点", "target": "工程节点2"},
        {"source": "中心节点", "target": "艺术节点"},
        {"source": "中心节点", "target": "数理节点"},
        {"source": "中心节点", "target": "视野节点"},
        {"source": "中心节点", "target": "人文节点"},
        {"source": "中心节点", "target": "沟通节点"},
        {"source": "中心节点", "target": "FCL节点"},
        {"source": "工程节点1", "target": "工程节点2"},
        {"source": "工程节点1", "target": "数理节点"},
        {"source": "工程节点1", "target": "非线性拟合"},
        {"source": "艺术节点", "target": "视野节点"},
        {"source": "人文节点", "target": "沟通节点"},
        {"source": "工程节点2", "target": "非线性拟合"},
        {"source": "数理节点", "target": "非线性拟合"},
        {"source": "视野节点", "target": "非线性拟合"},
        {"source": "沟通节点", "target": "非线性拟合"},
        {"source": "FCL节点", "target": "非线性拟合"}
    ]
    
    return categories,nodes, links

# 添加一个示例数据生成函数，方便测试
def generate_example_json():
    """生成一个示例JSON文件，用于测试"""
    nodes, links = load_example_data()
    data = {
        "nodes": nodes,
        "links": links
    }
    
    with open("example_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("示例数据已生成到 example_data.json")
    return "example_data.json"

def fix_js_paths(content):
    """统一处理 JS 文件路径"""
    # 定义目标路径格式
    target_jquery_path = '../js/jquery-3.7.1.min.js'
    target_echarts_path = '../js/echarts.min.js'
    
    # 首先替换简单路径
    content = content.replace('src="js/echarts.min.js"', f'src="{target_echarts_path}"')
    content = content.replace('src="js/echarts.js"', f'src="{target_echarts_path}"')
    content = content.replace('src="js/jquery-3.7.1.min.js"', f'src="{target_jquery_path}"')
    
    # 然后处理其他可能的路径
    # patterns = [
    #     # CDN 路径
    #     ('https://assets.pyecharts.org/assets/v5/echarts.min.js', target_echarts_path),
    #     ('https://assets.pyecharts.org/assets/v5/jquery.min.js', target_jquery_path),

       
    #     # 其他可能的路径
    #     ('./js/echarts.min.js', target_echarts_path),
    #     ('./js/jquery.min.js', target_jquery_path),
    #     ('/js/echarts.min.js', target_echarts_path),
    #     ('/js/echarts.js', target_echarts_path),
    #     ('/js/jquery-3.7.1.min.js', target_jquery_path)
    # ]
    
    # for old_path, new_path in patterns:
    #     content = content.replace(f'src="{old_path}"', f'src="{new_path}"')
    
    return content

def modify_html_structure(content):
    """修改HTML结构，确保只加载一次echarts"""
    # 定义要插入的脚本（只保留jQuery）
    scripts_to_insert = """
    <script type="text/javascript" src="../js/jquery-3.7.1.min.js"></script>
    """
    
    # 移除重复的echarts加载
    content = content.replace('<script type="text/javascript" src="../js/echarts.js"></script>', '')
    
    # 确保echarts.min.js只出现一次
    if '<script type="text/javascript" src="../js/echarts.min.js"></script>' in content:
        content = content.replace(
            '<script type="text/javascript" src="./js/echarts.min.js"></script>', 
            '', 
            1  # 只替换第一次出现
        )
    
    # 找到<head>标签的位置
    head_start = content.find("<head>")
    if head_start == -1:
        return content
    
    # 找到<head>标签结束的位置
    head_end = content.find(">", head_start) + 1
    
    # 插入脚本到<head>标签后面
    modified_content = content[:head_end] + scripts_to_insert + content[head_end:]
    
    # 确保最后有echarts.min.js
    if '<script type="text/javascript" src="../js/echarts.min.js"></script>' not in modified_content:
        head_close = modified_content.find("</head>")
        if head_close != -1:
            modified_content = (
                modified_content[:head_close] +
                '<script type="text/javascript" src="../js/echarts.min.js"></script>' +
                modified_content[head_close:]
            )
    
    return modified_content
# 主函数
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='创建神经网络关系图')
    parser.add_argument('--json_path',default='dlgc.json', type=str, help='JSON数据文件路径')
    parser.add_argument('--save-json', action='store_true', help='保存当前示例数据为JSON文件')
    parser.add_argument('--output', type=str, default='course_graph_html/nn_output_enhanced.html', help='输出HTML文件路径')
    args = parser.parse_args()
    
    try:
        # 是否保存JSON示例数据
        if args.save_json:
            json_file = generate_example_json()
            print(f"示例数据已保存到 {json_file}")
        
        # 是否使用指定JSON文件
        if args.json_path:
            categories, nodes, links = load_json_data(args.json_path)
            if nodes and links:
                c = create_graph(categories, nodes, links)
            else:
                print(f"无法从{args.json_path}加载有效数据，将使用默认示例数据")
                c = create_graph()
        else:
            # 默认使用示例数据
            c = create_graph()
        
        # 直接生成带交互功能的HTML文件
        output_file = args.output
        
        # 先保存基础图表
        c.render(output_file)
        
        # 检查js目录是否存在
        js_dir = os.path.join(os.path.dirname(__file__), "js")
        if not os.path.exists(js_dir):
            print(f"警告: JS目录不存在，创建目录: {js_dir}")
            os.makedirs(js_dir, exist_ok=True)
            
        # 检查必要的JS文件是否存在
        echarts_min_js = os.path.join(js_dir, "echarts.min.js")
        jquery_min_js = os.path.join(js_dir, "jquery-3.7.1.min.js")
        
        if not os.path.exists(echarts_min_js):
            print(f"警告: 缺少必要的JS文件: {echarts_min_js}")
            print("请确保将echarts.min.js文件放入js目录中")
            
        if not os.path.exists(jquery_min_js):
            print(f"提示: jQuery文件不存在: {jquery_min_js}")
            
        # 读取基础HTML文件
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"读取生成的HTML文件时出错: {e}")
            print("将重新生成HTML内容")
            # 如果无法读取生成的HTML，尝试直接生成
            content = """<!DOCTYPE html>
<html>
<head>
    <script type="text/javascript" src="../js/jquery-3.7.1.min.js"></script>
    <script type="text/javascript" src="../js/echarts.js"></script>

    <meta charset="UTF-8">
    <title>Awesome-pyecharts</title>
    <script type="text/javascript" src="../js/echarts.min.js"></script>
</head>
<body>
    <div id="chart_container" class="chart-container" style="width:1000px; height:800px;"></div>

    <script>
        // 基础图表代码将在这里插入
    </script>
</body>
</html>"""

        # 替换CDN链接为本地链接
            # 
        # content = content.replace('https://assets.pyecharts.org/assets/v5/echarts.min.js', '../js/echarts.min.js')
        # content = content.replace('https://assets.pyecharts.org/assets/v5/jquery.min.js', '../js/jquery-3.7.1.min.js')

        content = fix_js_paths(content)
        content = modify_html_structure(content)
        # 添加CSS样式
        css_styles = """
<style>
    /* 对话框样式 */
    .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.6);
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .modal-content {
        background-color: #ffffff;
        margin: 10% auto;
        padding: 25px;
        border: none;
        width: 60%;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        max-height: 80vh;
        overflow-y: auto;
        transform: translateY(-20px);
        animation: slideIn 0.3s forwards;
    }
    
    @keyframes slideIn {
        to { transform: translateY(0); }
    }
    
    .close {
        color: #666;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .close:hover,
    .close:focus {
        color: #000;
        transform: rotate(90deg);
    }

    .modal-title {
        margin-top: 0;
        color: #333;
        font-size: 24px;
        border-bottom: 2px solid #4b8bf4;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    .modal-body {
        margin-bottom: 20px;
        line-height: 1.6;
    }
    
    .modal-body p {
        margin: 12px 0;
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 5px;
        transition: background-color 0.2s;
    }
    
    .modal-body p:hover {
        background-color: #f0f7ff;
    }
    
    .modal-body strong {
        color: #4b8bf4;
        margin-right: 5px;
        display: inline-block;
        min-width: 60px;
    }
    
    /* 搜索框样式 - 修改为在图表内部而不是整个浏览器窗口 */
    .search-container {
        position: absolute;
        top: 60px; /* 位于图表标题下方 */
        right: 20px;
        z-index: 100;
        display: flex;
        background-color: white;
        padding: 8px;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        /* 添加半透明背景，使其与图表更好地融合 */
        background-color: rgba(255,255,255,0.9);
    }
    
    .search-input {
        padding: 6px 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 13px;
        width: 180px;
        outline: none;
        transition: all 0.3s;
    }
    
    .search-input:focus {
        border-color: #4b8bf4;
        box-shadow: 0 0 0 2px rgba(75,139,244,0.2);
    }
    
    .search-button {
        margin-left: 6px;
        padding: 6px 12px;
        background-color: #4b8bf4;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
        font-size: 13px;
    }
    
    .search-button:hover {
        background-color: #3a7ce0;
    }
    
    /* 搜索结果样式 */
    .search-results {
        position: absolute;
        top: 105px; /* 位于搜索框下方 */
        right: 20px;
        width: 280px;
        max-height: 300px;
        overflow-y: auto;
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 100;
        display: none;
    }
    
    .search-result-item {
        padding: 10px 15px;
        border-bottom: 1px solid #eee;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .search-result-item:hover {
        background-color: #f0f7ff;
    }
    
    .search-result-item:last-child {
        border-bottom: none;
    }
    
    /* 调试模式状态显示 */
    .debug-panel {
        position: fixed;
        left: 10px;
        bottom: 10px;
        background-color: rgba(0,0,0,0.8);
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 12px;
        z-index: 1000;
        max-width: 300px;
        max-height: 200px;
        overflow: auto;
    }
</style>
"""

        # 添加模态框HTML和搜索框
        modal_html = """
<!-- 添加对话框结构 -->
<div id="nodeModal" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <h2 id="modalTitle" class="modal-title"></h2>
        <div id="modalBody" class="modal-body"></div>
    </div>
</div>

<!-- 调试面板 -->
<div id="debugPanel" class="debug-panel" style="display: none;"></div>
"""

        # 添加交互脚本
        click_script = """
<script>
    // 配置服务器URL，使用当前页面的主机地址，而不是硬编码localhost
    var serverUrl = window.location.protocol + '//' + window.location.hostname + ':7000';
    console.log("服务器URL设置为:", serverUrl);
    
    // 图表操作相关变量
    var myChart = null;          // 图表实例
    var rawData = {              // 原始数据
        nodes: [],
        links: []
    };
    var currentState = {         // 当前状态
        mode: 'full',            // 显示模式：'full'=完整图谱, 'focus'=聚焦模式
        focusedNode: null,       // 当前聚焦的节点名称
        highlightedNode: null    // 当前高亮的节点名称
    };
    var categoriesCache = [];    // 用于缓存分类数据，避免重复获取
    
    // DOM元素
    var modal = document.getElementById("nodeModal");
    var modalTitle = document.getElementById("modalTitle");
    var modalBody = document.getElementById("modalBody");
    var closeBtn = document.getElementsByClassName("close")[0];
    var searchInput, searchBtn, searchResults;
    var debugPanel = document.getElementById("debugPanel");
    
    // 调试辅助函数
    var isDebug = false; // 是否启用调试
    
    function debugLog(message) {
        if (!isDebug) return;
        
        var time = new Date().toLocaleTimeString();
        var logItem = document.createElement('div');
        logItem.innerHTML = `<span style="color:#aaa">[${time}]</span> ${message}`;
        
        if (debugPanel) {
            debugPanel.style.display = 'block';
            debugPanel.appendChild(logItem);
            debugPanel.scrollTop = debugPanel.scrollHeight;
            
            // 保留最多30条日志
            while (debugPanel.children.length > 30) {
                debugPanel.removeChild(debugPanel.children[0]);
            }
        }
        
        console.log(`[DEBUG] ${message}`);
    }
    
    // 按键监听 - 按D键切换调试模式
    document.addEventListener('keydown', function(e) {
        if (e.key === 'D' && e.ctrlKey && e.shiftKey) {
            isDebug = !isDebug;
            debugPanel.style.display = isDebug ? 'block' : 'none';
            if (isDebug) {
                debugLog('调试模式已启用');
                debugLog(`当前状态: ${JSON.stringify(currentState)}`);
            }
        }
    });
    
    // 事件绑定
    closeBtn.onclick = function() {
        modal.style.display = "none";
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
        
        // 点击外部时关闭搜索结果
        if (searchResults && 
            !event.target.matches('.search-input') && 
            !event.target.matches('.search-button') && 
            !event.target.matches('.search-results') &&
            !event.target.matches('.search-result-item')) {
            searchResults.style.display = "none";
        }
    }
    
    // 添加防抖动函数
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // 优化后的搜索函数
    const debouncedSearch = debounce(function() {
        searchNodes();
    }, 300); // 300ms 的延迟
    
    // 在页面加载后创建搜索框
    function createSearchBox() {
        // 查找echarts图表容器 - 使用更精确的选择器
        var chartContainer = document.querySelector('.chart-container[_echarts_instance_]');
        if (!chartContainer) {
            debugLog('无法找到图表容器，5秒后重试');
            setTimeout(createSearchBox, 5000);
            return;
        }
        
        debugLog(`找到图表容器: ${chartContainer.id}`);
        
        // 确保图表容器具有正确的定位
        if (getComputedStyle(chartContainer).position !== 'relative') {
            chartContainer.style.position = 'relative';
            debugLog('已将图表容器设置为相对定位');
        }
        
        // 创建搜索框元素
        var searchBox = document.createElement('div');
        searchBox.id = 'chart-search-box';
        searchBox.style.cssText = 'position: absolute; top: 20px; right: 20px; z-index: 1001; background-color: rgba(255,255,255,0.9); ' +
                                 'padding: 8px; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);';
        
        // 创建输入和按钮容器
        var inputContainer = document.createElement('div');
        inputContainer.style.display = 'flex';
        
        // 创建输入框
        searchInput = document.createElement('input');
        searchInput.id = 'nodeSearchInput';
        searchInput.type = 'text';
        searchInput.placeholder = '输入节点名称搜索';
        searchInput.style.cssText = 'padding: 6px 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 13px; ' +
                                   'width: 180px; outline: none;';
        
        // 创建按钮
        searchBtn = document.createElement('button');
        searchBtn.id = 'nodeSearchBtn';
        searchBtn.textContent = '搜索';
        searchBtn.style.cssText = 'margin-left: 6px; padding: 6px 12px; background-color: #4b8bf4; color: white; ' +
                                 'border: none; border-radius: 4px; cursor: pointer; font-size: 13px;';
        
        // 创建搜索结果容器
        
        reset = document.createElement('button')
        reset.id = 'refreshButton'
        reset.textContent = '刷新页面'
        reset.setAttribute('onclick', 'location.reload()')
        reset.style.cssText = 'padding:8px 15px; background-color:#4b8bf4; color:white; border:none; border-radius:4px; cursor:pointer; margin:10px 0;'
        
        
        searchResults = document.createElement('div');
        searchResults.id = 'searchResults';
        searchResults.style.cssText = 'display: none; position: absolute; top: 45px; left: 0; right: 0; max-height: 300px; ' +
                                     'overflow-y: auto; background-color: white; border-radius: 5px; ' +
                                     'box-shadow: 0 2px 8px rgba(0,0,0,0.2); z-index: 1002;';
        
        // 组装DOM
        // 共同样式变量
        var buttonHeight = '36px';
        var fontSize = '13px';
        var padding = '6px 12px';
        var borderRadius = '4px';

        // 搜索输入框样式
        searchInput.style.cssText = `
            padding: ${padding}; 
            border: 1px solid #ddd; 
            border-radius: ${borderRadius}; 
            font-size: ${fontSize}; 
            width: 180px; 
            outline: none;
            height: ${buttonHeight};
            box-sizing: border-box;
            vertical-align: middle;
        `;

        // 搜索按钮样式
        searchBtn.style.cssText = `
            margin-left: 6px; 
            padding: ${padding}; 
            background-color: #4b8bf4; 
            color: white; 
            border: none; 
            border-radius: ${borderRadius}; 
            cursor: pointer; 
            font-size: ${fontSize};
            height: ${buttonHeight};
            box-sizing: border-box;
            vertical-align: middle;
        `;

        // 刷新按钮样式
        reset.style.cssText = `
            margin-left: 6px;
            padding: ${padding}; 
            background-color: #4b8bf4; 
            color: white; 
            border: none; 
            border-radius: ${borderRadius}; 
            cursor: pointer; 
            font-size: ${fontSize};
            height: ${buttonHeight};
            box-sizing: border-box;
            vertical-align: middle;
        `;
        inputContainer.appendChild(searchInput);
        inputContainer.appendChild(searchBtn);
        inputContainer.appendChild(reset);
        searchBox.appendChild(inputContainer);
        searchBox.appendChild(searchResults);
        
        // 添加到图表容器
        chartContainer.appendChild(searchBox);
        
        debugLog('搜索框已添加到图表容器');
        
        // 绑定事件
        searchBtn.onclick = function() {
            searchNodes();
        };
        
        // 修改搜索框事件监听，改为实时搜索
        searchInput.addEventListener('input', function() {
            debouncedSearch();
        });
        
        // 保留回车键搜索功能
        searchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                // 如果搜索结果只有一个，直接选中该节点
                var resultItems = document.querySelectorAll('.search-result-item');
                if (resultItems.length === 1 && !resultItems[0].textContent.includes('无匹配结果')) {
                    var nodeName = resultItems[0].getAttribute('data-name');
                    focusNode(nodeName);
                    searchResults.style.display = "none";
                }
            }
        });

        // 添加搜索框焦点事件
        searchInput.addEventListener('focus', function() {
            if (this.value.trim() !== '') {
                searchNodes();
            }
        });

        // 添加搜索框失焦事件，延迟隐藏结果
        searchInput.addEventListener('blur', function() {
            setTimeout(function() {
                searchResults.style.display = "none";
            }, 200);
        });
    }
    
    // 核心功能函数
    // 1. 搜索节点
    function searchNodes() {
        var searchTerm = searchInput.value.trim().toLowerCase();
        if (searchTerm === "") {
            searchResults.style.display = "none";
            return;
        }
        
        debugLog(`搜索节点: ${searchTerm}`);
        
        // 过滤匹配的节点
        var matchedNodes = rawData.nodes.filter(function(node) {
            // 在名称和描述中搜索
            return node.name.toLowerCase().includes(searchTerm) || 
                  (node.des && node.des.toLowerCase().includes(searchTerm));
        });
        
        // 显示搜索结果
        if (matchedNodes.length > 0) {
            var resultsHTML = "";
            matchedNodes.forEach(function(node) {
                resultsHTML += '<div class="search-result-item" data-name="' + node.name + '">' + 
                               node.name + 
                               (node.des ? ' <small>(' + node.des.substring(0, 30) + (node.des.length > 30 ? '...' : '') + ')</small>' : '') + 
                               '</div>';
            });
            searchResults.innerHTML = resultsHTML;
            searchResults.style.display = "block";
            
            // 为结果项添加点击事件
            var resultItems = document.querySelectorAll('.search-result-item');
            resultItems.forEach(function(item) {
                item.addEventListener('click', function() {
                    var nodeName = this.getAttribute('data-name');
                    debugLog(`选择搜索结果: ${nodeName}`);
                    focusNode(nodeName);
                    searchResults.style.display = "none";
                });
            });
        } else {
            searchResults.innerHTML = '<div class="search-result-item">无匹配结果</div>';
            searchResults.style.display = "block";
        }
    }
    
    // 2. 聚焦节点及其相连节点
    function focusNode(nodeName) {
        if (!myChart || !rawData.nodes.length) {
            debugLog('图表或数据未初始化，无法聚焦节点');
            return;
        }
        
        debugLog(`准备聚焦节点: ${nodeName}`);
        
        // 如果已经聚焦到同一节点，切换回完整图谱
        if (currentState.mode === 'focus' && currentState.focusedNode === nodeName) {
            debugLog('已经聚焦到此节点，恢复完整图谱');
            restoreFullGraph();
            return;
        }
        
        try {
            // 查找目标节点
            var targetNode = null;
            var linkedNodeNames = [];
            
            // 从当前图表中查找目标节点
            var option = myChart.getOption();
            var currentNodes = option.series[0].data;
            var currentLinks = option.series[0].links;
            
            // 1. 首先从当前显示的节点中查找
            for (var i = 0; i < currentNodes.length; i++) {
                if (currentNodes[i].name === nodeName) {
                    targetNode = currentNodes[i];
                    break;
                }
            }
            
            // 2. 如果当前图表中没有找到，则从原始数据中查找
            if (!targetNode) {
                for (var i = 0; i < rawData.nodes.length; i++) {
                    if (rawData.nodes[i].name === nodeName) {
                        targetNode = rawData.nodes[i];
                        break;
                    }
                }
            }
            
            if (!targetNode) {
                debugLog(`未找到节点: ${nodeName}`);
                return;
            }
            
            // 3. 从原始数据中找出所有与目标节点相连的节点
            for (var i = 0; i < rawData.links.length; i++) {
                if (rawData.links[i].source === nodeName) {
                    linkedNodeNames.push(rawData.links[i].target);
                } else if (rawData.links[i].target === nodeName) {
                    linkedNodeNames.push(rawData.links[i].source);
                }
            }
            
            debugLog(`找到 ${linkedNodeNames.length} 个相连节点`);
            
            // 4. 创建新的节点和连接集合
            var focusedNodes = [];
            var focusedLinks = [];
            
            // 添加目标节点
            focusedNodes.push(JSON.parse(JSON.stringify(targetNode)));
            
            // 添加相连节点
            for (var i = 0; i < rawData.nodes.length; i++) {
                if (linkedNodeNames.includes(rawData.nodes[i].name)) {
                    focusedNodes.push(JSON.parse(JSON.stringify(rawData.nodes[i])));
                }
            }
            
            // 添加相关连接
            for (var i = 0; i < rawData.links.length; i++) {
                if (rawData.links[i].source === nodeName || rawData.links[i].target === nodeName) {
                    focusedLinks.push(JSON.parse(JSON.stringify(rawData.links[i])));
                }
            }
            
            // 5. 更新图表
            option.series[0].data = focusedNodes;
            option.series[0].links = focusedLinks;
            
            // 6. 设置聚焦节点为特殊样式
            for (var i = 0; i < focusedNodes.length; i++) {
                if (focusedNodes[i].name === nodeName) {
                    // 设置焦点节点样式
                    focusedNodes[i].itemStyle = {
                        color: '#ff5500',
                        borderWidth: 5,
                        borderColor: '#ff9500'
                    };
                    focusedNodes[i].symbolSize = 60; // 增大焦点节点
                    break;
                }
            }
            
            myChart.setOption(option, {replaceMerge: ['series']});
            
            // 更新状态
            currentState.mode = 'focus';
            currentState.focusedNode = nodeName;
            
            debugLog(`节点聚焦完成: ${nodeName}`);
            
        } catch (error) {
            debugLog(`聚焦节点失败: ${error.message}`);
            console.error(error);
            // 出错时恢复完整图表
            setTimeout(restoreFullGraph, 500);
        }
    }
    
    // 3. 恢复完整图谱
    function restoreFullGraph() {
        if (!myChart || !rawData.nodes.length) {
            debugLog('图表或数据未初始化');
            return;
        }
        
        debugLog('恢复完整图谱');
        
        try {
            var option = myChart.getOption();
            
            // 使用深拷贝确保不改变原始数据
            var nodesCopy = JSON.parse(JSON.stringify(rawData.nodes));
            var linksCopy = JSON.parse(JSON.stringify(rawData.links));
            
            // 设置图表数据
            option.series[0].data = nodesCopy;
            option.series[0].links = linksCopy;
            
            // 使用 setOption 更新图表，替换所有系列数据
            myChart.setOption(option, {replaceMerge: ['series']});
            
            // 重置状态
            currentState.mode = 'full';
            currentState.focusedNode = null;
            
            debugLog('已恢复完整图谱');
        } catch (error) {
            debugLog(`恢复图谱失败: ${error.message}`);
            console.error(error);
        }
    }
    
    // 4. 显示节点详情
    function showNodeDetails(nodeName) {
        if (!nodeName) return;
        
        debugLog(`显示节点详情: ${nodeName}`);
        
        // 查找节点数据
        var nodeData = null;
        for (var i = 0; i < rawData.nodes.length; i++) {
            if (rawData.nodes[i].name === nodeName) {
                nodeData = rawData.nodes[i];
                break;
            }
        }
        
        if (!nodeData) {
            debugLog(`未找到节点详情: ${nodeName}`);
            return;
        }
        
        // 设置模态框标题和内容
        modalTitle.innerText = nodeData.name || "节点详情";
        
        // 构建详细信息
        var content = "";
        
        if (nodeData.category !== undefined) {
            // 使用缓存的分类数据
            if (categoriesCache.length > nodeData.category) {
                content += "<p><strong>分类：</strong>" + categoriesCache[nodeData.category] + "</p>";
            } else {
                debugLog(`分类索引超出范围: ${nodeData.category}, 分类数组长度: ${categoriesCache.length}`);
                content += "<p><strong>分类：</strong>未知分类</p>";
            }
        }
        
        if (nodeData.des) {
            content += "<p><strong>描述：</strong>" + nodeData.des + "</p>";
        }
        
        // 添加其他属性
        for (var key in nodeData) {
            if (["name", "des", "category", "symbolSize", "x", "y", "fixed", "id", "index", "originSize", "itemStyle"].indexOf(key) === -1) {
                content += "<p><strong>" + key + "：</strong>" + nodeData[key] + "</p>";
            }
        }
        
        // 添加生成知识图谱按钮
        content += `<div style="margin-top: 20px; text-align: center;">
            <button id="generateKGBtn" style="padding: 8px 16px; background-color: #4b8bf4; color: white; 
            border: none; border-radius: 4px; cursor: pointer; font-size: 14px;">生成知识图谱</button>
            <div id="kgStatus" style="margin-top: 10px; font-size: 14px; display: none;"></div>
        </div>`;
        
        modalBody.innerHTML = content || "<p>没有详细信息</p>";
        
        // 显示模态框
        modal.style.display = "block";
        
        // 为生成知识图谱按钮添加点击事件
        var generateKGBtn = document.getElementById('generateKGBtn');
        if (generateKGBtn) {
            generateKGBtn.addEventListener('click', function() {
                generateKnowledgeGraph(nodeData.name);
            });
        }
    }
    
    // 生成知识图谱的函数
    function generateKnowledgeGraph(keyword) {
        if (!keyword) return;
        
        var statusEl = document.getElementById('kgStatus');
        if (statusEl) {
            statusEl.style.display = 'block';
            statusEl.textContent = `正在为 "${keyword}" 生成知识图谱，请稍候...`;
        }
        
        debugLog(`开始为 "${keyword}" 生成知识图谱，使用URL: ${serverUrl}`);
        console.log(`开始为 "${keyword}" 生成知识图谱，使用URL: ${serverUrl}`);
        
        // 先使用一组简单的静态数据作为备选
        var fallbackData = {
            nodes: [
                {name: keyword, symbolSize: 70, category: 0},
                {name: "功能", symbolSize: 50, category: 1},
                {name: "特性", symbolSize: 50, category: 1},
                {name: "应用", symbolSize: 50, category: 1},
                {name: "分类", symbolSize: 50, category: 1},
                {name: "历史", symbolSize: 50, category: 1}
            ],
            links: [
                {source: keyword, target: "功能", name: "具有"},
                {source: keyword, target: "特性", name: "具有"},
                {source: keyword, target: "应用", name: "用于"},
                {source: keyword, target: "分类", name: "属于"},
                {source: keyword, target: "历史", name: "发展于"}
            ]
        };
        
        // 使用Fetch API调用后端接口
        fetch(serverUrl + '/generate_kg', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                keyword: keyword,
                display_mode: 'current_page',  // 设置显示模式为当前页面
                source_file: window.location.pathname.split('/').pop() // 添加当前HTML文件名
            })
        })
        .then(response => {
            debugLog(`收到服务器响应: 状态${response.status}`);
            console.log(`收到服务器响应: 状态${response.status}`);
            
            if (!response.ok) {
                // 如果服务器响应错误，使用本地备选数据
                debugLog(`服务器响应错误，使用本地备选数据`);
                updateChartWithNewData(fallbackData.nodes, fallbackData.links, keyword);
                
                if (statusEl) {
                    statusEl.textContent = `使用本地数据更新图表！`;
                    setTimeout(function() {
                        modal.style.display = "none"; // 关闭模态框
                    }, 1500);
                }
                
                throw new Error(`网络请求失败，状态码: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            debugLog(`解析响应数据: ${JSON.stringify(data).substring(0, 100)}...`);
            console.log(`解析响应数据: `, data);
            
            if (data.display_mode === 'current_page' && data.nodes && data.links) {
                // 更新当前页面的图表
                debugLog(`使用当前页面模式，更新图表`);
                updateChartWithNewData(data.nodes, data.links, keyword);
                
                if (statusEl) {
                    statusEl.textContent = `知识图谱已更新！`;
                    setTimeout(function() {
                        modal.style.display = "none"; // 关闭模态框
                    }, 1500);
                }
            } else {
                // 保持原有的行为 - 提供链接打开新页面
                debugLog(`使用新页面模式，提供链接`);
                if (statusEl) {
                    statusEl.textContent = `知识图谱生成成功！`;
                    
                    // 添加查看按钮
                    setTimeout(function() {
                        statusEl.innerHTML = `知识图谱生成成功！<a href="${data.html_path}" target="_blank" 
                            style="margin-left: 10px; color: #4b8bf4; text-decoration: underline;">点击查看</a>`;
                    }, 1000);
                }
            }
            debugLog(`知识图谱生成成功: ${data.html_path}`);
        })
        .catch(error => {
            debugLog(`知识图谱生成失败: ${error.message}`);
            console.error('知识图谱生成错误:', error);
            
            if (statusEl) {
                statusEl.textContent = `生成失败: ${error.message}`;
                statusEl.style.color = 'red';
            }
        });
    }
    
    // 使用新数据更新图表
    function updateChartWithNewData(nodes, links, centerNodeName) {
        if (!myChart) {
            debugLog('图表实例不存在，无法更新');
            return;
        }
        
        debugLog(`使用新数据更新图表，中心节点: ${centerNodeName}`);
        
        try {
            // 设置中心节点的大小和类别
            for (let i = 0; i < nodes.length; i++) {
                if (nodes[i].name === centerNodeName) {
                    nodes[i].symbolSize = 70;
                    nodes[i].category = 0; // Neural Center 类别
                } else {
                    // 可以根据需要调整其他节点的大小
                    nodes[i].symbolSize = 50;
                }
            }
            
            // 获取当前图表配置
            var option = myChart.getOption();
            
            // 更新数据
            option.series[0].data = nodes;
            option.series[0].links = links;
            
            // 应用更新
            myChart.setOption(option, {replaceMerge: ['series']});
            
            // 更新原始数据引用，使得其他功能（如搜索、聚焦等）可以正常工作
            rawData.nodes = JSON.parse(JSON.stringify(nodes));
            rawData.links = JSON.parse(JSON.stringify(links));
            
            // 重置状态
            currentState.mode = 'full';
            currentState.focusedNode = null;
            
            debugLog(`图表更新成功，共 ${nodes.length} 个节点，${links.length} 个连接`);
        } catch (error) {
            debugLog(`更新图表失败: ${error.message}`);
            console.error('更新图表错误:', error);
        }
    }
    
    // 页面加载完成后初始化图表交互
    document.addEventListener('DOMContentLoaded', function() {
        debugLog('DOM加载完成，初始化图表交互');
        
        setTimeout(function() {
            var charts = document.querySelectorAll('[_echarts_instance_]');
            if (charts.length > 0) {
                var chartDom = charts[0];
                myChart = echarts.getInstanceByDom(chartDom);
                
                // 获取图表容器
                var chartContainer = chartDom.parentNode;
                if (chartContainer) {
                    // 在图表容器内添加搜索框
                    createSearchBox();
                }
                
                if (myChart) {
                    debugLog('成功获取图表实例');
                    
                    // 获取并保存原始数据
                    var option = myChart.getOption();
                    
                    // 获取并缓存分类数据
                    if (option.legend && option.legend[0] && option.legend[0].data) {
                        categoriesCache = option.legend[0].data;
                        debugLog(`已缓存${categoriesCache.length}个分类: ${categoriesCache.join(', ')}`);
                    } else if (option.series && option.series[0] && option.series[0].categories) {
                        categoriesCache = option.series[0].categories.map(function(cat) {
                            return cat.name;
                        });
                        debugLog(`已缓存${categoriesCache.length}个分类: ${categoriesCache.join(', ')}`);
                    }
                    
                    // 确保深拷贝原始数据，避免引用问题
                    if (option.series[0].data && option.series[0].links) {
                        rawData.nodes = JSON.parse(JSON.stringify(option.series[0].data));
                        rawData.links = JSON.parse(JSON.stringify(option.series[0].links));
                        
                        debugLog(`初始化完成，共 ${rawData.nodes.length} 个节点，${rawData.links.length} 个连接`);
                    } else {
                        debugLog('ERROR: 图表数据结构不完整');
                    }
                    
                    // 使用更可靠的方式处理点击事件
                    var clickTimer = null;
                    var clickDelay = 300;
                    
                    myChart.off('click');
                    myChart.on('click', function(params) {
                        if (params.dataType === 'node') {
                            var nodeName = params.data.name;
                            
                            // 如果有计时器，说明这是双击的第二次点击，取消单击事件
                            if (clickTimer) {
                                clearTimeout(clickTimer);
                                clickTimer = null;
                                return;
                            }
                            
                            // 设置延时执行单击事件
                            clickTimer = setTimeout(function() {
                                clickTimer = null;
                                // 单击事件 - 显示节点详情
                                debugLog(`单击节点: ${nodeName}`);
                                showNodeDetails(nodeName);
                            }, clickDelay);
                        }
                    });
                    
                    myChart.off('dblclick');
                    myChart.on('dblclick', function(params) {
                        if (params.dataType === 'node') {
                            var nodeName = params.data.name;
                            
                            // 取消可能的单击事件
                            if (clickTimer) {
                                clearTimeout(clickTimer);
                                clickTimer = null;
                            }
                            
                            // 双击事件 - 聚焦/恢复节点
                            debugLog(`双击节点: ${nodeName}`);
                            
                            if (currentState.mode === 'focus' && currentState.focusedNode === nodeName) {
                                restoreFullGraph();
                            } else {
                                focusNode(nodeName);
                            }
                        }
                    });
                    
                    debugLog('交互事件绑定完成');
                } else {
                    debugLog('ERROR: 未能获取图表实例');
                }
            } else {
                debugLog('ERROR: 未找到图表元素');
            }
        }, 500);
    });
</script>
"""

        # 插入CSS到<head>结束前
        if "</head>" in content:
            content = content.replace("</head>", css_styles + "</head>")
        else:
            content = css_styles + content

        # 插入模态框HTML到<body>结束前
        if "</body>" in content:
            content = content.replace("</body>", modal_html + "</body>")
        else:
            content = content + modal_html

        # 插入点击事件脚本到<body>结束前
        if "</body>" in content:
            content = content.replace("</body>", click_script + "</body>")
        else:
            content = content + click_script

        # 写入文件
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"图表已生成并保存为: {output_file}")
        except Exception as e:
            print(f"写入HTML文件时出错: {e}")
            # 尝试使用不同的文件名
            alt_output_file = f"backup_{output_file}"
            try:
                with open(alt_output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"已使用备用文件名保存: {alt_output_file}")
                output_file = alt_output_file
            except Exception as e2:
                print(f"备用文件名也无法写入: {e2}")
                print("无法生成HTML文件，请检查文件系统权限")
                # 无法写入文件，抛出异常中断执行
                raise IOError("无法写入HTML文件")

        # 检查文件是否已成功生成
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            # 自动打开生成的HTML文件
            try:
                # webbrowser.open('file://' + os.path.realpath(output_file))
                print("请手动在浏览器中打开图表文件")
            except Exception as e:
                print(f"无法自动打开文件: {e}")
                print(f"请手动打开文件: {os.path.realpath(output_file)}")
        else:
            print(f"警告: 生成的文件 {output_file} 不存在或为空")
        if not args.json_path:
            print("提示：")
            print("1. 使用自定义JSON文件：python nn.py --json_path 你的数据文件.json")
            print("2. 保存示例数据为JSON文件：python nn.py --save-json")
    except Exception as e:
        print(f"程序运行出错: {e}")
        print("请检查pyecharts版本是否为2.0.8，可以使用 pip install pyecharts==2.0.8 安装兼容版本") 