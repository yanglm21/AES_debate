from openai import OpenAI
import pandas as pd
import tqdm
import time

def judge(essay, essay_id, review_a, review_b, review_c):
    client = OpenAI(api_key="sk-f14970f964474d029f90362666b66524", base_url="https://api.deepseek.com")

    prompt = """
    There is an essay and it received 3 different sets of feedback from 3 reviewers. I would like you to analyze and compare them to determine which one is more constructive, insightful, and helpful for improving the essay. Consider the following criteria in your evaluation:

    - The feedback aligns with author's original intention, and the advice is provided to enhance that intention.
    - The feedback fits the essay's genre and style.
    - Specificity: Feedback provides detailed examples to support suggestions.
    - Constructiveness: Feedback offers actionable steps (e.g., specific transitions, grammar fixes) for improvement.
    - Depth: Feedback explores counterarguments and rebuttals to create balanced arguments.
    
    
    Directly tell me review A or B or C is better, don't give me any other information.

    Essay: {essay}
    Review A: {review_a}
    Review B: {review_b}
    Review C: {review_c}

    Response Format:
    A or B or C
    """.format(essay=essay, review_a=review_a, review_b=review_b, review_c=review_c)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    filename = "/Users/maggieyang/Desktop/AES_debate/output/ivypanda/win/chat_output_" + str(essay_id) + ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

if __name__ == "__main__":
    all_essays = pd.read_csv("/Users/maggieyang/Desktop/AES_debate/data/ivypanda.csv")
    all_reviews_debate = pd.read_csv("/Users/maggieyang/Desktop/AES_debate/output/ivypanda/debate/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_baseline = pd.read_csv("/Users/maggieyang/Desktop/AES_debate/output/ivypanda/baseline/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_rubric = pd.read_csv("/Users/maggieyang/Desktop/AES_debate/output/ivypanda/rubric/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

    # all_reviews_debate = pd.read_csv("/Users/ylm/THU/code/AES_debate/output/ivypanda/debate/0.feedbacks.csv")
    # all_reviews_baseline = pd.read_csv("/Users/ylm/THU/code/AES_debate/output/ivypanda/baseline/0.feedbacks.csv")
    # all_reviews_rubric = pd.read_csv("/Users/ylm/THU/code/AES_debate/output/ivypanda/rubric/0.feedbacks.csv")

    errors = []
    import pdb
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        if row['essay_id'] >6:
            continue
        # 进度条
        try:
            judge(row["essay"], row["essay_id"], all_reviews_rubric.loc[index]["feedback"], all_reviews_baseline.loc[index]["feedback"], all_reviews_debate.loc[index]["feedback"])
        except Exception as e:
            errors.append([row["essay_id"], e])
            continue
