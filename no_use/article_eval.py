import os
import autogen
from typing import List, Dict, Any, Tuple

# Configuration
config_list = [
    {
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com",
        "api_key": os.environ.get("OPENAI_API_KEY"),
    }
]

# Define agent configurations with appropriate prompts
def create_agent_configs(config_list):
    """Create configuration for all agents in the system"""
    
    # Base config for all agents
    base_config = {
        "config_list": config_list,
        "temperature": 0.2,
        "request_timeout": 120,
    }
    
    # Specific agent configurations
    agent_configs = {
        "moderator": {
            **base_config,
            "system_message": """你是一个主持人(Moderator)，负责主持多位专家对文章进行讨论评估。
            你的职责是：
            1. 理解用户提交的文章及其体裁类型
            2. 协调讨论流程，决定在每个讨论阶段邀请哪位专家发言
            3. 根据文章体裁和特点动态决定讨论的重点和方向
            4. 在必要时提出问题，引导专家们深入探讨某些方面
            5. 阶段性总结讨论内容，确保讨论的连贯性
            6. 在讨论结束时，提出最终的综合评价和建议
            
            作为讨论主持人，你需要：
            - 在每次发言后，明确指出下一位发言的专家，并提出你希望他们关注的问题。可选的专家有：structure_analyst, content_rater, language_doctor, audience_consultant, education_expert. 
            - 格式："@专家名称 请针对[具体问题/方面]发表你的看法。"注意，每次只选一位！注意，如果不是邀请下一个专家发言，请不要@他们。
            - 每次structure_analyst, content_rater, language_doctor, audience_consultant, education_expert中的某个专家发言后，你都需要邀请devils_advocate跟之前的专家相互进行讨论，然后将两者说的话总结到一起。
            - 确保所有专家都有机会发言，但可以根据文章特点和讨论需要多次邀请某些专家
            - 在讨论达到一定深度后，进行阶段性总结
            - 在判断讨论已经全面且深入后，做出最终总结并结束讨论
            
            请记住，你是讨论的引导者和协调者，应该根据讨论的实际进展灵活调整。
            """,
        },
        "structure_analyst": {
            **base_config,
            "system_message": """你是结构分析师(Structure Analyst)，专门负责分析文章的结构组织。
            你的职责是：
            1. 分析文章的论点树状结构
            2. 检测逻辑漏洞和结构缺陷
            3. 评估段落间的衔接和过渡
            4. 针对不同体裁文章，使用不同的结构评估标准
            5. 提出改进文章结构的具体建议
            
            在讨论中，你应该：
            - 只在主持人(@moderator)邀请你发言时才发言
            - 聚焦于文章结构方面的分析
            - 可以回应和补充其他专家关于结构的观点
            - 提出具体、可操作的结构改进建议
            """,
        },
        "content_rater": {
            **base_config,
            "system_message": """你是内容评分员(Content Rater)，专门评价文章内容的丰富度和创意性。
            你的职责是：
            1. 评估文章内容的丰富度和深度
            2. 判断内容与主题的相关性
            3. 评价观点的独创性和新颖性
            4. 识别内容中的创意亮点
            5. 提出增强内容质量的建议
            
            在讨论中，你应该：
            - 只在主持人(@moderator)邀请你发言时才发言
            - 聚焦于文章内容质量的评估
            - 可以回应和补充其他专家关于内容的观点
            - 提出具体、可操作的内容改进建议
            """,
        },
        "language_doctor": {
            **base_config,
            "system_message": """你是语言医生(Language Doctor)，专门诊断语法错误和表达问题。
            你的职责是：
            1. 识别文章中的语法错误
            2. 发现词语使用不当或表达不清的地方
            3. 评估语言的流畅性和多样性
            4. 针对不同体裁，提出适合的语言风格建议
            5. 提供具体的语言修改建议
            
            在讨论中，你应该：
            - 只在主持人(@moderator)邀请你发言时才发言
            - 聚焦于文章语言表达方面的问题
            - 可以回应和补充其他专家关于语言的观点
            - 提出具体、可操作的语言改进建议
            """,
        },
        "audience_consultant": {
            **base_config,
            "system_message": """你是受众顾问(Audience Consultant)，专门评估文章对目标读者的适配性。
            你的职责是：
            1. 评估文章与目标受众的匹配度
            2. 分析可能的理解障碍
            3. 预测不同读者群体的接受程度
            4. 模拟不同读者的视角和反应
            5. 提出增强受众接受度的建议
            
            在讨论中，你应该：
            - 只在主持人(@moderator)邀请你发言时才发言
            - 聚焦于文章与读者的关系
            - 可以回应和补充其他专家关于受众接受度的观点
            - 提出具体、可操作的提高受众接受度的建议
            """,
        },
        "devils_advocate": {
            **base_config,
            "system_message": """你是魔鬼代言人(Devil's Advocate)，专门质疑和挑战其他专家的观点，引导他们进行批判性思考，从而得出更合适、更丰富、幻觉更少的回答。
            
            在讨论中，你应该：
            - 只在主持人(@moderator)邀请你发言时才发言
            - 可以回应和补充其他专家关于论证的观点
            - 以建设性的方式提出质疑和改进建议
            """,
        },
        "education_expert": {
            **base_config,
            "system_message": """你是教育专家(Education Expert)，专门从教学角度评价文章。
            你的职责是：
            1. 评估文章的教育价值
            2. 分析文章对学习者的帮助程度
            3. 考虑文章在教学环境中的适用性
            4. 提出增强教育价值的建议
            5. 针对不同教育场景提供定制化建议
            
            在讨论中，你应该：
            - 只在主持人(@moderator)邀请你发言时才发言
            - 聚焦于文章的教育价值和应用
            - 可以回应和补充其他专家关于教育应用的观点
            - 提出具体、可操作的提高教育价值的建议
            """,
        },
    }
    
    return agent_configs

