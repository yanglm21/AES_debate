from openai import OpenAI
import pandas as pd
import tqdm
import time

def judge(essay, r, ref, ref_score, essay_id):
    client = OpenAI(
        base_url='https://xiaoai.plus/v1',
        # sk-xxx替换为自己的key
        api_key="sk-deB5aUH0rl7T13aDLNJs0bROhXETg6qaTUpbOJ7mK8t4heV9"
    )

    prompt = """
        Assign a score from 1-100 based on the overall quality of the writing, and then provide feedback. Your feedback should focus on the the content, structure, and language of the essay. About 700 words in total.
        
        Essay: {essay}

        Rubrics: {r}

        Reference essay (You are provided with a reference essay for your convenience. This is a {reference_score}): {reference_essay} 

        Your output MUST follow this format:
        [[score]]: Brief overall evaluation (1-2 sentences)
        ------******
        CONTENT IMPROVEMENTS:
        [xxxx]

        LANGUAGE IMPROVEMENTS:
        [xxxx]

        STRUCTURE IMPROVEMENTS:
        [xxxx]
        ------******
        """.format(essay=essay, r=r, reference_score=ref_score, reference_essay=ref)

    response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "text"}
        )
    filename = "/Users/ylm/THU/code/exp/data/llm_rubric/chat_output_" + str(essay_id) + ".txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

