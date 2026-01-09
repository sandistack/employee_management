# Struktur Frontend - Employee Management

Dokumentasi lengkap struktur folder frontend yang sudah di-setup.

## 📁 Struktur Folder Final

```
employee-frontend/
├── config/                    # Konfigurasi Umi.js
│   ├── config.ts             # Main config
│   ├── routes.ts             # Route definitions ⭐
│   ├── defaultSettings.ts    # Layout settings
│   └── proxy.ts              # API proxy untuk development
│
├── public/                    # Static files
│   └── icons/                
│
├── src/
│   ├── api/                  # 🔥 API Layer (Backend communication)
│   │   ├── axios.ts          # Axios instance + interceptors
│   │   ├── auth.api.ts       # Auth endpoints
│   │   ├── employee.api.ts   # Employee endpoints
│   │   └── index.ts          # Export all APIs
│   │
│   ├── components/           # 🔥 Reusable UI Components
│   │   ├── index.ts          # Export all components
│   │   └── (akan diisi nanti)
│   │
│   ├── features/             # 🔥 Feature Modules (Most Important!)
│   │   ├── auth/            
│   │   │   ├── LoginPage.tsx
│   │   │   ├── LoginPage.less
│   │   │   └── (store/hooks akan ditambah)
│   │   │
│   │   └── employee/
│   │       ├── EmployeeListPage.tsx
│   │       └── (EmployeeForm, dll akan ditambah)
│   │
│   ├── layouts/              # Layout components
│   │   └── (akan diisi nanti)
│   │
│   ├── types/                # 🔥 TypeScript Types
│   │   └── index.ts          # Common types
│   │
│   ├── utils/                # Helper functions
│   │   └── helpers/
│   │
│   ├── pages/                # Special pages
│   │   └── 404.tsx           # Not found page
│   │
│   ├── app.tsx               # Runtime config
│   ├── access.ts             # Permission logic
│   └── requestErrorConfig.ts # Error handling config
│
├── package.json
├── tsconfig.json
└── .env.example              # Environment variables template
```

---

## 🔥 Penjelasan Per Folder

### 1. `src/api/` - API Layer

**Purpose:** Semua komunikasi dengan Django backend ada di sini.

#### `axios.ts` - Axios Instance
```typescript
// Setup base configuration
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// Request interceptor: inject token ke setiap request
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: handle token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Handle 401, retry with refresh token
  }
);
```

