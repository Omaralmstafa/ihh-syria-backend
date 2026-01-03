from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from src.models.user import db, User, Post, PostLike
import os
import uuid

media_bp = Blueprint('media', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'wmv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in {'png', 'jpg', 'jpeg', 'gif'}:
        return 'image'
    elif ext in {'mp4', 'avi', 'mov', 'wmv'}:
        return 'video'
    return 'unknown'

@media_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Check if user can upload media
        if current_user.role not in ['general_manager', 'office_manager']:
            return jsonify({'error': 'ليس لديك صلاحية لرفع الوسائط'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            from flask import current_app
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Get file type
            file_type = get_file_type(filename)
            
            file_url = f"/api/media/files/{unique_filename}"
            
            return jsonify({
                'message': 'تم رفع الملف بنجاح',
                'file_url': file_url,
                'file_type': file_type,
                'filename': unique_filename
            }), 200
        
        return jsonify({'error': 'نوع الملف غير مدعوم'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@media_bp.route('/files/<filename>')
def uploaded_file(filename):
    from flask import current_app
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@media_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Check if user can create posts
        if current_user.role not in ['general_manager', 'office_manager']:
            return jsonify({'error': 'ليس لديك صلاحية لإنشاء منشورات'}), 403
        
        data = request.get_json()
        
        post = Post(
            title=data['title'],
            content=data['content'],
            author_id=current_user.id,
            media_type=data.get('media_type'),
            media_url=data.get('media_url'),
            is_public=(current_user.role == 'general_manager'),
            office_id=current_user.office_id if current_user.role == 'office_manager' else None
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء المنشور بنجاح',
            'post': post.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@media_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Get posts based on user role and office
        if current_user.role == 'general_manager':
            # General manager sees all posts
            posts = Post.query.order_by(Post.created_at.desc()).all()
        else:
            # Other users see public posts and posts from their office
            posts = Post.query.filter(
                (Post.is_public == True) | 
                (Post.office_id == current_user.office_id)
            ).order_by(Post.created_at.desc()).all()
        
        return jsonify({
            'posts': [post.to_dict() for post in posts]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@media_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    try:
        current_user_id = get_jwt_identity()
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'المنشور غير موجود'}), 404
        
        # Check if user already liked this post
        existing_like = PostLike.query.filter_by(
            user_id=current_user_id,
            post_id=post_id
        ).first()
        
        if existing_like:
            # Unlike the post
            db.session.delete(existing_like)
            post.likes_count -= 1
            action = 'unliked'
        else:
            # Like the post
            like = PostLike(user_id=current_user_id, post_id=post_id)
            db.session.add(like)
            post.likes_count += 1
            action = 'liked'
        
        db.session.commit()
        
        return jsonify({
            'message': f'تم {action} المنشور',
            'likes_count': post.likes_count,
            'action': action
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@media_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({'error': 'المنشور غير موجود'}), 404
        
        # Check if user can delete this post
        can_delete = (
            post.author_id == current_user_id or
            current_user.role == 'general_manager' or
            (current_user.role == 'office_manager' and post.office_id == current_user.office_id)
        )
        
        if not can_delete:
            return jsonify({'error': 'ليس لديك صلاحية لحذف هذا المنشور'}), 403
        
        # Delete associated likes
        PostLike.query.filter_by(post_id=post_id).delete()
        
        # Delete the post
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({'message': 'تم حذف المنشور بنجاح'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

