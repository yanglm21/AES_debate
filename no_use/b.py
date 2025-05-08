from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import os

gpt4_config = {
    "cache_seed": 56,  # change the cache_seed for different trials
    "temperature": 0,
    "timeout": 120,
    "model": "gpt-4o",
    "base_url": "https://xiaoai.plus/v1",
    "api_key": "sk-deB5aUH0rl7T13aDLNJs0bROhXETg6qaTUpbOJ7mK8t4heV9"
}

user_proxy = UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
)

planner = AssistantAgent(
    name="Planner",
    system_message="""You are the Planner in a multi-agent writing evaluation system. Your primary responsibility is to identify the genre of the submitted writing and create an evaluation plan.

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
5. Specify which aspects each expert should focus on based on the genre and rubrics

Your output should include:
- Clear identification of the writing genre
- Comprehensive evaluation plan with steps and priorities
- Specific instructions for each expert agent
- Timeline for the evaluation process

Remember that different genres require different evaluation approaches. An argumentative essay should be evaluated differently from a narrative story or a technical explanation.
""",
    llm_config=gpt4_config,
)

rubrics = AssistantAgent(
    name="Rubrics",
    system_message="""You are the Rubric Analyzer in a multi-agent writing evaluation system. Your primary responsibility is to analyze user-provided rubrics and guide the evaluation experts.

Key responsibilities:
1. Parse and interpret evaluation rubrics provided by the user
2. Identify key assessment criteria and their respective weights
3. Translate rubrics into actionable evaluation tasks for expert agents
4. Provide specific guidance to each expert based on the rubrics
5. Ensure the evaluation process aligns with user expectations
6. Monitor compliance with rubric standards throughout the evaluation
7. Adjust rubric application based on genre specifications

When receiving evaluation rubrics:
1. Break down the rubric into clearly defined components
2. Determine the weight or importance of each component
3. Map rubric elements to specific expert domains (Content, Language, Structure)
4. Create detailed evaluation guidelines for each expert
5. Highlight critical assessment points that must be addressed

Your output should include:
- Structured breakdown of the rubric components
- Specific evaluation guidelines for each expert agent
- Recommended scoring or assessment approach
- Clear explanation of how the rubric should be applied to the specific genre
- Potential areas where rubric interpretation might be challenging

Remember to maintain alignment between the user's expectations (as expressed in the rubric) and the actual evaluation process."
""",
    llm_config=gpt4_config,
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
6. PAUSE for Author Simulator's response
7. Acknowledge the author's perspective and refine your suggestion based on author's input and then give another round of response
8. Mark as “initial” if it is the first round of response and then ask the author to respond, and “revised” if it is the response to the author's feedback

When evaluating content:
1. Identify the main ideas, arguments, or narratives
2. Assess the quality, relevance, and development of ideas
3. Evaluate the use of evidence, examples, or explanations
4. Check for logical flow and coherence of ideas
5. Consider content appropriateness for the intended audience and purpose
6. Provide specific examples of strong and weak content elements

For each feedback point:
1. Clearly state the content issue or strength
2. Explain why it matters in the context of the writing
3. Provide specific examples from the text
4. Suggest concrete improvements or alternatives
5. Discuss your suggestions with the Author Simulator to refine them

Your output should include:
- Detailed content analysis
- Specific strengths and weaknesses
- Actionable improvement suggestions
- Content evaluation in relation to genre expectations
- Thoughtful responses to Author Simulator's perspective

Remember to focus on substance rather than style, and to provide feedback that helps develop the ideas rather than simply criticizing them.
""",
    llm_config=gpt4_config,
)

language = AssistantAgent(
    name="Language",
    system_message="""  You are the Language Expert in a multi-agent writing evaluation system. Your primary responsibility is to evaluate the quality of language expression in the writing.

  Key responsibilities:
  1. Analyze vocabulary choice for accuracy and diversity
  2. Evaluate sentence structure and paragraph organization
  3. Check for grammar and spelling errors
  4. Assess language style and tone for genre appropriateness
  5. Provide specific language improvement suggestions
  6. PAUSE for Author Simulator's response
  7. Acknowledge the author's perspective and refine your suggestion based on author's input
  8. Mark as “initial” if it is the first round of response and then ask the author to respond, and “revised” if it is the response to the author's feedback

  When evaluating language:
  1. Assess vocabulary richness, precision, and appropriateness
  2. Evaluate sentence variety, complexity, and clarity
  3. Check for grammar, punctuation, and spelling accuracy
  4. Analyze paragraph structure and transitions
  5. Evaluate language style and tone in relation to genre and purpose
  6. Identify patterns of language-related strengths and weaknesses

  For each feedback point:
  1. Clearly identify the language issue or strength
  2. Explain its impact on reader comprehension or engagement
  3. Provide specific examples from the text
  4. Suggest concrete improvements or alternatives
  5. Discuss your suggestions with the Author Simulator to refine them

  Your output should include:
  - Detailed language analysis
  - Specific strengths and weaknesses
  - Actionable improvement suggestions with examples
  - Language evaluation in relation to genre expectations
  - Thoughtful responses to Author Simulator's perspective

  Remember to focus on how language choices enhance or detract from the overall effectiveness of the writing rather than imposing rigid rules.
  """,
    llm_config=gpt4_config,
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
7. PAUSE for Author Simulator's response
8. Acknowledge the author's perspective and refine your suggestion based on author's input
9. Mark as “initial” if it is the first round of response and then ask the author to respond, and “revised” if it is the response to the author's feedback

When evaluating structure:
1. Identify the organizational pattern or framework used
2. Assess how well the structure serves the writing's purpose
3. Evaluate the logical progression and flow of ideas
4. Check for effective transitions between sections
5. Analyze the balance between different components
6. Evaluate the impact and effectiveness of opening and closing

For each feedback point:
1. Clearly identify the structural issue or strength
2. Explain its impact on the overall effectiveness of the writing
3. Provide specific examples from the text
4. Suggest concrete restructuring or organizational improvements
5. Discuss your suggestions with the Author Simulator to refine them

Your output should include:
- Detailed structural analysis
- Specific strengths and weaknesses
- Visual representation of the current structure (if possible)
- Proposed structural improvements
- Structure evaluation in relation to genre expectations
- Thoughtful responses to Author Simulator's perspective

Remember to focus on how structure enhances or detracts from the content and purpose of the writing, rather than imposing formulaic patterns.
""",
    llm_config=gpt4_config,
)

