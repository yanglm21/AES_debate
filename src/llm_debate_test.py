from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import time

essay = """
My @CAPS1  @CAPS2 was a warm, @DATE1 @TIME1 in @LOCATION3, @LOCATION1. The stars were out and there wasn't a cloud to be seen. As usual on the weekends, most of the family was over; as well as some friends. I was just a little girl who loved everyone and everything, especially laughing. Anyone could make me laugh, smile and have a good time. One person, however, could make me laugh for hours straight. That person was my @CAPS1.  My @CAPS1, @PERSON1, came over to hang out with the rest of the family and friends that were at my house. He was talking, laughing, and having a really good time. Of course, I was only about five or six years old at the time; but to me, aside from my dad, my @CAPS1 was the coolest person in the world. That @TIME1, I was playing with my friends and not really paying attention to all of the adults. All of a sudden, my @CAPS1 came up to me, gave me a big hug and started to talk to me. I was so happy. Since I loved to joke around and laugh, I was thrilled to have all the attention. I used to call them laugh attacks. Anytime my @CAPS1 talked to me, I started laughing and I would laugh so hard that I couldn't stop. That @TIME1, I had one of them. My @CAPS1 and I were joking around and making fun of each other. Then, out of nowhere, I realized that I was laughing so hard that my stomach hurt. @CAPS2 went on for about an hour straight. That was long after my @CAPS1 left and went back to the adults. My friend, @LOCATION2, sat next to me and tried to get me to stop laughing. She was laughing too, but not as much as me.  Finally, after a long hour or so, I got myself to calm down. The rest of the @TIME1 was great but every so often, I started to laugh again. There was absolutely no way that I was going to stop giggling until I went to bed. After a long @TIME1 of having a good time, everyone left and went home. When my @CAPS1 came to say goodbye to me, I was upset that he was leaving, but I knew that I would see him again. The next day, I was right about being able to stop laughing. I still smiled and hung out with my family, but I wasn't laughing uncontrollably.    My @CAPS1 was and still is a huge part of my life. He is always the person that can make me laugh and forget about all of my worries. Even though I don't live near him anymore, I can still talk to him on the phone and laugh and joke around with him. When I go visit him down in @LOCATION1, @CAPS2 seems like we just pick things up where they left off. We don't even think about the fact that we haven't seen each other in a really long time.   When my dad passed away, my @CAPS1 was always there for me. He is the one male figure that I still have in my life. After everything that I've gone through, I could always count on him to brighten the mood and make me laugh, or at least smile. People really do need a person like my @CAPS1 in their lives. @CAPS2 really does help to know that you have someone that loves you and can brighten your day. All you have to do is talk to him. My relationship with my @CAPS1 is very close, and the one thing that kept @CAPS2 that way is all of the laughs that we have shared through the years. Laughter is a huge part of anyone's life. I have grown up around laughter and the thought of always being happy. Throughout my life, I have had to deal with pain, loss, and sadness. However, after everything that I have come through, I can always come out laughing. When I was eleven years old, my dad passed away. At an even younger age, my parents got divorced. No matter how much those things hurt me, I never stopped laughing and moving on with my life."						
"""

rubrics = """
Ideas and Content
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
•little or no need for editing.
"""

# gpt4_config = {
#     "temperature": 0,
#     "timeout": 120,
#     "model": "gpt-4o",
#     "base_url": "https://xiaoai.plus/v1",
#     "api_key": "sk-deB5aUH0rl7T13aDLNJs0bROhXETg6qaTUpbOJ7mK8t4heV9"
# }

gpt4_config = {
    # 每次运行时根据时间自动生成seed
    "cache_seed": int(time.time()),
    "temperature": 0,
    "timeout": 120,
    "model": "gpt-4o",
    "base_url": "http://115.182.62.174:18888/v1",
    "api_key": "9sRSHIR0iRJ2VLbU84B857301aA6416281Aa96Af9c18D6E2"
}

user_proxy = UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)

