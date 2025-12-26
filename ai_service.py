from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

class AIService:
    # 动态初始化 Client，防止导入时因为 Key 为空直接报错
    _client = None

    @classmethod
    def get_client(cls):
        """懒加载 Client，确保只在需要时初始化"""
        if cls._client is None:
            if not DEEPSEEK_API_KEY:
                return None # Key 未配置
            cls._client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL
            )
        return cls._client

    @staticmethod
    def _chat(messages):
        """底层对话接口"""
        client = AIService.get_client()
        
        # 安全检查
        if not client:
            return "⚠️ 系统错误: DeepSeek API Key 未配置，请联系管理员。"

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                stream=False,
                temperature=1.3
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"⚠️ DeepSeek 连接失败: {str(e)}"

    @staticmethod
    def student_pre_review(task, work):
        msgs = [
            {"role": "system", "content": "你是一位资深影视学院导师。请从技术（运镜、光影）和艺术（叙事、情感）两个维度点评学生的作业，并给出具体修改建议。语气要鼓励为主，但在专业问题上要严谨。"},
            {"role": "user", "content": f"【作业题目】：{task}\n【学生提交】：{work}"}
        ]
        return AIService._chat(msgs)

    @staticmethod
    def teacher_summary(task, works_text):
        msgs = [
            {"role": "system", "content": "你是助教。请阅读全班学生的提交内容，总结共性问题，提炼优秀案例，并为老师提供讲评重点。请分点作答。"},
            {"role": "user", "content": f"【题目】：{task}\n【全班提交列表】：\n{works_text}"}
        ]
        return AIService._chat(msgs)