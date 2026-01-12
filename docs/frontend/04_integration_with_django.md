# Integrasi React Frontend dengan Django Backend

Dokumentasi ini menjelaskan cara menghubungkan frontend React (Ant Design Pro + Umi.js) dengan backend Django, sehingga bisa dijalankan dari satu server Django.

## 📋 Konsep Dasar

### Arsitektur
```
┌─────────────────────────────────────────┐
│     Browser: http://localhost:8000      │
└─────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
┌────────┐    ┌──────────┐    ┌──────────┐
│   /    │    │  /admin  │    │   /api   │
│ React  │    │  Django  │    │  Django  │
│  SPA   │    │  Admin   │    │   REST   │
└────────┘    └──────────┘    └──────────┘
```

**Prinsip:**
- `/` → Frontend React (SPA)
- `/admin` → Django Admin Panel
- `/api/v1/` → REST API Backend
- Static files (CSS, JS) → `/static/`

---

## 🚀 Langkah Setup (Step by Step)

### **Langkah 1: Persiapan Frontend**

#### 1.1. Install Dependencies
```bash
cd employee-frontend
npm install
npm install --save-dev chokidar-cli
```

#### 1.2. Konfigurasi Public Path
Edit `employee-frontend/config/config.ts`:

```typescript
// Ubah PUBLIC_PATH agar assets di-serve dari /static/
const PUBLIC_PATH: string = '/static/';

export default defineConfig({
  publicPath: PUBLIC_PATH,
  
  request: {
    // API base URL mengarah ke Django backend
    baseURL: 'http://localhost:8000',
  },
  
  // ... config lainnya
});
```

**Penjelasan:**
- `publicPath: '/static/'` → Semua file JS/CSS akan diminta dari `http://localhost:8000/static/`
- `baseURL: 'http://localhost:8000'` → API request akan ke Django backend

#### 1.3. Build Frontend (Pertama Kali)
```bash
npm run build
```

Ini akan generate folder `dist/` yang berisi:
- `index.html` (entry point)
- File JS, CSS, images
- Semua asset statis

---

### **Langkah 2: Konfigurasi Django Backend**

#### 2.1. Setup `config/settings.py`

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST = BASE_DIR / "employee-frontend" / "dist"

# Static files configuration
STATIC_URL = "/static/"  # ← Harus pakai leading slash
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [FRONTEND_DIST] if FRONTEND_DIST.exists() else []

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIST],  # ← Django akan cari index.html di sini
        "APP_DIRS": True,
        # ...
    },
]

# CORS untuk development (jika pakai dev server terpisah)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8001",  # Port dev server frontend
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]
```

**Penjelasan:**
- `FRONTEND_DIST`: Path ke folder build React
- `STATICFILES_DIRS`: Django akan serve static files dari folder ini
- `TEMPLATES["DIRS"]`: Django akan cari `index.html` React di sini
- `CORS_ALLOWED_ORIGINS`: Izinkan request dari frontend dev server

#### 2.2. Setup `config/urls.py`

```python
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),
    
    # API Routes
    path('api/', include(('api.urls', 'api'), namespace='api')),

    # React SPA - serve index.html untuk root
    path('', TemplateView.as_view(template_name="index.html"), name='frontend'),
    
    # Fallback untuk SPA routing (semua route selain admin/api/static)
    re_path(
        r'^(?!admin)(?!admin/)(?!api/)(?!static/)(?!media/).*$',
        TemplateView.as_view(template_name="index.html")
    ),
]
```

**Penjelasan:**
- `path('')` → Root URL serve `index.html` React
- `re_path(r'^(?!admin)...')` → Semua route yang BUKAN admin/api/static akan di-handle React Router
- Regex negative lookahead `(?!...)` memastikan Django admin tetap bisa diakses

---

### **Langkah 3: Test Integrasi**

#### 3.1. Jalankan Django Server
```bash
python manage.py runserver
```

#### 3.2. Test URLs
- `http://127.0.0.1:8000/` → React App ✅
- `http://127.0.0.1:8000/admin/` → Django Admin ✅
- `http://127.0.0.1:8000/api/v1/...` → REST API ✅
- `http://127.0.0.1:8000/static/logo.svg` → Static file ✅

#### 3.3. Troubleshooting
| Masalah | Penyebab | Solusi |
|---------|----------|--------|
| Admin page 403/blank | Fallback regex salah | Cek regex di `urls.py` |
| Logo tidak muncul | PUBLIC_PATH salah | Set `PUBLIC_PATH = '/static/'` |
| API CORS error | CORS belum diatur | Tambah origin di `CORS_ALLOWED_ORIGINS` |
| 404 untuk static files | Build belum ada | Jalankan `npm run build` |

---

## 🔄 Mode Development (Auto Rebuild)

Ada **2 cara** untuk development dengan auto-reload:

### **Cara 1: Watch Mode (Rebuild dist otomatis)** ⭐ RECOMMENDED

Cara ini mirip dengan `webpack --watch` di kantor Anda.

