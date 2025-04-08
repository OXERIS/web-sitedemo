from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用于闪现消息

# 创建数据库连接
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# 创建数据库表
def create_user_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# 首页
@app.route('/')
def home():
    return render_template('index.html')

# 注册用户
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 处理注册表单的提交
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 密码加密
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        # 检查用户是否已存在
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            flash('用户已存在，请直接登录！')
            return redirect(url_for('home'))

        # 插入用户数据
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash('注册成功，请登录！')
        return redirect(url_for('home'))
    
    # 如果是 GET 请求，显示注册页面
    return render_template('register.html')

# 用户登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']

        if not email or not password:
            flash('请输入电子邮件和密码')
            return redirect(url_for('login'))

    

        # 从数据库中查询用户
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user:
            # 验证密码是否正确
            if check_password_hash(user['password'], password):
                flash('登录成功！')
                return redirect(url_for('home'))
            else:
                flash('密码错误，请重试！')
        else:
            flash('用户不存在，请先注册！')

        return redirect(url_for('login'))

    return render_template('login.html')


#案例页面
@app.route('/case_page', endpoint='case_page')
def case_page():
    return render_template('case.html')

#问卷页面
@app.route('/form')
def form():
    return render_template('form.html')


# 运行应用
if __name__ == '__main__':
    create_user_table()  # 确保数据库和表存在
    app.run(debug=True)
