from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Course, Favorite

content_bp = Blueprint('content', __name__)

@content_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('content.chat'))
    return render_template('index.html')

@content_bp.route('/chat')
@login_required
def chat():
    chat_url = "http://180.85.206.30:3000/chat/share?shareId=rrc0cvrtg9kl80bgl3mz9778"
    return render_template('chat.html', chat_url=chat_url)

@content_bp.route('/courses')
@login_required
def courses():
    all_courses = Course.query.all()
    user_favorites = [fav.course_id for fav in current_user.favorites]
    return render_template('courses.html', courses=all_courses, user_favorites=user_favorites)

@content_bp.route('/course/<int:course_id>')
@login_required
def view_course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_view.html', course=course)

@content_bp.route('/favorites')
@login_required
def favorites():
    user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    favorite_courses = [fav.course for fav in user_favorites]
    return render_template('favorites.html', favorite_courses=favorite_courses)

@content_bp.route('/favorite/<int:course_id>', methods=['POST'])
@login_required
def add_favorite(course_id):
    course = Course.query.get_or_404(course_id)
    
    # 检查是否已经收藏
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).first()
    
    if existing_favorite:
        flash('您已经收藏过这个课程了', 'info')
    else:
        favorite = Favorite(user_id=current_user.id, course_id=course_id)
        db.session.add(favorite)
        db.session.commit()
        flash('收藏成功', 'success')
    
    return redirect(url_for('content.courses'))

@content_bp.route('/unfavorite/<int:course_id>', methods=['POST'])
@login_required
def remove_favorite(course_id):
    favorite = Favorite.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).first_or_404()
    
    db.session.delete(favorite)
    db.session.commit()
    flash('已取消收藏', 'success')
    
    return redirect(url_for('content.favorites'))