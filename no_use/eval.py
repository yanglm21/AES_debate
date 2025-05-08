import os
from autogen import ConversableAgent, GroupChat, GroupChatManager

# 定义主持人（Moderator）
moderator = ConversableAgent(
    name="Moderator",
    system_message="""
    You are the moderator of the discussion. Your responsibilities include:
    1. Controlling the flow of the discussion. You need to choose the next agent to provide feedback according to the genre of the article(e.g. narrative: language and audience first; argumentative: structure first).
    2. Guide agents to judge according to the rubrics of this genre(e.g. argumentative's language should be precise while narrative doesn't have to).
    3. Asking key questions to guide the analysis.
    4. Summarizing the consensus and final recommendations.
    Ensure that each agent has a chance to speak and that the discussion stays focused on the genre-aware evaluation of the article.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# 定义结构分析师（Structure Analyst）
structure_analyst = ConversableAgent(
    name="Structure_Analyst",
    system_message="""
    You are a structure analyst. Your responsibilities include:
    1. Analyzing the hierarchical structure of the arguments in the article.
    2. Detecting logical flaws or inconsistencies in the argument tree.
    3. Providing a visual representation of the structure (describe it in text).
    Focus on how well the article's structure aligns with the genre's expectations.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# 定义语言医生（Language Doctor）
language_doctor = ConversableAgent(
    name="Language_Doctor",
    system_message="""
    You are a language doctor. Your responsibilities include:
    1. Diagnosing grammatical errors and awkward expressions in the article.
    2. Providing specific suggestions for improving clarity and fluency.
    3. Ensuring the language style matches the genre's conventions.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# 定义受众顾问（Audience Consultant）
audience_consultant = ConversableAgent(
    name="Audience_Consultant",
    system_message="""
    You are an audience consultant. Your responsibilities include:
    1. Evaluating how well the article adapts to its target audience.
    2. Predicting potential comprehension barriers for different reader groups.
    3. Simulating the perspectives of various readers (e.g., experts, beginners).
    Provide recommendations to improve audience engagement.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# 定义魔鬼代言人（Devil's Advocate）
devils_advocate = ConversableAgent(
    name="Devils_Advocate",
    system_message="""
    You are the devil's advocate. Your responsibilities include:
    1. Challenging the conclusions and assumptions in the article.
    2. Providing counterarguments and alternative perspectives.
    3. Forcing the system to engage in counterfactual reasoning.
    Be critical but constructive in your feedback.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.8, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# 定义教育专家（Education Expert）
education_expert = ConversableAgent(
    name="Education_Expert",
    system_message="""
    You are an education expert. Your responsibilities include:
    1. Evaluating the practicality of the improvement suggestions.
    2. Providing recommendations for adapting the article to educational contexts.
    3. Suggesting how the article can be used as a teaching tool.
    Focus on the pedagogical value of the article.
    """,
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# 定义群组聊天（Group Chat）
group_chat = GroupChat(
    agents=[moderator, structure_analyst, language_doctor, audience_consultant, devils_advocate, education_expert],
    messages=[],
    max_round=10,  # 最多进行 10 轮对话
    speaker_selection_method="auto",  # 动态选择下一个发言者
)

# 定义群组聊天管理器（Group Chat Manager）
group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ.get("OPENAI_API_KEY")}]},
)


# 启动讨论
moderator.initiate_chat(
    group_chat_manager,
    message="""
    Let's begin the genre-aware evaluation of the following article:
    ---
    article:"Morose and somnolent, I woke up. I woke up to go to @LOCATION1. Going to @LOCATION1 to watch a few basketball games, I was. Although I was unable to partake in the activity because I was @CAPS1 injured in the previous week of practice. Unfortunately though, I still had to go and support my friends and teammates. It was about @NUM1 o'clock when we all got onto the bus and set off to @LOCATION1. All of my friends were mirthful and talkative; but me on the other hand, I was in a lackadaisical stare. The bus ride seemed to last a whole lifetime; but in two hours we arrived at our destination. @LOCATION1 had a nice school; but we were all about to find that it sometimes resembled a ghost town. The high school seemed lifeless in comparison with other schools we had played at in the past. There was nobody around and not a soul to be heard. We all sat there patiently waiting; then, after maybe five minutes or so a man showed up and led us to the locker rooms. The boys had to wait till the girls were done playing their game; so, we all went and started shooting on one of the auxiliary courts. Although, sadly due to my injury I could not participate in the activity. They were all having so much fun screwing around down there. Just the thought of not being down there with them made me ill. After the girls game we all went to change. After that we all sat there, joking around and waiting for our coach to come in and give us our pre-game pep talk. It seemed like ages before our coach finally came into the locker room. He talked about what we should and shouldn't do in order to get the win. When the game started I was really getting depressed, but I sucked it up and cheered on my team. The first half of the game was great and we were on top. Although the second half wasn't so great. We only scored six points and ended up losing the game by a large margin. My friends tried to be stoical; but I could tell that they were ashamed. Ashamed of their performance in the second half. This once again made me feel sad and depressed. Next, I had no choice but to go and watch two more games in the old, vulgar, and uncomfortable bleachers of @LOCATION1. The first of the two games was a great one; we won by two points. The next game on the other hand, was a very boring one. It seemed to take forever; but the worst of it was the fact that we lost. After that final game I had to wait for my cousin to come out from the locker room. When he did, we went to check out with our coaches; we had to check out in order to ride home with our parents. So off we went; but first we had to get something to eat. Once again, like all the times before we chose to eat at @ORGANIZATION1. We went through the drive through, got our food, then pulled over so we could eat. At first everything seemed right; but then my cousin noticed he didn't receive the @CAPS2 he ordered. So we went in to get the problem solved. Afterwords, we were all kind of joking about the restaurant not getting the order right; then I took a bite of my burger. It was then that I realized I had received a burger without a patty. I was really upset that @ORGANIZATION1's made such a silly mistake. So once more me and my cousin went in to the restaurant. When told what the problem was they were all just in shock. They couldn't believe what they had done. So after they all settled down they made me another burger.  Me and and the family were all having a ball about the events at the @ORGANIZATION1. It was a great trip home fillled with lots of fun and laughter; which was not what me, my cousin, or anybody else expected.So in the end of my once gloomy day, I found myself stricken with laughter."			
    ---
    Please analyze the article based on your respective roles and provide feedback.
    """,
)