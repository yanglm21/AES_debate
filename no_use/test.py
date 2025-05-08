import os
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
os.environ["OPENAI_API_KEY"] = "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"


cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # 从不要求人类输入。
)
joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.7, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",  # 从不要求人类输入。
)

result = joe.initiate_chat(cathy, message="Cathy, tell me a joke.", max_turns=2)