# Create agents
def create_agents(agent_configs):
    """Create all agents based on configurations"""
    agents = {}
    
    # Create each agent
    for agent_name, config in agent_configs.items():
        if agent_name == "moderator":
            agents[agent_name] = autogen.AssistantAgent(
                name=agent_name,
                system_message=config["system_message"],
                llm_config={"config_list": config["config_list"], "temperature": config["temperature"]},
            )
        else:
            agents[agent_name] = autogen.AssistantAgent(
                name=agent_name,
                system_message=config["system_message"],
                llm_config={"config_list": config["config_list"], "temperature": config["temperature"]},
            )
    
    # Add user proxy agent
    agents["user_proxy"] = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="TERMINATE",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("EVALUATION_COMPLETE"),
        code_execution_config={"work_dir": "coding", "use_docker": False},
    )
    
    return agents

# Define genre-specific evaluation suggestions (not strict rubrics)
def get_genre_suggestions(genre: str) -> Dict:
    """Get evaluation suggestions based on genre"""
    suggestions = {
        "议论文": {
            "structure": 0.4,
            "language": 0.3,
            "content": 0.3,
            "suggested_focus": "论证结构、逻辑性、论据有效性",
        },
        "创意写作": {
            "content": 0.5,
            "language": 0.3,
            "structure": 0.2,
            "suggested_focus": "创意性、表现力、情感共鸣",
        },
        "说明文": {
            "clarity": 0.4,
            "structure": 0.3,
            "completeness": 0.3,
            "suggested_focus": "清晰度、完整性、结构合理性",
        },
        "记叙文": {
            "storytelling": 0.4,
            "engagement": 0.3,
            "language": 0.3,
            "suggested_focus": "叙事手法、情节发展、人物塑造",
        },
        "应用文": {
            "practicality": 0.5,
            "clarity": 0.3,
            "completeness": 0.2,
            "suggested_focus": "实用性、格式规范、信息完整性",
        }
    }
    
    return suggestions.get(genre, {
        "structure": 0.33,
        "language": 0.33,
        "content": 0.34,
        "suggested_focus": "整体质量、表达清晰度、内容相关性",
    })

