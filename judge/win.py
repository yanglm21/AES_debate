from openai import OpenAI
import pandas as pd
import tqdm
import time

def judge(essay, essay_id, review_a, review_b):
    client = OpenAI(api_key="sk-f14970f964474d029f90362666b66524", base_url="https://api.deepseek.com")

    prompt = """
    There is an essay and it received two different sets of feedback from two reviewers. I would like you to analyze and compare the two sets of feedback to determine which one is more constructive, insightful, and helpful for improving the essay. Consider the following criteria in your evaluation:

    1. Specificity: Feedback provides detailed examples (e.g., studies, platforms) to support suggestions.
    2. Constructiveness: Feedback offers actionable steps (e.g., specific transitions, grammar fixes) for improvement.
    3. Depth: Feedback explores counterarguments and rebuttals to create balanced arguments.
    
    Don't show me any reason. Directly tell me review A or B is better.

    Essay: {essay}
    Review A: {review_a}
    Review B: {review_b}

    Response Format:
    A or B
    """.format(essay=essay, review_a=review_a, review_b=review_b)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    filename = "/Users/ylm/THU/code/exp/data/win/rubric_vs_baseline/chat_output_" + str(essay_id) + ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

if __name__ == "__main__":
    all_essays = pd.read_csv("/Users/ylm/THU/code/exp/data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_debate = pd.read_csv("/Users/ylm/THU/code/exp/data/llm_debate/feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_baseline = pd.read_csv("/Users/ylm/THU/code/exp/data/llm_baseline/feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_rubric = pd.read_csv("/Users/ylm/THU/code/exp/data/llm_rubric/feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

    errors = []
    import pdb
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        # 进度条
        try:
            judge(row["essay"], row["essay_id"], all_reviews_rubric.loc[index]["feedback"], all_reviews_baseline.loc[index]["feedback"])
        except Exception as e:
            errors.append([row["essay_id"], e])
            continue
        # save errors to a file
        with open("/Users/ylm/THU/code/exp/data/win/errors.txt", "w", encoding="utf-8") as file:
            for error in errors:
                file.write(f"{error[0]}: {error[1]}\n")
