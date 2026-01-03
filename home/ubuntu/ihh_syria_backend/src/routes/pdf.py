"""
PDF Generation Routes with Arabic support
"""
from flask import Blueprint, request, jsonify, send_file, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.utils.i18n import get_language, translate
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

pdf_bp = Blueprint('pdf', __name__)

# Register Arabic font (you need to have a font file that supports Arabic)
# For production, you should include a font file like Arial Unicode MS or Noto Sans Arabic
ARABIC_FONT_PATH = None  # Set this to your Arabic font file path if available

def register_arabic_font():
    """Register Arabic font if available"""
    if ARABIC_FONT_PATH and os.path.exists(ARABIC_FONT_PATH):
        try:
            pdfmetrics.registerFont(TTFont('Arabic', ARABIC_FONT_PATH))
            return True
        except:
            pass
    return False

def create_user_pdf(user, lang='ar'):
    """Create PDF for user profile"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Register Arabic font if available
    has_arabic_font = register_arabic_font()
    font_name = 'Arabic' if has_arabic_font else 'Helvetica'
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        fontName=font_name if has_arabic_font else 'Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12,
        fontName=font_name if has_arabic_font else 'Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        spaceAfter=6,
        fontName=font_name if has_arabic_font else 'Helvetica'
    )
    
    # Title
    if lang == 'ar':
        title = f"<b>ملف المتطوع: {user.full_name}</b>"
    elif lang == 'tr':
        title = f"<b>Gönüllü Dosyası: {user.full_name}</b>"
    else:
        title = f"<b>Volunteer Profile: {user.full_name}</b>"
    
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    # User Information Table
    data = []
    
    if lang == 'ar':
        fields = [
            ('البريد الإلكتروني', user.email or ''),
            ('الاسم الكامل', user.full_name or ''),
            ('الجنس', user.gender or ''),
            ('تاريخ الميلاد', str(user.birth_date) if user.birth_date else ''),
            ('مكان الإقامة الحالي', user.current_residence or ''),
            ('البلد الأصلي', user.original_country or ''),
            ('رقم الهاتف', user.phone_number or ''),
            ('الجامعة', user.university or ''),
            ('التخصص', user.major or ''),
            ('السنة الدراسية', user.academic_year or ''),
            ('المهارات', user.skills or ''),
            ('الدور', user.role or ''),
            ('النقاط', str(user.points)),
            ('التقييم', str(user.rating)),
        ]
    elif lang == 'tr':
        fields = [
            ('E-posta', user.email or ''),
            ('Ad Soyad', user.full_name or ''),
            ('Cinsiyet', user.gender or ''),
            ('Doğum Tarihi', str(user.birth_date) if user.birth_date else ''),
            ('Mevcut İkamet', user.current_residence or ''),
            ('Orijinal Ülke', user.original_country or ''),
            ('Telefon', user.phone_number or ''),
            ('Üniversite', user.university or ''),
            ('Bölüm', user.major or ''),
            ('Akademik Yıl', user.academic_year or ''),
            ('Yetenekler', user.skills or ''),
            ('Rol', user.role or ''),
            ('Puanlar', str(user.points)),
            ('Değerlendirme', str(user.rating)),
        ]
    else:  # English
        fields = [
            ('Email', user.email or ''),
            ('Full Name', user.full_name or ''),
            ('Gender', user.gender or ''),
            ('Birth Date', str(user.birth_date) if user.birth_date else ''),
            ('Current Residence', user.current_residence or ''),
            ('Original Country', user.original_country or ''),
            ('Phone Number', user.phone_number or ''),
            ('University', user.university or ''),
            ('Major', user.major or ''),
            ('Academic Year', user.academic_year or ''),
            ('Skills', user.skills or ''),
            ('Role', user.role or ''),
            ('Points', str(user.points)),
            ('Rating', str(user.rating)),
        ]
    
    for label, value in fields:
        if value:
            data.append([Paragraph(f"<b>{label}</b>", normal_style), Paragraph(str(value), normal_style)])
    
    if data:
        table = Table(data, colWidths=[60*mm, 120*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), font_name if has_arabic_font else 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), font_name if has_arabic_font else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

@pdf_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def generate_user_pdf(user_id):
    """Generate PDF for user profile"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': translate('user_not_found')}), 404
        
        # Check permissions
        can_view = (
            current_user.role == 'general_manager' or
            current_user.id == user.id or
            (current_user.role == 'office_manager' and user.office_id == current_user.office_id)
        )
        
        if not can_view:
            return jsonify({'error': translate('no_permission')}), 403
        
        # Get language from request
        lang = request.args.get('lang', get_language())
        if lang not in ['ar', 'en', 'tr']:
            lang = 'ar'
        
        # Generate PDF
        pdf_buffer = create_user_pdf(user, lang)
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=user_{user_id}_{lang}.pdf'
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


