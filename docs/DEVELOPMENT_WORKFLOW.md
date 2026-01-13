# Development Workflow

## Cara Running Development

### Mode Development (Recommended untuk Development)

Jalankan **2 terminal** secara bersamaan:

#### Terminal 1: Django Backend
```bash
cd /home/fe/Desktop/employee_management
source venv/bin/activate
python manage.py runserver 8000
```

#### Terminal 2: React Frontend Dev Server
```bash
cd /home/fe/Desktop/employee_management/employee-frontend
npm run start:dev
```

Akses aplikasi di: **http://localhost:8001**

React dev server akan:
- Hot reload ketika ada perubahan
- Proxy semua request `/api/*` ke Django di `http://localhost:8000`
- Tidak perlu build setiap kali ada perubahan

---

## Kenapa Perlu 2 Server?

### Development Mode (2 Servers)
- **React Dev Server** (port 8001): Hot reload, fast refresh
- **Django Backend** (port 8000): API server
- Request dari React → proxy → Django
- CORS sudah dikonfigurasi untuk allow localhost:8001

### Production Mode (1 Server)
- Build React: `npm run build` (creates `/dist` folder)
- Django serves static files dari `/dist`
- Hanya perlu jalankan Django
- Semua request handled oleh Django

---

## Troubleshooting

### Error "static files not found" di `npm run start:dev`
✅ **Normal!** Dev server tidak perlu static files. Kalau ada error lain, restart dev server.

### CORS Error
Pastikan:
1. Django running di port 8000
2. React dev server running di port 8001
3. CORS middleware sudah aktif di Django (sudah dikonfigurasi)

### Login Tidak Bisa
Pastikan:
1. Akses aplikasi di `http://localhost:8001` (bukan 8000)
2. Django running di background
3. Token tersimpan di localStorage

---

## Development Scripts

### React Frontend

```bash
# Development dengan hot reload (no mock data)
npm run start:dev

# Development dengan hot reload di port 8001
npm start

# Build untuk production
npm run build

# Preview production build
npm run preview
```

### Django Backend

```bash
# Run server
python manage.py runserver

# Run server dengan port custom
python manage.py runserver 8000

# Migrations
python manage.py makemigrations
python manage.py migrate
```

---

## Quick Start

```bash
# Terminal 1
cd /home/fe/Desktop/employee_management && source venv/bin/activate && python manage.py runserver 8000

# Terminal 2  
cd /home/fe/Desktop/employee_management/employee-frontend && npm run start:dev
```

Buka browser: `http://localhost:8001`
