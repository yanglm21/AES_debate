from openai import OpenAI
import pandas as pd
import tqdm
import time
import api_config

def judge(essay, filename="baseline/chat_output.txt"):
    client = OpenAI(
    base_url = "https://api.deepseek.com",
    api_key = "sk-f14970f964474d029f90362666b66524")
    
    prompt = """
        Assign a score from 1-100 based on the overall quality of the writing, and then provide feedback. Your feedback should focus on the the content, structure, and language of the essay. About 500 words in total.
        
        Essay: {essay}

        Language: 
            - Assess language style and tone for genre appropriateness
            - Provide specific language improvement suggestions, but do not go into too much detail
            - Your response should be informative yet concise, no more than 200 words for each round
            - Don't focus on technical jargon and format standards too much. Your focus should be on language itself.

        Content:
            - Assess content depth and breadth based on genre requirements
            - Provide specific content improvement suggestions, but do not go into too much detail
            - Your response should be informative yet concise, no more than 200 words for each round
            - Don't focus on technical jargon and format standards too much. Your focus should be on the content itself.

        Structure:
            - Analyze the overall architecture of the writing
            - Evaluate logical connections between paragraphs
            - Evaluate structure appropriateness for the specific genre
            - Provide specific structural improvement suggestions, but do not go into too much detail
            - Your response should be informative yet concise, no more than 200 words for each round
            - Don't focus on technical jargon and format standards too much. Your focus should be on the structure itself.


        Your output MUST STRICTLY follow this format:
        [[score]]: Brief overall evaluation (1-2 sentences)
        ------
        CONTENT IMPROVEMENTS:
        [xxxx]

        LANGUAGE IMPROVEMENTS:
        [xxxx]

        STRUCTURE IMPROVEMENTS:
        [xxxx]
        ------
        """.format(essay=essay)

    response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "text"}
        )
    filename = f"../output/{filename}"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.choices[0].message.content)

if __name__ == "__main__":
    essay = """
    My @CAPS1  @CAPS2 was a warm, @DATE1 @TIME1 in @LOCATION3, @LOCATION1. The stars were out and there wasn't a cloud to be seen. As usual on the weekends, most of the family was over; as well as some friends. I was just a little girl who loved everyone and everything, especially laughing. Anyone could make me laugh, smile and have a good time. One person, however, could make me laugh for hours straight. That person was my @CAPS1.  My @CAPS1, @PERSON1, came over to hang out with the rest of the family and friends that were at my house. He was talking, laughing, and having a really good time. Of course, I was only about five or six years old at the time; but to me, aside from my dad, my @CAPS1 was the coolest person in the world. That @TIME1, I was playing with my friends and not really paying attention to all of the adults. All of a sudden, my @CAPS1 came up to me, gave me a big hug and started to talk to me. I was so happy. Since I loved to joke around and laugh, I was thrilled to have all the attention. I used to call them laugh attacks. Anytime my @CAPS1 talked to me, I started laughing and I would laugh so hard that I couldn't stop. That @TIME1, I had one of them. My @CAPS1 and I were joking around and making fun of each other. Then, out of nowhere, I realized that I was laughing so hard that my stomach hurt. @CAPS2 went on for about an hour straight. That was long after my @CAPS1 left and went back to the adults. My friend, @LOCATION2, sat next to me and tried to get me to stop laughing. She was laughing too, but not as much as me.  Finally, after a long hour or so, I got myself to calm down. The rest of the @TIME1 was great but every so often, I started to laugh again. There was absolutely no way that I was going to stop giggling until I went to bed. After a long @TIME1 of having a good time, everyone left and went home. When my @CAPS1 came to say goodbye to me, I was upset that he was leaving, but I knew that I would see him again. The next day, I was right about being able to stop laughing. I still smiled and hung out with my family, but I wasn't laughing uncontrollably.    My @CAPS1 was and still is a huge part of my life. He is always the person that can make me laugh and forget about all of my worries. Even though I don't live near him anymore, I can still talk to him on the phone and laugh and joke around with him. When I go visit him down in @LOCATION1, @CAPS2 seems like we just pick things up where they left off. We don't even think about the fact that we haven't seen each other in a really long time.   When my dad passed away, my @CAPS1 was always there for me. He is the one male figure that I still have in my life. After everything that I've gone through, I could always count on him to brighten the mood and make me laugh, or at least smile. People really do need a person like my @CAPS1 in their lives. @CAPS2 really does help to know that you have someone that loves you and can brighten your day. All you have to do is talk to him. My relationship with my @CAPS1 is very close, and the one thing that kept @CAPS2 that way is all of the laughs that we have shared through the years. Laughter is a huge part of anyone's life. I have grown up around laughter and the thought of always being happy. Throughout my life, I have had to deal with pain, loss, and sadness. However, after everything that I have come through, I can always come out laughing. When I was eleven years old, my dad passed away. At an even younger age, my parents got divorced. No matter how much those things hurt me, I never stopped laughing and moving on with my life."						
    """
    r = """
Ideas and Content
The writing is exceptionally clear, focused, and interesting. It holds the reader's attention throughout. Main ideas stand out and are developed by strong support and rich details suitable to audience and purpose. The writing is characterized by
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
•little or no need for editing.
"""
    judge(essay)