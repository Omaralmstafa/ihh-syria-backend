# IHH Syria Project - Backend API

تطبيق إدارة المتطوعين لمؤسسة IHH سوريا

## المميزات

- نظام إدارة المستخدمين مع صلاحيات متعددة المستويات
- إدارة المكاتب والمناطق
- نظام النشر والوسائط (صور وفيديوهات)
- نظام النقاط والتقييمات
- API كامل مع JWT Authentication

## التقنيات المستخدمة

- **Backend**: Flask (Python)
- **Database**: SQLite (محلي) / PostgreSQL (الإنتاج)
- **Authentication**: Flask-JWT-Extended
- **CORS**: Flask-CORS

## متطلبات التشغيل

- Python 3.11+
- pip

## التثبيت المحلي

1. استنساخ المشروع:
```bash
git clone <repository-url>
cd ihh_syria_project_final
```

2. إنشاء بيئة افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate
```

3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

4. إنشاء ملف `.env`:
```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=jwt-secret-string
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=*
PORT=5000
FLASK_ENV=development
```

5. تشغيل التطبيق:
```bash
python -m home.ubuntu.ihh_syria_backend.src.main
```

أو:
```bash
gunicorn --bind 0.0.0.0:5000 home.ubuntu.ihh_syria_backend.src.main:app
```

## النشر على Render

### الخطوات:

1. **إنشاء حساب على Render** وربط مستودع GitHub الخاص بك

2. **إنشاء قاعدة بيانات PostgreSQL**:
   - اذهب إلى Dashboard > New > PostgreSQL
   - اختر الخطة المناسبة (Free للبداية)
   - احفظ معلومات الاتصال

3. **إنشاء Web Service**:
   - اذهب إلى Dashboard > New > Web Service
   - اختر المستودع الخاص بك
   - الإعدادات:
     - **Name**: ihh-syria-backend
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT home.ubuntu.ihh_syria_backend.src.main:app`
     - **Plan**: Free (أو حسب احتياجك)

4. **إضافة متغيرات البيئة**:
   - في قسم Environment Variables:
     - `SECRET_KEY`: قم بإنشاء مفتاح سري قوي
     - `JWT_SECRET_KEY`: قم بإنشاء مفتاح JWT سري قوي
     - `DATABASE_URL`: من قاعدة البيانات التي أنشأتها (سيتم إضافتها تلقائياً إذا ربطت قاعدة البيانات)
     - `FLASK_ENV`: `production`
     - `CORS_ORIGINS`: `*` (أو قائمة بالمواقع المسموحة مفصولة بفواصل)

5. **ربط قاعدة البيانات**:
   - في قسم Database:
   - اختر قاعدة البيانات التي أنشأتها
   - سيتم إضافة `DATABASE_URL` تلقائياً

6. **النشر**:
   - اضغط على "Create Web Service"
   - سيبدأ Render ببناء وتشغيل التطبيق تلقائياً

### استخدام render.yaml (اختياري):

يمكنك استخدام ملف `render.yaml` الموجود في المشروع لتكوين كل شيء تلقائياً:

1. اذهب إلى Dashboard > New > Blueprint
2. اختر المستودع الخاص بك
3. Render سيقوم بقراءة `render.yaml` وإنشاء جميع الخدمات تلقائياً

## هيكل المشروع

```
ihh_syria_project_final/
├── home/
│   └── ubuntu/
│       └── ihh_syria_backend/
│           ├── src/
│           │   ├── main.py          # نقطة الدخول الرئيسية
│           │   ├── models/          # نماذج قاعدة البيانات
│           │   ├── routes/          # مسارات API
│           │   ├── static/         # الملفات الثابتة
│           │   └── database/        # قاعدة البيانات المحلية
│           └── requirements.txt
├── requirements.txt                 # متطلبات المشروع الرئيسية
├── render.yaml                      # تكوين Render
├── Procfile                         # ملف تشغيل Render
├── build.sh                         # سكريبت البناء
├── .gitignore
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - تسجيل مستخدم جديد
- `POST /api/auth/login` - تسجيل الدخول
- `GET /api/auth/me` - معلومات المستخدم الحالي
- `POST /api/auth/change-password` - تغيير كلمة المرور

### Users
- `GET /api/users` - قائمة المستخدمين (حسب الصلاحيات)
- `GET /api/users/<id>` - معلومات مستخدم محدد
- `PUT /api/users/<id>` - تحديث مستخدم
- `GET /api/users/search` - البحث عن مستخدمين

### Offices
- `GET /api/offices` - قائمة المكاتب
- `POST /api/offices` - إنشاء مكتب جديد (General Manager فقط)
- `GET /api/offices/<id>` - معلومات مكتب محدد
- `PUT /api/offices/<id>` - تحديث مكتب
- `GET /api/offices/<id>/users` - مستخدمو مكتب محدد
- `GET /api/offices/<id>/stats` - إحصائيات مكتب

### Media & Posts
- `POST /api/media/upload` - رفع ملف (صورة/فيديو)
- `GET /api/media/files/<filename>` - تحميل ملف
- `POST /api/media/posts` - إنشاء منشور
- `GET /api/media/posts` - قائمة المنشورات
- `POST /api/media/posts/<id>/like` - إعجاب/إلغاء إعجاب
- `DELETE /api/media/posts/<id>` - حذف منشور

## الصلاحيات

- **volunteer**: متطوع عادي
- **section_manager**: مدير قسم
- **office_manager**: مدير مكتب
- **general_manager**: المدير العام

## ملاحظات مهمة

1. **الأمان**: تأكد من تغيير `SECRET_KEY` و `JWT_SECRET_KEY` في الإنتاج
2. **قاعدة البيانات**: SQLite للمطورين المحليين، PostgreSQL للإنتاج
3. **الملفات المرفوعة**: يتم حفظها في `static/uploads/`
4. **CORS**: تأكد من تكوين CORS بشكل صحيح للسماح بالوصول من الواجهة الأمامية

## الدعم

للمساعدة أو الإبلاغ عن مشاكل، يرجى فتح issue في المستودع.

## الترخيص

جميع الحقوق محفوظة © IHH Syria


