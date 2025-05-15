# 交互式知识图谱生成器

这是一个基于Flask和PyEcharts的交互式知识图谱可视化和生成工具。该工具允许用户通过简单的操作来查看、探索和生成知识图谱。

## 项目概述

本项目是一个完整的知识图谱生成和可视化系统，包含以下主要组件：
- 后端服务器（Flask）
- 知识图谱生成器
- 交互式可视化界面
- 数据存储和管理

## 功能特点

### 1. 知识图谱可视化
- 使用PyEcharts实现动态、交互式的知识图谱展示
- 支持节点拖拽、缩放和平移
- 自动布局优化，提供清晰的节点关系展示

### 2. 交互功能
- 节点搜索：快速定位特定节点
- 节点聚焦：双击节点可聚焦查看其关联关系
- 节点详情：点击节点查看详细信息
- 知识图谱生成：支持基于任意节点生成新的知识图谱

### 3. 数据管理
- 支持JSON格式的数据导入导出
- 自动保存生成的知识图谱
- 提供示例数据用于测试和演示

## 技术栈

- 后端：Python 3.x, Flask
- 前端：HTML, JavaScript, PyEcharts
- 数据处理：JSON
- 知识图谱生成：基于大语言模型的知识图谱生成器

## 安装说明

### 1. 环境要求
- Python 3.6+
- pip 包管理器

### 2. 克隆代码库
```bash
git clone <项目仓库地址>
cd knowledge-graph-generator
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置API接口
编辑`kg_json.py`文件，配置以下参数：
```python
# API配置
api_url = "http://your-api-endpoint.com/api"
share_id = "your-share-id"
kg_model = "your-kg-model"
kg_api_base = "http://your-api-base.com"
kg_api_key = "your-api-key"
```

### 5. 运行服务器
```bash
python server.py
```

服务器将在`http://localhost:7000`启动

## 使用指南

### 1. 基本操作
- 在浏览器中访问`http://localhost:7000`
- 使用鼠标滚轮缩放图谱
- 点击并拖动节点调整位置
- 使用搜索框快速定位节点

### 2. 节点操作
- 单击节点：查看节点详细信息
- 双击节点：聚焦该节点及其关联节点
- 再次双击：恢复完整图谱视图

### 3. 生成新图谱
1. 在搜索框中输入关键词
2. 选择显示模式（当前页面或新页面）
3. 点击"生成知识图谱"按钮
4. 等待系统生成新的知识图谱
5. 新图谱将在当前页面或新页面中显示

## 项目结构

```
.
├── server.py          # Flask服务器主程序
├── kg_json2graph.py   # 知识图谱可视化工具
├── kg_json.py         # 知识图谱生成器
├── static/            # 静态资源目录
│   └── output/        # 生成的图谱文件
├── js/                # JavaScript库文件
├── course_graph_html/ # 预生成的知识图谱HTML文件
├── kg-gen/            # 知识图谱生成核心库
│   └── src/           # 源代码
│       └── kg_gen/    # 知识图谱生成模块
├── requirements.txt   # 项目依赖
└── README.md          # 项目文档
```

## 开发指南

### 1. 添加新功能
- 在`kg_json2graph.py`中修改可视化逻辑
- 在`kg_json.py`中扩展知识图谱生成功能
- 在`server.py`中添加新的API端点

### 2. 自定义配置
- 修改`server.py`中的端口和主机设置
- 调整`kg_json2graph.py`中的图表样式和交互参数
- 在`kg_json.py`中配置知识图谱生成参数

## 常见问题

1. **服务器无法启动**
   - 检查端口是否被占用
   - 确认所有依赖已正确安装

2. **图谱生成失败**
   - 检查API配置是否正确
   - 确认网络连接正常
   - 查看服务器日志获取详细错误信息

3. **可视化效果异常**
   - 清除浏览器缓存
   - 检查浏览器控制台错误信息
   - 确认JavaScript库文件已正确加载

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。在提交代码前，请确保：
1. 代码符合项目规范
2. 添加必要的注释
3. 更新相关文档

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

## 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues
- Email: [您的邮箱地址] 