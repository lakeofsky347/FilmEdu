# core/architecture.py
from agents.roles import TeacherAgent, StudentAgent, AssistantAgent
from core.collaboration import TriadicCollaborationEngine

class EducationalAgentArchitecture:
    [cite_start]
    """
    教育智能体核心架构 [cite: 4]
    """

    def __init__(self):
        self.teacher_agent = TeacherAgent()
        self.student_agent = StudentAgent()
        self.assistant_agent = AssistantAgent()
        self.collaboration_engine = TriadicCollaborationEngine()

    def triadic_collaboration(self, teacher_input: str, student_input: dict) -> dict:
        [cite_start]
        """
        三元协同处理流程 [cite: 11]
        """
        # 教师意图分析
        teacher_intent = self.teacher_agent.analyze_intent(teacher_input)
        
        # 学生学习状态分析
        student_state = self.student_agent.analyze_state(student_input)
        
        # 智能体协同决策
        return self.collaboration_engine.coordinate(
            teacher_intent, student_state
        )