import streamlit as st
import time
import requests
import os
import json
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from streamlit_echarts import st_echarts
from cuc_particle import cuc_particle_effect
from db_manager import DBManager
from ai_service import AIService
from config import QWEN_API_KEY
from qwenclient import generate_image_sync

# ==========================================
# 🛠️ 基础工具与配置
# ==========================================
UPLOAD_DIR = "student_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, user_id, task_id):
    if uploaded_file is None: return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{user_id}_{task_id}_{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# ==========================================
# 🌌 核心资源加载 (纯本地绝对路径版)
# ==========================================
def load_lottie_local(filename: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, "assets", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def render_lottie(filename, height=300, key=None):
    anim_data = load_lottie_local(filename)
    if anim_data:
        st_lottie(anim_data, height=height, key=key)
    else:
        st.markdown(f"""
        <div style='height:{height}px; border:1px dashed rgba(0,242,255,0.3); 
        display:flex; align-items:center; justify-content:center; 
        color:rgba(0,242,255,0.5); font-family:"Orbitron";'>
        [ {filename.upper()} ]
        </div>""", unsafe_allow_html=True)

# 资源列表
lottie_assets = {
    "robot": "robot.json",
    "empty": "empty.json", 
    "success": "success.json",
    "welcome": "welcome.json",
    "files": "files.json"
}

def render_particles():
    particles_js = """
    <!DOCTYPE html><html lang="en"><head><style>
        body, html { margin:0; padding:0; overflow:hidden; width:100%; height:100%; }
        #bg-gradient {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
            background: radial-gradient(circle at center, #1a2a3a 0%, #0e1117 100%);
        }
        #particles-js { position: fixed; width: 100vw; height: 100vh; top: 0; left: 0; z-index: -1; }
    </style></head>
    <body>
    <div id="bg-gradient"></div>
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>particlesJS("particles-js", {"particles":{"number":{"value":40},"color":{"value":"#00f2ff"},"shape":{"type":"circle"},"opacity":{"value":0.3,"random":true},"size":{"value":2,"random":true},"line_linked":{"enable":true,"distance":150,"color":"#00f2ff","opacity":0.15,"width":1},"move":{"enable":true,"speed":0.8,"direction":"none","random":false,"straight":false,"out_mode":"out","bounce":false}}});</script>
    </body></html>
    """
    components.html(particles_js, height=0, width=0)

def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Noto+Sans+SC:wght@300;400;700&display=swap');
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0e1117; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #00f2ff; }

        .stApp { font-family: 'Noto Sans SC', sans-serif; }
        
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(120deg, #E0F7FA, #00f2ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(0 0 10px rgba(0, 242, 255, 0.5));
        }

        div[data-testid="stMetric"], .glass-card, div.stForm {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        div[data-testid="stMetric"]:hover, .glass-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0, 242, 255, 0.5);
            box-shadow: 0 15px 40px rgba(0, 242, 255, 0.15);
        }

        .system-bar {
            position: fixed; top: 0; right: 0; padding: 10px 20px;
            color: rgba(0, 242, 255, 0.8); font-family: 'Orbitron'; font-size: 0.75rem;
            z-index: 9999; letter-spacing: 1px;
        }
        
        /* --- 动画类 --- */
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .reveal-1 { animation: fadeInUp 0.8s ease-out forwards; opacity: 0; animation-delay: 0.1s; }
        .reveal-2 { animation: fadeInUp 0.8s ease-out forwards; opacity: 0; animation-delay: 0.3s; }
        .reveal-3 { animation: fadeInUp 0.8s ease-out forwards; opacity: 0; animation-delay: 0.5s; }
        .reveal-4 { animation: fadeIn 1.2s ease-out forwards; opacity: 0; animation-delay: 0.8s; }

        @keyframes bounce { 0%, 20%, 50%, 80%, 100% {transform: translateY(0);} 40% {transform: translateY(-10px);} 60% {transform: translateY(-5px);} }
        .scroll-down { text-align: center; margin-top: 50px; cursor: pointer; animation: bounce 2s infinite; opacity: 0.7; }
        
        /* --- 团队卡片样式 (3x2 矩阵版) --- */
        .team-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        @media (max-width: 900px) { .team-container { grid-template-columns: 1fr; } }

        .team-card {
            width: 100%; height: 360px;
            background: rgba(255,255,255,0.02);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            position: relative;
            transition: all 0.4s ease;
            text-align: center;
            display: flex; flex-direction: column; align-items: center;
        }
        .team-card:hover {
            transform: translateY(-10px);
            border-color: #00f2ff;
            background: rgba(0, 242, 255, 0.05);
            box-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
        }

        .avatar-box {
            width: 100px; height: 100px;
            border-radius: 50%;
            margin: 40px auto 20px;
            border: 3px solid rgba(255,255,255,0.2);
            background: linear-gradient(135deg, #00c6ff, #0072ff);
            color: white;
            font-family: 'Noto Sans SC', sans-serif;
            font-size: 45px;
            font-weight: bold;
            display: flex; align-items: center; justify-content: center;
            transition: all 0.4s ease;
            box-shadow: 0 0 15px rgba(0,0,0,0.5);
        }
        .team-card:hover .avatar-box {
            border-color: #00ff88;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
            transform: rotate(10deg) scale(1.1);
        }
        .avatar-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }

        .team-name { font-family: 'Orbitron', 'Noto Sans SC'; font-size: 1.4rem; color: white; margin-bottom: 5px; font-weight: bold; }
        .team-role { color: #00f2ff; font-size: 0.85rem; margin-bottom: 10px; letter-spacing: 1px; }
        .team-id { color: #666; font-size: 0.75rem; margin-bottom: 10px; }
        .team-desc { padding: 0 20px; color: #ccc; font-size: 0.8rem; line-height: 1.4; }
        
        .gray-card { filter: grayscale(100%); opacity: 0.6; }
        .gray-card:hover { filter: grayscale(0%); opacity: 1; }
    </style>
    """, unsafe_allow_html=True)

def setup_page():
    st.set_page_config(page_title="FilmEdu OS", page_icon="💠", layout="wide", initial_sidebar_state="collapsed")
    render_particles()
    inject_custom_css()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f'<div class="system-bar">SYSTEM ONLINE | {now} | CUC_NET: SECURE</div>', unsafe_allow_html=True)

def init_session():
    if 'db' not in st.session_state: st.session_state.db = DBManager()
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    if 'user_info' not in st.session_state: st.session_state.user_info = {}

# ==========================================
# 📊 图表组件
# ==========================================
def render_radar_chart(scores=None):
    if not scores:
        data_val = [50, 50, 50, 50, 50]
        title = "等待数据初始化..."
    else:
        avg = int(scores)
        data_val = [avg, avg+5, avg-5, avg+2, avg-2]
        data_val = [max(0, min(100, x)) for x in data_val]
        title = "当前能力模型"
    option = {"backgroundColor": "transparent","radar": {"indicator": [{"name": "剧本结构", "max": 100},{"name": "视觉叙事", "max": 100},{"name": "剪辑节奏", "max": 100},{"name": "声音设计", "max": 100},{"name": "创意构思", "max": 100}],"splitArea": {"show": False},"axisLine": {"lineStyle": {"color": "rgba(255, 255, 255, 0.3)"}}},"series": [{"type": "radar","data": [{"value": data_val,"name": title,"areaStyle": {"color": "rgba(0, 242, 255, 0.4)"},"lineStyle": {"color": "#00f2ff", "width": 2},"symbol": "circle","symbolSize": 6}]}]}
    st_echarts(options=option, height="300px")

# ==========================================
# 🚪 门户页
# ==========================================
def landing_page():
    with st.container():
        st.markdown("<div style='height: 5vh;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.markdown("""
            <div class='reveal-1'>
                <h1 style='font-size: 3.5rem; margin-bottom: 0;'>FilmEdu OS <span style='font-size:1.5rem; color:#00ff88'>Ultimate</span></h1>
                <h3 style='font-weight: 300; color: #ccc; margin-top: 0;'>The Next-Gen Cinema Education Platform</h3>
            </div>
            <div class='reveal-2' style='margin: 30px 0; border-left: 4px solid #00f2ff; padding-left: 20px;'>
                <p style='font-size: 1.1rem; line-height: 1.6; color: #e0e0e0;'>
                    欢迎接入 <strong>中国传媒大学</strong> 影视智能实训终端。<br>
                    融合 <strong>DeepSeek</strong> 深度推理与 <strong>Qwen</strong> 视觉生成，<br>
                    重新定义从剧本到荧幕的创作流程。
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='reveal-3'>", unsafe_allow_html=True)
            tab_login, tab_reg = st.tabs(["⚡ 接入系统 (Login)", "🧬 创建档案 (Register)"])
            with tab_login:
                with st.form("login_form"):
                    u = st.text_input("Access ID")
                    p = st.text_input("Passcode", type="password")
                    if st.form_submit_button("CONNECT", use_container_width=True):
                        with st.spinner("Handshaking..."):
                            time.sleep(0.5)
                            role = st.session_state.db.login(u, p)
                            if role:
                                st.session_state.logged_in = True
                                st.session_state.user_info = {'username': u, 'role': role}
                                st.rerun()
                            else: st.error("Access Denied.")
            with tab_reg:
                with st.form("reg_form"):
                    nu = st.text_input("New ID")
                    np = st.text_input("Set Passcode", type="password")
                    nr = st.selectbox("Role Identity", ["student", "teacher"])
                    if st.form_submit_button("INITIALIZE", use_container_width=True):
                        if st.session_state.db.register(nu, np, nr): st.success("Profile Created.")
                        else: st.error("ID Conflict.")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown("<div class='reveal-4'>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)
            cuc_particle_effect()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='reveal-4 scroll-down' onclick="window.scrollTo(0, document.body.scrollHeight);">
        <p style='color: #00f2ff; font-size: 0.8rem; letter-spacing: 2px;'>SCROLL TO MEET THE TEAM</p>
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#00f2ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7 13l5 5 5-5M7 6l5 5 5-5"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25vh;'></div>", unsafe_allow_html=True)

    # --- 团队展示 ---
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 50px 0;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-bottom: 50px;'>ARCHITECTS OF THE SYSTEM</h2>", unsafe_allow_html=True)

    team_html = """
<div class="team-container">
    <!-- 1. 陈虹宇 -->
    <div class="team-card">
        <div class="avatar-box">
                <img src="https://cdn.jsdelivr.net/gh/lakeofsky347/FilmEdu@main/heads/chen.jpg" class="avatar-img">
            </div>
        <div class="team-name">陈虹宇</div>
        <div class="team-role">Lead Architect & UI Designer</div>
        <div class="team-id">ID: 202413093053</div>
        <div class="team-desc">项目总负责人。<br>负责核心程序设计、AI 接口集成及全站 UI/UX 动效实现。</div>
    </div>
<!-- 2. 纪坤江 -->
    <div class="team-card">
        <div class="avatar-box">
                <img src="https://cdn.jsdelivr.net/gh/lakeofsky347/FilmEdu@main/heads/ji.jpg" class="avatar-img">
            </div>
        <div class="team-name">纪坤江</div>
        <div class="team-role">Backend Developer</div>
        <div class="team-id">ID: 202413093052</div>
        <div class="team-desc">后端逻辑与结构优化。<br>负责数据库架构设计及功能模块的底层实现。</div>
    </div>
<!-- 3. 马行键 -->
    <div class="team-card">
        <div class="avatar-box">
                <img src="https://cdn.jsdelivr.net/gh/lakeofsky347/FilmEdu@main/heads/ma.jpg" class="avatar-img">
            </div>
        <div class="team-name">马行键</div>
        <div class="team-role">QA Engineer</div>
        <div class="team-id">ID: 202413093062</div>
        <div class="team-desc">集成测试专家。<br>负责系统功能测试、Bug 追踪及用户体验反馈。</div>
    </div>
<!-- 4. 唐艺玲 (暖色调区分) -->
    <div class="team-card">
        <div class="avatar-box">
                <img src="https://cdn.jsdelivr.net/gh/lakeofsky347/FilmEdu@main/heads/tang.jpg" class="avatar-img">
            </div>
        <div class="team-name">唐艺玲</div>
        <div class="team-role">Technical Writer</div>
        <div class="team-id">ID: 202328043016</div>
        <div class="team-desc">文档与报告撰写。<br>负责项目书面材料整理及技术文档的规范化输出。</div>
    </div>
<!-- 5. 李祈芸 (暖色调区分) -->
    <div class="team-card">
        <div class="avatar-box" style="background: linear-gradient(135deg, #ff9966, #ff5e62);">李</div>
        <div class="team-name">李祈芸</div>
        <div class="team-role">Project Manager</div>
        <div class="team-id">ID: 202413093059</div>
        <div class="team-desc">项目进度管理。<br>负责材料统筹整理及团队协作进度的推进。</div>
    </div>
<!-- 6. 吴起帆 -->
    <div class="team-card">
        <div class="avatar-box">吴</div>
        <div class="team-name">吴起帆</div>
        <div class="team-role">Code</div>
        <div class="team-id">ID: 202413093055</div>
        <div class="team-desc">Code<br><br></div>
    </div>
</div>
"""
    st.markdown(team_html, unsafe_allow_html=True)
    st.markdown("<br><br><div style='text-align:center; color:#555; font-size:0.8rem;'>© 2025 FilmEdu OS Project. All Systems Nominal.</div>", unsafe_allow_html=True)

# ==========================================
# 👨‍🏫 教师端
# ==========================================
def teacher_dashboard():
    user = st.session_state.user_info['username']
    my_tasks = st.session_state.db.get_teacher_tasks(user)
    task_count = len(my_tasks)
    
    submission_count = 0
    graded_count = 0
    for t in my_tasks:
        subs = st.session_state.db.get_submissions(t[0])
        submission_count += len(subs)
        # status index is 8 due to new file_path col
        graded_count += len([s for s in subs if s[8] == 'graded'])

    with st.sidebar:
        st.markdown(f"### 🟢 COMMANDER: {user}")
        nav = option_menu(None, ["概览", "任务发布", "作业批阅", "断开连接"], 
            icons=["grid", "broadcast", "check2-square", "power"])
        if nav == "断开连接": st.session_state.logged_in=False; st.rerun()

    if nav == "概览":
        st.title("🎛️ 教学数据看板")
        c1, c2, c3 = st.columns(3)
        c1.metric("已发布任务", str(task_count))
        c2.metric("收到提交", str(submission_count))
        c3.metric("已批阅", str(graded_count))
        st.markdown("---")
        if task_count == 0:
            c_empty, _ = st.columns([1, 2])
            with c_empty:
                st.info("当前系统空闲。")
                render_lottie("empty.json", height=200, key="empty")
        else:
            st.subheader("📋 活跃任务流")
            for t in my_tasks[-3:]: 
                with st.container():
                    st.markdown(f"**{t[2]}**")
                    st.caption(f"发布时间: {t[4]}")
                    st.progress(100, "状态: 进行中")

    elif nav == "任务发布":
        st.title("📡 新任务广播")
        c1, c2 = st.columns([2, 1])
        with c1:
            with st.form("pub_task"):
                title = st.text_input("任务代号")
                content = st.text_area("任务指令详情", height=200)
                if st.form_submit_button("🚀 发布任务"):
                    success = st.session_state.db.create_task(user, title, content)
                    if success:
                        st.balloons()
                        st.toast("任务已同步")
                        time.sleep(1)
                        st.rerun()
                    else: st.error("⚠️ 错误：该任务代号已存在！")
        with c2: st.info("💡 提示: 任务代号必须唯一。")

    elif nav == "作业批阅":
        st.title("📝 作业评估终端")
        if not my_tasks: st.warning("请先发布任务。"); return
        t_titles = [t[2] for t in my_tasks]
        sel_t = st.selectbox("选择任务频道", t_titles)
        t_id = next(t[0] for t in my_tasks if t[2] == sel_t)
        t_content = next(t[3] for t in my_tasks if t[2] == sel_t)
        subs = st.session_state.db.get_submissions(t_id)
        
        if not subs:
            st.info("暂无信号。")
            render_lottie("empty.json", height=200, key="empty_sub")
        else:
            if st.button("📊 运行 AI 学情分析"):
                with st.spinner("Analyzing..."):
                    all_text = "\n".join([f"学生{s[2]}: {s[3]}" for s in subs])
                    report = AIService.teacher_summary(t_content, all_text)
                    st.success(report)
            st.divider()
            for s in subs:
                status_icon = "✅" if s[8] == 'graded' else "⏳"
                with st.expander(f"{status_icon} 学员: {s[2]}"):
                    c_l, c_r = st.columns([2, 1])
                    with c_l:
                        st.markdown("**📄 文本作业:**"); st.code(s[3], language="text")
                        if s[4]:
                            st.markdown("---")
                            st.markdown(f"**📎 附件:** `{os.path.basename(s[4])}`")
                            if s[4].endswith(('.png', '.jpg', '.jpeg')): st.image(s[4], width=300)
                            elif s[4].endswith('.mp4'): st.video(s[4])
                            elif s[4].endswith('.pdf'):
                                with open(s[4], "rb") as f: st.download_button("下载 PDF", f, file_name=os.path.basename(s[4]))
                            else:
                                with open(s[4], "rb") as f: st.download_button("下载文件", f, file_name=os.path.basename(s[4]))
                        st.markdown(f"**🤖 AI 预审记录:**\n> {s[5]}")
                    with c_r:
                        g = st.text_input("评分", s[6] or "", key=f"g_{s[0]}")
                        c = st.text_area("评语", s[7] or "", key=f"c_{s[0]}")
                        if st.button("确认评估", key=f"b_{s[0]}"):
                            st.session_state.db.grade_submission(s[0], g, c)
                            st.toast("已上传"); st.rerun()

# ==========================================
# 👨‍🎓 学生端
# ==========================================
def student_dashboard():
    user = st.session_state.user_info['username']
    nav = option_menu(None, ["工作台", "个人档案", "退出"], 
        icons=["pc-display", "person-vcard", "power"], orientation="horizontal",
        styles={"container": {"background-color": "transparent"}})
    if nav == "退出": st.session_state.logged_in=False; st.rerun()

    if nav == "工作台":
        all_tasks = st.session_state.db.get_all_tasks()
        if not all_tasks: st.info("系统待机中。"); render_lottie("files.json", height=300, key="idle"); return
        c_list, c_detail = st.columns([1, 2.5])
        with c_list:
            st.subheader("📥 任务收件箱")
            for t in all_tasks:
                if st.button(f"📄 {t[2]}", key=f"sel_{t[0]}", use_container_width=True): st.session_state['curr_t_id'] = t[0]
            if 'curr_t_id' not in st.session_state: st.session_state['curr_t_id'] = all_tasks[0][0]
        curr_t = next((t for t in all_tasks if t[0] == st.session_state['curr_t_id']), None)
        if curr_t:
            my_sub = st.session_state.db.get_my_submission(curr_t[0], user)
            with c_detail:
                st.markdown(f"### 🚩 {curr_t[2]}"); st.info(f"指令: {curr_t[3]}")
                tab_main, tab_ai = st.tabs(["✍️ 创作终端", "🔮 AI 辅助"])
                with tab_main:
                    val = my_sub[3] if my_sub else ""
                    u_input = st.text_area("内容输入...", value=val, height=200, placeholder="剧本概述...")
                    st.markdown("##### 📎 附件上传")
                    uploaded_file = st.file_uploader("拖拽文件", type=['png', 'jpg', 'mp4', 'pdf'])
                    if st.button("📡 提交作业", type="primary"):
                        file_path = None
                        if uploaded_file: file_path = save_uploaded_file(uploaded_file, user, curr_t[0])
                        elif my_sub and my_sub[4]: file_path = my_sub[4]
                        fb = st.session_state.get(f"fb_{curr_t[0]}", my_sub[5] if my_sub else "")
                        st.session_state.db.submit_work(curr_t[0], user, u_input, file_path, fb)
                        render_lottie("success.json", height=100, key="ok"); st.success("数据传输完成！")
                with tab_ai:
                    c_a1, c_a2 = st.columns(2)
                    with c_a1:
                        # 1. 允许学生输入自己的画面描述
                        st.markdown("#### 🎨 视觉化实验室")
                        img_prompt = st.text_area("分镜画面描述", height=100, 
                                                placeholder="在此输入画面构思...\n例如：清晨的森林，阳光透过树叶，丁达尔效应，电影质感",
                                                key=f"img_p_{curr_t[0]}")
                        
                        # 2. 风格选择器
                        img_style = st.selectbox("风格滤镜", ["无 (Custom)", "电影写实 (Cinematic)", "赛博朋克 (Cyberpunk)", "水墨国风 (Ink)", "皮克斯动画 (3D Cartoon)"], key=f"style_{curr_t[0]}")

                        if st.button("✨ 生成分镜图", use_container_width=True, key=f"gen_btn_{curr_t[0]}"):
                            if not img_prompt:
                                st.warning("请先输入画面描述。")
                            else:
                                with st.spinner("通义万相正在绘图..."):
                                    # 组合 Prompt
                                    style_tag = ""
                                    if "电影写实" in img_style: style_tag = ", cinematic shot, photorealistic, 8k"
                                    elif "赛博朋克" in img_style: style_tag = ", cyberpunk, neon lights, futuristic"
                                    elif "水墨" in img_style: style_tag = ", chinese ink painting style, artistic"
                                    elif "皮克斯" in img_style: style_tag = ", 3d style, pixar, cute, vibrant"
                                    
                                    final_prompt = f"{img_prompt}{style_tag}"
                                    
                                    res = generate_image_sync(QWEN_API_KEY, final_prompt)
                                    if res['success']:
                                        st.image(res['paths'][0], caption=f"Prompt: {img_prompt}", use_container_width=True)
                                    else:
                                        st.error(f"生成失败: {res.get('message')}")

                    with c_a2:
                        if st.button("🤖 智能预审"):
                            if u_input:
                                with st.spinner("DeepSeek Scanning..."):
                                    res = AIService.student_pre_review(curr_t[3], u_input)
                                    st.session_state[f"fb_{curr_t[0]}"] = res
                            else: st.warning("请先输入文本。")
                        
                        fb_display = st.session_state.get(f"fb_{curr_t[0]}", my_sub[5] if my_sub else None)
                        if fb_display: st.info(f"AI反馈: {fb_display}")

    elif nav == "个人档案":
        c1, c2 = st.columns([1, 2])
        with c1:
            render_lottie("robot.json", height=250, key="profile")
            st.metric("Access ID", user); st.metric("Role", "Student Unit")
        with c2:
            st.subheader("能力矩阵")
            recent_score = None
            all_tasks = st.session_state.db.get_all_tasks()
            for t in all_tasks:
                s = st.session_state.db.get_my_submission(t[0], user)
                if s and s[6]: recent_score = s[6]; break
            render_radar_chart(recent_score)
            if not recent_score: st.caption("完成作业以激活数据。")

# ==========================================
# 🚀 启动器
# ==========================================
def main():
    setup_page()
    init_session()
    if st.session_state.logged_in:
        if st.session_state.user_info['role'] == 'teacher': teacher_dashboard()
        else: student_dashboard()
    else: landing_page()

if __name__ == "__main__":
    main()