# Function to create a group chat for all agents
def create_group_chat(agents):
    """Create a group chat with all agents and set moderator as manager"""
    
    # Get all agents except user_proxy
    assistant_agents = [agent for name, agent in agents.items() if name != "user_proxy"]
    
    # Create the group chat
    group_chat = autogen.GroupChat(
        agents=assistant_agents + [agents["user_proxy"]],
        messages=[],
        max_round=50,
        speaker_selection_method="round_robin",  # Start with round robin but moderator will override
        allow_repeat_speaker=False,
    )
    
    # Custom speaker selection function to let moderator control who speaks next
    def select_next_speaker(last_speaker, groupchat):
        # Extract the message to find the next speaker mentioned by the moderator
        last_message = groupchat.messages[-1]["content"] if groupchat.messages else ""
        
        # If moderator was the last speaker, check for @mentions
        if last_speaker.name == "moderator":
            for agent in groupchat.agents:
                if f"@{agent.name}" in last_message and agent.name != "moderator":
                    return agent
        
        # Default to moderator if no clear direction or if someone else was speaking
        if last_speaker.name != "moderator":
            for agent in groupchat.agents:
                if agent.name == "moderator":
                    return agent
        
        # If unclear, default to moderator
        for agent in groupchat.agents:
            if agent.name == "moderator":
                return agent
    
    # Override the speaker selection method
    group_chat.speaker_selection_method = select_next_speaker
    
    return group_chat

# Function to start the group discussion
def evaluate_writing_with_discussion(agents, text: str, genre: str):
    """Orchestrate a group discussion among agents moderated by the moderator agent"""
    
    # Get suggestions for the genre
    suggestions = get_genre_suggestions(genre)
    
    # Create a group chat
    group_chat = create_group_chat(agents)
    
    # Create a group chat manager
    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": config_list, "temperature": 0.2},
    )
    
    # Initial message to start the discussion
    initial_message = f"""
    请评估以下{genre}:
    
    ---
    {text}
    ---
    
    请根据{genre}的特点进行评估，参考权重建议如下（但可以根据文章特点灵活调整）：
    {suggestions}
    
    我希望所有专家在主持人(@moderator)的引导下进行讨论。主持人将决定谁来发言，并提出关注的问题。
    
    请主持人(@moderator)开始引导讨论，首先分析文章的特点和需要重点评估的方面，然后邀请第一位专家发言。
    
    讨论结束后，请主持人(@moderator)总结所有专家的意见，给出最终评价和改进建议，并以"EVALUATION_COMPLETE"结束。
    """
    
    # Start the discussion
    agents["user_proxy"].initiate_chat(
        manager,
        message=initial_message
    )
    
    # Return the final messages from the discussion
    return agents["user_proxy"].chat_messages

# Main execution function
def main():
    """Main execution function"""
    # Example usage
    sample_text = """
    Dear @PERSON1, Advances in technology and computers is a bad thing. When the computer company's such as @CAPS1, @ORGANIZATION2, and @ORGANIZATION1, make cool updates to their computer systems people do not want to shut their computer off, which is not a good thing. As a child did you spend all of your time indoors and online? Computers take time away from spending time outside, or exercising. And they affect very crucial family time. Computer advances are bad for our country and town. Now-a -days, kids would much rather spend time on their computers than outside. This can have a very negative affect. First of all, it is important that students see and feel nature, and last time I checked they can not do that on a computer. Children need to see animals, smell the sweet scent of flowers and feel the breeze brush against their cheeks. A second reason that going outside is important is for the sun. Even though the sun does have harmful days, it is still important for health that everyone spends some time in the sun. The computer takes times away from nature which is unhealthy and dangerous. Computer also take precious time away from exercise. If people spend all their time on computers, then do they exercise. Everyone is supposed to get at least @NUM1 minutes of activity daily, but no one ever spends that much time working out. Also, obesity numbers have increased greatly since the invention of personal computer and the internet. Obesity can make life difficult for people and can also lead to disease. Life with computers has lead to less people exercising and obesity rates increasing. Another issue computers cause is that people are spending less time with their families. Family is one of the most important things in the world and everyone should spend a few hours daily with their family. Plus with encouregement from their family, many students excel in school and sports, which gives them graet self-confidence. Computers take time away from something that should be thw most important to everyone, family. Many people are affected negatively by computers. The technology takes very important time away from children and adults. It takes time away from the outdoors, exercising, and family. Yes, computers @MONTH1 make life easier, but they have a much more negative affect than they do a positive one.    
    """
    
    # Create agent configurations
    agent_configs = create_agent_configs(config_list)
    
    # Create agents
    agents = create_agents(agent_configs)
    
    # Evaluate the writing through group discussion
    discussion_results = evaluate_writing_with_discussion(agents, sample_text, "议论文")
    
    # Print the final messages
    for message in discussion_results["groupchat"][-5:]:
        print(f"{message['name']}: {message['content']}\n")

if __name__ == "__main__":
    main()