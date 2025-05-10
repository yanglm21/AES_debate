import time

gpt4_config = {
    # 每次运行时根据时间自动生成seed
    "cache_seed": int(time.time()),
    "temperature": 0,
    "timeout": 120,
    "model": "gpt-4o",
    "base_url": "https://xiaoai.plus/v1",
    "api_key": "sk-deB5aUH0rl7T13aDLNJs0bROhXETg6qaTUpbOJ7mK8t4heV9"
}

deepseek_config = {
    "cache_seed": int(time.time()),
    "temperature": 0,
    "timeout": 120,
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com",
    "api_key": "sk-f14970f964474d029f90362666b66524"
}