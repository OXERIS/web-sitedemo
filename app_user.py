from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 设置用于闪现消息和 session 的密钥

# 获取数据库连接的函数
def get_db_connection():
    conn = sqlite3.connect('users.db')  # 连接到SQLite数据库
    conn.row_factory = sqlite3.Row  # 设置行工厂，使得查询结果可以通过列名访问
    return conn

# 确保用户表存在，如果不存在则创建该表
def create_user_table():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# 首页路由
@app.route('/')
def home():
    return render_template('index.html')  # 渲染首页

# 用户注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:  # 检查是否已存在
            flash('用户已存在，请直接登录！')
            return redirect(url_for('home'))

        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash('注册成功，请登录！')
        return redirect(url_for('home'))
    
    return render_template('register.html')

# 用户登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form['password']

        if not email or not password:
            flash('请输入电子邮件和密码')
            return redirect(url_for('login'))

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

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
    session.clear()  # 清除用户会话状态
    flash('您已成功登出！')
    return redirect(url_for('home'))



# 用户个人信息页面路由，确保用户已登录
@app.route('/profile')
def profile():
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



@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:  # 确保用户已登录
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
    return render_template('case.html')

# 问卷填写页面
@app.route('/form')
def form():
    return render_template('form.html')

# 启动应用程序
if __name__ == '__main__':
    create_user_table()  # 启动时确保数据库表已创建
    app.run(debug=True)  # 运行应用