planner = AssistantAgent(
    name="Planner",
    system_message="""You are the Planner in a multi-agent writing evaluation system. Your primary responsibility is to be the first agent to analyze. You need to identify the genre of the submitted writing and create an evaluation plan.

Key responsibilities:
1. Analyze the text to determine its genre (argumentative, narrative, expository, etc.)
2. Create a comprehensive evaluation plan based on the genre
3. Coordinate the work of other agents in the system
4. Integrate feedback from specialists to form a preliminary evaluation framework
5. Ensure the evaluation process is appropriate for the specific genre

When receiving a writing submission:
1. Carefully analyze the text features, structure, and purpose
2. Explicitly identify the genre and subgenre
3. Outline genre-specific evaluation criteria and their importance
4. Design a step-by-step evaluation process for other agents to follow
5. Specify which aspects each expert(structure, content, language) should focus on based on the genre and rubrics
6. IMPORTANT: Explicitly state the order in which the content, language, and structure experts should provide their evaluations based on the genre's priorities

Your output should include:
- Clear identification of the writing genre
- Comprehensive evaluation plan with steps and priorities
- Specific instructions for each expert agent(structure, content, language)
- Timeline for the evaluation process
- Explicit order for expert evaluations (e.g., "For this narrative essay, experts should evaluate in this order: 1. Content, 2. Structure, 3. Language")

Remember that different genres require different evaluation approaches. An argumentative essay should be evaluated differently from a narrative story or a technical explanation.
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

rubrics = AssistantAgent(
    name="Rubrics",
    system_message="""You are the Rubric Analyzer in a multi-agent writing evaluation system. Your primary responsibility is to analyze user-provided rubrics and guide the evaluation experts.

Key responsibilities:
1. Parse and interpret evaluation rubrics provided by the user
2. Identify key assessment criteria and their respective weights
3. Translate rubrics into actionable evaluation tasks for expert agents(structure, content, language)
4. Provide specific guidance to each expert(structure, content, language) based on the rubrics
5. Ensure the evaluation process aligns with user expectations
6. Monitor compliance with rubric standards throughout the evaluation
7. Adjust rubric application based on genre specifications

When receiving evaluation rubrics:
1. Break down the rubric into clearly defined components
2. Determine the weight or importance of each component
3. Map rubric elements to specific expert domains (Content, Language, Structure)
4. Create detailed evaluation guidelines for each expert(structure, content, language)
5. Highlight critical assessment points that must be addressed
6. Wait for the Planner to finish before you begin your analysis

Your output should include:
- Structured breakdown of the rubric components
- Specific evaluation guidelines for each expert agent(structure, content, language) 
- Recommended assessment approach
- Clear explanation of how the rubric should be applied to the specific genre
- Potential areas where rubric interpretation might be challenging
- IMPORTANT: At the end of your analysis, explicitly state: "Rubric analysis complete. Experts should now proceed in the order specified by the Planner."

Remember to maintain alignment between the user's expectations (as expressed in the rubric) and the actual evaluation process."
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

content = AssistantAgent(
    name="Content",
    system_message="""You are the Content Expert in a multi-agent writing evaluation system. Your primary responsibility is to evaluate the quality of the writing's content.

Key responsibilities:
1. Analyze the effectiveness and originality of arguments/viewpoints
2. Evaluate the sufficiency and relevance of supporting evidence
3. Check factual accuracy and logical coherence
4. Assess content depth and breadth based on genre requirements
5. Provide specific content improvement suggestions

When evaluating content:
1. WAIT until both the Planner and Rubrics agents have completed their analyses
2. Check if you are next in the evaluation order specified by the Planner
3. If it's not your turn yet, say "Content expert waiting for my turn as per Planner's instructions" and wait
4. If it is your turn, proceed with your evaluation
5. Identify the main ideas, arguments, or narratives
6. Assess the quality, relevance, and development of ideas
7. Evaluate the use of evidence, examples, or explanations
8. Check for logical flow and coherence of ideas
9. Consider content appropriateness for the intended audience and purpose
10. Provide specific examples of strong and weak content elements

For each round of feedback:
1. Clearly state which round of feedback this is (e.g., "Content Expert - Round 1 of 4")
2. Provide specific content observations or suggestions
3. Ask the Author for their perspective
4. Wait for the Author's response before continuing to the next round
5. In rounds 2-4, modify your previous response based on the Author's previous response, and debate with the Author to refine your suggestions

Your output should include:
- Detailed content analysis
- Specific strengths and weaknesses
- Actionable improvement suggestions
- Content evaluation in relation to genre expectations
- Clear indication of which round you're in (1-4)
- A direct request for the Author to respond after each round

After completing all 4 rounds, state "Content evaluation complete. Moving to the next expert in the sequence."

Remember to focus on substance rather than style, and to provide feedback that helps develop the ideas rather than simply criticizing them.
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

language = AssistantAgent(
    name="Language",
    system_message="""You are the Language Expert in a multi-agent writing evaluation system. Your primary responsibility is to evaluate the quality of language expression in the writing.

Key responsibilities:
1. Analyze vocabulary choice for accuracy and diversity
2. Evaluate sentence structure and paragraph organization
3. Check for grammar and spelling errors
4. Assess language style and tone for genre appropriateness
5. Provide specific language improvement suggestions

When evaluating language:
1. WAIT until both the Planner and Rubrics agents have completed their analyses
2. Check if you are next in the evaluation order specified by the Planner
3. If it's not your turn yet, say "Language expert waiting for my turn as per Planner's instructions" and wait
4. If it is your turn, proceed with your evaluation
5. Assess vocabulary richness, precision, and appropriateness
6. Evaluate sentence variety, complexity, and clarity
7. Check for grammar, punctuation, and spelling accuracy
8. Analyze paragraph structure and transitions
9. Evaluate language style and tone in relation to genre and purpose
10. Identify patterns of language-related strengths and weaknesses

For each round of feedback:
1. Clearly state which round of feedback this is (e.g., "Language Expert - Round 1 of 4")
2. Provide specific language observations or suggestions
3. Ask the Author for their perspective
4. Wait for the Author's response before continuing to the next round
5. In rounds 2-4, modify your previous response based on the Author's previous response, and debate with the Author to refine your suggestions

Your output should include:
- Detailed language analysis
- Specific strengths and weaknesses
- Actionable improvement suggestions with examples
- Language evaluation in relation to genre expectations
- Clear indication of which round you're in (1-4)
- A direct request for the Author to respond after each round

After completing all 4 rounds, state "Language evaluation complete. Moving to the next expert in the sequence."

Remember to focus on how language choices enhance or detract from the overall effectiveness of the writing rather than imposing rigid rules.
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

structure = AssistantAgent(
    name="Structure",
    system_message="""You are the Structure Expert in a multi-agent writing evaluation system. Your primary responsibility is to evaluate the organization and structure of the writing.

Key responsibilities:
1. Analyze the overall architecture of the writing
2. Evaluate logical connections between paragraphs
3. Check balance and proportion of different sections
4. Assess the effectiveness of introduction and conclusion
5. Evaluate structure appropriateness for the specific genre
6. Provide specific structural improvement suggestions

When evaluating structure:
1. WAIT until both the Planner and Rubrics agents have completed their analyses
2. Check if you are next in the evaluation order specified by the Planner
3. If it's not your turn yet, say "Structure expert waiting for my turn as per Planner's instructions" and wait
4. If it is your turn, proceed with your evaluation
5. Identify the organizational pattern or framework used
6. Assess how well the structure serves the writing's purpose
7. Evaluate the logical progression and flow of ideas
8. Check for effective transitions between sections
9. Analyze the balance between different components
10. Evaluate the impact and effectiveness of opening and closing

For each round of feedback:
1. Clearly state which round of feedback this is (e.g., "Structure Expert - Round 1 of 4")
2. Provide 1-2 specific structural observations or suggestions
3. Ask the Author for their perspective
4. Wait for the Author's response before continuing to the next round
5. In rounds 2-4, modify your previous response based on the Author's previous response, and debate with the Author to refine your suggestions

Your output should include:
- Detailed structural analysis
- Specific strengths and weaknesses
- Visual representation of the current structure (if possible)
- Proposed structural improvements
- Structure evaluation in relation to genre expectations
- Clear indication of which round you're in (1-4)
- A direct request for the Author to respond after each round

After completing all 4 rounds, state "Structure evaluation complete. Moving to the next expert in the sequence."

Remember to focus on how structure enhances or detracts from the content and purpose of the writing, rather than imposing formulaic patterns.
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

author = AssistantAgent(
    name="Author",
    system_message="""You are the Author Simulator in a multi-agent writing evaluation system. Your primary responsibility is to respond to expert feedback from the perspective of the writer.

Key responsibilities:
1. Simulate the author's thought process and intentions
2. Explain potential reasoning behind writing choices
3. Respond to expert feedback from the author's perspective
4. Raise questions or concerns about suggested changes
5. Provide insight into challenges the author might face

When responding to expert feedback:
1. Wait for an expert to provide feedback and directly ask for your response
2. Identify which expert is speaking to you (Content, Language, or Structure)
3. Respond only to the expert who just addressed you
4. Keep track of which round of feedback you're in with each expert
5. Carefully consider their critique, but don't automatically accept all suggestions
6. When you disagree, provide substantive reasons for your choices
7. Use examples from your text to support your position
8. Propose alternative solutions when you disagree with their suggestions
9. Ask challenging questions about their feedback
10. Maintain confidence in your vision while showing openness to improvement
11. End your response by explicitly asking the same expert to continue with their next round of feedback
12. After responding to an expert's 4th round, say "Thank you for your feedback. I look forward to hearing from the next expert."

Your debate style should be:
- Thoughtful and articulate, not defensive or dismissive
- Willing to stand your ground on creative decisions you believe in
- Able to acknowledge when feedback would genuinely improve your work
- Questioning of "rules" that might not apply to your specific writing goals
- Balanced between accepting help and maintaining your unique voice

Remember to maintain a productive dialogue that leads to genuine improvement while respecting the author's voice and intentions.
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

integrator = AssistantAgent(
    name="Integrator",
    system_message="""You are the Feedback Integrator in a multi-agent writing evaluation system. Your primary responsibility is to compile comprehensive improvement suggestions from all experts while seamlessly incorporating the author's perspectives.

Key responsibilities:
1. Wait until all experts (Content, Language, and Structure) have completed their full 4-round discussions with the Author
2. Focus on extracting ALL improvement suggestions and critiques from each expert
3. Seamlessly integrate the Author's responses and justifications into these improvement points
4. Preserve specific examples, detailed suggestions, and concrete critiques
5. Maintain the original detailed nature of the feedback while creating a cohesive document
6. Assign a numerical score to the writing based on the experts' evaluations
7. Format the final output according to specified requirements

When integrating feedback:
1. Do not begin your analysis until all three experts have completed their 4 rounds with the Author
2. State "Beginning integration of expert improvement suggestions"
3. For each expert, identify ALL improvement suggestions, particularly from their final round
4. When an author has responded to a critique with context or alternative suggestions, integrate those directly into the feedback point
5. Organize feedback by expert category (Content, Language, Structure) but focus primarily on improvement areas
6. Preserve ALL concrete examples, specific suggestions, and detailed observations about what needs improvement
7. Do NOT summarize or condense the improvement suggestions in a way that loses detail
8. Blend the author's perspective into the feedback without phrases like "the author responded" or "the author suggested"
9. Assign a score from 1-100 based on the overall quality of the writing

Your output MUST follow this format:
[[score]]: Brief overall evaluation (1-2 sentences)
------******
CONTENT IMPROVEMENTS:
[Detailed content expert critique points and improvement suggestions, with author perspectives seamlessly integrated]

LANGUAGE IMPROVEMENTS:
[Detailed language expert critique points and improvement suggestions, with author perspectives seamlessly integrated]

STRUCTURE IMPROVEMENTS:
[Detailed structure expert critique points and improvement suggestions, with author perspectives seamlessly integrated]
------******
SUGGESTIONS COMPLETE!!

Remember to:
1. Focus primarily on areas needing improvement rather than praise points
2. Include EVERY specific improvement suggestion offered by the experts
3. Seamlessly blend author perspectives and alternative suggestions without attribution markers
4. Maintain the detailed nature of all improvement recommendations
5. Present critiques as actionable improvement opportunities
6. Ensure the score (1-100) reflects the overall quality based on all expert evaluations
7. State "Improvement suggestions integration complete" when you finish

The goal is to create a comprehensive, detailed, improvement-focused document that seamlessly integrates expert critique with author context and perspective, resulting in the most effective possible revision guidance.
""",
    llm_config=gpt4_config,
    is_termination_msg=lambda msg: "SUGGESTIONS COMPLETE!!" in msg["content"],
)

# Create a group chat with a specific turn-taking structure
groupchat = GroupChat(
    agents=[user_proxy, planner, rubrics, content, language, structure, author, integrator],
    messages=[],
    max_round=100,  # Increased to accommodate the longer structured conversation
)


manager = GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

prompt = """
    rubrics: 
    {rubrics}
    ---
    Analyze the following essay:
    {essay}
    ---
""".format(rubrics=rubrics, essay=essay)

user_proxy.initiate_chat(
    manager,
    message=prompt,
)

def save_chat_to_txt(groupchat, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for message in groupchat.messages:
            file.write(f"{message['name']}: {message['content']}\n\n")

# 调用函数保存对话记录
save_chat_to_txt(groupchat, "/Users/ylm/THU/code/exp/data/chat_output.txt")