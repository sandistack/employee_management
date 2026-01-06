

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

### Step 4: Upgrade pip & Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install semua dependencies
pip install -r requirements.txt
```

**⏳ Tunggu proses instalasi (3-7 menit tergantung koneksi)**

**⚠️ Note:** 
- Face recognition library bisa lama karena compile C dependencies
- Jika face-recognition gagal install, skip dulu (tidak wajib untuk development awal)

---

## 🔧 Setup Environment Variables

### Step 5: Copy .env.example ke .env

```bash
# Copy .env.example ke .env
cp .env.example .env
```

### Step 6: Edit .env (Optional)

```bash
# Edit jika perlu custom config
nano .env
```

**Default config (.env):**
```env
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=django-insecure-CHANGE-THIS-IN-PRODUCTION-xyz123abc456
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Default: SQLite)
DB_ENGINE=sqlite
```

**✅ Untuk development awal, biarkan default (SQLite) dulu!**

---

## 🗄️ Setup Database

### Step 7: Run Migrations

```bash
# Buat database tables
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, core, accounts
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying accounts.0001_initial... OK
```

### Step 8: Create Superuser (Admin)

```bash
# Buat superuser untuk akses admin panel
python manage.py createsuperuser
```

**Follow prompts:**
```
Username: admin
Email: admin@example.com
Password: ******** (min 8 characters)
Password (again): ********
Superuser created successfully.
```

---

## ✅ Run Development Server

### Step 9: Start Server

```bash
# Run development server
python manage.py runserver
```

**✅ Berhasil jika muncul:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Step 10: Test Installation

Buka browser dan test:

1. **Homepage**: http://127.0.0.1:8000/
   - ✅ Harus tampil halaman success atau homepage

2. **Admin Panel**: http://127.0.0.1:8000/admin/
   - ✅ Login dengan superuser yang dibuat
   - ✅ Harus bisa akses dashboard admin

3. **API Health Check** (jika sudah ada): http://127.0.0.1:8000/api/health/
   - ✅ Harus return JSON: `{"status": "ok"}`

**🛑 Stop server dengan: CTRL + C**

---

## 🎯 Next Steps

### Development Workflow

Setelah instalasi berhasil:

1. **Buat branch baru** untuk fitur baru:
   ```bash
   git checkout -b feature/nama-fitur
   ```

2. **Jalankan tests** sebelum commit:
   ```bash
   pytest
   ```

3. **Format code** dengan black:
   ```bash
   black .
   ```

4. **Check linting**:
   ```bash
   flake8 apps/
   ```

### Learn Project Structure

Baca dokumentasi berikutnya:

- **[guides/00_prerequisites.md](guides/00_prerequisites.md)** - Project architecture & design decisions
- **[guides/01_core_app_setup.md](guides/01_core_app_setup.md)** - Core app structure explained
- **[guides/02_core-app.md](guides/02_core-app.md)** - Build your first Django app

---

## 🐛 Troubleshooting

### Issue 1: Python Version Error

**Error:**
```
ERROR: Python 3.11 or higher is required
```

**Solution:**
```bash
# Cek versi Python
python --version

# Jika < 3.11, install Python 3.11+
# Lalu buat ulang venv
python3.11 -m venv venv
source venv/bin/activate
```

### Issue 2: pip install Failed

**Error:**
```
ERROR: Could not install packages due to an OSError
```

**Solution:**
```bash
# Upgrade pip dulu
pip install --upgrade pip

# Install ulang
pip install -r requirements.txt
```

### Issue 3: face-recognition Install Failed

**Error:**
```
error: Microsoft Visual C++ 14.0 is required (Windows)
atau
error: command 'gcc' failed (Linux/Mac)
```

**Solution:**
```bash
# Option 1: Comment face-recognition di requirements.txt
# Edit requirements.txt, tambah # di depan:
# face-recognition==1.3.0
# opencv-python==4.8.1.78

# Option 2: Install build tools
# Windows: Install Visual C++ Build Tools
# Mac: xcode-select --install
# Linux: sudo apt install build-essential python3-dev
```

### Issue 4: Database Migration Error

**Error:**
```
django.db.utils.OperationalError: no such table: django_session
```

**Solution:**
```bash
# Hapus database dan migrate ulang
rm db.sqlite3
python manage.py migrate
```

### Issue 5: Port 8000 Already in Use

**Error:**
```
Error: That port is already in use
```

**Solution:**
```bash
# Option 1: Kill process yang pakai port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Option 2: Pakai port lain
python manage.py runserver 8001
```

---

## 📝 Important Files

| File | Deskripsi |
|------|-----------|
| `.env` | Environment variables (gitignored) |
| `requirements.txt` | Python dependencies |
| `manage.py` | Django management script |
| `config/settings/` | Django settings (split by environment) |
| `db.sqlite3` | SQLite database (gitignored) |

---

## 🔐 Security Notes

**⚠️ JANGAN commit file berikut ke Git:**
- `.env` - Contains secrets
- `db.sqlite3` - Database (use migrations instead)
- `media/` - User uploads
- `logs/` - Log files
- `venv/` - Virtual environment

**✅ Sudah di-handle di `.gitignore`**

---

## 📚 Resources

- [Django Documentation](https://docs.djangoproject.com/en/5.0/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

**🎉 Installation Complete!**

Lanjut ke: **[guides/00_prerequisites.md](guides/00_prerequisites.md)** untuk memahami arsitektur project.

**Questions?** Review troubleshooting section atau check [project README](../README.md).
