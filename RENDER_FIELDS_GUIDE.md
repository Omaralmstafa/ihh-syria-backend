# دليل الحقول في Render - ما يجب وضعه في كل حقل

## 📋 الحقول المطلوبة في Render لنشر Frontend (Static Site)

### 1. **Name** (الاسم)
```
ihh-syria-frontend
```
أو أي اسم تريده (سيستخدم في الرابط: `https://ihh-syria-frontend.onrender.com`)

---

### 2. **Branch** (الفرع)
```
main
```
أو `master` حسب الفرع الذي تستخدمه في Git

**للتحقق:**
- اذهب إلى GitHub
- انظر إلى الفرع الرئيسي (عادة `main` أو `master`)

---

### 3. **Root Directory** (المجلد الجذر) ⚠️ **مهم جداً!**

هذا الحقل يحدد أين يبحث Render عن `package.json`

#### إذا كان `package.json` في **جذر المستودع**:
```
(اتركه فارغاً - لا تكتب شيء)
```

#### إذا كان `package.json` في مجلد `frontend`:
```
frontend
```

#### إذا كان في مجلد آخر:
```
اسم_المجلد
```

**كيف تعرف؟**
1. اذهب إلى GitHub
2. افتح المستودع
3. ابحث عن `package.json`
4. انظر في أي مجلد هو

**أمثلة:**
- `repository/package.json` → Root Directory: (فارغ)
- `repository/frontend/package.json` → Root Directory: `frontend`
- `repository/src/package.json` → Root Directory: `src`

---

### 4. **Build Command** (أمر البناء)
```
npm install && npm run build
```

**شرح:**
- `npm install` - تثبيت المكتبات
- `&&` - ثم
- `npm run build` - بناء المشروع

---

### 5. **Publish Directory** (مجلد النشر)
```
build
```

**ملاحظة:** 
- إذا كنت تستخدم **Vite**: استخدم `dist`
- إذا كنت تستخدم **Create React App**: استخدم `build`
- إذا كنت تستخدم **Next.js**: استخدم `.next`

---

### 6. **Environment Variables** (متغيرات البيئة) - اختياري

اضغط **Advanced** ثم **Add Environment Variable**

#### متغير 1: رابط Backend
- **Key**: `REACT_APP_API_URL`
- **Value**: `https://ihh-syria-backend.onrender.com`
  (استبدل `ihh-syria-backend` باسم Backend الفعلي)

#### متغيرات أخرى (إذا لزم الأمر):
- **Key**: `REACT_APP_ENV`
- **Value**: `production`

---

## 📋 الحقول المطلوبة في Render لنشر Backend (Web Service)

### 1. **Name**
```
ihh-syria-backend
```

---

### 2. **Environment**
```
Python 3
```

---

### 3. **Region**
```
Oregon (US West)
```
أو أي منطقة قريبة منك

---

### 4. **Branch**
```
main
```
أو `master`

---

### 5. **Root Directory**
```
(اتركه فارغاً)
```
ما لم يكن Backend في مجلد فرعي

---

### 6. **Build Command**
```
pip install -r requirements.txt
```

---

### 7. **Start Command**
```
gunicorn --bind 0.0.0.0:$PORT home.ubuntu.ihh_syria_backend.src.main:app
```

**شرح:**
- `gunicorn` - خادم Python
- `--bind 0.0.0.0:$PORT` - الاستماع على المنفذ
- `home.ubuntu.ihh_syria_backend.src.main:app` - مسار التطبيق

---

### 8. **Environment Variables** (Backend)

#### متغير 1: Secret Key
- **Key**: `SECRET_KEY`
- **Value**: (يمكن استخدام Generate Value)

#### متغير 2: JWT Secret
- **Key**: `JWT_SECRET_KEY`
- **Value**: (يمكن استخدام Generate Value)

#### متغير 3: Flask Environment
- **Key**: `FLASK_ENV`
- **Value**: `production`

#### متغير 4: CORS Origins
- **Key**: `CORS_ORIGINS`
- **Value**: `https://ihh-syria-frontend.onrender.com`
  (أو `*` للسماح بجميع المواقع)

#### متغير 5: Database URL
- **Key**: `DATABASE_URL`
- **Value**: (يتم إضافته تلقائياً عند ربط قاعدة البيانات)

---

## 📸 مثال: نموذج Static Site في Render

