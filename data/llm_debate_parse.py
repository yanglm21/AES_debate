import re
import pandas as pd

def extract_feedback(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 提取 [[分数]]
    score_pattern = r'\[\[(\d+)\]\]'
    scores = re.findall(score_pattern, content)

    # 提取两个 ------****** 之间的评语
    feedback_pattern = r'------\*{6}(.*?)------\*{6}'
    feedbacks = re.findall(feedback_pattern, content, re.DOTALL)

    return scores, feedbacks

all_essays = pd.read_csv("/Users/ylm/THU/code/exp/data/random_essays_200.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

# res 空dataframe保存结果
res = pd.DataFrame(columns=['essay_id', 'score', 'feedback'])
for index, row in all_essays.iterrows():
    essay_id = row['essay_id']
    if essay_id > 1667:
        continue
    filepath = '/Users/ylm/THU/code/exp/data/llm_debate/chat_output_' + str(essay_id) + '.txt'
    # 提取分数和评语
    scores, feedbacks = extract_feedback(filepath)
    if scores == []:
        continue
    scores = float(scores[0])/100.0
    # scores, feedbacks 存入dataframe res
    new_row = pd.DataFrame({'essay_id': [essay_id], 'score': [scores], 'feedback': [feedbacks]})
    res = pd.concat([res, new_row], ignore_index=True)
    



# 输出结果
res.to_csv('/Users/ylm/THU/code/exp/data/llm_debate/feedbacks.csv', sep='\t')