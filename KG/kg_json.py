import requests
from kg_gen import KGGen, Graph
import json

class KnowledgeGraphGenerator:
    """
    知识图谱生成器类，用于从API获取知识并生成知识图谱
    """ 
    DEFAULT_SHARE_ID = "ytln4c6g30jgcl99z2wjms1q"    # 这里可以是一个公共知识库
    
    def __init__(self, api_url="http://180.85.206.30:3000/api/v1/chat/completions", 
                 share_id="ytln4c6g30jgcl99z2wjms1q",          
                 kg_model="openai/Qwen/Qwen2.5-72B-Instruct",
                 kg_api_base="http://180.85.206.19:8123/v1",
                 kg_api_key="local"):
        """
        初始化知识图谱生成器
        
        Args:
            api_url: 知识获取API的URL
            share_id: 分享ID
            kg_model: 知识图谱生成模型
            kg_api_base: 知识图谱API基础URL
            kg_api_key: 知识图谱API密钥
        """
        
        self.share_id = share_id if share_id is not None else self.DEFAULT_SHARE_ID
        self.api_url = api_url
        self.kg_model = kg_model
        self.kg_api_base = kg_api_base
        self.kg_api_key = kg_api_key
        
        # 预定义的提示词模板
        self.prompt1 = "请以自然语言的形式，围绕【第一性原理】展开详细介绍。你的回答需要包含以下要素：1.首先用通俗易懂的方式解释这个知识点的基础概念和关键特征。2.然后沿着时间维度或逻辑维度，梳理该知识点的发展脉络或内在逻辑关系。3.接着说明与之直接相关的一些重要关联知识点，对每个关联点简要说明其与核心知识点的关系。请注意：1.保持叙述的连贯性，不需要使用项目符号或结构化排版。2.适当使用过渡词和连接词展现知识点之间的关联性。3.涉及专业术语时请附带简单解释。4.重点呈现知识之间的网状联系而非孤立事实。5.禁止任何形式的实例或案例说明，禁止对知识点进行价值判断或主观评价。现在请就【第一性原理】进行详细阐述。"
        self.prompt2 = "请系统性地介绍 {keyword} 的核心定义、关键属性，以及与之直接或间接相关的其他知识点，并明确说明它们之间的逻辑关系或层级结构。回答需严格遵循以下要求：核心知识点的解析,准确定义 {keyword} 的本质内涵,阐明其基本特征或分类维度（如适用）.直接关联知识点,列出与 {keyword} 存在因果、依赖、互补或对立关系的其他概念.说明这些关联的具体性质（例如：理论基础到应用延伸、上层概念到子类分支、前提条件到推论结果等）.间接关联知识点,提及跨领域或跨层级的弱关联概念,标注关联类型（如：方法论支撑、历史渊源、并行理论等）。约束条件：禁止任何形式的实例或案例说明，禁止对知识点进行价值判断或主观评价。"
        
    def get_knowledge(self, keyword="没有传入关键词"):
        """
        从API获取关于特定关键词的知识
        
        Args:
            keyword: 要查询的关键词
            
        Returns:
            requests.Response: API的响应对象
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # data = {
        #     "shareId": self.share_id,
        #     "outLinkUid": "test_user_001",
        #     "chatId": "",
        #     "stream": False,
        #     "detail": False,
        #     "messages": [
        #         {
        #             "role": "user",
        #             "content": f"""请系统性地介绍 {keyword} 的核心定义、关键属性，并构建一个两跳节点的知识图谱。
        #                             1. 核心知识点的解析
        #                             - 准确定义 {keyword} 的本质内涵，阐明其基本特征或分类维度（如适用）。

        #                             2. 第一跳直接关联知识点
        #                             - 列出与 {keyword} 存在紧密关系的第一层关联概念，例如特定的功能、特性或者组成部分。
        #                             - 说明这些第一层关联概念与 {keyword} 之间的逻辑关系或层级结构（例如：理论基础到应用延伸、上层概念到子类分支、前提条件到推论结果等）。

        #                             3. 第二跳间接关联知识点
        #                             - 针对每一个第一跳关联概念，进一步探索与其相关的第二层知识点。
        #                             - 提及这些第二层知识点与对应的第一层知识点之间的逻辑关系或层级结构（如方法支撑、扩展内容、依赖条件等）。
        #                             - 注明每个第二跳知识点与原始{keyword}的关系类型（例如：方法论支撑、并行理论、应用场景等），但请注意，这里不进行实例说明或价值判断。

        #                             约束条件：
        #                             - 禁止任何形式的实例或案例说明。
        #                             - 禁止对知识点进行价值判断或主观评价。"""
        #         }
        
        data = {
            "shareId": self.share_id,
            "outLinkUid": "test_user_001",
            "chatId": "",
            "stream": False,
            "detail": False,
            "responseChatItemId": "my_responseChatItemId",
            "messages": [
                {
                    "role": "user",
                    "content": f"{keyword}"
                }
            ]
        }
        
        response = requests.post(self.api_url, headers=headers, json=data)
        return response
    
    def get_graph(self, response):
        """
        从API响应生成知识图谱
        
        Args:
            response: API的响应对象
            
        Returns:
            Graph: 知识图谱对象，如果请求失败则返回None
        """
        if response.status_code == 200:
            try:
                # 尝试初始化KGGen
                kg = KGGen(
                    model=self.kg_model,
                    api_base=self.kg_api_base,
                    api_key=self.kg_api_key,
                    model_type="chat",  # 指定为聊天模型
                )
                
                # 生成图谱
                graph = kg.generate(
                    input_data=response.json(),
                    context="Knowledge relationships"
                )
                return graph
            except RuntimeError as e:
                # 捕获dspy.settings错误
                if "dspy.settings can only be changed" in str(e):
                    print(f"遇到dspy线程错误: {e}")
                    print("使用备用方法提取关系...")
                    
                    # 创建一个简单的图谱作为备用
                    result = response.json()
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    # 从文本中提取简单的关系
                    # 这是一个备用方案，仅提取文本中明显的关系
                    entities = set()
                    relations = set()
                    
                    # 添加核心关键词
                    keyword = content.split()[0] if content else "未知"
                    entities.add(keyword)
                    
                    # 提取明显的关系词
                    relation_keywords = ["是", "具有", "包括", "属于", "决定", "影响"]
                    lines = content.split("\n")
                    
                    for line in lines:
                        for rel in relation_keywords:
                            if rel in line:
                                parts = line.split(rel)
                                if len(parts) >= 2:
                                    try:
                                        source = parts[0].strip().split("、")[-1].strip("。，、；：""''")
                                        target = parts[1].strip().split("、")[0].strip("。，、；：""''")
                                        if source and target:
                                            entities.add(source)
                                            entities.add(target)
                                            relations.add((source, rel, target))
                                    except:
                                        pass
                    
                    # 创建备用图谱对象
                    return Graph(
                        entities=entities,
                        relations=relations,
                        edges=set(rel[1] for rel in relations)
                    )
                else:
                    # 其他错误直接抛出
                    raise
        else:
            print("请求失败")
            return None
    
    def get_entity(self, graph):
        """
        从图中提取实体，只获取关系三元组中的第一项和最后一项
        
        Args:
            graph: 知识图谱对象
            
        Returns:
            set: 包含所有实体的集合
        """
        all_strings = set()
        for relation in graph.relations:
            # 只添加三元组中的第一项(source)和最后一项(target)
            all_strings.add(relation[0])  # 添加源实体
            all_strings.add(relation[2])  # 添加目标实体
        return all_strings
    
    def convert_to_json_format(self, relations, nodes):
        """
        将关系和节点转换为指定的JSON格式
        
        Args:
            relations: 关系集合，包含(source, target, relation)元组
            nodes: 节点集合
            
        Returns:
            dict: 符合要求的JSON格式数据
        """
        # 构建节点数据
        json_nodes = [
            {
                "name": node,
                "symbolSize": 50,  # 默认大小，可以根据需要调整
                "category": 1      # 默认类别，可以根据需要调整
            }
            for node in nodes
        ]
        
        # 构建关系数据
        json_links = [
            {
                "source": source,
                "target": target,
                "name": relation
            }
            for source, relation, target in relations
        ]
        
        # 组合成最终的JSON格式
        json_data = {
            "nodes": json_nodes,
            "links": json_links
        }
        
        return json_data
    
    def generate_knowledge_graph(self, keyword="第一性原理", output_file="knowledge_graph.json"):
        """
        生成知识图谱并保存为JSON文件
        
        Args:
            keyword: 要查询的关键词
            output_file: 输出JSON文件的路径
            
        Returns:
            dict: 生成的知识图谱JSON数据
        """
        # 获取知识
        response = self.get_knowledge(keyword)
        
        # 生成图谱
        graph = self.get_graph(response)
        
        if graph is None:
            return None
        
        # 提取关系和节点
        relations = graph.relations
        nodes = self.get_entity(graph)
        
        # 转换为JSON格式
        json_result = self.convert_to_json_format(relations, nodes)
        
        # 将JSON数据保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_result, f, ensure_ascii=False, indent=4)
        
        print(f"JSON数据已保存到 {output_file} 文件中")
        return json_result


if __name__ == "__main__":
    # 创建知识图谱生成器实例
    kg_generator = KnowledgeGraphGenerator()
    
    # 生成知识图谱
    json_result = kg_generator.generate_knowledge_graph(keyword="朱元璋")