#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SGLang 部署的 LLM 的 KGGen 类使用示例
"""

import os
import sys
import json

# 添加项目根目录到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kg_gen import KGGen

def main():
    """
    展示如何使用 SGLang 部署的 LLM 的 KGGen 类
    """
    # 初始化 KGGen 实例，使用 SGLang 部署的 LLM
    kg_gen = KGGen(
        model="llama3",  # 根据您实际部署的模型修改
        api_base="http://localhost:8000/v1",  # 根据您的实际部署修改
        api_key="local",  # SGLang 通常使用 "local" 作为 API 密钥
        model_type="chat",  # 指定为聊天模型
        temperature=0.0  # 设置温度为 0，使输出更确定性
    )
    
    print("KGGen 实例已初始化，使用 SGLang 部署的 LLM")
    
    # 示例 1：从简单文本生成知识图谱
    simple_text = """
    人工智能（AI）是计算机科学的一个分支，它致力于创建能够模拟人类智能的系统。
    机器学习是AI的一个子领域，它使用数据来训练模型。
    深度学习是机器学习的一种特殊形式，它使用神经网络进行学习。
    """
    
    print("\n示例 1：从简单文本生成知识图谱")
    graph1 = kg_gen.generate(simple_text)
    
    print("\n生成的知识图谱信息:")
    print(f"实体数量: {len(graph1.entities)}")
    print(f"关系数量: {len(graph1.relations)}")
    print(f"边数量: {len(graph1.edges)}")
    
    print("\n实体示例:")
    for entity in list(graph1.entities)[:5]:
        print(f"- {entity}")
        
    print("\n关系示例:")
    for relation in list(graph1.relations)[:5]:
        print(f"- {relation[0]} --[{relation[1]}]--> {relation[2]}")
    
    # 示例 2：从对话生成知识图谱
    conversation = [
        {"role": "user", "content": "什么是知识图谱？"},
        {"role": "assistant", "content": "知识图谱是一种结构化的知识表示方式，它以图的形式存储实体和它们之间的关系。知识图谱广泛应用于搜索引擎、推荐系统和问答系统等领域。"},
        {"role": "user", "content": "它与数据库有什么区别？"},
        {"role": "assistant", "content": "知识图谱与传统数据库的主要区别在于：知识图谱强调实体间的语义关系，而传统数据库主要关注数据的结构化存储。知识图谱更适合处理复杂的关联查询和推理任务。"}
    ]
    
    print("\n示例 2：从对话生成知识图谱")
    graph2 = kg_gen.generate(conversation)
    
    print("\n生成的知识图谱信息:")
    print(f"实体数量: {len(graph2.entities)}")
    print(f"关系数量: {len(graph2.relations)}")
    print(f"边数量: {len(graph2.edges)}")
    
    # 示例 3：使用分块功能处理长文本
    print("\n示例 3：使用分块功能处理长文本")
    long_text = simple_text * 10  # 创建一个较长的文本
    graph3 = kg_gen.generate(long_text, chunk_size=500)
    
    print("\n使用分块功能生成的知识图谱信息:")
    print(f"实体数量: {len(graph3.entities)}")
    print(f"关系数量: {len(graph3.relations)}")
    print(f"边数量: {len(graph3.edges)}")
    
    # 示例 4：生成知识图谱并进行聚类
    print("\n示例 4：生成知识图谱并进行聚类")
    graph4 = kg_gen.generate(simple_text, cluster=True, context="人工智能领域")
    
    print("\n聚类后的知识图谱信息:")
    print(f"实体聚类数量: {len(graph4.entity_clusters) if graph4.entity_clusters else 0}")
    print(f"边聚类数量: {len(graph4.edge_clusters) if graph4.edge_clusters else 0}")
    
    # 示例 5：聚合多个知识图谱
    print("\n示例 5：聚合多个知识图谱")
    aggregated_graph = kg_gen.aggregate([graph1, graph2])
    
    print("\n聚合后的知识图谱信息:")
    print(f"实体数量: {len(aggregated_graph.entities)}")
    print(f"关系数量: {len(aggregated_graph.relations)}")
    print(f"边数量: {len(aggregated_graph.edges)}")
    
    # 将结果保存到文件
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 将知识图谱保存为 JSON 格式
    def save_graph_to_json(graph, filename):
        graph_dict = {
            "entities": list(graph.entities),
            "relations": [list(relation) for relation in graph.relations],
            "edges": list(graph.edges)
        }
        
        if graph.entity_clusters:
            graph_dict["entity_clusters"] = {
                key: list(values) for key, values in graph.entity_clusters.items()
            }
            
        if graph.edge_clusters:
            graph_dict["edge_clusters"] = {
                key: list(values) for key, values in graph.edge_clusters.items()
            }
            
        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
            json.dump(graph_dict, f, ensure_ascii=False, indent=2)
    
    save_graph_to_json(graph1, "simple_text_graph.json")
    save_graph_to_json(graph2, "conversation_graph.json")
    save_graph_to_json(graph4, "clustered_graph.json")
    save_graph_to_json(aggregated_graph, "aggregated_graph.json")
    
    print(f"\n知识图谱已保存到 {output_dir} 目录")

if __name__ == "__main__":
    main() 