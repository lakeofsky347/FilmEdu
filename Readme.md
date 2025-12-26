# 🎬 FilmEdu | 影视制作智能教育平台

> **Python 程序设计课程结课作业**  
> _一个基于多智能体协同架构、融合 AIGC 技术的沉浸式教学 Web 系统_

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![AI Models](https://img.shields.io/badge/AI%20Core-DeepSeek%20%7C%20Qwen-purple)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)

---

## 🌟 项目简介 (Project Synopsis)

**FilmEdu OS** 是一个专为影视制作教育设计的、具有未来主义风格的在线实训平台。它从最初的“师-机-生”三元协同架构理念出发，逐步演化为一个功能完备、视觉酷炫、数据驱动的 Web 应用程序。

本项目旨在解决传统教学模式中的反馈延迟、创意可视化困难等问题，通过深度集成 **DeepSeek 逻辑推理引擎** 和 **通义万相 (Qwen) 视觉生成核心**，为学生提供从剧本构思到后期评估的全流程智能辅助，同时为教师提供强大的数据看板与学情分析工具。

## ✨ 核心功能 (Key Features)

### 👨‍🎓 学生端 (Student Terminal)
*   **🎮 游戏化学习**: 引入等级、经验值和学分进度条，提升学习动力。
*   **🤖 AI 智能预审**: 在提交作业前，可调用 DeepSeek 引擎对剧本、分镜描述进行实时分析，获取专业修改建议。
*   **🎨 AI 概念图生成**: 集成通义万相，一键将文字描述转化为高质量的电影分镜参考图，激发视觉灵感。
*   **📊 动态能力档案**: 在“个人中心”中，系统会根据历史作业评分，动态生成个人能力雷达图，强弱项一目了然。

### 👨‍🏫 教师端 (Commander Console)
*   **🎛️ 数据驾驶舱**: 实时展示已发布任务数、收到提交数、已批阅数等核心教学指标。
*   **🧠 AI 学情分析**: 一键调用 AI 分析全班作业，自动总结共性问题、提炼优秀案例，为课堂讲评提供数据支持。
*   **📢 任务发布与管理**: 轻松创建、发布课程任务，所有学生终端将实时同步。
*   **📝 Streamlined 批阅**: 在线查看学生提交内容及 AI 预审意见，直接评分与填写评语。

### 🔮 技术亮点 (Tech Highlights)
*   **🚀 动态粒子背景**: 使用 `Particles.js` 实现交互式神经网络背景，科技感十足。
*   **✨ 赛博朋克 UI**: 采用玻璃拟态、霓虹光晕和科幻字体，打造沉浸式用户体验。
*   **🎬 Lottie 矢量动画**: 在关键交互节点（如加载、成功）使用流畅的矢量动画，提升界面生动性。
*   **📈 Echarts 数据可视化**: 引入专业图表库，实现动态雷达图等高级数据可视化功能。


## 🛠️ 技术栈 (Technology Stack)
Web 框架: Streamlit
UI 扩展: streamlit-option-menu, streamlit-lottie, streamlit-echarts
AI 模型 SDK: openai (for DeepSeek), dashscope (for Qwen)
数据库: Python内置 sqlite3
HTTP 请求: requests
其他: Pillow (图像处理), pandas (数据结构)

## 🚀 快速开始 (Quick Start)
1. 环境准备
确保你的电脑已安装 Python 3.8 或更高版本。
2. 克隆与安装
下载并解压项目，然后在项目根目录打开终端，运行：
pip install -r requirements.txt
3. 配置 API Key
打开 config.py 文件，填入你自己的 API Key：
QWEN_API_KEY = "sk-你的阿里云Key" 
DEEPSEEK_API_KEY = "sk-你的DeepSeek Key"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
4. 运行系统
在终端中执行以下命令：
streamlit run web_app.py
程序启动后，你的浏览器将自动打开 http://localhost:8501 地址。
5. 清空测试数据
如果需要重置系统（删除所有用户和作业数据），只需关闭程序，然后删除项目根目录下的 film_edu.db 文件即可。下次启动时会自动重建。


## 👨‍💻 团队信息
姓名	        学号	                分工
陈虹宇	202413093053	程序设计、功能实现及 UI 设计
纪坤江	202413093052	功能实现及结构优化
马行键	202413093062	功能集成测试及反馈
唐艺玲	202308043016	项目报告及书面整理
李祈芸	202413093059	材料整理及进度推进


