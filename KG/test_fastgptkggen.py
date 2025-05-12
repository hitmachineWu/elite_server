from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import uuid
from kg_json import KnowledgeGraphGenerator
from kg_json2graph import create_graph, load_json_data


kg_generator = KnowledgeGraphGenerator()
result = kg_generator.generate_knowledge_graph(keyword="第一性原理")
print("生成结果:", result)