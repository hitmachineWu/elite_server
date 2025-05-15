import sys 
import os 
import json

from kg_gen import KGGen, Graph

def convert_to_json_format(relations, nodes):
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
            "symbolSize": 50,  # 默认大小
            "category": 1      # 默认类别
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

def get_entity(graph):
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

def connect_entities_to_key(relations, nodes, key):
    """
    将所有实体连接到指定的key节点
    
    Args:
        relations: 原始关系列表
        nodes: 节点集合
        key: 中心节点名称
        
    Returns:
        list: 添加了新关系的关系列表
    """
    new_relations = relations.copy()
    
    # 如果key节点不在节点集合中，需要添加
    if key not in nodes:
        nodes.add(key)
    
    # 为每个不是key的节点添加与key的连接关系
    for node in nodes:
        if node != key:
            # 添加从实体到key的关系，使用"关联"作为关系名称
            new_relations.add((node, "关联", key))
    
    return new_relations

if __name__ == "__main__":
  # Load environment variables
  
  # Initialize KGGen
  kg = KGGen(
      model="openai/Qwen/Qwen2.5-72B-Instruct",
      api_base="http://180.85.206.19:8123/v1",
      api_key="local",
      model_type="chat",  # 指定为聊天模型
  )
  
text_input = """# STM32微控制器：定义与架构核心

## 1. 定义与产品定位
STM32是意法半导体（STMicroelectronics）基于ARM Cortex-M内核开发的32位微控制器系列，其设计面向嵌入式实时应用场景。  
**三元组联结**：  
- (STM32, 基于, ARM Cortex-M内核)  
- (ARM Cortex-M内核, 提供, 实时处理能力)  

该系列通过不同子系列（如STM32F0/F1/F4/H7）覆盖从低成本到高性能的全频谱需求，形成完整生态链。例如，STM32F1采用Cortex-M3内核，而STM32H7则搭载双核Cortex-M7+M4架构。  
**三元组联结**：  
- (STM32F1, 搭载, Cortex-M3内核)  
- (STM32H7, 采用, 双核异构架构)  

## 2. 关键硬件特性

### 2.1 外设集成
STM32通过高度集成的外设模块（如GPIO、ADC、定时器、通信接口）降低系统复杂度。以STM32F407为例，其包含3个12位ADC和17个定时器，支持多任务同步触发。  
**三元组联结**：  
- (STM32F407, 集成, 多通道ADC)  
- (定时器模块, 支持, PWM波形生成)  

### 2.2 低功耗设计
STM32L系列引入动态电压调节和多种休眠模式，例如Stop模式下电流可低至1μA。这种特性使其在IoT传感器节点中具有显著优势。  
**三元组联结**：  
- (STM32L系列, 实现, 动态电压调节)  
- (Stop模式, 降低, 系统功耗)  

## 3. 软件开发生态

### 3.1 HAL库与LL库
STM32CubeMX工具链提供HAL（硬件抽象层）和LL（底层）两种驱动库。HAL库通过标准化API简化移植，而LL库直接操作寄存器以实现极致性能。  
**三元组联结**：  
- (STM32CubeMX, 生成, HAL/LL库代码)  
- (LL库, 直接访问, 寄存器层)  

### 3.2 RTOS支持
FreeRTOS和ThreadX等实时操作系统可原生运行于STM32，借助其内存保护单元（MPU）实现任务隔离。例如Cortex-M7内核的STM32F7支持精确的MPU区域配置。  
**三元组联结**：  
- (FreeRTOS, 适配, STM32硬件平台)  
- (MPU模块, 保障, 多任务安全性)  

## 4. 典型应用场景

### 4.1 工业控制
在PLC系统中，STM32F4系列凭借144MHz主频和浮点运算单元（FPU）实现高速PID控制环路，同时通过CAN总线与IO模块通信。  
**三元组联结**：  
- (STM32F4, 集成, FPU单元)  
- (CAN总线, 连接, 分布式IO设备)  

### 4.2 消费电子
STM32WB系列整合蓝牙5.0射频前端，在无线耳机设计中可同时处理音频编解码和射频协议栈，体现其异构处理能力。  
**三元组联结**：  
- (STM32WB, 内置, 蓝牙射频模块)  
- (Cortex-M4内核, 处理, 音频DSP算法)  

## 5. 开发挑战与解决方案

### 5.1 电源噪声抑制
高频运行的STM32H7需配合多层PCB设计和去耦电容网络，其参考手册明确要求每个VDD引脚需配置100nF+10μF电容组合。  
**三元组联结**：  
- (STM32H7, 要求, 严格电源滤波)  
- (去耦电容, 抑制, 高频噪声)  

### 5.2 代码优化
针对时间敏感应用，开发者需平衡HAL库便利性与LL库效率。通过I-Cache/D-Cache配置可提升Cortex-M7内核的指令吞吐量30%以上。  
**三元组联结**：  
- (Cache配置, 影响, 指令执行效率)  
- (时间关键代码, 建议使用, LL库)"""

prompt = "请以自然语言的形式，围绕【第一性原理】展开详细介绍。你的回答需要包含以下要素：1.首先用通俗易懂的方式解释这个知识点的基础概念和关键特征。2.然后沿着时间维度或逻辑维度，梳理该知识点的发展脉络或内在逻辑关系。3.接着说明与之直接相关的一些重要关联知识点，对每个关联点简要说明其与核心知识点的关系。请注意：1.保持叙述的连贯性，不需要使用项目符号或结构化排版。2.适当使用过渡词和连接词展现知识点之间的关联性。3.涉及专业术语时请附带简单解释。4.重点呈现知识之间的网状联系而非孤立事实。5.禁止任何形式的实例或案例说明，禁止对知识点进行价值判断或主观评价。现在请就【第一性原理】进行详细阐述。"

graph_1 = kg.generate(
  input_data=text_input,
  context="Knowledge relationships"
)
print(graph_1)

key = "stm32"
# 从图谱中提取实体和关系
nodes = get_entity(graph_1)
relations = graph_1.relations

# 将所有实体连接到key节点
relations = connect_entities_to_key(relations, nodes, key)

# 转换为JSON格式
json_result = convert_to_json_format(relations, nodes)

# 将JSON数据保存到文件
output_file = "stm32_knowledge_graph.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(json_result, f, ensure_ascii=False, indent=4)

print(f"JSON数据已保存到 {output_file} 文件中")



### 连接搜索实体