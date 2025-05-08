import os
import json
import spacy
from openai import OpenAI
from dotenv import load_dotenv
import plotly.graph_objects as go

# 加载环境变量
# load_dotenv()
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MetaStructureAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.structure_rules = {
            "argumentative": {
                "required_sections": ["thesis", "supporting", "counterargument", "conclusion"],
                "min_arguments": 2,
                "max_section_length_ratio": 0.4
            },
            "narrative": {
                "required_sections": ["exposition", "rising_action", "climax", "falling_action"],
                "min_plot_points": 3
            }
        }
    
    def analyze_structure(self, text, genre="argumentative"):
        """主分析函数"""
        # Step 1: 分块处理（长文本优化）
        # chunks = self._chunk_text(text)
        
        # LLM结构标注
        # structure_data = self._llm_structure_analysis(text, genre)
        # 把这串字符串转换成json：
        structure_data = {'core_claim': '计算机是社会发展和扩展的必需品', 'logic_tree': {'node_id': 'root', 'content': '计算机是社会发展和扩展的必需品', 'children': [{'node_id': 'A1', 'content': '计算机帮助培养手眼协调能力', 'children': [{'node_id': 'A1a', 'content': '手眼协调有助于体育运动中的表现', 'evidence': ['@PERCENT1的儿童认为计算机使用后手眼协调有所提高', '@CAPS2 @PERSON1表明计算机加强了手眼协调'], 'children': [{'node_id': 'A1a1', 'content': '提高手眼协调的人在体育运动中表现更好', 'evidence': ['手眼协调有助提升棒球和篮球等运动'], 'children': [{'node_id': 'A1a1a', 'content': '运动表现提升可带来更好的健康状况', 'evidence': []}]}]}, {'node_id': 'A1b', 'content': '常规操作如打字也可促进手眼协调', 'evidence': []}]}, {'node_id': 'B1', 'content': '计算机使人们能够了解遥远地方和人民', 'children': [{'node_id': 'B1a', 'content': '提供搜索功能，易于获取信息', 'evidence': []}, {'node_id': 'B1b', 'content': '易于学习不同文化，促进包容性', 'evidence': []}]}, {'node_id': 'C1', 'content': '计算机使人们可以在线交流', 'children': [{'node_id': 'C1a', 'content': '视频聊天和在线对话减少电话费', 'evidence': []}, {'node_id': 'C1b', 'content': '帮助与家人和朋友保持联系', 'evidence': ['提供与家乡人联系的方式'], 'children': [{'node_id': 'C1b1', 'content': '更多地了解家庭和朋友的生活', 'evidence': []}]}]}]}, 'depth': 4}
        print(structure_data)
        import pdb; pdb.set_trace()
        # Step 3: 规则验证
        # is_valid, errors = self._validate_structure(structure_data, genre)
        
        # Step 4: 生成逻辑树
        # if not is_valid:
        #     structure_data = self._correct_errors(structure_data, errors)
        logic_tree = self._build_logic_tree(structure_data)
        
        # return {
        #     "structure_type": genre,
        #     "sections": structure_data,
        #     "logic_tree": logic_tree,
        #     "validation_errors": errors
        # }
    
    def _chunk_text(self, text, max_length=2000):
        """智能分块：按段落分割，保留完整语义"""
        paragraphs = [p for p in text.split('\n') if p.strip()]
        chunks = []
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            if current_length + len(para) < max_length:
                current_chunk.append(para)
                current_length += len(para)
            else:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [para]
                current_length = len(para)
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        return chunks
    
    def _llm_structure_analysis(self, chunks, genre):
        """调用GPT-4进行结构分析"""
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0.3,  # 降低随机性，提升结构稳定性
            messages=[{
                "role": "user",
                "content": f"""你是一个专业的议论文逻辑结构分析系统，请按照以下要求解析文本：
                1. **深度逻辑挖掘**：识别所有层级的论点关系，允许任意层级的嵌套（如主论点→分论点→子论点→论据）
                2. **动态结构构建**：根据实际内容生成树状结构，不预设层级数量
                3. **论点精炼原则**：
                - 每个论点内可做概括，表述尽量精简
                - 尊重原文，不做论点的增添和删除，同时保留原文顺序
                4. 返回的结果使用文章原本的语言种类（如中文、英文等）
                5. **结构化输出**：使用以下灵活嵌套的JSON格式：
                {{
                    "core_claim": "提炼后的核心论点（20词内）",
                    "logic_tree": {{
                        "node_id": "root",
                        "content": "核心论点",
                        "children": [
                        {{
                            "node_id": "A1",
                            "content": "一级分论点",
                            "children": [
                            {{
                                "node_id": "A1a",
                                "content": "二级子论点",
                                "evidence": ["支撑论据1", "支撑论据2"],
                                "children": [...] 
                            }}
                            ]
                        }},
                        {{
                            "node_id": "B1",
                            "content": "另一条一级分论点",
                            "evidence": ["直接支撑论据"]
                        }}
                        ]
                    }},
                    "depth": 3,  // 最大逻辑深度
                }}

                文本内容：{chunks}
                """
            }],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def _validate_structure(self, data, genre):
        """基于规则的验证"""
        rules = self.structure_rules.get(genre, {})
        errors = []
        
        # 检查必要部分
        required = rules.get("required_sections", [])
        existing_sections = [s['type'] for s in data['paragraphs']]
        missing = [s for s in required if s not in existing_sections]
        if missing:
            errors.append(f"缺失必要部分: {missing}")
        
        # 检查论点数量
        min_args = rules.get("min_arguments", 2)
        args = [s for s in data['paragraphs'] if s['type'] == 'supporting_argument']
        if len(args) < min_args:
            errors.append(f"支持论点不足（需要至少{min_args}个）")
        
        return len(errors) == 0, errors
    
    def _correct_errors(self, data, errors):
        """异常修正：根据错误类型自动修补"""
        # 示例：自动添加缺失的结论段
        if "缺失必要部分: ['conclusion']" in errors:
            data['paragraphs'].append({
                "type": "conclusion",
                "content": "[自动生成] 综上所述...",
                "is_generated": True
            })
        return data
    
    def _build_logic_tree(self, data):
        """使用 Plotly 生成交互式逻辑树"""
        fig = go.Figure()
        
        # 坐标计算
        positions = {}
        evidence_positions = {}  # 存储证据节点的坐标
        evidence_contents = {}  # 存储证据内容
        def calculate_positions(node, x=0, y=0, depth=0):
            positions[node["node_id"]] = (x, y)
            num_children = len(node.get("children", []))
            if num_children > 0:
                x_step = 4.0 / (2 ** depth)  # 动态调整横向间隔
                start_x = x - (num_children-1)*x_step/2
                for i, child in enumerate(node.get("children", [])):
                    child_x = start_x + i*x_step
                    child_y = y - 1
                    calculate_positions(child, child_x, child_y, depth+1)

            # 计算证据节点的坐标
            if node.get("evidence"):
                evidence_x = x + 1  # 证据节点放在右侧
                evidence_y = y
                for i, evidence in enumerate(node.get("evidence")):
                    evidence_id = f"{node['node_id']}_evidence_{i}"
                    evidence_positions[evidence_id] = (evidence_x, evidence_y - i * 0.5)  # 垂直排列证据
                    evidence_contents[evidence_id] = evidence  # 存储证据内容

        calculate_positions(data["logic_tree"], y=0)

        # 添加边
        edges_x = []
        edges_y = []
        def add_edges(node):
            for child in node.get("children", []):
                edges_x.extend([positions[node["node_id"]][0], positions[child["node_id"]][0], None])
                edges_y.extend([positions[node["node_id"]][1], positions[child["node_id"]][1], None])
                add_edges(child)
        
        add_edges(data["logic_tree"])
        fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line=dict(color='#888')))

        # 添加证据节点和边
        evidence_edges_x = []
        evidence_edges_y = []
        for evidence_id, (x, y) in evidence_positions.items():
            # 添加证据节点到主节点的边
            parent_id = evidence_id.split("_evidence_")[0]
            evidence_edges_x.extend([positions[parent_id][0], x, None])
            evidence_edges_y.extend([positions[parent_id][1], y, None])

        fig.add_trace(go.Scatter(
            x=evidence_edges_x, y=evidence_edges_y,
            mode='lines',
            line=dict(color='#FFA500', dash='dot'),  # 使用虚线表示证据边
            hoverinfo='none'
        ))


        # 添加逻辑树节点
        node_x = []
        node_y = []
        node_text = []
        for node_id, (x, y) in positions.items():
            node_x.append(x)
            node_y.append(y)
            node = find_node(data["logic_tree"], node_id)
            node_text.append(node["content"])

        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                color='#4CAF50',
                size=40,
                line=dict(width=2, color='DarkSlateGrey')
            ),
            hoverinfo='text',
            textfont=dict(size=10)
        ))

        # 添加证据节点
        evidence_x = []
        evidence_y = []
        evidence_text = []
        for evidence_id, (x, y) in evidence_positions.items():
            evidence_x.append(x)
            evidence_y.append(y)
            evidence_text.append(evidence_contents[evidence_id])  # 显示证据内容

        fig.add_trace(go.Scatter(
            x=evidence_x, y=evidence_y,
            mode='markers+text',
            text=evidence_text,
            # 下方显示证据内容
            textposition="bottom center",  
            marker=dict(
                color='#FFA500',
                size=20,
                line=dict(width=1, color='DarkSlateGrey')
            ),
            hoverinfo='text',
            textfont=dict(size=8)
        ))

        # 设置布局
        fig.update_layout(
            title=f"逻辑树可视化 - 最大深度 {data['depth']}",
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            plot_bgcolor='white'
        )
        fig.show()

