#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import sys
from typing import List, Tuple

# 添加项目根目录到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kg_gen import KGGen
from kg_gen.models import Graph

class TestKGGenWithSGLang(unittest.TestCase):
    """测试使用 SGLang 部署的 LLM 的 KGGen 类"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 设置 SGLang 服务器的 URL 和模型类型
        # 注意：这里假设您已经有一个运行中的 SGLang 服务器
        self.api_base = "http://180.85.206.19:8123/v1"  # 根据您的实际部署修改
        self.model_type = "chat"
        self.model = "Qwen/Qwen2.5-72B-Instruct"  # 根据您实际部署的模型修改
        
        # 初始化 KGGen 实例
        self.kg_gen = KGGen(
            model=self.model,
            api_base=self.api_base,
            model_type=self.model_type,
            temperature=0.0
        )
        
        # 测试用的简单文本
        self.simple_text = """
        人工智能（AI）是计算机科学的一个分支，它致力于创建能够模拟人类智能的系统。
        机器学习是AI的一个子领域，它使用数据来训练模型。
        深度学习是机器学习的一种特殊形式，它使用神经网络进行学习。
        """
        
        # 测试用的对话文本
        self.conversation = [
            {"role": "user", "content": "什么是知识图谱？"},
            {"role": "assistant", "content": "知识图谱是一种结构化的知识表示方式，它以图的形式存储实体和它们之间的关系。知识图谱广泛应用于搜索引擎、推荐系统和问答系统等领域。"},
            {"role": "user", "content": "它与数据库有什么区别？"},
            {"role": "assistant", "content": "知识图谱与传统数据库的主要区别在于：知识图谱强调实体间的语义关系，而传统数据库主要关注数据的结构化存储。知识图谱更适合处理复杂的关联查询和推理任务。"}
        ]
    
    def test_generate_from_text(self):
        """测试从文本生成知识图谱"""
        try:
            # 从简单文本生成知识图谱
            graph = self.kg_gen.generate(self.simple_text)
            
            # 验证生成的图是否符合预期
            self.assertIsInstance(graph, Graph)
            self.assertTrue(len(graph.entities) > 0, "实体列表不应为空")
            self.assertTrue(len(graph.relations) > 0, "关系列表不应为空")
            self.assertTrue(len(graph.edges) > 0, "边列表不应为空")
            
            # 验证是否包含预期的实体
            expected_entities = ["人工智能", "AI", "计算机科学", "机器学习", "深度学习", "神经网络"]
            for entity in expected_entities:
                self.assertTrue(
                    any(entity.lower() in e.lower() for e in graph.entities),
                    f"未找到预期的实体: {entity}"
                )
            
            # 打印生成的知识图谱信息
            print("\n生成的知识图谱信息:")
            print(f"实体数量: {len(graph.entities)}")
            print(f"关系数量: {len(graph.relations)}")
            print(f"边数量: {len(graph.edges)}")
            
            # 打印部分实体和关系示例
            print("\n实体示例:")
            for entity in list(graph.entities)[:5]:
                print(f"- {entity}")
                
            print("\n关系示例:")
            for relation in list(graph.relations)[:5]:
                print(f"- {relation[0]} --[{relation[1]}]--> {relation[2]}")
                
        except Exception as e:
            self.fail(f"测试失败，出现异常: {str(e)}")
    
    def test_generate_from_conversation(self):
        """测试从对话生成知识图谱"""
        try:
            # 从对话生成知识图谱
            graph = self.kg_gen.generate(self.conversation)
            
            # 验证生成的图是否符合预期
            self.assertIsInstance(graph, Graph)
            self.assertTrue(len(graph.entities) > 0, "实体列表不应为空")
            self.assertTrue(len(graph.relations) > 0, "关系列表不应为空")
            self.assertTrue(len(graph.edges) > 0, "边列表不应为空")
            
            # 验证是否包含预期的实体
            expected_entities = ["知识图谱", "实体", "关系", "数据库", "搜索引擎", "推荐系统", "问答系统"]
            for entity in expected_entities:
                self.assertTrue(
                    any(entity.lower() in e.lower() for e in graph.entities),
                    f"未找到预期的实体: {entity}"
                )
            
            # 打印生成的知识图谱信息
            print("\n从对话生成的知识图谱信息:")
            print(f"实体数量: {len(graph.entities)}")
            print(f"关系数量: {len(graph.relations)}")
            print(f"边数量: {len(graph.edges)}")
            
            # 打印部分实体和关系示例
            print("\n实体示例:")
            for entity in list(graph.entities)[:5]:
                print(f"- {entity}")
                
            print("\n关系示例:")
            for relation in list(graph.relations)[:5]:
                print(f"- {relation[0]} --[{relation[1]}]--> {relation[2]}")
                
        except Exception as e:
            self.fail(f"测试失败，出现异常: {str(e)}")
    
    def test_chunking(self):
        """测试文本分块功能"""
        # 创建一个较长的文本
        long_text = self.simple_text * 10
        
        try:
            # 使用分块功能生成知识图谱
            graph = self.kg_gen.generate(long_text, chunk_size=500)
            
            # 验证生成的图是否符合预期
            self.assertIsInstance(graph, Graph)
            self.assertTrue(len(graph.entities) > 0, "实体列表不应为空")
            self.assertTrue(len(graph.relations) > 0, "关系列表不应为空")
            self.assertTrue(len(graph.edges) > 0, "边列表不应为空")
            
            print("\n使用分块功能生成的知识图谱信息:")
            print(f"实体数量: {len(graph.entities)}")
            print(f"关系数量: {len(graph.relations)}")
            print(f"边数量: {len(graph.edges)}")
            
        except Exception as e:
            self.fail(f"测试分块功能失败，出现异常: {str(e)}")
    
    def test_clustering(self):
        """测试图聚类功能"""
        try:
            # 生成知识图谱并进行聚类
            graph = self.kg_gen.generate(self.simple_text, cluster=True, context="人工智能领域")
            
            # 验证聚类结果
            self.assertIsInstance(graph, Graph)
            self.assertIsNotNone(graph.entity_clusters, "实体聚类结果不应为空")
            self.assertIsNotNone(graph.edge_clusters, "边聚类结果不应为空")
            
            print("\n聚类后的知识图谱信息:")
            print(f"实体聚类数量: {len(graph.entity_clusters) if graph.entity_clusters else 0}")
            print(f"边聚类数量: {len(graph.edge_clusters) if graph.edge_clusters else 0}")
            
            # 打印部分聚类示例
            if graph.entity_clusters:
                print("\n实体聚类示例:")
                for cluster_key, cluster_values in list(graph.entity_clusters.items())[:3]:
                    print(f"- 聚类: {cluster_key}")
                    print(f"  成员: {', '.join(list(cluster_values)[:5])}")
            
        except Exception as e:
            self.fail(f"测试聚类功能失败，出现异常: {str(e)}")
    
    def test_model_switching(self):
        """测试模型切换功能"""
        try:
            # 使用初始模型生成知识图谱
            graph1 = self.kg_gen.generate(self.simple_text)
            
            # 切换到另一个模型（如果有）
            alternative_model = "gpt-3.5-turbo"  # 根据实际情况修改
            graph2 = self.kg_gen.generate(self.simple_text, model=alternative_model)
            
            # 验证两个图都生成成功
            self.assertIsInstance(graph1, Graph)
            self.assertIsInstance(graph2, Graph)
            
            print("\n模型切换测试:")
            print(f"原始模型 ({self.model}) 生成的实体数量: {len(graph1.entities)}")
            print(f"替代模型 ({alternative_model}) 生成的实体数量: {len(graph2.entities)}")
            
        except Exception as e:
            self.fail(f"测试模型切换功能失败，出现异常: {str(e)}")
    
    def test_graph_aggregation(self):
        """测试图聚合功能"""
        try:
            # 生成两个知识图谱
            graph1 = self.kg_gen.generate(self.simple_text)
            graph2 = self.kg_gen.generate(self.conversation)
            
            # 聚合两个图
            aggregated_graph = self.kg_gen.aggregate([graph1, graph2])
            
            # 验证聚合结果
            self.assertIsInstance(aggregated_graph, Graph)
            self.assertTrue(len(aggregated_graph.entities) >= len(graph1.entities), "聚合后的实体数量应不少于单个图")
            self.assertTrue(len(aggregated_graph.relations) >= len(graph1.relations), "聚合后的关系数量应不少于单个图")
            
            print("\n图聚合测试:")
            print(f"图1实体数量: {len(graph1.entities)}")
            print(f"图2实体数量: {len(graph2.entities)}")
            print(f"聚合后实体数量: {len(aggregated_graph.entities)}")
            print(f"图1关系数量: {len(graph1.relations)}")
            print(f"图2关系数量: {len(graph2.relations)}")
            print(f"聚合后关系数量: {len(aggregated_graph.relations)}")
            
        except Exception as e:
            self.fail(f"测试图聚合功能失败，出现异常: {str(e)}")

if __name__ == "__main__":
    unittest.main()
