from transformers import pipeline
import pandas as pd
import tqdm

pipe = pipeline("text-classification", model="raoel/bert-finetuned-ASAP-AEStask")

# 定义计算作文分数的函数
def calculate_essay_score(text, pipe):
    """
    使用 pipeline 计算作文分数
    :param text: 作文文本
    :param pipe: 加载的 pipeline 对象
    :return: 作文分数
    """
    # 使用 pipeline 提取特征
    features = pipe(text)
    # 假设分数是特征向量的均值（根据任务需求调整）
    score = features[0]['score']  # 取第一个 token 的特征均值
    return score

# 读取数据
all_candidates = pd.read_csv("/Users/ylm/THU/code/exp/data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

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
        "bert_finetuned_score": score
    })

# 转换为 DataFrame
finetuned_df = pd.DataFrame(results)

# 保存结果
finetuned_df.to_csv("/Users/ylm/THU/code/exp/data/bert_scores.csv", sep='\t', index=False)

