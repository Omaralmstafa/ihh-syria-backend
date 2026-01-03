# إعداد Git - Git Setup Guide

## ✅ تم حل المشاكل

تم حل جميع المشاكل المتعلقة بـ Git:
- ✅ حذف مجلد `.git` الفرعي الذي كان يسبب المشكلة
- ✅ تحديث `.gitignore` لاستبعاد `venv` من أي مكان
- ✅ إضافة جميع الملفات بنجاح
- ✅ إنشاء commit الأولي
- ✅ إنشاء branch `main`

## الخطوات التالية

### 1. إضافة Remote Repository

إذا كان لديك مستودع على GitHub/GitLab، أضفه:

```powershell
# استبدل <your-repo-url> برابط المستودع الفعلي
git remote add origin https://github.com/username/repository-name.git
```

أمثلة:
```powershell
# GitHub
git remote add origin https://github.com/yourusername/ihh-syria-backend.git

# GitLab
git remote add origin https://gitlab.com/yourusername/ihh-syria-backend.git
```

### 2. رفع المشروع

```powershell
git push -u origin main
```

### 3. إذا لم يكن لديك مستودع بعد

#### إنشاء مستودع جديد على GitHub:

1. اذهب إلى [GitHub](https://github.com)
2. اضغط على **New repository**
3. املأ المعلومات:
   - **Repository name**: `ihh-syria-backend`
   - **Description**: `IHH Syria Volunteer Management System Backend`
   - **Visibility**: Public أو Private
   - **لا** تضع علامة على "Initialize this repository with a README"
4. اضغط **Create repository**
5. اتبع التعليمات التي تظهر (أو استخدم الأوامر أعلاه)

#### إنشاء مستودع جديد على GitLab:

1. اذهب إلى [GitLab](https://gitlab.com)
2. اضغط على **New project**
3. اختر **Create blank project**
4. املأ المعلومات واضغط **Create project**
5. استخدم الأوامر أعلاه لربط المشروع

## ملاحظات

- التحذيرات حول LF/CRLF طبيعية على Windows ولا تؤثر على المشروع
- مجلد `venv` مستبعد تلقائياً من Git
- ملفات قاعدة البيانات (`*.db`) مستبعدة أيضاً

## التحقق من الحالة

```powershell
# عرض حالة Git
git status

# عرض الـ remotes
git remote -v

# عرض الـ branches
git branch
```

## إذا واجهت مشاكل

### إعادة تعيين Git (إذا لزم الأمر):
```powershell
# احذر: هذا سيحذف جميع الـ commits
rm -rf .git
git init
git add .
git commit -m "Initial commit"
```

### إزالة remote وإضافته مرة أخرى:
```powershell
git remote remove origin
git remote add origin <your-repo-url>
```

## بعد رفع المشروع

بعد رفع المشروع إلى Git، يمكنك:
1. ربطه بـ Render
2. استخدام `render.yaml` للنشر التلقائي
3. أو النشر اليدوي من Render Dashboard

راجع `DEPLOYMENT.md` للتعليمات التفصيلية.


