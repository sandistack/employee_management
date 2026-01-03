# Setup Guide - Employee Management System

> Panduan lengkap setup project dari NOL untuk development.

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

### 2. PostgreSQL 14+
```bash
# Cek versi PostgreSQL
psql --version

# Harus 14 atau lebih baru
```

**Belum punya PostgreSQL?**
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

## 🚀 Step-by-Step Setup

### Step 1: Clone / Setup Project Folder
```bash
# Jika clone dari Git
git clone 
cd employee_management

# Atau jika buat baru (sudah dilakukan di Step 0)
# mkdir employee_management
# cd employee_management
```

### Step 2: Buat Virtual Environment

**⚠️ PENTING: SELALU gunakan virtual environment!**
```bash
# Buat virtual environment
python -m venv venv

# Atau jika python command tidak work
python3 -m venv venv
```

### Step 3: Aktivasi Virtual Environment

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

### Step 5: Install Django (Temporary)
```bash
# Install Django dulu untuk buat project
pip install django
```

### Step 6: Buat Django Project
```bash
# Buat project dengan nama 'config'
django-admin startproject config .

# Perhatikan titik (.) di akhir!
# Ini bikin project di folder current, bukan buat folder baru
```

**Struktur setelah command ini:**
```
employee_management/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── venv/
└── ...
```

### Step 7: Test Run Server
```bash
# Test jalankan server
python manage.py runserver
```

**✅ Berhasil jika muncul:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Buka browser: `http://127.0.0.1:8000/`

**Harus muncul halaman "The install worked successfully!"**

**🛑 Stop server dengan: CTRL + C**

---

## 📦 Setup Requirements

### Step 8: Buat Requirements Files
```bash
# Buat file requirements untuk base
touch requirements/base.txt

# Buat file requirements untuk development
touch requirements/development.txt

# Buat file requirements untuk production
touch requirements/production.txt

# Buat file requirements untuk testing
touch requirements/testing.txt
```

### Step 9: Isi Requirements Files

**File: `requirements/base.txt`**
```txt
# Core Django
Django==5.0.0
psycopg2-binary==2.9.9

# Django REST Framework
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1

# Filtering & Pagination
django-filter==23.5

# CORS Headers
django-cors-headers==4.3.1

# Environment Variables
python-decouple==3.8

# Pillow untuk ImageField
Pillow==10.1.0

# Face Recognition
face-recognition==1.3.0
opencv-python==4.8.1.78
numpy==1.26.2
```

**File: `requirements/development.txt`**
```txt
-r base.txt

# Development Tools
django-debug-toolbar==4.2.0
django-extensions==3.2.3

# Code Quality
black==23.12.1
flake8==7.0.0
isort==5.13.2

# Pre-commit hooks
pre-commit==3.6.0

# IPython for better shell
ipython==8.19.0
```

**File: `requirements/production.txt`**
```txt
-r base.txt

# Production Server
gunicorn==21.2.0

# Monitoring
sentry-sdk==1.39.2

# Redis (optional - untuk caching/celery)
redis==5.0.1
django-redis==5.4.0
```

**File: `requirements/testing.txt`**
```txt
-r base.txt

# Testing
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
factory-boy==3.3.0
faker==22.0.0
```

### Step 10: Install Development Requirements
```bash
pip install -r requirements/development.txt
```

**⏳ Tunggu proses instalasi (bisa 2-5 menit)**

### Step 11: Freeze Installed Packages (Backup)
```bash
# Simpan list semua package yang terinstall
pip freeze > requirements/installed.txt
```

---

## 🗄️ Setup Database

### Step 12: Buat Database PostgreSQL
```bash
# Masuk ke PostgreSQL
psql -U postgres

# Di dalam psql:
CREATE DATABASE employee_mgmt_dev;
CREATE USER employee_user WITH PASSWORD 'your_secure_password';
ALTER ROLE employee_user SET client_encoding TO 'utf8';
ALTER ROLE employee_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE employee_user SET timezone TO 'Asia/Jakarta';
GRANT ALL PRIVILEGES ON DATABASE employee_mgmt_dev TO employee_user;

# Keluar dari psql
\q
```

### Step 13: Setup Environment Variables
```bash
# Copy .env.example ke .env
cp .env.example .env

# Edit .env
nano .env
```

**File: `.env.example`**
```env
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-xyz123
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=employee_mgmt_dev
DB_USER=employee_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Environment
DJANGO_SETTINGS_MODULE=config.settings.development
```

**File: `.env` (copy dari .env.example dan edit password)**

---

## 🔧 Restructure Settings

### Step 14: Split Settings
```bash
# Buat folder settings
mkdir config/settings

# Pindahkan settings.py jadi base.py
mv config/settings.py config/settings/base.py

# Buat __init__.py
touch config/settings/__init__.py

# Buat development.py
touch config/settings/development.py

# Buat production.py
touch config/settings/production.py
```

**Akan dijelaskan isi filenya di step berikutnya...**

---

## ✅ Checkpoint

Setelah semua step di atas, struktur folder Anda harus seperti ini:
```
employee_management/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py            ✅
│   │   ├── development.py     ✅
│   │   └── production.py      ✅
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
│   └── 01_setup.md            ✅ (file ini)
├── requirements/
│   ├── base.txt               ✅
│   ├── development.txt        ✅
│   ├── production.txt         ✅
│   ├── testing.txt            ✅
│   └── installed.txt          ✅
├── venv/                      ✅
├── manage.py                  ✅
├── .env                       ✅
├── .env.example               ✅
├── .gitignore                 ✅
└── README.md                  ✅
```

---

## 🎯 Next Steps

**✅ Setup dasar sudah selesai!**

**Lanjut ke:** [docs/02_structure.md](02_structure.md) - Setting up project structure

---

## 🐛 Troubleshooting

### Error: "python: command not found"
**Solusi:** Gunakan `python3` instead of `python`

### Error: "psycopg2 installation failed"
**Solusi (Linux):**
```bash
sudo apt-get install python3-dev libpq-dev
pip install psycopg2-binary
```

### Error: "face_recognition installation failed"
**Solusi (Windows):** Install CMake dan Visual C++ Build Tools dulu
**Solusi (Mac):** `brew install cmake`
**Solusi (Linux):** `sudo apt-get install cmake`

### Error: "Permission denied" saat aktivasi venv (Windows PowerShell)
**Solusi:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

**🎉 Setup Complete! Lanjut ke docs berikutnya!**
