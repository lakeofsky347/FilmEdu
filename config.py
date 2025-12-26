# config.py
import streamlit as st
import os

def get_secret(key_name):
    """
    安全获取密钥的函数：
    1. 优先尝试从 Streamlit Cloud / 本地 .streamlit/secrets.toml 读取
    2. 其次尝试从系统环境变量读取
    3. 如果都没有，返回 None
    """
    # 尝试 Streamlit secrets
    try:
        if key_name in st.secrets:
            return st.secrets[key_name]
    except (FileNotFoundError, AttributeError):
        pass

    # 尝试环境变量
    return os.environ.get(key_name)

# --- 配置加载 (关键修改：不要写死 Key，而是调用函数) ---

# 通义万相 (Qwen) API Key
QWEN_API_KEY = get_secret("QWEN_API_KEY")

# DeepSeek 配置
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# --- 安全检查 ---
if not QWEN_API_KEY:
    # 这里的 print 只会在后台终端显示，不会暴露给前端用户
    print("⚠️ 警告: QWEN_API_KEY 未配置，生图功能将无法使用。")

if not DEEPSEEK_API_KEY:
    print("⚠️ 警告: DEEPSEEK_API_KEY 未配置，对话功能将无法使用。")