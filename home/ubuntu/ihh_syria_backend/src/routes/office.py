from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User, Office

office_bp = Blueprint('offices', __name__)

@office_bp.route('/', methods=['GET'])
def get_offices():
    try:
        offices = Office.query.filter_by(is_active=True).all()
        return jsonify({
            'offices': [office.to_dict() for office in offices]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@office_bp.route('/', methods=['POST'])
@jwt_required()
def create_office():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Only general manager can create offices
        if current_user.role != 'general_manager':
            return jsonify({'error': 'ليس لديك صلاحية لإنشاء مكاتب'}), 403
        
        data = request.get_json()
        
        office = Office(
            name=data['name'],
            location=data.get('location'),
            description=data.get('description'),
            manager_id=data.get('manager_id')
        )
        
        db.session.add(office)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء المكتب بنجاح',
            'office': office.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@office_bp.route('/<int:office_id>', methods=['GET'])
@jwt_required()
def get_office(office_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        office = Office.query.get(office_id)
        
        if not office:
            return jsonify({'error': 'المكتب غير موجود'}), 404
        
        # Check permissions
        can_view = (
            current_user.role == 'general_manager' or
            current_user.office_id == office_id
        )
        
        if not can_view:
            return jsonify({'error': 'ليس لديك صلاحية لعرض هذا المكتب'}), 403
        
        return jsonify({'office': office.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@office_bp.route('/<int:office_id>', methods=['PUT'])
@jwt_required()
def update_office(office_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        office = Office.query.get(office_id)
        
        if not office:
            return jsonify({'error': 'المكتب غير موجود'}), 404
        
        # Check permissions
        can_edit = (
            current_user.role == 'general_manager' or
            (current_user.role == 'office_manager' and current_user.office_id == office_id)
        )
        
        if not can_edit:
            return jsonify({'error': 'ليس لديك صلاحية لتعديل هذا المكتب'}), 403
        
        data = request.get_json()
        
        if 'name' in data:
            office.name = data['name']
        if 'location' in data:
            office.location = data['location']
        if 'description' in data:
            office.description = data['description']
        
        # Only general manager can change manager
        if current_user.role == 'general_manager' and 'manager_id' in data:
            office.manager_id = data['manager_id']
        
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث المكتب بنجاح',
            'office': office.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@office_bp.route('/<int:office_id>/users', methods=['GET'])
@jwt_required()
def get_office_users(office_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        office = Office.query.get(office_id)
        
        if not office:
            return jsonify({'error': 'المكتب غير موجود'}), 404
        
        # Check permissions
        can_view = (
            current_user.role == 'general_manager' or
            current_user.office_id == office_id
        )
        
        if not can_view:
            return jsonify({'error': 'ليس لديك صلاحية لعرض مستخدمي هذا المكتب'}), 403
        
        users = User.query.filter_by(office_id=office_id).all()
        
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@office_bp.route('/<int:office_id>/stats', methods=['GET'])
@jwt_required()
def get_office_stats(office_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        office = Office.query.get(office_id)
        
        if not office:
            return jsonify({'error': 'المكتب غير موجود'}), 404
        
        # Check permissions
        can_view = (
            current_user.role == 'general_manager' or
            current_user.office_id == office_id
        )
        
        if not can_view:
            return jsonify({'error': 'ليس لديك صلاحية لعرض إحصائيات هذا المكتب'}), 403
        
        users = User.query.filter_by(office_id=office_id).all()
        
        stats = {
            'total_users': len(users),
            'volunteers': len([u for u in users if u.role == 'volunteer']),
            'section_managers': len([u for u in users if u.role == 'section_manager']),
            'office_managers': len([u for u in users if u.role == 'office_manager']),
            'total_points': sum(u.points for u in users),
            'average_rating': sum(u.rating for u in users) / len(users) if users else 0,
            'active_users': len([u for u in users if u.is_active])
        }
        
        return jsonify({'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

