from nltk import ngrams, word_tokenize
import pandas as pd

# 候选作文（学生作文原文，保留所有占位符和错误）
all_candidates = pd.read_csv("../data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

def calculate_distinct(tokens, max_n=4):
    """
    计算DISTINCT-1/2/4
    :param tokens: 分词后的词列表（如 ['I', 'love', 'NLP']）
    :param max_n: 最大n-gram长度（默认为4）
    :return: 字典 {distinct_1, distinct_2, distinct_4}
    """
    distinct_scores = {}
    for n in [1, 2, 4]:
        if n > max_n:
            distinct_scores[f"distinct_{n}"] = 0.0
            continue
        # 生成n-gram并统计唯一数
        n_grams = list(ngrams(tokens, n))
        unique_ngrams = set(n_grams)
        total = len(n_grams)
        # 避免除以零错误
        score = len(unique_ngrams) / total if total > 0 else 0.0
        distinct_scores[f"distinct_{n}"] = round(score, 4)
    return distinct_scores

# 初始化结果列表
results = []

for index, row in all_candidates.iterrows():
    essay_id = row["essay_id"]
    candidate_text = row["essay"]
    
    # 分词处理（保留大小写）
    tokens = word_tokenize(candidate_text)
    
    # 计算DISTINCT分数
    distinct = calculate_distinct(tokens)
    
    # 合并结果
    results.append({
        "essay_id": essay_id,
        **distinct
    })

# 转换为DataFrame
distinct_df = pd.DataFrame(results)

# 按需设置列顺序
final_df = distinct_df[["essay_id", "distinct_1", "distinct_2", "distinct_4"]]
final_df["distinct_1"] = final_df["distinct_1"].round(3)
final_df["distinct_2"] = final_df["distinct_2"].round(3)
final_df["distinct_4"] = final_df["distinct_4"].round(3)

# 保存结果
final_df.to_csv("../data/distinct_scores.csv", sep='\t', index=False)