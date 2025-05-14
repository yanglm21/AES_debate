from openai import OpenAI
import pandas as pd
import tqdm
import time

def judge(essay, essay_id, dataset_name, review_a, review_b, review_c):
    client = OpenAI(api_key="sk-f14970f964474d029f90362666b66524", base_url="https://api.deepseek.com")

    prompt = """
    There is an essay and it received 3 different sets of feedback from 3 reviewers. 
    I would like you to analyze and compare them to determine which one is more constructive, insightful, and helpful for improving the essay. 
    Consider the following criteria in your evaluation, and then rate the reviews based on these criteria:

    1. Intention: The feedback aligns with author's original intention of composing the essay, and the advice is provided to enhance that intention.(rate from 1 to 10)
    2. Genre: The feedback fits the essay's genre and style.(rate from 1 to 10)
    3. Contradiction: There are no contradictions between each category of feedback.(rate from 1 to 10, a higher score means less contradiction)
    3. Specificity: Feedback provides detailed examples to support suggestions.(rate from 1 to 10)
    4. Constructiveness: Feedback offers actionable steps (e.g., specific transitions, grammar fixes) for improvement.(rate from 1 to 10)
    5. Depth: Feedback explores counterarguments and rebuttals to create balanced arguments.(rate from 1 to 10)
    
    
    Your answer should be in json and follow this format:
    {{
        "reviews": {{
            "A": {{
                "Intention": score,
                "Genre": score,
                "Contradiction": score,
                "Specificity": score,
                "Constructiveness": score,
                "Depth": score
            }},
            "B": {{...}},
            "C": {{...}}
        }},
        "best_review": "A/B/C"
    }}

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
        response_format={"type": "json_object"},
        stream=False
    )
    filename = f"../output/{dataset_name}/win/chat_output_" + str(essay_id) + ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

if __name__ == "__main__":
    dataset_name = "ivypanda"
    if dataset_name == "AES":
        all_essays = pd.read_csv("../data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    else:
        all_essays = pd.read_csv("../data/ivypanda.csv")
    all_reviews_debate = pd.read_csv(f"../output/{dataset_name}/debate/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_baseline = pd.read_csv(f"../output/{dataset_name}/baseline/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_rubric = pd.read_csv(f"../output/{dataset_name}/rubric/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    all_reviews_ma = pd.read_csv(f"../output/{dataset_name}/ma/0.feedbacks.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

    errors = []
    import pdb
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        # 进度条
        # try:
        if dataset_name == "AES":
            judge(row["essay"], row["essay_id"], dataset_name, all_reviews_rubric.loc[index]["feedback"], all_reviews_ma.loc[index]["feedback"], all_reviews_debate.loc[index]["feedback"])
        else:
            judge(row["essay"], row["essay_id"], dataset_name, all_reviews_baseline.loc[index]["feedback"], all_reviews_ma.loc[index]["feedback"], all_reviews_debate.loc[index]["feedback"])
        # except Exception as e:
        #     errors.append([row["essay_id"], e])
        #     continue
