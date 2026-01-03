# دليل سريع لنشر واجهة المستخدم

## السيناريو الحالي

المشروع الحالي يحتوي على:
- ✅ Backend API (Flask) - منشور على Render
- ⚠️ واجهة بسيطة (HTML) في `static/index.html` - للاختبار فقط

## الخيارات السريعة

### الخيار 1: استخدام الواجهة الحالية (الأسرع)

الواجهة موجودة بالفعل في `static/index.html` وتُخدم تلقائياً من Backend.

**الوصول إليها:**
```
https://your-backend.onrender.com/
```

**ملاحظة:** هذه واجهة بسيطة للاختبار فقط.

### الخيار 2: إنشاء واجهة React جديدة (موصى به)

#### خطوات سريعة:

1. **إنشاء مشروع React:**
```bash
npx create-react-app ihh-syria-frontend
cd ihh-syria-frontend
```

2. **إعداد API:**
```bash
# أنشئ ملف .env
echo "REACT_APP_API_URL=https://your-backend.onrender.com" > .env
```

3. **تثبيت المكتبات:**
```bash
npm install axios react-router-dom
```

4. **Build:**
```bash
npm run build
```

5. **النشر على Vercel (الأسهل):**
   - اذهب إلى [vercel.com](https://vercel.com)
   - اضغط **New Project**
   - اختر المستودع
   - اضغط **Deploy**

### الخيار 3: رفع ملفات HTML/CSS/JS مباشرة

إذا كان لديك ملفات HTML/CSS/JS جاهزة:

1. ضعها في `home/ubuntu/ihh_syria_backend/src/static/`
2. ارفع التحديثات إلى Git
3. Backend سيقوم بتقديمها تلقائياً

## مثال سريع: صفحة تسجيل الدخول

أنشئ ملف `src/pages/Login.js`:

```javascript
import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend.onrender.com';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password
      });
      
      localStorage.setItem('token', response.data.access_token);
      window.location.href = '/dashboard';
    } catch (error) {
      alert('خطأ في تسجيل الدخول');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="البريد الإلكتروني"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="كلمة المرور"
      />
      <button type="submit">تسجيل الدخول</button>
    </form>
  );
}

export default Login;
```

## تحديث CORS في Backend

في Render Dashboard:
1. اذهب إلى Web Service
2. Environment Variables
3. أضف أو عدّل:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
   أو للسماح بجميع المواقع:
   ```
   CORS_ORIGINS=*
   ```

## الخطوات الكاملة (5 دقائق)

### 1. إنشاء React App
```bash
npx create-react-app ihh-syria-frontend
cd ihh-syria-frontend
```

### 2. إعداد API
```bash
echo "REACT_APP_API_URL=https://your-backend.onrender.com" > .env
```

### 3. تثبيت المكتبات
```bash
npm install axios
```

### 4. تحديث App.js
```javascript
import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    const response = await axios.post(`${API_URL}/api/auth/login`, {
      email,
      password
    });
    localStorage.setItem('token', response.data.access_token);
    alert('تم تسجيل الدخول بنجاح!');
  };

  return (
    <div>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default App;
```

### 5. Build
```bash
npm run build
```

### 6. النشر على Vercel
- ارفع المشروع إلى GitHub
- اذهب إلى vercel.com
- اختر المستودع
- اضغط Deploy

## النتيجة

- Backend: `https://your-backend.onrender.com`
- Frontend: `https://your-frontend.vercel.app`

## للمزيد من التفاصيل

راجع `FRONTEND_DEPLOYMENT.md` للدليل الكامل.


