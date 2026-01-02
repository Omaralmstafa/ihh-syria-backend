# دليل النشر على Render

## الخطوات التفصيلية للنشر

### 1. إعداد المستودع

تأكد من أن جميع الملفات موجودة في المستودع:
- `requirements.txt`
- `Procfile`
- `render.yaml` (اختياري)
- `build.sh`
- `runtime.txt`
- `.gitignore`

### 2. إنشاء قاعدة بيانات PostgreSQL

1. سجل الدخول إلى [Render Dashboard](https://dashboard.render.com)
2. اضغط على **New +** > **PostgreSQL**
3. املأ المعلومات:
   - **Name**: `ihh-syria-db`
   - **Database**: `ihh_syria`
   - **User**: `ihh_syria_user`
   - **Region**: اختر الأقرب إليك
   - **Plan**: Free (للبداية)
4. اضغط **Create Database**
5. احفظ معلومات الاتصال (ستحتاجها لاحقاً)

### 3. إنشاء Web Service

#### الطريقة الأولى: استخدام واجهة Render

1. اضغط على **New +** > **Web Service**
2. اختر المستودع الخاص بك من GitHub/GitLab
3. املأ المعلومات:
   - **Name**: `ihh-syria-backend`
   - **Environment**: `Python 3`
   - **Region**: نفس منطقة قاعدة البيانات
   - **Branch**: `main` (أو `master`)
   - **Root Directory**: اتركه فارغاً (أو `ihh_syria_project_final` إذا كان المشروع في مجلد فرعي)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT home.ubuntu.ihh_syria_backend.src.main:app`
   - **Plan**: Free (للبداية)

4. في قسم **Environment Variables**، أضف:
   ```
   SECRET_KEY = [قم بإنشاء مفتاح سري قوي - يمكن استخدام: openssl rand -hex 32]
   JWT_SECRET_KEY = [قم بإنشاء مفتاح JWT سري قوي]
   FLASK_ENV = production
   CORS_ORIGINS = *
   ```

5. في قسم **Database**:
   - اختر قاعدة البيانات التي أنشأتها (`ihh-syria-db`)
   - سيتم إضافة `DATABASE_URL` تلقائياً

6. اضغط **Create Web Service**

#### الطريقة الثانية: استخدام render.yaml (موصى بها)

1. اضغط على **New +** > **Blueprint**
2. اختر المستودع الخاص بك
3. Render سيقوم بقراءة `render.yaml` وإنشاء كل شيء تلقائياً
4. راجع الإعدادات واضغط **Apply**

### 4. التحقق من النشر

1. بعد اكتمال البناء، ستجد رابط التطبيق في Dashboard
2. افتح الرابط للتحقق من أن التطبيق يعمل
3. جرب `/health` للتأكد من أن كل شيء يعمل:
   ```
   https://your-app.onrender.com/health
   ```

### 5. إعدادات إضافية (اختياري)

#### إضافة Custom Domain

1. في Dashboard > Web Service > Settings
2. اذهب إلى **Custom Domains**
3. أضف النطاق الخاص بك
4. اتبع التعليمات لإعداد DNS

#### إعداد Auto-Deploy

- بشكل افتراضي، Render يقوم بنشر تلقائي عند كل push إلى الفرع الرئيسي
- يمكنك تعطيله من Settings > Auto-Deploy

#### إعدادات متقدمة

- **Health Check Path**: `/health`
- **Docker**: يمكنك استخدام Dockerfile بدلاً من Build Command

## استكشاف الأخطاء

### المشكلة: Build Fails

**الحل**:
- تحقق من أن `requirements.txt` موجود وصحيح
- تأكد من أن جميع المسارات صحيحة
- راجع Build Logs في Render Dashboard

### المشكلة: Application Crashes

**الحل**:
- تحقق من Logs في Render Dashboard
- تأكد من أن جميع متغيرات البيئة موجودة
- تحقق من أن `DATABASE_URL` صحيح

### المشكلة: Database Connection Error

**الحل**:
- تأكد من ربط قاعدة البيانات بالخدمة
- تحقق من أن `DATABASE_URL` موجود في Environment Variables
- تأكد من أن قاعدة البيانات نشطة

### المشكلة: Static Files Not Loading

**الحل**:
- تأكد من أن مجلد `static` موجود
- تحقق من المسارات في `main.py`
- قد تحتاج إلى استخدام خدمة CDN للملفات الثابتة

## نصائح مهمة

1. **الأمان**:
   - استخدم مفاتيح سرية قوية لـ `SECRET_KEY` و `JWT_SECRET_KEY`
   - لا تشارك متغيرات البيئة مع أي شخص
   - استخدم HTTPS دائماً

2. **الأداء**:
   - Free Plan قد يكون بطيئاً في البداية (Cold Start)
   - فكر في الترقية إلى Paid Plan للإنتاج

3. **النسخ الاحتياطي**:
   - قم بعمل نسخ احتياطي من قاعدة البيانات بانتظام
   - استخدم Render's Backup feature

4. **المراقبة**:
   - راقب Logs بانتظام
   - استخدم Health Checks للتأكد من أن التطبيق يعمل

## الدعم

- [Render Documentation](https://render.com/docs)
- [Render Community](https://community.render.com)
- [Render Support](https://render.com/support)

