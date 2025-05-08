import os
import json
import spacy
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class FluencyAgent:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def analyze_fluency(self, text):
        """主分析函数"""
        # Step 1: 提取文本特征
        features = self._extract_text_features(text)
        
        # Step 2: 调用GPT-4进行流畅性分析
        fluency_analysis = self._llm_fluency_analysis(text)
                
        return {
            "detailed_analysis": fluency_analysis,
            "text_features": features
        }
    
    def _extract_text_features(self, text):
        """使用spaCy提取文本特征"""
        doc = self.nlp(text)
        features = {
            "avg_sentence_length": sum(len(sent) for sent in doc.sents) / len(list(doc.sents)),
            "num_sentences": len(list(doc.sents)),
            "num_words": len(doc),
            "num_errors": self._count_grammar_errors(doc),
            "transition_words": self._count_transition_words(doc),
            "passive_voice": sum(1 for sent in doc.sents if any(tok.dep_ == "nsubjpass" for tok in sent))
        }
        return features
    
    def _count_grammar_errors(self, doc):
        """检测常见语法错误"""
        errors = 0
        for sent in doc.sents:
            # 检测主谓一致错误
            subjects = [tok for tok in sent if tok.dep_ in ["nsubj", "nsubjpass"]]
            verbs = [tok for tok in sent if tok.dep_ in ["ROOT", "aux", "auxpass"]]
            for subj in subjects:
                for verb in verbs:
                    if subj.head == verb and subj.tag_ != verb.tag_:
                        errors += 1
        return errors
    
    def _count_transition_words(self, doc):
        """统计过渡词数量"""
        transition_words = ["however", "therefore", "moreover", "furthermore", "in addition"]
        return sum(1 for token in doc if token.text.lower() in transition_words)
    
    def _llm_fluency_analysis(self, text):
        """调用GPT-4进行流畅性分析"""
        prompt = f"""
        你是一个专业的文本分析系统，请根据以下要求分析文本的流畅性：
        1. **句法复杂性**：句子结构是否多样且合理
        2. **连贯性**：段落间是否有清晰的逻辑过渡
        3. **语言错误**：是否存在语法、拼写或用词不当问题
        4. **输出格式**：必须使用 JSON 格式，结构如下：
           {{
             "syntax_analysis": "句法复杂性分析结果",
             "cohesion_analysis": "连贯性分析结果",
             "error_analysis": "语言错误分析结果",
             "fluency_score": 0-10  // 流畅性评分
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
    
# 使用示例
agent = FluencyAgent()
text = """
Dear @ORGANIZATION1, The computer blinked to life and an image of a blonde haired girl filled the screen. It was easy to find out how life was in @LOCATION2, thanks to the actual @CAPS1 girl explaining it. Going to the library wouldn't have filled one with this priceless information and human interection. Computers are a nessessity of life if soceity wishes to grow and expand. They should be supported because they teach hand eye coordination, give people the ability to learn about faraway places, and allow people to talk to others online.
"""
result = agent.analyze_fluency(text)
print(json.dumps(result, indent=2, ensure_ascii=False))