```
┌─────────────────────────────────────────────┐
│  New Static Site                            │
├─────────────────────────────────────────────┤
│  Connect a repository                       │
│  [GitHub ▼]                                 │
│                                             │
│  Select repository:                        │
│  [▼ ihh-syria-frontend]                     │
│                                             │
│  Name: [ihh-syria-frontend]               │
│  Branch: [main]                            │
│  Root Directory: [        ]                │
│                                             │
│  Build Command:                             │
│  [npm install && npm run build]            │
│                                             │
│  Publish Directory:                         │
│  [build]                                    │
│                                             │
│  [Advanced ▼]                               │
│  Environment Variables:                     │
│  REACT_APP_API_URL = https://...          │
│                                             │
│  Plan: [Free]                              │
│                                             │
│  [Create Static Site]                      │
└─────────────────────────────────────────────┘
```

---

## ✅ قائمة فحص سريعة

### للـ Frontend (Static Site):

- [ ] **Name**: `ihh-syria-frontend`
- [ ] **Branch**: `main`
- [ ] **Root Directory**: (فارغ أو `frontend` حسب موقع package.json)
- [ ] **Build Command**: `npm install && npm run build`
- [ ] **Publish Directory**: `build`
- [ ] **Environment Variables**: `REACT_APP_API_URL=https://ihh-syria-backend.onrender.com`

### للـ Backend (Web Service):

- [ ] **Name**: `ihh-syria-backend`
- [ ] **Environment**: `Python 3`
- [ ] **Branch**: `main`
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `gunicorn --bind 0.0.0.0:$PORT home.ubuntu.ihh_syria_backend.src.main:app`
- [ ] **Environment Variables**: 
  - [ ] `SECRET_KEY` (Generate Value)
  - [ ] `JWT_SECRET_KEY` (Generate Value)
  - [ ] `FLASK_ENV=production`
  - [ ] `CORS_ORIGINS=https://ihh-syria-frontend.onrender.com`
  - [ ] `DATABASE_URL` (يضاف تلقائياً)

---

## 🔍 كيف تعرف ما يجب وضعه؟

### 1. Root Directory:
- اذهب إلى GitHub
- ابحث عن `package.json` (للـ Frontend) أو `requirements.txt` (للـ Backend)
- انظر في أي مجلد هو

### 2. Build Command:
- Frontend: `npm install && npm run build`
- Backend: `pip install -r requirements.txt`

### 3. Start Command (Backend فقط):
- ابحث عن ملف `main.py` أو `app.py`
- استخدم المسار الكامل: `home.ubuntu.ihh_syria_backend.src.main:app`

### 4. Publish Directory:
- Frontend: `build` (أو `dist` لـ Vite)
- Backend: لا يوجد (ليس مطلوب)

---

## ⚠️ أخطاء شائعة

### خطأ: package.json not found
**السبب:** Root Directory غير صحيح
**الحل:** حدّث Root Directory حسب موقع package.json

### خطأ: Build fails
**السبب:** Build Command غير صحيح
**الحل:** استخدم `npm install && npm run build`

### خطأ: Module not found
**السبب:** المكتبات غير مثبتة
**الحل:** تأكد من وجود `package.json` و `npm install` في Build Command

---

## 💡 نصائح

1. **Root Directory** هو الأهم - تحققه دائماً
2. استخدم **Generate Value** للمفاتيح السرية
3. راجع **Build Logs** إذا فشل البناء
4. استخدم **Clear build cache** عند التعديل

---

## 📞 مثال كامل

### Frontend:
```
Name: ihh-syria-frontend
Branch: main
Root Directory: (فارغ)
Build Command: npm install && npm run build
Publish Directory: build
Environment Variables:
  REACT_APP_API_URL = https://ihh-syria-backend.onrender.com
```

### Backend:
```
Name: ihh-syria-backend
Environment: Python 3
Branch: main
Root Directory: (فارغ)
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT home.ubuntu.ihh_syria_backend.src.main:app
Environment Variables:
  SECRET_KEY = (Generate Value)
  JWT_SECRET_KEY = (Generate Value)
  FLASK_ENV = production
  CORS_ORIGINS = https://ihh-syria-frontend.onrender.com
  DATABASE_URL = (يضاف تلقائياً)
```

---

## ✅ بعد ملء الحقول

1. راجع جميع الإعدادات
2. اضغط **Create Static Site** (للـ Frontend)
3. أو **Create Web Service** (للـ Backend)
4. انتظر اكتمال البناء (2-5 دقائق)
5. تحقق من الرابط المقدم

