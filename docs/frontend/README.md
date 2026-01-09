# Frontend Documentation - Employee Management

Dokumentasi lengkap untuk frontend development dengan React + Ant Design Pro.

## 📚 Daftar Isi

### 1. [Pengetahuan Dasar](./00_pengetahuan_dasar.md)
Panduan lengkap tentang teknologi yang digunakan dan yang perlu dipelajari:
- ⭐ Modern JavaScript ES6+
- ⭐ React Fundamentals
- ⭐ TypeScript Basics
- ⭐ Axios & API Integration
- ⭐ Ant Design UI Library
- ⏳ Webpack (opsional, nanti)
- ⏳ Docker (opsional, untuk deployment)

**Baca ini kalau:**
- Baru mulai dengan React
- Bingung teknologi apa yang harus dipelajari
- Ingin roadmap belajar yang terstruktur

---

### 2. [Struktur Folder](./01_struktur_folder.md)
Penjelasan detail struktur folder frontend yang sudah di-setup:
- 📁 `src/api/` - API Layer & Axios configuration
- 📁 `src/features/` - Feature-based modules (auth, employee)
- 📁 `src/components/` - Reusable UI components
- 📁 `src/types/` - TypeScript type definitions
- 📁 `src/utils/` - Helper functions
- 📁 `config/` - Umi.js configuration & routes

**Baca ini kalau:**
- Ingin paham struktur project
- Mau tau file apa taruh di mana
- Penasaran kenapa pakai feature folder pattern

---

### 3. [Cleanup Checklist](./02_cleanup_checklist.md)
Daftar file yang dihapus dan dipertahankan dari template Ant Design Pro:
- ❌ File yang dihapus (mock, examples, tests)
- ✅ File yang dipertahankan (core, config)
- 🆕 File yang baru dibuat (API, features, types)

**Baca ini kalau:**
- Penasaran apa yang sudah dihapus
- Mau verify cleanup berhasil
- Salah hapus file dan mau restore

---

### 4. [Quick Start Guide](./03_quick_start.md)
Panduan praktis untuk mulai development:
- 🚀 Setup awal & run dev server
- 📋 Development workflow (Backend → Postman → Frontend)
- 🔍 Debugging tips & common issues
- 📝 Cara develop feature baru
- 🎨 Styling dengan Ant Design
- ⚡ Performance tips

**Baca ini kalau:**
- Siap mulai coding
- Mau develop feature baru
- Ada error dan perlu troubleshoot

---

## 🎯 Quick Navigation

### Untuk Pemula
1. Baca [Pengetahuan Dasar](./00_pengetahuan_dasar.md) untuk roadmap belajar
2. Baca [Struktur Folder](./01_struktur_folder.md) untuk paham project structure
3. Ikuti [Quick Start Guide](./03_quick_start.md) untuk mulai coding

### Untuk Yang Sudah Setup
1. [Quick Start Guide](./03_quick_start.md) - Development workflow
2. [Struktur Folder](./01_struktur_folder.md) - Referensi cepat

