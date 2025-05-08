from openai import OpenAI
import pandas as pd
import tqdm
import time

def judge(essay, ref, ref_score, essay_id):
    client = OpenAI(
        base_url='https://xiaoai.plus/v1',
        # sk-xxx替换为自己的key
        api_key="sk-deB5aUH0rl7T13aDLNJs0bROhXETg6qaTUpbOJ7mK8t4heV9"
    )
    print(ref)
    prompt = """
        Assign a score from 1-100 based on the overall quality of the writing, and then provide feedback. Your feedback should focus on the the content, structure, and language of the essay. About 700 words in total.
        
        Essay: {essay}

        Reference essay (You are provided with a reference essay for your convenience. This is a {reference_score}): {reference_essay} 

        Your output MUST follow this format:
        [[score]]: Brief overall evaluation (1-2 sentences)
        ------
        CONTENT IMPROVEMENTS:
        [xxxx]

        LANGUAGE IMPROVEMENTS:
        [xxxx]

        STRUCTURE IMPROVEMENTS:
        [xxxx]
        ------
        """.format(essay=essay, reference_essay=ref, reference_score=ref_score)

    print(prompt)
    response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "text"}
        )
    filename = "/Users/ylm/THU/code/exp/data/llm_baseline/chat_output_" + str(essay_id) + ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

if __name__ == "__main__":
    all_essays = pd.read_csv("/Users/ylm/THU/code/exp/data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

    all_ref = {
        1:"""Dear local newspaper, I think effects computers have on people are great learning skills/affects because they give us time to chat with friends/new people, helps us learn about the globe(astronomy) and keeps us out of troble! Thing about! Dont you think so? How would you feel if your teenager is always on the phone with friends! Do you ever time to chat with your friends or buisness partner about things. Well now - there's a new way to chat the computer, theirs plenty of sites on the internet to do so: @ORGANIZATION1, @ORGANIZATION2, @CAPS1, facebook, myspace ect. Just think now while your setting up meeting with your boss on the computer, your teenager is having fun on the phone not rushing to get off cause you want to use it. How did you learn about other countrys/states outside of yours? Well I have by computer/internet, it's a new way to learn about what going on in our time! You might think your child spends a lot of time on the computer, but ask them so question about the economy, sea floor spreading or even about the @DATE1's you'll be surprise at how much he/she knows. Believe it or not the computer is much interesting then in class all day reading out of books. If your child is home on your computer or at a local library, it's better than being out with friends being fresh, or being perpressured to doing something they know isnt right. You might not know where your child is, @CAPS2 forbidde in a hospital bed because of a drive-by. Rather than your child on the computer learning, chatting or just playing games, safe and sound in your home or community place. Now I hope you have reached a point to understand and agree with me, because computers can have great effects on you or child because it gives us time to chat with friends/new people, helps us learn about the globe and believe or not keeps us out of troble. Thank you for listening.
        """
    }

    all_ref_score = {
        1: 67
    }

    errors = []
    import pdb
    for index, row in tqdm.tqdm(all_essays.iterrows(), total=len(all_essays), desc="Processing essays"):
        # 进度条
        try:
            ref = all_ref[row["essay_set"]]
            print("here:",ref)
            ref_score = all_ref_score[row["essay_set"]]
            judge(row["essay"], ref, ref_score, row["essay_id"])
        except Exception as e:
            errors.append([row["essay_id"], e])
            continue
        # save errors to a file
        with open("/Users/ylm/THU/code/exp/data/llm_debate/errors.txt", "w", encoding="utf-8") as file:
            for error in errors:
                file.write(f"{error[0]}: {error[1]}\n")

        time.sleep(5)