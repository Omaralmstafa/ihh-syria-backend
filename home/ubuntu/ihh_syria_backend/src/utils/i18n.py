"""
Internationalization (i18n) support for Arabic, English, and Turkish
"""
from flask import request

# Translation dictionaries
translations = {
    'ar': {
        'user_not_found': 'المستخدم غير موجود',
        'update_success': 'تم التحديث بنجاح',
        'no_permission': 'ليس لديك صلاحية',
        'file_uploaded': 'تم رفع الملف بنجاح',
        'file_not_supported': 'نوع الملف غير مدعوم',
        'profile_image_updated': 'تم تحديث صورة المستخدم بنجاح',
        'image_path_required': 'مسار الصورة مطلوب',
        'user_created': 'تم إنشاء الحساب بنجاح',
        'login_success': 'تم تسجيل الدخول بنجاح',
        'invalid_credentials': 'البريد الإلكتروني أو كلمة المرور غير صحيحة',
        'account_inactive': 'الحساب غير نشط',
        'password_changed': 'تم تغيير كلمة المرور بنجاح',
        'post_created': 'تم إنشاء المنشور بنجاح',
        'post_deleted': 'تم حذف المنشور بنجاح',
        'office_created': 'تم إنشاء المكتب بنجاح',
        'office_updated': 'تم تحديث المكتب بنجاح',
    },
    'en': {
        'user_not_found': 'User not found',
        'update_success': 'Updated successfully',
        'no_permission': 'You do not have permission',
        'file_uploaded': 'File uploaded successfully',
        'file_not_supported': 'File type not supported',
        'profile_image_updated': 'Profile image updated successfully',
        'image_path_required': 'Image path is required',
        'user_created': 'Account created successfully',
        'login_success': 'Login successful',
        'invalid_credentials': 'Invalid email or password',
        'account_inactive': 'Account is inactive',
        'password_changed': 'Password changed successfully',
        'post_created': 'Post created successfully',
        'post_deleted': 'Post deleted successfully',
        'office_created': 'Office created successfully',
        'office_updated': 'Office updated successfully',
    },
    'tr': {
        'user_not_found': 'Kullanıcı bulunamadı',
        'update_success': 'Başarıyla güncellendi',
        'no_permission': 'İzin yok',
        'file_uploaded': 'Dosya başarıyla yüklendi',
        'file_not_supported': 'Dosya türü desteklenmiyor',
        'profile_image_updated': 'Profil resmi başarıyla güncellendi',
        'image_path_required': 'Resim yolu gerekli',
        'user_created': 'Hesap başarıyla oluşturuldu',
        'login_success': 'Giriş başarılı',
        'invalid_credentials': 'Geçersiz e-posta veya şifre',
        'account_inactive': 'Hesap aktif değil',
        'password_changed': 'Şifre başarıyla değiştirildi',
        'post_created': 'Gönderi başarıyla oluşturuldu',
        'post_deleted': 'Gönderi başarıyla silindi',
        'office_created': 'Ofis başarıyla oluşturuldu',
        'office_updated': 'Ofis başarıyla güncellendi',
    }
}

def get_language():
    """Get language from request header or default to Arabic"""
    lang = request.headers.get('Accept-Language', 'ar')
    # Extract language code (e.g., 'ar', 'en', 'tr')
    if lang.startswith('ar'):
        return 'ar'
    elif lang.startswith('en'):
        return 'en'
    elif lang.startswith('tr'):
        return 'tr'
    return 'ar'  # Default to Arabic

def translate(key, lang=None):
    """Translate a key to the specified language"""
    if lang is None:
        lang = get_language()
    
    return translations.get(lang, translations['ar']).get(key, key)

def get_translations(lang=None):
    """Get all translations for a language"""
    if lang is None:
        lang = get_language()
    
    return translations.get(lang, translations['ar'])

