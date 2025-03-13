from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, UserInfo
from werkzeug.urls import url_parse

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('content.chat'))
    
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        
        user = UserInfo.query.filter_by(UID=uid).first()
        
        if user is None or not user.check_password(password):
            flash('学号或密码不正确', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('content.chat')
        return redirect(next_page)
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('content.chat'))
    
    if request.method == 'POST':
        uid = request.form.get('uid')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return redirect(url_for('auth.register'))
        
        existing_user = UserInfo.query.filter_by(UID=uid).first()
        if existing_user:
            flash('该学号已被注册', 'danger')
            return redirect(url_for('auth.register'))
        
        user = UserInfo(UID=uid, UName=uid)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))