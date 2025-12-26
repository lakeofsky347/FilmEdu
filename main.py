# config.py
import streamlit as st
import os

def get_secret(key_name, default_value=None):
    """
    优先从 Streamlit Secrets 读取，
    如果找不到（比如在本地运行），则回退到环境变量或直接返回空
    """
    # 1. 尝试从 st.secrets 读取 (云端模式)
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except FileNotFoundError:
        pass # 本地没有 .streamlit/secrets.toml 文件

    # 2. 尝试从环境变量读取
    if key_name in os.environ:
        return os.environ[key_name]

    # 3. 返回默认值 (本地测试用，或者你把Key写死在这里，但不推荐上传到GitHub)
    return default_value

# 配置读取逻辑
QWEN_API_KEY = get_secret("QWEN_API_KEY", "sk-这里填你的阿里云Key用于本地测试")
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY", "sk-这里填你的DeepSeekKey用于本地测试")
DEEPSEEK_BASE_URL = get_secret("DEEPSEEK_BASE_URL", "https://api.deepseek.com")