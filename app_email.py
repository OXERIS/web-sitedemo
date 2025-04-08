from flask import Flask, request, render_template, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import email_verification  # 引入邮箱验证模块

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 用于加密 session 和闪现消息

# 获取数据库连接
def get_db_connection():
    """
    创建与 SQLite 数据库的连接，设置 row_factory 以便通过列名访问数据
    """
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# 首页路由
@app.route('/')
def home():
    """
    显示网站的首页
    """
    return render_template('index.html')

# 邮箱验证码发送请求
@app.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    """
    接收用户输入的邮箱，生成验证码并发送验证邮件
    """
    email = request.form['email']
    
    # 检查邮箱是否已注册
    conn = get_db_connection()
    existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    if existing_user:
        flash('该邮箱已注册，请直接登录或使用忘记密码功能')
        print(f"邮箱 {email} 已注册", flush=True)  # 强制输出调试信息
        return redirect(url_for('login'))  # 如果邮箱已存在，重定向到登录页面

    # 生成验证码
    code = email_verification.generate_verification_code()

    # 保存验证码到数据库
    email_verification.store_verification_code(email, code)

    # 发送验证码邮件
    try:
        email_verification.send_verification_email(email, code)  # 发送验证码邮件
        print(f"验证码发送给 {email}", flush=True)  # 强制输出调试信息
        flash('验证码已发送，请检查您的邮箱')
    except Exception as e:
        print(f"验证码发送失败: {e}", flush=True)  # 打印错误并强制输出调试信息
        flash(f'验证码发送失败，请稍后再试。错误信息: {str(e)}')
        return redirect(url_for('register'))  # 如果邮件发送失败，返回注册页面

    return redirect(url_for('register'))  # 邮件发送成功后返回注册页面

# 用户注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    处理用户注册流程，验证验证码，允许用户继续填写用户名和密码
    """
    if request.method == 'POST':
        email = request.form['email']
        user_code = request.form['verification_code']

        # 验证用户输入的验证码是否正确且未过期
        if not email_verification.verify_code(email, user_code):
            flash('验证码错误或已过期，请重新获取验证码')  # 验证失败提示
            return redirect(url_for('register'))

        # 验证通过，继续处理其他注册信息
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 检查密码是否一致
        if password != confirm_password:
            flash('两次输入的密码不一致，请重新输入')  # 密码不一致提示
            return redirect(url_for('register'))

        # 加密密码并保存到数据库
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # 加密密码

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:  # 如果用户已存在
            flash('该邮箱已注册，请直接登录！')
            return redirect(url_for('login'))

        # 插入新用户数据
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash('注册成功，请登录！')
        return redirect(url_for('login'))

    return render_template('register.html')

# 用户登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    处理用户登录逻辑，验证邮箱和密码
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']

        if not email or not password:
            flash('请输入电子邮件和密码')
            return redirect(url_for('login'))

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        # 检查用户是否存在以及密码是否正确
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']  # 保存用户登录状态
            session['username'] = user['username']
            flash(f'登录成功！欢迎, {user["username"]}')
            return redirect(url_for('home'))  # 成功登录后重定向到首页
        else:
            flash('登录失败，邮箱或密码错误！')
            return redirect(url_for('login'))

    return render_template('login.html')

# 用户登出路由
@app.route('/logout')
def logout():
    """
    处理用户登出逻辑，清除 session 数据
    """
    session.clear()  # 清除用户会话状态
    flash('您已成功登出！')
    return redirect(url_for('home'))

# 用户个人信息页面路由
@app.route('/profile')
def profile():
    """
    显示用户个人信息页面，确保用户已登录
    """
    if 'user_id' not in session:  # 如果用户未登录，重定向到登录页面
        flash('请先登录')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user:  # 如果用户存在，渲染个人信息页面
        return render_template('profile.html', user=user)
    else:
        flash('用户信息不存在')
        return redirect(url_for('home'))

# 编辑个人信息页面路由
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
    允许用户编辑其个人信息，确保用户已登录
    """
    if 'user_id' not in session:
        flash('请先登录')
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    if request.method == 'POST':  # 处理表单提交
        fullname = request.form.get('fullname')
        phone = request.form.get('phone')
        address = request.form.get('address')
        birthdate = request.form.get('birthdate')
        bio = request.form.get('bio')

        # 更新用户信息
        conn.execute('UPDATE users SET fullname = ?, phone = ?, address = ?, birthdate = ?, bio = ? WHERE id = ?',
                     (fullname, phone, address, birthdate, bio, user_id))
        conn.commit()
        conn.close()

        flash('信息已更新')
        return redirect(url_for('profile'))

    conn.close()
    return render_template('edit_profile.html', user=user)

# 案例展示页面
@app.route('/case_page', endpoint='case_page')
def case_page():
    """
    渲染案例展示页面
    """
    return render_template('case.html')

# 问卷填写页面路由
@app.route('/form')
def form():
    # 检查 session 中是否有登录信息
    if 'username' not in session:
        # 如果用户未登录，重定向到登录页面
        flash("请先登录以填写问卷")
        return redirect(url_for('login'))
    
    # 如果用户已登录，渲染问卷页面
    return render_template('form.html')

# 启动应用程序
if __name__ == '__main__':
    # 确保用户表已创建
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        fullname TEXT,
        phone TEXT,
        address TEXT,
        birthdate TEXT,
        bio TEXT
    )''')
    conn.commit()
    conn.close()
    app.run(debug=True)
