# سجل التحديثات - Changelog

## التحديثات الجديدة (Latest Updates)

### ✅ 1. تحسين تعديل بيانات المتطوع
- **تم تحديث**: `PUT /api/users/<user_id>`
- **المميزات الجديدة**:
  - يمكن للمتطوع تعديل جميع بياناته الشخصية من الواجهة الأمامية
  - دعم تحديث جميع الحقول: الاسم، الجنس، تاريخ الميلاد، العنوان، الهاتف، الجامعة، التخصص، المهارات، إلخ
  - المتطوعون يمكنهم تحديث بياناتهم الخاصة
  - المديرون يمكنهم تحديث بيانات أي متطوع

### ✅ 2. دعم تحميل ملفات PDF
- **تم إضافة**: دعم PDF في `POST /api/media/upload`
- **المميزات**:
  - يمكن رفع ملفات PDF مع الصور والفيديوهات
  - دعم جميع أنواع الملفات: صور، فيديوهات، PDF
  - التحقق من نوع الملف تلقائياً

### ✅ 3. نظام متعدد اللغات (i18n)
- **تم إضافة**: نظام دعم متعدد اللغات
- **اللغات المدعومة**:
  - العربية (ar) - الافتراضي
  - الإنجليزية (en)
  - التركية (tr)
- **الاستخدام**:
  - أرسل header `Accept-Language: ar` أو `en` أو `tr`
  - أو استخدم parameter `?lang=ar` في الطلبات
- **الملفات**:
  - `src/utils/i18n.py` - نظام الترجمة
  - جميع الرسائل تدعم الترجمة

### ✅ 4. حفظ مسار الصورة في قاعدة البيانات
- **تم إضافة**: حقل `profile_image_url` في نموذج User
- **تم إضافة**: `POST /api/users/<user_id>/profile-image`
- **المميزات**:
  - يمكن حفظ مسار صورة المستخدم في قاعدة البيانات
  - عند رفع صورة، يتم إرجاع URL كامل يمكن حفظه
  - يمكن تحديث صورة المستخدم من الواجهة الأمامية

### ✅ 5. توليد PDF بالعربية
- **تم إضافة**: `GET /api/pdf/user/<user_id>?lang=ar`
- **المميزات**:
  - توليد ملف PDF لملف المتطوع
  - دعم اللغة العربية في PDF
  - دعم الإنجليزية والتركية أيضاً
  - تنسيق احترافي مع جداول
- **الاستخدام**:
  ```
  GET /api/pdf/user/1?lang=ar  # PDF بالعربية
  GET /api/pdf/user/1?lang=en  # PDF بالإنجليزية
  GET /api/pdf/user/1?lang=tr  # PDF بالتركية
  ```

## API Endpoints الجديدة

### 1. تحديث صورة المستخدم
```
POST /api/users/<user_id>/profile-image
Headers: Authorization: Bearer <token>
Body: {
  "profile_image_url": "https://example.com/image.jpg"
}
```

### 2. توليد PDF للمستخدم
```
GET /api/pdf/user/<user_id>?lang=ar
Headers: Authorization: Bearer <token>
Response: PDF file
```

## التحديثات في النماذج (Models)

### User Model
- **حقل جديد**: `profile_image_url` (String, nullable)
  - يحفظ مسار صورة المستخدم
  - يمكن تحديثه من API

## التحديثات في Routes

### user.py
- تحديث `update_user` لدعم جميع الحقول
- إضافة `update_profile_image` endpoint

### media.py
- إضافة دعم PDF في `allowed_file`
- تحسين إرجاع URL كامل للصورة

### pdf.py (جديد)
- `generate_user_pdf` - توليد PDF للمستخدم

## المكتبات المضافة

- `reportlab==4.2.5` - لتوليد ملفات PDF

## ملاحظات مهمة

1. **خطوط العربية في PDF**: 
   - يحتاج ملف خط يدعم العربية (مثل Arial Unicode MS أو Noto Sans Arabic)
   - يمكن إضافة الخط في `src/routes/pdf.py` في متغير `ARABIC_FONT_PATH`

2. **مسار الصورة**:
   - عند رفع صورة، يتم إرجاع URL كامل
   - احفظ هذا URL في `profile_image_url` باستخدام endpoint الجديد

3. **متعدد اللغات**:
   - أرسل `Accept-Language` header في الطلبات
   - أو استخدم `?lang=ar` parameter

## أمثلة الاستخدام

### مثال 1: تحديث بيانات متطوع
```javascript
PUT /api/users/1
{
  "full_name": "أحمد محمد",
  "phone_number": "123456789",
  "university": "جامعة دمشق",
  "major": "هندسة معلوماتية",
  "skills": "برمجة، تصميم",
  "profile_image_url": "https://example.com/profile.jpg"
}
```

### مثال 2: رفع صورة وحفظها
```javascript
// 1. رفع الصورة
POST /api/media/upload
FormData: file

// Response:
{
  "file_url": "https://yourapp.com/api/media/files/uuid_filename.jpg",
  "file_type": "image"
}

// 2. حفظ المسار في قاعدة البيانات
POST /api/users/1/profile-image
{
  "profile_image_url": "https://yourapp.com/api/media/files/uuid_filename.jpg"
}
```

### مثال 3: توليد PDF
```javascript
GET /api/pdf/user/1?lang=ar
// Returns PDF file with Arabic text
```

## الترقية من الإصدار السابق

1. قم بتثبيت المكتبات الجديدة:
   ```bash
   pip install -r requirements.txt
   ```

2. قم بتشغيل migration لإضافة الحقل الجديد:
   ```python
   # في Python shell
   from src.models.user import db, User
   from src.main import app
   
   with app.app_context():
       db.create_all()  # سيتم إضافة profile_image_url تلقائياً
   ```

3. ابدأ استخدام المميزات الجديدة!