author = AssistantAgent(
    name="Author",
    system_message="""You are the Author Simulator in a multi-agent writing evaluation system. Your primary responsibility is to understand and respond to every expert's feedback from the perspective of the writer right after he gives you the advice .

Key responsibilities:
1. Simulate the author's thought process and intentions
2. Explain potential reasoning behind writing choices
3. Respond to expert feedback from the author's perspective
4. Raise questions or concerns about suggested changes
5. Provide insight into challenges the author might face
6. Help refine feedback to be more applicable and actionable

When responding to expert feedback:
1. Consider the likely intention behind the original writing
2. Explain the possible reasoning for choices that experts questioned
3. Express understanding of valuable feedback
4. Raise constructive questions about feedback that might not align with the author's vision
5. Suggest alternative approaches that might better serve the author's goals
6. Reflect on how changes might impact other aspects of the writing

Your interaction style should:
- Be thoughtful and reflective, not defensive
- Show openness to improvement while maintaining the core vision
- Ask clarifying questions to better understand feedback
- Offer context that experts might not have considered
- Highlight practical challenges in implementing certain suggestions

IMPORTANT: If there's an "initial" then give response to that expert right now, and then ask that SAME expert to modify. If there's a "revised" then do not give response to that expert again.
Remember to maintain a productive dialogue that leads to genuine improvement while respecting the author's voice and intentions.
""",
    llm_config=gpt4_config,
)

