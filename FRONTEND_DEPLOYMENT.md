# دليل نشر واجهة المستخدم - Frontend Deployment Guide

## الخيارات المتاحة

### الخيار 1: نشر واجهة React منفصلة (موصى به)

إذا كان لديك تطبيق React منفصل، يمكنك نشره على:

#### أ) Render (Static Site)
1. اذهب إلى [render.com](https://render.com)
2. **New +** > **Static Site**
3. اختر المستودع الخاص بواجهة React
4. الإعدادات:
   - **Name**: `ihh-syria-frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build` (أو `dist` حسب إعداداتك)
5. في **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```
6. اضغط **Create Static Site**

#### ب) Vercel (موصى به للـ React)
1. اذهب إلى [vercel.com](https://vercel.com)
2. اضغط **New Project**
3. اختر المستودع الخاص بواجهة React
4. الإعدادات:
   - **Framework Preset**: Create React App (أو Next.js)
   - **Root Directory**: `./`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
5. في **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```
6. اضغط **Deploy**

#### ج) Netlify
1. اذهب إلى [netlify.com](https://netlify.com)
2. **Add new site** > **Import an existing project**
3. اختر المستودع
4. الإعدادات:
   - **Build command**: `npm run build`
   - **Publish directory**: `build`
5. في **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.onrender.com
   ```
6. اضغط **Deploy site**

### الخيار 2: نشر الواجهة مع Backend (Static Files)

إذا كانت الواجهة عبارة عن ملفات HTML/CSS/JS ثابتة:

#### الطريقة 1: وضع الملفات في مجلد static
1. ضع جميع ملفات الواجهة في `home/ubuntu/ihh_syria_backend/src/static/`
2. تأكد من أن `index.html` موجود في المجلد
3. Backend سيقوم بتقديم الملفات تلقائياً
4. الواجهة ستكون متاحة على: `https://your-backend.onrender.com/`

#### الطريقة 2: تحديث main.py لخدمة Static Files
الملف `main.py` موجود بالفعل ويخدم الملفات الثابتة من مجلد `static`.

### الخيار 3: إنشاء واجهة بسيطة (إذا لم تكن موجودة)

إذا لم تكن لديك واجهة، يمكنك إنشاء واحدة بسيطة:

## إعداد واجهة React جديدة

### 1. إنشاء مشروع React

```bash
npx create-react-app ihh-syria-frontend
cd ihh-syria-frontend
```

### 2. تثبيت المكتبات المطلوبة

```bash
npm install axios react-router-dom
```

### 3. إعداد API Configuration

أنشئ ملف `.env`:
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

أنشئ ملف `src/config/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default API_BASE_URL;
```

### 4. مثال على Service للاتصال بالـ API

`src/services/api.js`:
```javascript
import axios from 'axios';
import API_BASE_URL from '../config/api';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة token تلقائياً
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 5. مثال على صفحة تسجيل الدخول

`src/pages/Login.js`:
```javascript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/auth/login', { email, password });
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      navigate('/dashboard');
    } catch (error) {
      alert('خطأ في تسجيل الدخول');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="البريد الإلكتروني"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="كلمة المرور"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">تسجيل الدخول</button>
      </form>
    </div>
  );
}

export default Login;
```

### 6. Build للـ Production

```bash
npm run build
```

هذا سينشئ مجلد `build` يحتوي على الملفات الجاهزة للنشر.

## إعداد CORS في Backend

تأكد من أن Backend يسمح بالطلبات من الواجهة:

في `main.py` (موجود بالفعل):
```python
CORS(app, origins="*")  # للإنتاج، استبدل * بعنوان الواجهة
```

أو في Render Environment Variables:
```
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
```

## مثال على package.json للواجهة

```json
{
  "name": "ihh-syria-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "axios": "^1.3.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

## خطوات النشر الكاملة

### 1. إعداد الواجهة

```bash
# إنشاء مشروع React
npx create-react-app ihh-syria-frontend
cd ihh-syria-frontend

# تثبيت المكتبات
npm install axios react-router-dom

# إعداد .env
echo "REACT_APP_API_URL=https://your-backend.onrender.com" > .env

# تطوير الواجهة
npm start
```

### 2. Build

```bash
npm run build
```

### 3. النشر على Vercel

```bash
# تثبيت Vercel CLI
npm i -g vercel

# النشر
vercel
```

أو ارفع المشروع إلى GitHub ونشره من واجهة Vercel.

### 4. تحديث CORS في Backend

في Render Dashboard:
- Environment Variables
- `CORS_ORIGINS` = `https://your-frontend.vercel.app`

## هيكل المشروع المقترح

```
ihh-syria-frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Dashboard.js
│   │   └── UserProfile.js
│   ├── services/
│   │   └── api.js
│   ├── config/
│   │   └── api.js
│   ├── App.js
│   └── index.js
├── .env
├── package.json
└── README.md
```

## ملاحظات مهمة

1. **API URL**: تأكد من تحديث `REACT_APP_API_URL` في `.env`
2. **CORS**: تأكد من إعداد CORS في Backend للسماح بالطلبات من الواجهة
3. **Authentication**: احفظ token في localStorage أو cookies
4. **Environment Variables**: استخدم `REACT_APP_` prefix للـ React
5. **HTTPS**: استخدم HTTPS دائماً في الإنتاج

## روابط مفيدة

- [React Documentation](https://react.dev)
- [Vercel Deployment](https://vercel.com/docs)
- [Netlify Deployment](https://docs.netlify.com)
- [Render Static Sites](https://render.com/docs/static-sites)

## الدعم

إذا واجهت مشاكل:
1. تحقق من أن Backend يعمل: `https://your-backend.onrender.com/health`
2. تحقق من CORS settings
3. تحقق من Environment Variables
4. راجع console في المتصفح للأخطاء

