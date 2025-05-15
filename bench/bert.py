from transformers import pipeline
from transformers import BertTokenizer
import pandas as pd
import tqdm

pipe = pipeline("text-classification", model="raoel/bert-finetuned-ASAP-AEStask")

tokenizer = BertTokenizer.from_pretrained("raoel/bert-finetuned-ASAP-AEStask")

def truncate_text(text, max_length=508):
    tokens = tokenizer.tokenize(text)
    if len(tokens) > max_length:
        tokens = tokens[:max_length]  # 直接截断前512个token
    return tokenizer.convert_tokens_to_string(tokens)  # 重新组合为文本

# 定义计算作文分数的函数
def calculate_essay_score(text, pipe):
    """
    使用 pipeline 计算作文分数
    :param text: 作文文本
    :param pipe: 加载的 pipeline 对象
    :return: 作文分数
    """
    truncated_text = truncate_text(text)  # 截断超长文本
    features = pipe(truncated_text)  # 处理截断后的文本
    # inputs = tokenizer(text, truncation=True, max_length=512, return_tensors="tf")
    # features = pipe(**inputs)
    return features[0]["score"]

# 读取数据
all_candidates = pd.read_csv("../data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

# 初始化结果列表
results = []

# 遍历 DataFrame 计算作文分数
for index, row in tqdm.tqdm(all_candidates.iterrows(), total=len(all_candidates), desc="Processing essays"):

# for index, row in all_candidates.iterrows():
    essay_id = row["essay_id"]
    candidate_text = row["essay"]
    # 计算分数
    score = calculate_essay_score(candidate_text, pipe)
    
    # 存储结果
    results.append({
        "essay_id": essay_id,
        "bert_finetuned_score": round(score, 3)
    })

# 转换为 DataFrame
finetuned_df = pd.DataFrame(results)

# 保存结果
finetuned_df.to_csv("../data/bert_scores.csv", sep='\t', index=False)