#### Setup
Edit `employee-frontend/package.json` (sudah dilakukan):
```json
{
  "scripts": {
    "watch:dist": "chokidar \"src/**/*\" -c \"npm run build\""
  }
}
```

#### Cara Pakai
**Terminal 1 (Frontend Watcher):**
```bash
cd employee-frontend
npm run watch:dist
```
- Watcher akan standby
- Setiap ada perubahan di folder `src/`, otomatis build ulang
- Hasil build masuk ke `dist/`

**Terminal 2 (Django Server):**
```bash
python manage.py runserver
```

**Cara Kerja:**
1. Edit file di `employee-frontend/src/`
2. Chokidar deteksi perubahan → trigger `npm run build`
3. File di `dist/` terupdate
4. Refresh browser → Django serve file baru dari `dist/`

**Kelebihan:**
- ✅ Satu URL (`localhost:8000`)
- ✅ Setup mirip kantor (webpack watch)
- ✅ Production-like environment

**Kekurangan:**
- ⚠️ Harus manual refresh browser
- ⚠️ Build agak lambat (5-10 detik)

---

### **Cara 2: Dev Server Terpisah (HMR Fast)** 🚀

Cara ini pakai Hot Module Replacement (lebih cepat).

#### Cara Pakai
**Terminal 1 (Frontend Dev Server):**
```bash
cd employee-frontend
PORT=8001 npm run start:dev
```

**Terminal 2 (Django Server):**
```bash
python manage.py runserver 8000
```

#### Akses
- Frontend: `http://localhost:8001/` (pakai ini untuk develop)
- Backend API: `http://localhost:8000/api/v1/`

**Cara Kerja:**
1. Frontend di-serve oleh Umi dev server (port 8001)
2. API request tetap ke Django (port 8000)
3. Perubahan code langsung reload otomatis (HMR)

**Kelebihan:**
- ✅ Super cepat (hot reload instant)
- ✅ Tidak perlu refresh manual
- ✅ Dev experience terbaik

**Kekurangan:**
- ⚠️ Dua port berbeda
- ⚠️ Beda dari production (production 1 port)

---

## 📦 Deployment Production

### Build Final
```bash
cd employee-frontend
npm run build
```

### Collect Static Files Django
```bash
python manage.py collectstatic --noinput
```

Ini akan copy semua static files ke `staticfiles/` untuk production.

### Server Config (Nginx/Apache)
```nginx
# Serve static files langsung
location /static/ {
    alias /path/to/staticfiles/;
}

# Pass semua request lain ke Django
location / {
    proxy_pass http://127.0.0.1:8000;
}
```

---

## 🔍 Debugging Tips

### 1. Static Files Tidak Load
```bash
# Cek apakah dist sudah ada
ls -la employee-frontend/dist/

# Cek STATIC_URL di Django
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_URL)
>>> print(settings.STATICFILES_DIRS)
```

### 2. API Request Gagal (CORS)
```python
# Pastikan corsheaders aktif
INSTALLED_APPS = [
    'corsheaders',  # ← Harus ada
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← Di atas CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

### 3. Logo/Image Tidak Muncul
```typescript
// Pastikan semua path pakai /static/
<img src="/static/logo.svg" />  // ✅ Benar
<img src="/logo.svg" />          // ❌ Salah
```

Atau lebih baik, set di config:
```typescript
const PUBLIC_PATH = '/static/';
// Semua asset otomatis pakai prefix /static/
```

---

## 📚 Referensi File Penting

| File | Fungsi |
|------|--------|
| `employee-frontend/config/config.ts` | Konfigurasi Umi (publicPath, baseURL) |
| `employee-frontend/package.json` | Script build & watch |
| `config/settings.py` | Django settings (STATIC, TEMPLATES) |
| `config/urls.py` | URL routing (admin, api, frontend) |
| `employee-frontend/dist/` | Build output React (auto-generate) |

---

## ✅ Checklist Setup

- [ ] `npm install` di folder frontend
- [ ] `npm install --save-dev chokidar-cli`
- [ ] Set `PUBLIC_PATH = '/static/'` di `config.ts`
- [ ] Set `STATIC_URL = '/static/'` di `settings.py`
- [ ] Set `STATICFILES_DIRS = [FRONTEND_DIST]`
- [ ] Setup URL patterns dengan SPA fallback di `urls.py`
- [ ] Build frontend: `npm run build`
- [ ] Test Django: `python manage.py runserver`
- [ ] Akses `localhost:8000/` → React ✅
- [ ] Akses `localhost:8000/admin/` → Django Admin ✅
- [ ] Untuk development: `npm run watch:dist` (Terminal 1) + `runserver` (Terminal 2)

---

## 🎯 Kesimpulan

**Untuk Daily Development:** Pakai **Cara 1 (watch:dist)** karena mirip workflow kantor dengan webpack.

**Cara Kerja Sederhana:**
1. Frontend di-build jadi static files (HTML, JS, CSS)
2. Django serve static files ini via `STATICFILES_DIRS`
3. Django return `index.html` untuk semua route (kecuali admin/api)
4. React Router handle client-side routing
5. API call dari React → Django REST API

Semua berjalan dari **1 server Django** di port 8000! 🎉
