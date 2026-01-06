# Installation Guide - Employee Management System

> Panduan instalasi project dari repository untuk development.

## 📋 Prerequisites

Pastikan sudah terinstall:

### 1. Python 3.11+
```bash
# Cek versi Python
python --version
# atau
python3 --version

# Harus 3.11 atau lebih baru
```

**Belum punya Python?**
- **Windows**: Download dari [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python@3.11`
- **Linux**: `sudo apt install python3.11 python3.11-venv python3-pip`

### 2. PostgreSQL 14+ (Optional - untuk Production)
```bash
# Cek versi PostgreSQL
psql --version
```

**⚠️ Note:** PostgreSQL **OPTIONAL** untuk development. Defaultnya pakai **SQLite** (sudah included di Python).

**Install PostgreSQL (jika perlu):**
- **Windows**: Download dari [postgresql.org](https://www.postgresql.org/download/windows/)
- **Mac**: `brew install postgresql@14`
- **Linux**: `sudo apt install postgresql postgresql-contrib`

### 3. Git
```bash
# Cek versi Git
git --version
```

### 4. Text Editor / IDE
Pilih salah satu:
- **VS Code** (Recommended) - Install extension: Python, Django
- **PyCharm Professional** (Punya Django support built-in)
- **Sublime Text** / **Vim** / **Neovim**

---

## 🚀 Quick Start

### Step 1: Clone Repository

```bash
# Clone project
git clone <repository-url> employee_management
cd employee_management

# Atau jika sudah ada folder
cd employee_management
git pull origin main
```

### Step 2: Create Virtual Environment

**⚠️ PENTING: SELALU gunakan virtual environment!**

```bash
# Buat virtual environment
python -m venv venv

# Atau jika python command tidak work
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**Linux / Mac:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**✅ Berhasil jika prompt berubah jadi:**
```bash
(venv) user@computer:~/employee_management$
```

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

---

## 📦 Setup Requirements

**⚠️ Simplified Approach:** Kita pakai **2 file requirements** aja untuk kemudahan:
- `requirements.txt` - Untuk development & testing (sehari-hari)
- `requirements-production.txt` - Untuk production server

### Step 5: Buat Requirements Files

```bash
# Buat file requirements untuk development & testing
touch requirements.txt

# Buat file requirements untuk production (nanti)
touch requirements-production.txt
```

### Step 6: Isi Requirements File

**File: `requirements.txt`** (Development & Testing)

Copy isi dari artifact `requirements.txt` yang sudah saya buatkan di atas.

**File: `requirements-production.txt`** (Production - bisa diisi nanti saat deploy)

Copy isi dari artifact `requirements-production.txt`.

### Step 7: Install Requirements

```bash
# Install semua dependencies untuk development & testing
pip install -r requirements.txt
```

**⏳ Tunggu proses instalasi (3-7 menit tergantung koneksi)**

**⚠️ Note:** 
- Face recognition library bisa lama karena compile C dependencies!
- Jika face-recognition gagal install, comment dulu di `requirements.txt`:
  ```txt
  # face-recognition==1.3.0
  # opencv-python==4.8.1.78
  ```

### Step 8: Buat Django Project

```bash
# Sekarang Django sudah terinstall, buat project
django-admin startproject config .
```

**⚠️ Perhatikan titik (.) di akhir!** Ini bikin project di folder current, bukan buat folder baru.

**Struktur setelah command ini:**
```
employee_management/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py      # Akan kita split nanti
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── venv/
└── ...
```

---

## 🔧 Setup Environment Variables

### Step 9: Buat .env.example

```bash
nano .env.example
```

**File: `.env.example`**
```env
# ============================================
# Environment Configuration
# ============================================
# Copy this file to .env and fill in your values
# DO NOT commit .env to version control!

# ============================================
# Django Settings
# ============================================
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=django-insecure-CHANGE-THIS-IN-PRODUCTION-xyz123abc456
ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================
# Database Configuration
# ============================================
# Use 'sqlite' for development or 'postgresql' for production
DB_ENGINE=sqlite

# SQLite (default for development)
# Tidak perlu setting tambahan, otomatis pakai db.sqlite3

# PostgreSQL (uncomment jika pakai PostgreSQL)
# DB_ENGINE=postgresql
# DB_NAME=employee_mgmt_dev
# DB_USER=employee_user
# DB_PASSWORD=your_secure_password_here
# DB_HOST=localhost
# DB_PORT=5432

# ============================================
# Security
# ============================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000

# ============================================
# Email Configuration
# ============================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Production Email (uncomment when needed)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# ============================================
# Redis (Optional - for caching/celery)
# ============================================
# REDIS_URL=redis://localhost:6379/0

# ============================================
# Sentry (Optional - for error tracking)
# ============================================
# SENTRY_DSN=your-sentry-dsn-here

# ============================================
# Face Recognition Settings
# ============================================
FACE_RECOGNITION_TOLERANCE=0.6
FACE_RECOGNITION_MODEL=hog
```

### Step 10: Copy ke .env

```bash
# Copy .env.example ke .env
cp .env.example .env

# Edit .env jika perlu (untuk sekarang biarkan default dulu)
# nano .env
```

---

## 🔧 Restructure Settings

### Step 11: Split Settings

```bash
# Buat folder settings
mkdir config/settings

# Pindahkan settings.py jadi base.py
mv config/settings.py config/settings/base.py

# Buat file-file settings lainnya
touch config/settings/__init__.py
touch config/settings/development.py
touch config/settings/production.py
```

### Step 12: Edit Settings Files

Lihat artifact terpisah untuk isi masing-masing file:
- `config/settings/__init__.py`
- `config/settings/base.py`
- `config/settings/development.py`
- `config/settings/production.py`

---

## ✅ Test Setup

### Step 13: Test Run Server

```bash
# Jalankan migration pertama kali (buat database tables)
python manage.py migrate

# Buat superuser untuk akses admin
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

**✅ Berhasil jika muncul:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Buka browser:
- `http://127.0.0.1:8000/` - Harus muncul halaman sukses
- `http://127.0.0.1:8000/admin/` - Login dengan superuser yang dibuat

**🛑 Stop server dengan: CTRL + C**

---

## ✅ Checkpoint

Setelah semua step di atas, struktur folder Anda harus seperti ini:

```
employee_management/
├── config/
│   ├── settings/
│   │   ├── __init__.py           ✅
│   │   ├── base.py               ✅
│   │   ├── development.py        ✅
│   │   └── production.py         ✅
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   └── 01_setup.md               ✅ (file ini)
├── requirements.txt              ✅
├── requirements-production.txt   ✅
├── apps/                         ✅
├── api/                          ✅
├── tests/                        ✅
├── logs/                         ✅
├── scripts/                      ✅
├── static/                       ✅
├── media/                        ✅
├── venv/                         ✅
├── manage.py                     ✅
├── db.sqlite3                    ✅ (setelah migrate)
├── .env                          ✅
├── .env.example                  ✅
├── .gitignore                    ✅
└── README.md                     ✅
```

---

## 🎯 Next Steps

**✅ Setup dasar sudah selesai!**

**Lanjut ke:** [docs/02_structure.md](02_structure.md) - Penjelasan struktur project & buat core app

---

## 🐛 Troubleshooting

### Error: "python: command not found"
**Solusi:** Gunakan `python3` instead of `python`

### Error: "psycopg installation failed"
**Solusi:** Skip dulu, pakai SQLite. Edit `.env`:
```env
DB_ENGINE=sqlite
```

**Solusi (Linux) jika tetap mau install PostgreSQL:**
```bash
sudo apt-get install python3-dev libpq-dev
pip install psycopg[binary]
```

### Error: "face_recognition installation failed"
**Solusi:** Skip dulu, install nanti saat butuh. Comment di `requirements/base.txt`:
```txt
# face-recognition==1.3.0
# opencv-python==4.8.1.78
```

**Solusi (Windows):** Install CMake dan Visual C++ Build Tools dulu  
**Solusi (Mac):** `brew install cmake`  
**Solusi (Linux):** `sudo apt-get install cmake`

### Error: "Permission denied" saat aktivasi venv (Windows PowerShell)
**Solusi:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "ModuleNotFoundError: No module named 'decouple'"
**Solusi:** Install ulang requirements:
```bash
pip install -r requirements.txt
```

### Error saat migrate: "no such table: django_session"
**Solusi:** Ini normal, jalankan migrate:
```bash
python manage.py migrate
```

---

## 📝 Summary Commands

```bash
# Setup lengkap (copy-paste semua sekaligus)
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

**🎉 Setup Complete! Lanjut ke docs berikutnya!**