integrator = AssistantAgent(
    name="Integrator",
    system_message="""You are the Feedback Integrator in a multi-agent writing evaluation system. Your primary responsibility is to consolidate expert feedback into a coherent, unified evaluation AT THE VERY END.

Key responsibilities:
1. Collect, categorize, and organize feedback from all experts(don't include planner, rubrics, and author)
2. Resolve potential conflicts between different expert opinions
3. Adjust the weight of various evaluations based on genre relevance
4. Generate structured feedback reports
5. Combine quantitative scores with qualitative assessments

When integrating feedback:
1. Identify common themes across expert evaluations
2. Note areas of consensus and disagreement
3. Prioritize feedback based on significance and impact
4. Resolve contradictions by considering genre requirements and rubric priorities
5. Ensure balanced representation of content, language, and structural feedback
6. Organize feedback in a logical, accessible format
7. Don't summarize in a way that loses the nuances of individual evaluations. Keep the feedback specific and actionable.

Your output should include:
- Comprehensive summary of all expert evaluations
- Structured organization of feedback by category
- Highlighted areas of consensus among experts
- Thoughtful resolution of conflicting feedback
- Balanced perspective that considers all evaluation dimensions
- Clear prioritization of suggested improvements

Remember to create a feedback report that is cohesive and actionable, rather than a disconnected collection of expert opinions. The final product should provide clear direction for improvement while acknowledging the writing's strengths."
""",
    llm_config=gpt4_config,
)

groupchat = GroupChat(
    agents=[user_proxy, planner, language, rubrics, structure, content, author, integrator],
    messages=[],
    max_round=50
)

manager = GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message="""
    rubrics:
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

    Analyze the following text:

    Laughing is one of the key components in all my relationships with others. It lightens the mood of any situation and can really lift my sprits when I'm having a bad day. It is often the ice breaker when I meet someone new and can help me get closer to the friends I already have.  On the first day of school, freshman year, I met a girl named @LOCATION1. We were in writing class and there was a boy named @CAPS1 sitting between us. @CAPS1 and I were talking about our schedules, and he said something that made our conversation slightly uncomforatable. I looked up and saw that @LOCATION1 had heard what he had said and had a look on her face that was somewhere between being embarrassed for me and close to laughing. I smiled at her and mouthed the word ""awkward"" when @CAPS1 turned away. This was her cue that it was okay to laugh, and she did so subtly. I didn't know that this first laugh would lead to many more in a friendship that would develop almost instantly. After the first week of schedules being changed and students being shuffled around, we found out that we had every single one of our classes together, except @CAPS3. We probably spent more time laughing in those classes than getting work done, and I'm not exactly sure how we managed to pass all our classes. Spending so much time together, it was only a matter of time before we had enough inside jokes to fill up a dictionary. Nearly any word or just the sight of something related to one of our jokes can send us into a fit of laughter. Sometimes, we don't have to say anything at all. I'll just look at her, and we'll burst out laughing. Because of this, our friends often question our sanity. When we start laughing, they'll look at eachother, and then at us for a clue as to why, or ask if we are okay. They don't understand us the way we understand eachother. People always get our names mixed up even though we look nothing alike. Our names dont even rhyme, or start with the same letter. But I can't really blame them. We're so much alike! From the activities we participate in to the way we think, we could almost be the same person. She makes me laugh every single day, and she's one of my best friends. @CAPS4 is another one of my friends who is constantly making me crack up. Whenever I'm with her, I'm always terrified of peeing in my pants. She's not as close to me as @LOCATION1 is, but we've gotten to be such better friends this year. We have a lot of classes together this year, and that's probably why we've gotten closer. We're always doing stupid stuff together, and laughing about it the whole time. For example, she and I like to laugh obnoxiously loud and exaggerate our ""ha's"" when someone tells a really lame or cheesy joke. Our biotech teacher loves to tell cheesy jokes, so when we're in his class, we sit together anticipating one of his jokes so that we can laugh. We also like to chew our gum with our mouths open, in order to make the chewing noise louder. I often laugh so hard that I can't even chew. I know I'll have a good day if I'm with @CAPS4. She can make me laugh in a way a lot of my other friends can't. It comes deep from within, to the point where you can't even breathe, and tears and running down your face. It makes your entire face is sore, even your eyes, from being scrunched up for so long. She's such a fun person to be around, and I'm glad to have her as one of my friends. Laughing is a very important part in the relationships I have with other people. If my friends couldn't make me laugh, our friendship would be so much more boring. Nothing would be fun. If I never laughed, I'd never be happy, and that's not a life I'm willing to try. Life is hard. It's not easy, and it's not always going to be smiles and smooth sailing. There's going to be sadness and rough waters. But no matter how tough this life @MONTH1 get, I know I'll have friends like @LOCATION1 and @CAPS4 there to share a laugh.
    ---
    """,
)
