# Requirements Management - Best Practices

> Panduan lengkap tentang cara manage dependencies Python/Django project

## 📦 Apa itu Requirements?

File `requirements.txt` berisi **list semua library/package** yang dibutuhkan project. Python menggunakan `pip` untuk install package dari file ini.

**Contoh isi `requirements.txt`:**
```txt
Django==5.0.0
djangorestframework==3.14.0
Pillow==10.2.0
```

---

## 🚀 Command Dasar

### Install dari requirements.txt
```bash
pip install -r requirements.txt
```

### Generate requirements.txt dari environment aktif
```bash
pip freeze > requirements.txt
```

**⚠️ Hati-hati:** `pip freeze` akan list **SEMUA** package termasuk dependencies. Lebih baik tulis manual.

### Install single package dan save ke requirements.txt
```bash
# Install package
pip install django-debug-toolbar

# Tambahkan manual ke requirements.txt
echo "django-debug-toolbar==4.2.0" >> requirements.txt
```

### Update package ke versi terbaru
```bash
# Cek versi terbaru
pip list --outdated

# Update specific package
pip install --upgrade Django

# Update requirements.txt manual dengan versi baru
```

---

## 📁 Project Ini: Single File Approach

Untuk project ini, kita pakai **1 file** aja: `requirements.txt`

**Alasan:**
- ✅ Simple & tidak ribet
- ✅ Project kecil-menengah (tidak ratusan dependencies)
- ✅ Tim kecil
- ✅ Development & testing di mesin yang sama

**Struktur:**
```
employee_management/
├── requirements.txt          # Semua dependencies (dev + prod)
└── requirements-production.txt   # (Optional) Production only
```

**Isi `requirements.txt`:** Sudah include development, testing, dan production tools.

---

## 🔀 Alternative: Split Requirements (Advanced)

Untuk project **besar** atau **tim besar**, bisa split jadi beberapa file:

### Struktur Split Requirements

```
requirements/
├── base.txt              # Core dependencies (shared)
├── development.txt       # Development tools
├── testing.txt           # Testing tools
├── production.txt        # Production-only
└── local.txt            # Local development (optional)
```

### Contoh Implementasi

**File: `requirements/base.txt`**
```txt
# Core dependencies yang dibutuhkan di semua environment
Django==5.0.0
djangorestframework==3.14.0
psycopg[binary]==3.1.19
python-decouple==3.8
Pillow==10.2.0
```

**File: `requirements/development.txt`**
```txt
# Include base requirements
-r base.txt

# Development-only tools
django-debug-toolbar==4.2.0
django-extensions==3.2.3
ipython==8.19.0
black==23.12.1
flake8==7.0.0
```

**File: `requirements/testing.txt`**
```txt
# Include base requirements
-r base.txt

# Testing tools
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
faker==20.1.0
factory-boy==3.3.0
```

**File: `requirements/production.txt`**
```txt
# Include base requirements
-r base.txt

# Production-only
gunicorn==21.2.0
whitenoise==6.6.0
sentry-sdk==1.40.0
```

### Install dari Split Requirements

```bash
# Development
pip install -r requirements/development.txt

# Testing
pip install -r requirements/testing.txt

# Production
pip install -r requirements/production.txt
```

**Note:** Syntax `-r base.txt` artinya "include file base.txt juga"

---

## 🤔 Kapan Harus Split?

### ✅ Gunakan Split Requirements jika:

1. **Project Besar**
   - 50+ dependencies
   - Dependencies berat yang tidak perlu di semua environment

2. **Tim Besar**
   - 10+ developers
   - Perlu standardisasi environment yang strict

3. **CI/CD Pipeline Kompleks**
   - Testing di CI/CD perlu dependencies minimal
   - Build time harus cepat

4. **Docker Multi-Stage Builds**
   - Production image harus sekecil mungkin
   - Tidak boleh ada dev tools di production

5. **Multiple Deployment Environments**
   - Staging, Production, QA masing-masing beda setup

### ❌ Tidak Perlu Split jika:

1. **Project Kecil-Menengah** (seperti project ini)
2. **Tim Kecil** (1-5 orang)
3. **Simple Deployment** (1 server)
4. **Dependencies Tidak Banyak** (< 30 packages)

---

## 📝 Best Practices

### 1. Selalu Pin Versi (Exact Version)

**❌ Jangan:**
```txt
Django
djangorestframework>=3.0.0
Pillow~=10.0
```

**✅ Lakukan:**
```txt
Django==5.0.0
djangorestframework==3.14.0
Pillow==10.2.0
```

**Alasan:** Menghindari breaking changes saat update otomatis.

### 2. Group & Comment Dependencies

**✅ Good:**
```txt
# ============================================
# Core Django
# ============================================
Django==5.0.0
djangorestframework==3.14.0

# ============================================
# Database
# ============================================
psycopg[binary]==3.1.19

# ============================================
# Development Tools
# ============================================
django-debug-toolbar==4.2.0
```

### 3. Pisahkan Optional Dependencies

```txt
# ============================================
# Face Recognition (Optional - Heavy!)
# ============================================
# Comment jika tidak butuh atau install gagal
face-recognition==1.3.0
opencv-python==4.8.1.78
numpy==1.26.2
```

### 4. Gunakan .env untuk Konfigurasi, Bukan Hard-code

**❌ Jangan:**
```python
# settings.py
DEBUG = True
SECRET_KEY = 'my-secret-123'
```

**✅ Lakukan:**
```python
# settings.py
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

### 5. Jangan Commit Virtual Environment

**.gitignore:**
```gitignore
venv/
env/
ENV/
.venv/
```

---

## 🔄 Update Dependencies

### Cara Update yang Aman

```bash
# 1. Cek package yang outdated
pip list --outdated

# 2. Baca changelog package yang mau diupdate
# Cek di GitHub/PyPI apakah ada breaking changes

# 3. Update di virtual environment test dulu
pip install --upgrade Django

# 4. Test aplikasi
python manage.py test
pytest

# 5. Kalau OK, update requirements.txt
# Edit manual dengan versi baru

# 6. Commit changes
git add requirements.txt
git commit -m "chore: update Django to 5.0.0"
```

### Tools untuk Check Security Vulnerabilities

```bash
# Install pip-audit
pip install pip-audit

# Scan vulnerabilities
pip-audit

# Install safety
pip install safety

# Check known security issues
safety check
```

---

## 🐳 Docker Best Practice

Jika pakai Docker, gunakan multi-stage build dengan split requirements:

```dockerfile
# Dockerfile
FROM python:3.11-slim as base

WORKDIR /app

# Install base dependencies
COPY requirements/base.txt .
RUN pip install -r base.txt

# Development stage
FROM base as development
COPY requirements/development.txt .
RUN pip install -r development.txt

# Production stage
FROM base as production
COPY requirements/production.txt .
RUN pip install -r production.txt

# Production image akan lebih kecil karena tidak ada dev tools
```

---

## 🎯 Kesimpulan

### Untuk Project Ini (Employee Management):
✅ **Pakai 1 file:** `requirements.txt`

### Untuk Project Production Besar:
✅ **Split requirements** sesuai kebutuhan

### Yang Penting:
1. ✅ Pin exact version
2. ✅ Group dan comment dengan jelas
3. ✅ Update secara berkala
4. ✅ Test setelah update
5. ✅ Gunakan virtual environment

---

## 📚 Resources

- [pip Documentation](https://pip.pypa.io/en/stable/)
- [Python Packaging Guide](https://packaging.python.org/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)

---

**💡 Tips:** Jangan overthink! Mulai dengan simple (1 file), baru split kalau memang butuh.