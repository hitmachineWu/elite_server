from kg_json import KnowledgeGraphGenerator

from kg_json2graph import create_graph, load_json_data


kg_generator = KnowledgeGraphGenerator()
result = kg_generator.generate_knowledge_graph(keyword="第一性原理")
print("生成结果:", result)