def find_node(node, target_id):
    """递归查找节点"""
    if node["node_id"] == target_id:
        return node
    for child in node.get("children", []):
        found = find_node(child, target_id)
        if found:
            return found
    return None


# 使用示例
agent = MetaStructureAgent()
result = agent.analyze_structure("""
Dear @ORGANIZATION1, The computer blinked to life and an image of a blonde haired girl filled the screen. It was easy to find out how life was in @LOCATION2, thanks to the actual @CAPS1 girl explaining it. Going to the library wouldn't have filled one with this priceless information and human interection. Computers are a nessessity of life if soceity wishes to grow and expand. They should be supported because they teach hand eye coordination, give people the ability to learn about faraway places, and allow people to talk to others online. Firstly, computers help teach hand eye coordination. Hand-eye coordination is a useful ability that is usod to excel in sports. In a recent survey, @PERCENT1 of kids felt their hand eye coordination improves after computer use. Even a simple thing like tying can build up this skill. Famous neurologist @CAPS2 @PERSON1 stated in an article last week that, ""@CAPS3 and computer strength the @CAPS2. When on the computer, you automatically process what the eyes see into a command for your hands."" @CAPS4 hand eye coordination can improve people in sports such as baseball and basketball. If someone wan't to become better in these sports, all they'd need to do was turn on the computer. Once people become better at sports, they're more likely to play them and become more healthy. In reality, computers can help with exercising instead of decreasing it. Additionaly, computers allow people to access information about faraway places and people. If someone wanted to reasearch @LOCATION1, all they'd need to do was type in a search would be presented to them in it would link forever to search through countless things. Also, having the ability to learn about cultures can make peole peole and their cultures, they understand others something. Increase tolerance people are. Computers are a resourceful tool that they can help people in every different aspect of life. Lastly, computer and in technology can allow people to chat. Computer chat and video chat can help the all different nations. Bring on good terms places other than can help us understand story comes out about something that happend in @LOCATION3, people can just go on their computer and ask an actual @LOCATION3 citizen their take on the matter. Also, video chat and online conversation can cut down on expensive phone bills. No one wants to pay more than they have to in this economy. Another good point is that you can acess family members you scaresly visit. It can help you connect within your own family more. Oviously, computers are a useful aid in todays era. their advancements push the world foreward to a better place. Computers can help people because they help teach handeye coordination, give people the bility to learn about faraway places and people, and allow people to talk online with others. Think of a world with no computers or technologicall advancements. The world would be sectored and unified, contact between people scare, and information even. The internet is like thousands or librarys put together. Nobody would know much about other nations and news would travel slower. Is that the kind of palce you want people to live in?
""")

# result['logic_tree'].show()  # 显示交互式图表
# print(json.dumps(result['sections'], indent=2))