**Keuntungan:**
- ✅ DRY (Don't Repeat Yourself) - ga perlu set token manual tiap request
- ✅ Auto refresh token kalau expired
- ✅ Centralized error handling

#### `auth.api.ts` - Auth Endpoints
```typescript
export const authAPI = {
  login: (credentials) => POST /api/auth/login/
  logout: () => POST /api/auth/logout/
  getCurrentUser: () => GET /api/auth/me/
  refreshToken: (token) => POST /api/auth/token/refresh/
}
```

#### `employee.api.ts` - Employee Endpoints
```typescript
export const employeeAPI = {
  getList: (params) => GET /api/employees/
  getById: (id) => GET /api/employees/:id/
  create: (data) => POST /api/employees/
  update: (id, data) => PATCH /api/employees/:id/
  delete: (id) => DELETE /api/employees/:id/
}
```

**Cara pakai:**
```typescript
import { employeeAPI } from '@/api';

// Di component
const fetchData = async () => {
  try {
    const response = await employeeAPI.getList({ page: 1 });
    setData(response.results);
  } catch (error) {
    message.error('Gagal memuat data');
  }
};
```

---

### 2. `src/components/` - Reusable Components

**Purpose:** Komponen UI yang bisa dipakai berkali-kali di berbagai halaman.

**Contoh yang bisa dibuat nanti:**
```
components/
├── Button/
│   ├── Button.tsx        # Custom button dengan styling konsisten
│   └── Button.less
├── Table/
│   ├── DataTable.tsx     # Table dengan pagination & search built-in
│   └── DataTable.less
├── Form/
│   ├── FormInput.tsx     # Input dengan validation display
│   └── FormSelect.tsx
└── Modal/
    ├── ConfirmModal.tsx  # Reusable confirm dialog
    └── FormModal.tsx     # Modal dengan form
```

**Prinsip:**
- Komponen harus **generic** dan **reusable**
- Terima props untuk customization
- Tidak boleh ada business logic (hanya UI)

**Contoh baik:**
```tsx
// ✅ GOOD - Generic button
<Button 
  text="Delete" 
  onClick={handleDelete} 
  danger 
  loading={loading} 
/>
```

**Contoh buruk:**
```tsx
// ❌ BAD - Terlalu spesifik
<DeleteEmployeeButton employeeId={123} />
```

---

### 3. `src/features/` - Feature Modules ⭐ IMPORTANT!

**Purpose:** Organize code by FEATURE, bukan by TYPE.

**Old way (by type):**
```
src/
├── components/
│   ├── EmployeeList.tsx
│   ├── EmployeeForm.tsx
│   └── LoginForm.tsx
├── api/
│   ├── employeeAPI.ts
│   └── authAPI.ts
└── store/
    ├── employeeStore.ts
    └── authStore.ts
```
❌ Problem: File yang related tersebar di berbagai folder

**New way (by feature):**
```
src/features/
├── auth/
│   ├── LoginPage.tsx        # UI
│   ├── auth.store.ts        # State management (nanti)
│   └── auth.hooks.ts        # Custom hooks (nanti)
│
└── employee/
    ├── EmployeeListPage.tsx
    ├── EmployeeForm.tsx
    ├── EmployeeDetail.tsx
    ├── employee.store.ts    # State management
    └── employee.hooks.ts    # Custom hooks
```
✅ Benefit: Semua yang related ke employee ada di 1 folder

**Struktur detail per feature:**
```
features/employee/
├── EmployeeListPage.tsx      # Main page - list semua employee
├── EmployeeForm.tsx          # Form untuk create/edit
├── EmployeeDetail.tsx        # Detail 1 employee
├── components/               # Sub-components (opsional)
│   ├── EmployeeCard.tsx
│   └── EmployeeFilter.tsx
├── employee.store.ts         # Zustand/Redux store (opsional)
├── employee.hooks.ts         # Custom hooks
└── employee.types.ts         # Types khusus feature ini
```

**Kapan bikin feature baru?**
- Kalau ada entitas/modul bisnis baru (Division, Position, Attendance, dll)
- Setiap feature punya CRUD sendiri

---

### 4. `src/types/` - TypeScript Types

**Purpose:** Type definitions yang dipakai di banyak tempat.

**Isi saat ini:**
```typescript
// User types
export interface User {
  id: number;
  username: string;
  email: string;
  // ...
}

// Auth state
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

// Pagination
export interface TablePaginationConfig {
  current: number;
  pageSize: number;
  total: number;
}
```

**Kapan naruh type di sini vs di feature?**
- Di `types/`: Type yang dipakai di multiple features (User, ApiResponse, Pagination)
- Di `feature/`: Type yang spesifik ke feature itu (EmployeeFormData)

---

### 5. `src/utils/` - Helper Functions

**Purpose:** Pure functions yang ga punya side effect.

**Contoh yang bisa dibuat:**
```typescript
// utils/helpers/date.ts
export const formatDate = (date: string) => {
  return dayjs(date).format('DD/MM/YYYY');
};

// utils/helpers/validation.ts
export const isValidEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// utils/helpers/format.ts
export const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
  }).format(amount);
};
```

**Usage:**
```typescript
import { formatDate, formatCurrency } from '@/utils/helpers';

const formatted = formatDate(employee.date_joined);
// "08/01/2026"
```

---

### 6. `config/routes.ts` - Route Configuration

**Purpose:** Define semua routes aplikasi.

**Struktur sekarang:**
```typescript
export default [
  // No layout (login page)
  {
    path: '/user',
    layout: false,
    routes: [
      {
        path: '/user/login',
        component: './features/auth/LoginPage',
      },
    ],
  },
  
  // With layout (main app)
  {
    path: '/employee',
    name: 'Employee',
    icon: 'team',
    routes: [
      {
        path: '/employee/list',
        component: './features/employee/EmployeeListPage',
      },
    ],
  },
];
```

**Nanti bisa expand:**
```typescript
{
  path: '/employee',
  name: 'Employee',
  icon: 'team',
  routes: [
    {
      path: '/employee/list',
      name: 'List',
      component: './features/employee/EmployeeListPage',
    },
    {
      path: '/employee/create',
      name: 'Create',
      component: './features/employee/EmployeeForm',
    },
    {
      path: '/employee/:id/edit',
      name: 'Edit',
      component: './features/employee/EmployeeForm',
      hideInMenu: true, // Ga muncul di sidebar
    },
    {
      path: '/employee/:id',
      name: 'Detail',
      component: './features/employee/EmployeeDetail',
      hideInMenu: true,
    },
  ],
},
{
  path: '/division',
  name: 'Division',
  icon: 'apartment',
  component: './features/division/DivisionPage',
},
```

---

## 🎯 Best Practices

### 1. **Import Aliases**
Pakai `@/` untuk import dari src:
```typescript
// ✅ GOOD
import { employeeAPI } from '@/api';
import { User } from '@/types';

// ❌ BAD
import { employeeAPI } from '../../../api';
```

### 2. **File Naming**
- Components: PascalCase → `EmployeeListPage.tsx`
- Utilities: camelCase → `formatDate.ts`
- Types: camelCase → `index.ts`
- Styles: same as component → `EmployeeListPage.less`

### 3. **Folder Structure**
Kalau feature punya banyak file, buat subfolder:
```
employee/
├── pages/
│   ├── EmployeeListPage.tsx
│   ├── EmployeeFormPage.tsx
│   └── EmployeeDetailPage.tsx
├── components/
│   ├── EmployeeCard.tsx
│   └── EmployeeFilter.tsx
└── hooks/
    └── useEmployee.ts
```

### 4. **Separation of Concerns**
- **API calls** → di `src/api/`
- **Business logic** → di feature hooks/store
- **UI** → di feature pages/components
- **Helpers** → di `src/utils/`

---

## 📝 Checklist: Apa yang Sudah & Belum

### ✅ Yang Sudah Dibuat
- [x] Struktur folder clean
- [x] API layer dengan axios
- [x] Auth API (login, logout, getCurrentUser)
- [x] Employee API (CRUD endpoints)
- [x] LoginPage dengan styling
- [x] EmployeeListPage dengan table
- [x] Routes configuration
- [x] TypeScript types
- [x] 404 page

### ⏳ Yang Perlu Dibuat Nanti
- [ ] EmployeeForm (create/edit)
- [ ] EmployeeDetail page
- [ ] Division CRUD
- [ ] Position CRUD
- [ ] Custom reusable components
- [ ] State management (kalau perlu)
- [ ] Unit tests
- [ ] E2E tests

---

## 🚀 Next Steps

1. **Buat backend API dulu** (Django)
   - POST `/api/auth/login/`
   - GET `/api/employees/`
   - dll.

2. **Test API di Postman**
   Pastikan return data sesuai TypeScript types

3. **Setup .env**
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

4. **Run frontend**
   ```bash
   npm install
   npm start
   ```

5. **Test login flow**
   Login → Lihat employee list

6. **Develop EmployeeForm**
   Create & Edit employee

---

## ❓ FAQ

**Q: Kenapa pakai feature folder pattern?**
A: Lebih scalable. Kalau ada 20 features, tetap rapi. Ga semua file tercampur jadi satu.

**Q: Kalau komponen cuma dipake di 1 feature, taruh di components/ atau feature/?**
A: Di dalam feature. Kalau nanti dipake di tempat lain, baru pindah ke components/.

**Q: Harus pakai state management (Redux/Zustand)?**
A: Belum perlu. Cukup useState/useEffect dulu. Kalau data sharing antar component ribet, baru pakai.

**Q: Styling pakai apa?**
A: Ant Design untuk components. Custom styling pakai .less files (sudah included).

**Q: API error handling gimana?**
A: Sudah di-handle di axios interceptor. Tinggal catch di component dan tampilkan message.

---

Semoga jelas! 🚀