### Troubleshooting
1. [Quick Start Guide - Debugging Section](./03_quick_start.md#-debugging-tips)
2. [Cleanup Checklist](./02_cleanup_checklist.md) - Kalau salah hapus file

---

## 🏗️ Struktur Cepat

```
employee-frontend/
├── config/
│   └── routes.ts              ← Define routes di sini
├── src/
│   ├── api/                   ← API calls ke Django backend
│   │   ├── axios.ts
│   │   ├── auth.api.ts
│   │   └── employee.api.ts
│   │
│   ├── features/              ← Feature modules (PENTING!)
│   │   ├── auth/
│   │   │   └── LoginPage.tsx
│   │   └── employee/
│   │       └── EmployeeListPage.tsx
│   │
│   ├── components/            ← Reusable components
│   ├── types/                 ← TypeScript types
│   └── utils/                 ← Helper functions
│
└── docs/frontend/             ← You are here!
```

---

## ⚡ Quick Commands

```bash
# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build

# Lint code
npm run lint

# Run tests
npm test
```

---

## 🔑 Key Concepts

### 1. Feature-Based Architecture
Organize code by FEATURE, not by TYPE:
```
features/
├── auth/         ← Everything about authentication
└── employee/     ← Everything about employee management
```

### 2. API Layer Separation
All backend communication in one place:
```typescript
import { employeeAPI } from '@/api';
const data = await employeeAPI.getList();
```

### 3. TypeScript for Type Safety
Define types for better DX:
```typescript
interface Employee {
  id: number;
  name: string;
  // ...
}
```

### 4. Ant Design Components
Use pre-built components:
```tsx
import { Table, Button, Form } from 'antd';
```

---

## 📋 Development Checklist

### Before Starting
- [ ] Backend API ready
- [ ] API tested in Postman
- [ ] Environment variables configured (.env)
- [ ] Dev server running

### Every Feature
- [ ] Create API service in `src/api/`
- [ ] Define TypeScript types
- [ ] Create feature folder & components
- [ ] Add route in `config/routes.ts`
- [ ] Handle loading & error states
- [ ] Test CRUD operations
- [ ] Proper validation
- [ ] Styling with Ant Design

### Before Deployment
- [ ] All features tested
- [ ] No console errors
- [ ] Responsive design (mobile)
- [ ] Build passes (`npm run build`)
- [ ] Environment variables for production

---

## 🆘 Need Help?

### Documentation
- [Pengetahuan Dasar](./00_pengetahuan_dasar.md) - Learning resources
- [Struktur Folder](./01_struktur_folder.md) - Architecture details
- [Quick Start](./03_quick_start.md) - Practical guide

### External Resources
- **React:** https://react.dev
- **Ant Design:** https://ant.design
- **Umi.js:** https://umijs.org
- **TypeScript:** https://typescriptlang.org
- **Axios:** https://axios-http.com

### Common Issues
| Problem | Solution |
|---------|----------|
| CORS error | Setup `django-cors-headers` in backend |
| 401 Unauthorized | Check token in localStorage |
| Data not showing | Verify API response format |
| TypeScript error | Check type definitions |
| Build fails | Check for unused imports |

---

## 🎓 Learning Path

### Week 1-2: JavaScript & React Basics
- Modern JavaScript ES6+
- React components, state, effects
- Practice: Build simple Todo app

### Week 3-4: TypeScript & Integration
- TypeScript fundamentals
- Axios & API calls
- Practice: Connect to fake API (JSONPlaceholder)

### Week 5-6: Project Development
- Understand project structure
- Develop Employee CRUD
- Add more features (Division, Position)

### Week 7-8: Advanced Concepts
- State management (if needed)
- Performance optimization
- Testing

### Week 9+: Deployment
- Docker basics
- CI/CD pipeline
- Production deployment

---

## 📊 Project Status

### ✅ Completed
- [x] Clean project structure
- [x] API layer with Axios
- [x] Auth API & Login page
- [x] Employee API & List page
- [x] Routes configuration
- [x] TypeScript types
- [x] Documentation

### 🚧 In Progress
- [ ] Employee Form (create/edit)
- [ ] Division CRUD
- [ ] Position CRUD

### 📝 Todo
- [ ] Reusable components library
- [ ] State management (if needed)
- [ ] Unit tests
- [ ] E2E tests
- [ ] Deployment setup

---

## 🚀 Next Steps

1. **Setup Development Environment**
   ```bash
   npm install
   npm start
   ```

2. **Develop Backend API**
   - Login endpoint
   - Employee CRUD endpoints
   - Test in Postman

3. **Connect & Test Frontend**
   - Login flow
   - Employee list
   - Add CRUD operations

4. **Expand Features**
   - Division management
   - Position management
   - Dashboard
   - Reports

---

## 💡 Best Practices

1. **Code Organization**
   - One feature = one folder
   - API calls in `src/api/`
   - Reusable components in `src/components/`

2. **TypeScript**
   - Always define types for API responses
   - Use interfaces for component props
   - Leverage type inference

3. **Error Handling**
   - Always use try-catch for async operations
   - Show user-friendly error messages
   - Log errors for debugging

4. **Performance**
   - Use React.memo for expensive components
   - Lazy load routes
   - Optimize images & assets

5. **Code Quality**
   - Run lint before commit
   - Write meaningful commit messages
   - Keep components small & focused

---

Selamat coding! 🎉

Kalau ada pertanyaan, refer ke dokumentasi atau ask for help.