if __name__ == "__main__":
    all_essays = pd.read_csv("/Users/ylm/THU/code/exp/data/random_essays_50.csv", sep='\t', encoding='utf-8', on_bad_lines='skip')

    all_rubrics = {
    1: """prompt & rubrics:
    More and more people use computers, but not everyone agrees that this benefits society. Those who support advances in technology believe that computers have a positive effect on people. They teach hand-eye coordination, give people the ability to learn about faraway places and people, and even allow people to talk online with other people. Others have different ideas. Some experts are concerned that people are spending too much time on their computers and less time exercising, enjoying nature, and interacting with family and friends. 
    Write a letter to your local newspaper in which you state your opinion on the effects computers have on people. Persuade the readers to agree with you.
    
    A well-developed response that takes a clear and thoughtful position and provides persuasive support. Typical elements:
    Has fully elaborated reasons with specific details.
    Exhibits strong organization.
    Is fluent and uses sophisticated transitional language.
    May show a heightened awareness of audience.""",

    2: """prompt & rubrics:
    Censorship in the Libraries
    "All of us can think of a book that we hope none of our children or any other children have taken off the shelf. But if I have the right to remove that book from the shelf -- that work I abhor -- then you also have exactly the same right and so does everyone else. And then we have no books left on the shelf for any of us." --Katherine Paterson, Author
    Write a persuasive essay to a newspaper reflecting your vies on censorship in libraries. Do you believe that certain materials, such as books, music, movies, magazines, etc., should be removed from the shelves if they are found offensive? Support your position with convincing arguments from your own experience, observations, and/or reading.

    Ideas and Content
    Does the writing sample fully accomplish the task (e.g., support an opinion, summarize, tell a story, or write an article)? Does it
    •present a unifying theme or main idea without going off on tangents?
    •stay completely focused on topic and task?
    Does the writing sample include thorough, relevant, and complete ideas? Does it
    •include in-depth information and exceptional supporting details that are fully developed?
    •fully explore many facets of the topic?

    Organization
    Are the ideas in the writing sample organized logically? Does the writing
    •present a meaningful, cohesive whole with a beginning, a middle, and an end (i.e., include an inviting introduction and a strong conclusion)?
    •progress in an order that enhances meaning?
    •include smooth transitions between ideas, sentences, and paragraphs to enhance meaning of text (i.e., have a clear connection of ideas and use topic sentences)?
    
    Style
    Does the writing sample exhibit exceptional word usage? Does it
    •include vocabulary to make explanations detailed and precise, descriptions rich, and actions clear and vivid (e.g., varied word choices, action words, appropriate modifiers, sensory details)?
    •demonstrate control of a challenging vocabulary?
    Does the writing sample demonstrate exceptional writing technique?
    •Is the writing exceptionally fluent?
    •Does it include varied sentence patterns, including complex sentences?
    •Does it demonstrate use of writer's techniques (e.g., literary conventions such as imagery and dialogue and/or literary genres such as humor and suspense)?
    
    Voice
    Does the writing sample demonstrate effective adjustment of language and tone to task and reader? Does it
    •exhibit appropriate register (e.g., formal, personal, or dialect) to suit task?
    •demonstrate a strong sense of audience?
    exhibit an original perspective (e.g., authoritative, lively, and/or exciting)?
    """,

    7: """prompt & rubrics:
    Write about patience. Being patient means that you are understanding and tolerant. A patient person experience difficulties without complaining.
    Do only one of the following: write a story about a time when you were patient OR write a story about a time when someone you know was patient OR write a story in your own way about patience.

    Ideas
    Tells a story with ideas that are clearly focused on the topic and are thoroughly developed with specific, relevant details.

    Organization
    Organization and connections between ideas and/or events are clear and logically sequenced. 
    
    Style
    Command of language, including effective and compelling word choice and varied sentence structure, clearly supports the writer's purpose and audience.
    
    Conventions
    Consistent, appropriate use of conventions of Standard English for grammar, usage, spelling, capitalization, and punctuation for the grade level.
    """,

    8: """Ideas and Content
    The writing is exceptionally clear, focused, and interesting. It holds the reader’s attention throughout. Main ideas stand out and are developed by strong support and rich details suitable to audience and purpose. The writing is characterized by
    •clarity, focus, and control.
    •main idea(s) that stand out.
    •supporting, relevant, carefully selected details; when appropriate, use of resources provides strong, accurate, credible support.
    •a thorough, balanced, in-depth explanation / exploration of the topic; the writing makes connections and shares insights.
    content and selected details that are well-suited to audience and purpose.

    Organization
    The organization enhances the central idea(s) and its development. The order and structure are compelling and move the reader through the text easily. The writing is characterized by
    •effective, perhaps creative, sequencing and paragraph breaks; the organizational structure fits the topic, and the writing is easy to follow.
    •a strong, inviting beginning that draws the reader in and a strong, satisfying sense of resolution or closure.
    •smooth, effective transitions among all elements (sentences, paragraphs, ideas).
    •details that fit where placed.

    Voice
    The writer has chosen a voice appropriate for the topic, purpose, and audience. The writer demonstrates deep commitment to the topic, and there is an exceptional sense of “writing to be read.” The writing is expressive, engaging, or sincere. The writing is characterized by
    •an effective level of closeness to or distance from the audience (e.g., a narrative should have a strong personal voice, while an expository piece may require extensive use of outside resources and a more academic voice; nevertheless, both should be engaging, lively, or interesting. Technical writing may require greater distance.).
    •an exceptionally strong sense of audience; the writer seems to be aware of the reader and of how to communicate the message most effectively. The reader may discern the writer behind the words and feel a sense of interaction.
    a sense that the topic has come to life; when appropriate, the writing may show originality, liveliness, honesty, conviction, excitement, humor, or suspense.

    Word Choice
    Words convey the intended message in an exceptionally interesting, precise, and natural way appropriate to audience and purpose. The writer employs a rich, broad range of words which have been carefully chosen and thoughtfully placed for impact. The writing is characterized by
    •accurate, strong, specific words; powerful words energize the writing.
    •fresh, original expression; slang, if used, seems purposeful and is effective.
    •vocabulary that is striking and varied, but that is natural and not overdone.
    •ordinary words used in an unusual way.
    words that evoke strong images; figurative language may be used.

    Sentence Fluency
    The writing has an effective flow and rhythm. Sentences show a high degree of craftsmanship, with consistently strong and varied structure that makes expressive oral reading easy and enjoyable. The writing is characterized by
    •a natural, fluent sound; it glides along with one sentence flowing effortlessly into the next.
    •extensive variation in sentence structure, length, and beginnings that add interest to the text.
    •sentence structure that enhances meaning by drawing attention to key ideas or reinforcing relationships among ideas.
    •varied sentence patterns that create an effective combination of power and grace.
    •strong control over sentence structure; fragments, if used at all, work well.
    •stylistic control; dialogue, if used, sounds natural.

    Conventions
    The writing demonstrates exceptionally strong control of standard writing conventions (e.g., punctuation, spelling, capitalization, grammar and usage) and uses them effectively to enhance communication. Errors are so few and so minor that the reader can easily skim right over them unless specifically searching for them. The writing is characterized by
    •strong control of conventions; manipulation of conventions may occur for stylistic effect.
    •strong, effective use of punctuation that guides the reader through the text.
    •correct spelling, even of more difficult words.
    •correct grammar and usage that contribute to clarity and style.
    •skill in using a wide range of conventions in a sufficiently long and complex piece.
    •little or no need for editing."
    """
    }

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
            r = all_rubrics[row["essay_set"]]
            ref = all_ref[row["essay_set"]]
            ref_score = all_ref_score[row["essay_set"]]
            judge(row["essay"], r, ref, ref_score, row["essay_id"])
        except Exception as e:
            errors.append([row["essay_id"], e])
            continue
        # save errors to a file
        with open("/Users/ylm/THU/code/exp/data/llm_debate/errors.txt", "w", encoding="utf-8") as file:
            for error in errors:
                file.write(f"{error[0]}: {error[1]}\n")

        time.sleep(5)