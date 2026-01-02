from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, Office

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        # Filter users based on role permissions
        if current_user.role == 'general_manager':
            users = User.query.all()
        elif current_user.role == 'office_manager':
            users = User.query.filter_by(office_id=current_user.office_id).all()
        elif current_user.role == 'section_manager':
            users = User.query.filter(
                User.office_id == current_user.office_id,
                User.department == current_user.department
            ).all()
        else:
            users = [current_user]  # Volunteers can only see themselves
        
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        # Check permissions
        can_view = False
        if current_user.role == 'general_manager':
            can_view = True
        elif current_user.role == 'office_manager' and user.office_id == current_user.office_id:
            can_view = True
        elif current_user.role == 'section_manager' and user.office_id == current_user.office_id and user.department == current_user.department:
            can_view = True
        elif current_user.id == user.id:
            can_view = True
        
        if not can_view:
            return jsonify({'error': 'ليس لديك صلاحية لعرض هذا المستخدم'}), 403
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        # Check permissions
        can_edit = False
        if current_user.role == 'general_manager':
            can_edit = True
        elif current_user.role == 'office_manager' and user.office_id == current_user.office_id:
            can_edit = True
        elif current_user.id == user.id:
            can_edit = True
        
        if not can_edit:
            return jsonify({'error': 'ليس لديك صلاحية لتعديل هذا المستخدم'}), 403
        
        data = request.get_json()
        
        # Update allowed fields - volunteers can update their own profile
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'gender' in data:
            user.gender = data['gender']
        if 'birth_date' in data:
            from datetime import datetime
            try:
                user.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except:
                pass
        if 'current_residence' in data:
            user.current_residence = data['current_residence']
        if 'original_country' in data:
            user.original_country = data['original_country']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'university' in data:
            user.university = data['university']
        if 'major' in data:
            user.major = data['major']
        if 'academic_year' in data:
            user.academic_year = data['academic_year']
        if 'previous_organizations' in data:
            user.previous_organizations = data['previous_organizations']
        if 'skills' in data:
            user.skills = data['skills']
        if 'previous_work' in data:
            user.previous_work = data['previous_work']
        if 'currently_working' in data:
            user.currently_working = data['currently_working']
        if 'volunteer_organization' in data:
            user.volunteer_organization = data['volunteer_organization']
        if 'available_for_volunteering' in data:
            user.available_for_volunteering = data['available_for_volunteering']
        if 'team_role' in data:
            user.team_role = data['team_role']
        if 'department' in data:
            user.department = data['department']
        if 'profile_image_url' in data:
            user.profile_image_url = data['profile_image_url']
        
        # Only managers can update role and office
        if current_user.role in ['general_manager', 'office_manager']:
            if 'role' in data:
                user.role = data['role']
            if 'office_id' in data:
                user.office_id = data['office_id']
            if 'points' in data:
                user.points = data['points']
            if 'rating' in data:
                user.rating = data['rating']
            if 'is_active' in data:
                user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث المستخدم بنجاح',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        query = request.args.get('q', '')
        role_filter = request.args.get('role', '')
        office_filter = request.args.get('office_id', '')
        
        # Base query based on permissions
        if current_user.role == 'general_manager':
            users_query = User.query
        elif current_user.role == 'office_manager':
            users_query = User.query.filter_by(office_id=current_user.office_id)
        elif current_user.role == 'section_manager':
            users_query = User.query.filter(
                User.office_id == current_user.office_id,
                User.department == current_user.department
            )
        else:
            users_query = User.query.filter_by(id=current_user.id)
        
        # Apply filters
        if query:
            users_query = users_query.filter(
                User.full_name.contains(query) | User.email.contains(query)
            )
        
        if role_filter:
            users_query = users_query.filter_by(role=role_filter)
        
        if office_filter:
            users_query = users_query.filter_by(office_id=int(office_filter))
        
        users = users_query.all()
        
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>/profile-image', methods=['POST'])
@jwt_required()
def update_profile_image(user_id):
    """Update user profile image"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'المستخدم غير موجود'}), 404
        
        # Check permissions - user can update their own image or managers can update any
        can_edit = (
            current_user.id == user.id or
            current_user.role in ['general_manager', 'office_manager']
        )
        
        if not can_edit:
            return jsonify({'error': 'ليس لديك صلاحية لتعديل صورة هذا المستخدم'}), 403
        
        data = request.get_json()
        
        if 'profile_image_url' not in data:
            return jsonify({'error': 'مسار الصورة مطلوب'}), 400
        
        user.profile_image_url = data['profile_image_url']
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث صورة المستخدم بنجاح',
            'profile_image_url': user.profile_image_url,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

