import re
import pandas as pd

def extract_feedback(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 提取 [[分数]]
    score_pattern1 = r'\[\[(\d+)\]\]'
    score_pattern2 = r'\[\[score\]\]: (\d+)'
    # 如果存在pattern1
    scores1 = re.findall(score_pattern1, content)
    if  scores1 != []:
        scores = int(scores1[0]) / 100.0
    else:
        scores = int(re.findall(score_pattern2, content)[0]) / 100.0

    # 提取两个 ------****** 之间的评语
    feedback_pattern = r'------\*{6}(.*?)------\*{6}'
    feedbacks = re.findall(feedback_pattern, content, re.DOTALL)

    return scores, feedbacks

all_essays = pd.read_csv("/Users/ylm/THU/code/AES_debate/data/ivypanda.csv")

# res 空dataframe保存结果
res = pd.DataFrame(columns=['essay_id', 'score', 'feedback'])
for index, row in all_essays.iterrows():
    essay_id = row['essay_id']
    filepath = '/Users/ylm/THU/code/AES_debate/output/ivypanda/rubric/chat_output_' + str(essay_id) + '.txt'
    # 提取分数和评语
    scores, feedbacks = extract_feedback(filepath)
    # scores, feedbacks 存入dataframe res
    new_row = pd.DataFrame({'essay_id': [essay_id], 'score': [scores], 'feedback': [feedbacks]})
    res = pd.concat([res, new_row], ignore_index=True)
    



# 输出结果
res.to_csv('/Users/ylm/THU/code/AES_debate/output/ivypanda/rubric/0.feedbacks.csv', sep='\t', index=False)