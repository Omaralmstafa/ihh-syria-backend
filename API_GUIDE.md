# دليل API - API Guide

## التحديثات الجديدة

### 1. تعديل بيانات المتطوع (محدث)

**Endpoint**: `PUT /api/users/<user_id>`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body** (جميع الحقول اختيارية):
```json
{
  "full_name": "أحمد محمد",
  "gender": "male",
  "birth_date": "1995-05-15",
  "current_residence": "دمشق",
  "original_country": "سوريا",
  "phone_number": "123456789",
  "university": "جامعة دمشق",
  "major": "هندسة معلوماتية",
  "academic_year": "السنة الرابعة",
  "previous_organizations": "منظمة X، منظمة Y",
  "skills": "برمجة، تصميم، إدارة",
  "previous_work": "عملت في...",
  "currently_working": false,
  "volunteer_organization": "IHH",
  "available_for_volunteering": true,
  "team_role": "مطور",
  "department": "IT",
  "profile_image_url": "https://example.com/image.jpg"
}
```

**Response**:
```json
{
  "message": "تم تحديث المستخدم بنجاح",
  "user": {
    "id": 1,
    "full_name": "أحمد محمد",
    ...
  }
}
```

### 2. رفع ملفات (محدث - يدعم PDF)

**Endpoint**: `POST /api/media/upload`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Body**:
```
file: <file> (صورة، فيديو، أو PDF)
```

**Response**:
```json
{
  "message": "تم رفع الملف بنجاح",
  "file_url": "https://yourapp.com/api/media/files/uuid_filename.pdf",
  "file_type": "pdf",
  "filename": "uuid_filename.pdf"
}
```

**ملاحظة**: الآن يدعم:
- الصور: png, jpg, jpeg, gif
- الفيديوهات: mp4, avi, mov, wmv
- PDF: pdf

### 3. حفظ صورة المستخدم في قاعدة البيانات (جديد)

**Endpoint**: `POST /api/users/<user_id>/profile-image`

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body**:
```json
{
  "profile_image_url": "https://yourapp.com/api/media/files/uuid_filename.jpg"
}
```

**Response**:
```json
{
  "message": "تم تحديث صورة المستخدم بنجاح",
  "profile_image_url": "https://yourapp.com/api/media/files/uuid_filename.jpg",
  "user": {
    "id": 1,
    "profile_image_url": "https://yourapp.com/api/media/files/uuid_filename.jpg",
    ...
  }
}
```

### 4. توليد PDF للمستخدم (جديد)

**Endpoint**: `GET /api/pdf/user/<user_id>?lang=ar`

**Headers**:
```
Authorization: Bearer <token>
Accept-Language: ar (اختياري)
```

**Query Parameters**:
- `lang`: ar (عربي) | en (إنجليزي) | tr (تركي) - الافتراضي: ar

**Response**: ملف PDF

**مثال**:
```
GET /api/pdf/user/1?lang=ar
```

### 5. متعدد اللغات

يمكنك استخدام نظام متعدد اللغات بإرسال header:

```
Accept-Language: ar  # عربي
Accept-Language: en  # إنجليزي
Accept-Language: tr  # تركي
```

أو استخدام parameter في URL:
```
?lang=ar
?lang=en
?lang=tr
```

## سير العمل الكامل: رفع صورة وحفظها

```javascript
// 1. رفع الصورة
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('/api/media/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});

const uploadData = await uploadResponse.json();
// uploadData.file_url = "https://yourapp.com/api/media/files/uuid_filename.jpg"

// 2. حفظ المسار في قاعدة البيانات
const saveResponse = await fetch(`/api/users/${userId}/profile-image`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    profile_image_url: uploadData.file_url
  })
});

const saveData = await saveResponse.json();
// الآن profile_image_url محفوظ في قاعدة البيانات
```

## سير العمل: تعديل بيانات متطوع

```javascript
const updateUser = async (userId, userData) => {
  const response = await fetch(`/api/users/${userId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'Accept-Language': 'ar'  // للترجمة
    },
    body: JSON.stringify(userData)
  });
  
  return await response.json();
};

// استخدام
await updateUser(1, {
  full_name: "أحمد محمد",
  phone_number: "123456789",
  university: "جامعة دمشق",
  major: "هندسة معلوماتية",
  skills: "برمجة، تصميم"
});
```

## سير العمل: توليد PDF

```javascript
const generatePDF = async (userId, lang = 'ar') => {
  const response = await fetch(`/api/pdf/user/${userId}?lang=${lang}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `user_${userId}_${lang}.pdf`;
    a.click();
  }
};

// استخدام
await generatePDF(1, 'ar');  // PDF بالعربية
await generatePDF(1, 'en');  // PDF بالإنجليزية
await generatePDF(1, 'tr');  // PDF بالتركية
```

## أخطاء شائعة وحلولها

### 1. مسار الصورة لا يُحفظ
**المشكلة**: رفعت الصورة لكن المسار لم يُحفظ في قاعدة البيانات

**الحل**: استخدم endpoint `POST /api/users/<user_id>/profile-image` بعد رفع الصورة

### 2. PDF لا يعرض العربية بشكل صحيح
**المشكلة**: النص العربي يظهر كرموز

**الحل**: أضف ملف خط عربي في `src/routes/pdf.py` في متغير `ARABIC_FONT_PATH`

### 3. اللغة لا تتغير
**المشكلة**: الرسائل لا تتغير حسب اللغة المطلوبة

**الحل**: تأكد من إرسال header `Accept-Language` أو parameter `?lang=ar`

## ملاحظات

- جميع endpoints تتطلب مصادقة (JWT token)
- الصلاحيات: المتطوعون يمكنهم تعديل بياناتهم فقط، المديرون يمكنهم تعديل أي متطوع
- PDF يدعم العربية لكن يحتاج خط عربي مخصص للإنتاج
- مسار الصورة يجب أن يكون URL كامل (ليس مسار نسبي)


