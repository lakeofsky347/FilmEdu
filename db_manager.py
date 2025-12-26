import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_name="film_edu.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      teacher_id TEXT, title TEXT, content TEXT, created_at TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS submissions 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      task_id INTEGER, student_id TEXT, content TEXT, file_path TEXT,
                      ai_feedback TEXT, grade TEXT, teacher_comment TEXT, status TEXT)''')
        self.conn.commit()

    # --- 用户逻辑 ---
    def register(self, username, password, role):
        try:
            self.conn.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):
        cur = self.conn.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        return row[0] if row else None

    # --- 教师逻辑 ---
    def create_task(self, teacher, title, content):
        # 检查该老师是否已经发布过同名任务
        check = self.conn.execute("SELECT id FROM tasks WHERE teacher_id=? AND title=?", (teacher, title)).fetchone()
        if check:
            return False # 任务已存在，返回失败

        self.conn.execute("INSERT INTO tasks (teacher_id, title, content, created_at) VALUES (?, ?, ?, ?)",
                          (teacher, title, content, datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.conn.commit()
        return True # 创建成功

    def get_teacher_tasks(self, teacher):
        return self.conn.execute("SELECT * FROM tasks WHERE teacher_id=?", (teacher,)).fetchall()

    def get_submissions(self, task_id):
        return self.conn.execute("SELECT * FROM submissions WHERE task_id=?", (task_id,)).fetchall()

    def grade_submission(self, sub_id, grade, comment):
        self.conn.execute("UPDATE submissions SET grade=?, teacher_comment=?, status='graded' WHERE id=?", 
                          (grade, comment, sub_id))
        self.conn.commit()

    # --- 学生逻辑 ---
    def get_all_tasks(self):
        return self.conn.execute("SELECT * FROM tasks").fetchall()

    def get_my_submission(self, task_id, student_id):
        return self.conn.execute("SELECT * FROM submissions WHERE task_id=? AND student_id=?", 
                                 (task_id, student_id)).fetchone()

    def submit_work(self, task_id, student_id, content, file_path, ai_feedback):
        exists = self.get_my_submission(task_id, student_id)
        if exists:
            # 更新时，如果新上传了文件(file_path不为空)，则更新路径；否则保留原路径
            if file_path:
                self.conn.execute("UPDATE submissions SET content=?, file_path=?, ai_feedback=?, status='submitted' WHERE id=?",
                                  (content, file_path, ai_feedback, exists[0]))
            else:
                self.conn.execute("UPDATE submissions SET content=?, ai_feedback=?, status='submitted' WHERE id=?",
                                  (content, ai_feedback, exists[0]))
        else:
            self.conn.execute("INSERT INTO submissions (task_id, student_id, content, file_path, ai_feedback, status) VALUES (?, ?, ?, ?, ?, 'submitted')",
                              (task_id, student_id, content, file_path, ai_feedback))
        self.conn.commit()