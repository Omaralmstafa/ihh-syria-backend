from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    current_residence = db.Column(db.String(100), nullable=True)
    original_country = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    university = db.Column(db.String(100), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(50), nullable=True)
    previous_organizations = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    previous_work = db.Column(db.Text, nullable=True)
    currently_working = db.Column(db.Boolean, default=False)
    volunteer_organization = db.Column(db.String(100), nullable=True)
    available_for_volunteering = db.Column(db.Boolean, default=True)
    team_role = db.Column(db.String(50), nullable=True)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(50), default='volunteer')  # volunteer, section_manager, office_manager, general_manager
    points = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    profile_image_url = db.Column(db.String(500), nullable=True)  # Profile image URL
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    office = db.relationship("Office", backref="users", foreign_keys=lambda: User.office_id)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == self.password_hash
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'current_residence': self.current_residence,
            'original_country': self.original_country,
            'phone_number': self.phone_number,
            'university': self.university,
            'major': self.major,
            'academic_year': self.academic_year,
            'previous_organizations': self.previous_organizations,
            'skills': self.skills,
            'previous_work': self.previous_work,
            'currently_working': self.currently_working,
            'volunteer_organization': self.volunteer_organization,
            'available_for_volunteering': self.available_for_volunteering,
            'team_role': self.team_role,
            'office_id': self.office_id,
            'office_name': self.office.name if self.office else None,
            'department': self.department,
            'role': self.role,
            'points': self.points,
            'rating': self.rating,
            'profile_image_url': self.profile_image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('User', foreign_keys=[manager_id], post_update=True)
    posts = db.relationship('Post', backref='office', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'manager_id': self.manager_id,
            'manager_name': self.manager.full_name if self.manager else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'user_count': len(self.users)
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'), nullable=True)
    media_type = db.Column(db.String(20), nullable=True)  # image, video, none
    media_url = db.Column(db.String(500), nullable=True)
    is_public = db.Column(db.Boolean, default=False)  # True for general manager posts
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author_name': self.author.full_name,
            'office_id': self.office_id,
            'office_name': self.office.name if self.office else None,
            'media_type': self.media_type,
            'media_url': self.media_url,
            'is_public': self.is_public,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate likes
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)

