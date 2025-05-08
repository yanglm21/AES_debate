import os
import json
import spacy
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AudienceAwarenessAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.audience_profiles = {
            "general": {"tone": "neutral", "complexity": "medium"},
            "academic": {"tone": "formal", "complexity": "high"},
            "casual": {"tone": "informal", "complexity": "low"}
        }
    
    def analyze_audience_awareness(self, text, target_audience="general"):
        """主分析函数"""
        
        # Step 2: 调用GPT-4进行受众适配性分析
        audience_analysis = self._llm_audience_analysis(text, target_audience)
        
        return {
            "detailed_analysis": audience_analysis
        }
    
    def _extract_text_features(self, text):
        """使用spaCy提取文本特征"""
        doc = self.nlp(text)
        features = {
            "avg_sentence_length": sum(len(sent) for sent in doc.sents) / len(list(doc.sents)),
            "formal_words": sum(1 for token in doc if token.lemma_ in ["therefore", "however", "moreover"]),
            "informal_words": sum(1 for token in doc if token.lemma_ in ["like", "gonna", "wanna"]),
            "pronoun_usage": sum(1 for token in doc if token.pos_ == "PRON"),
            "passive_voice": sum(1 for sent in doc.sents if any(tok.dep_ == "nsubjpass" for tok in sent))
        }
        return features
    
    def _llm_audience_analysis(self, text, target_audience):
        """调用GPT-4进行受众适配性分析"""
        prompt = f"""
        你是一个专业的文本分析系统，请根据以下要求分析文本的受众适配性：
        1. **目标受众**：{target_audience}
        2. **分析维度**：
           - 语气（tone）：是否符合目标受众的预期（如学术受众需正式语气）
           - 复杂度（complexity）：词汇和句法是否适合目标受众
           - 互动性（engagement）：是否有效吸引目标受众的注意力
        3. **输出格式（json）**：
           {{
             "tone_analysis": "语气分析结果",
             "complexity_analysis": "复杂度分析结果",
             "engagement_analysis": "互动性分析结果",
             "audience_fit_score": 0-10  // 受众适配性评分
           }}

        待分析文本：
        {text}
        """
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    
    def _evaluate_audience_awareness(self, features, analysis, target_audience):
        """基于规则验证与评分"""
        target_profile = self.audience_profiles.get(target_audience, self.audience_profiles["general"])
        
        # 评分规则
        score = 0
        feedback = []
        
        # 语气评分
        if "formal" in analysis["tone_analysis"].lower() and target_profile["tone"] == "formal":
            score += 3
        elif "informal" in analysis["tone_analysis"].lower() and target_profile["tone"] == "informal":
            score += 3
        else:
            feedback.append(f"语气不符合目标受众：当前语气为{analysis['tone_analysis']}，预期为{target_profile['tone']}")
        
        # 复杂度评分
        if features["avg_sentence_length"] > 15 and target_profile["complexity"] == "high":
            score += 3
        elif features["avg_sentence_length"] < 10 and target_profile["complexity"] == "low":
            score += 3
        else:
            feedback.append(f"复杂度不符合目标受众：当前句子平均长度为{features['avg_sentence_length']}，预期为{target_profile['complexity']}")
        
        # 互动性评分
        if features["pronoun_usage"] > 5 and target_audience == "casual":
            score += 2
        elif features["pronoun_usage"] < 3 and target_audience == "academic":
            score += 2
        else:
            feedback.append(f"互动性不符合目标受众：当前代词使用次数为{features['pronoun_usage']}")
        
        # 最终评分
        score = min(10, score)  # 确保评分不超过10
        return score, feedback

# 使用示例
agent = AudienceAwarenessAgent()
text = """
Dear @ORGANIZATION1, The computer blinked to life and an image of a blonde haired girl filled the screen. It was easy to find out how life was in @LOCATION2, thanks to the actual @CAPS1 girl explaining it. Going to the library wouldn't have filled one with this priceless information and human interection. Computers are a nessessity of life if soceity wishes to grow and expand. They should be supported because they teach hand eye coordination, give people the ability to learn about faraway places, and allow people to talk to others online. Firstly, computers help teach hand eye coordination. Hand-eye coordination is a useful ability that is usod to excel in sports. In a recent survey, @PERCENT1 of kids felt their hand eye coordination improves after computer use. Even a simple thing like tying can build up this skill. Famous neurologist @CAPS2 @PERSON1 stated in an article last week that, ""@CAPS3 and computer strength the @CAPS2. When on the computer, you automatically process what the eyes see into a command for your hands."" @CAPS4 hand eye coordination can improve people in sports such as baseball and basketball. If someone wan't to become better in these sports, all they'd need to do was turn on the computer. Once people become better at sports, they're more likely to play them and become more healthy. In reality, computers can help with exercising instead of decreasing it. Additionaly, computers allow people to access information about faraway places and people. If someone wanted to reasearch @LOCATION1, all they'd need to do was type in a search would be presented to them in it would link forever to search through countless things. Also, having the ability to learn about cultures can make peole peole and their cultures, they understand others something. Increase tolerance people are. Computers are a resourceful tool that they can help people in every different aspect of life. Lastly, computer and in technology can allow people to chat. Computer chat and video chat can help the all different nations. Bring on good terms places other than can help us understand story comes out about something that happend in @LOCATION3, people can just go on their computer and ask an actual @LOCATION3 citizen their take on the matter. Also, video chat and online conversation can cut down on expensive phone bills. No one wants to pay more than they have to in this economy. Another good point is that you can acess family members you scaresly visit. It can help you connect within your own family more. Oviously, computers are a useful aid in todays era. their advancements push the world foreward to a better place. Computers can help people because they help teach handeye coordination, give people the bility to learn about faraway places and people, and allow people to talk online with others. Think of a world with no computers or technologicall advancements. The world would be sectored and unified, contact between people scare, and information even. The internet is like thousands or librarys put together. Nobody would know much about other nations and news would travel slower. Is that the kind of palce you want people to live in?
"""
result = agent.analyze_audience_awareness(text, target_audience="general")
print(json.dumps(result, indent=2, ensure_ascii=False))