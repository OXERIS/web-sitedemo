import random
import smtplib
from email.mime.text import MIMEText
from flask import flash
import sqlite3

# 获取数据库连接
def get_db_connection():
    """
    创建与 SQLite 数据库的连接，设置 row_factory 以便通过列名访问数据
    """
    conn = sqlite3.connect('users.db')  # 连接到名为 'users.db' 的数据库
    conn.row_factory = sqlite3.Row  # 设置为字典式访问行数据
    return conn

# 生成验证码
def generate_verification_code():
    """
    生成一个6位数的随机验证码
    """
    return str(random.randint(100000, 999999))  # 生成6位验证码

# 发送验证码邮件
def send_verification_email(email, code):
    """
    使用Gmail SMTP服务器发送带有验证码的电子邮件，并记录日志
    """
    # 构建电子邮件内容
    msg = MIMEText(f"您的验证码是：{code}")  # 邮件内容为发送验证码
    msg['Subject'] = '验证码'  # 邮件主题
    msg['From'] = 'thegodofoxeris@gmail.com'  # 发送者邮箱
    msg['To'] = email  # 接收者邮箱

    # Gmail SMTP 服务器配置
    smtp_server = 'smtp.gmail.com'  # Gmail SMTP 服务器
    smtp_port = 587  # 使用端口 587
    smtp_user = 'thegodofoxeris@gmail.com'  # 你的 Gmail 地址
    smtp_password = 'mzhh vtub lqrb rzto'  # 使用应用专用密码

    try:
        # 连接到 SMTP 服务器并发送邮件
        print(f"正在连接到 SMTP 服务器: {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用 TLS 加密
        print("连接到 SMTP 服务器成功，开始登录...")
        server.login(smtp_user, smtp_password)  # 登录 Gmail
        print("登录成功，正在发送邮件...")
        server.send_message(msg)  # 发送邮件
        server.quit()  # 断开连接
        print("验证码邮件发送成功")
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP 认证错误: {e}")  # 打印认证错误信息
        flash('发送验证码失败，请检查 SMTP 配置或 Gmail 账户设置')
    except Exception as e:
        print(f"验证码邮件发送失败: {e}")  # 打印其他异常信息
        flash('发送验证码失败，请稍后再试')

# 存储验证码到数据库
def store_verification_code(email, code):
    """
    将生成的验证码和邮箱地址存储到数据库中
    """
    conn = get_db_connection()  # 获取数据库连接
    # 插入验证码和对应邮箱
    conn.execute('INSERT INTO email_verification (email, code) VALUES (?, ?)', (email, code))
    conn.commit()  # 提交事务
    conn.close()  # 关闭连接

# 验证用户输入的验证码
def verify_code(email, user_code):
    """
    检查用户输入的验证码是否与数据库中匹配
    """
    conn = get_db_connection()  # 获取数据库连接
    # 检查数据库中是否存在匹配的验证码
    record = conn.execute('SELECT * FROM email_verification WHERE email = ? AND code = ?', (email, user_code)).fetchone()
    conn.close()  # 关闭连接
    if record:  # 如果找到匹配记录
        return True  # 验证码正确
    else:
        flash('验证码不正确或已过期')  # 如果验证码不匹配或已过期，显示错误消息
        return False
