import llm_debate_new, llm_rubric, llm_baseline, llm_ma, prompt.all_rubrics
import tqdm 
import pandas as pd
import time

def debate_judge(all_essays, dataset_name, with_rubric=True):
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        print(f"Processing essay {row['essay_id']}")
        try:
            if with_rubric:
                r = prompt.all_rubrics.all_rubrics[row["essay_set"]]
            else:
                r = "No rubric"
            llm_debate_new.judge(row["essay"], r, f"{dataset_name}/debate/chat_output_{row['essay_id']}.txt")
        except Exception as e:
            # 处理异常
            print(f"Error processing essay {row['essay_id']}: {e}")
            continue


def rubric_judge(all_essays, dataset_name, with_rubric=True):
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        # 进度条
        
        print(f"Processing essay {row['essay_id']}")
        try:
            if with_rubric:
                r = prompt.all_rubrics.all_rubrics[row["essay_set"]]
            else:
                r = "No rubric"
            llm_rubric.judge(row["essay"], r, f"{dataset_name}/rubric/chat_output_{row['essay_id']}.txt")
        except Exception as e:
            continue

def baseline_judge(all_essays, dataset_name):
    
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        # 进度条
        print(f"Processing essay {row['essay_id']}")
        try:
            llm_baseline.judge(row["essay"], f"{dataset_name}/baseline/chat_output_{row['essay_id']}.txt")
        except Exception as e:
            continue

def ma_judge(all_essays, dataset_name):
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        # 进度条
        if dataset_name=="AES" and row['essay_id'] < 18292:
            continue
        print(f"Processing essay {row['essay_id']}")
        try:
            llm_ma.judge(row["essay"], f"{dataset_name}/ma/chat_output_{row['essay_id']}.txt")
        except Exception as e:
            continue

if __name__ == "__main__":
    all_essays = pd.read_csv("../data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')
    # debate_judge(all_essays, "AES")
    ma_judge(all_essays, "AES")

    ivypanda = pd.read_csv("../data/ivypanda.csv")
    # debate_judge(ivypanda, "ivypanda", with_rubric=False)
    ma_judge(ivypanda, "ivypanda")



