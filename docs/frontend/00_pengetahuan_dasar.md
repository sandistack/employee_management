# Pengetahuan Dasar Frontend - React, Docker & Webpack

Sebagai instruktur dengan 5++ tahun pengalaman web development, saya akan jelaskan secara lengkap dan bertahap.

## 🎯 Yang Harus Anda Pelajari (Berurutan)

### 1. **Modern JavaScript (ES6+)** - WAJIB! ⭐⭐⭐
Ini fondasi paling penting. Kalau ini belum kuat, React akan susah.

**Yang harus dikuasai:**
- Arrow Functions
- Destructuring
- Spread/Rest Operator
- Template Literals
- Promises & Async/Await
- Array Methods (map, filter, reduce)
- Modules (import/export)

**Contoh Real di Project:**
```javascript
// Destructuring dari API response
const { data, message, success } = response;

// Arrow function di React
const handleLogin = async (values) => {
  try {
    const response = await authAPI.login(values);
    // ...
  } catch (error) {
    // ...
  }
};

// Array map untuk render list
{employees.map(emp => (
  <Tag key={emp.id}>{emp.name}</Tag>
))}
```

**Waktu belajar:** 1-2 minggu
**Resource:** 
- JavaScript.info (website)
- MDN Web Docs

---

### 2. **React Fundamentals** - WAJIB! ⭐⭐⭐

**Konsep Core yang HARUS paham:**

#### a. Components & Props
```jsx
// Functional Component (yang modern)
const Button = ({ text, onClick, loading }) => {
  return (
    <button onClick={onClick} disabled={loading}>
      {text}
    </button>
  );
};

// Usage
<Button text="Login" onClick={handleLogin} loading={isLoading} />
```

#### b. State Management (useState)
```jsx
const [loading, setLoading] = useState(false);
const [data, setData] = useState([]);

// Update state
setLoading(true);
setData(newData);
```

#### c. Effects (useEffect)
```jsx
// Jalankan saat component mount
useEffect(() => {
  fetchEmployees();
}, []); // Empty array = run once

// Jalankan saat params berubah
useEffect(() => {
  fetchEmployees();
}, [params]); // Run when params changes
```

#### d. Event Handling
```jsx
const handleDelete = async (id) => {
  try {
    await employeeAPI.delete(id);
    message.success('Berhasil');
  } catch (error) {
    message.error('Gagal');
  }
};
```

**Waktu belajar:** 2-3 minggu
**Resource:**
- React.dev (official docs - TERBAIK!)
- Buat mini project: Todo List, Calculator

---

### 3. **TypeScript Basics** - PENTING ⭐⭐

**Kenapa TypeScript?**
- Deteksi error sebelum runtime
- Autocomplete lebih bagus di VS Code
- Code lebih maintainable

**Yang perlu dipahami:**
```typescript
// Type definition
interface Employee {
  id: number;
  name: string;
  email: string;
  positions: Position[];
}

// Function with types
const fetchEmployee = async (id: number): Promise<Employee> => {
  const response = await api.get(`/employees/${id}`);
  return response.data;
};

// Props typing
interface ButtonProps {
  text: string;
  onClick: () => void;
  loading?: boolean; // optional
}

const Button: React.FC<ButtonProps> = ({ text, onClick, loading }) => {
  // ...
};
```

**Waktu belajar:** 1 minggu (sambil praktek)
**Resource:**
- TypeScriptLang.org
- React TypeScript Cheatsheet

---

### 4. **Axios & API Integration** - PENTING ⭐⭐

**Konsep yang harus paham:**

#### a. HTTP Methods
- GET: Ambil data
- POST: Create data
- PUT/PATCH: Update data
- DELETE: Hapus data

#### b. Axios Instance (sudah saya buatkan!)
```typescript
// File: src/api/axios.ts
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// Request interceptor - inject token
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

#### c. Error Handling
```typescript
try {
  const response = await employeeAPI.getList();
  setData(response.results);
} catch (error) {
  if (error.response?.status === 401) {
    // Unauthorized - redirect to login
  } else if (error.response?.status === 500) {
    // Server error
  }
  message.error('Terjadi kesalahan');
}
```

**Waktu belajar:** 3-4 hari
**Resource:**
- Axios documentation
- Praktek langsung di project ini

---

### 5. **Ant Design (UI Library)** - MUDAH ⭐

**Yang perlu tau:**
- Components: Table, Form, Button, Modal, Message
- Grid System: Row, Col
- Icons: @ant-design/icons

**Contoh:**
```jsx
import { Table, Button, Space, message } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';

<Table
  columns={columns}
  dataSource={data}
  loading={loading}
  pagination={{
    current: page,
    total: total,
  }}
/>
```

**Waktu belajar:** Belajar sambil jalan (learning by doing)
**Resource:**
- ant.design (official docs)
- Lihat contoh di project ini

---

### 6. **Webpack** - OPSIONAL (Nanti aja) ⭐

**Apa itu Webpack?**
Webpack adalah **module bundler** yang mengcompile/bundle semua file JavaScript, CSS, gambar menjadi file static yang bisa dijalankan browser.

**Analogi sederhana:**
Bayangkan punya 100 file JS terpisah. Browser ga bisa langsung baca. Webpack "ngepack" semua jadi 1-2 file yang udah dioptimasi.

```
src/
  ├── App.tsx
  ├── api/
  ├── components/
  └── features/
         ↓
    WEBPACK BUILD
         ↓
dist/
  ├── main.js (semua JS jadi 1 file)
  ├── main.css
  └── index.html
```

**Apa yang Webpack lakukan:**
1. **Bundle JS modules** - gabung semua import/export
2. **Transpile** - convert TS ke JS, JSX ke JS
3. **Minify** - compress code biar lebih kecil
4. **Code splitting** - pecah jadi chunks untuk lazy load
5. **Asset processing** - handle images, fonts, CSS

**Di project Anda:**
Untungnya **Umi.js** (framework Ant Design Pro) sudah handle webpack secara internal! Jadi Anda **TIDAK PERLU** konfigurasi webpack manual.

**Kapan perlu belajar Webpack?**
- Kalau mau custom build process
- Optimasi performa advanced
- Setup dari scratch (tanpa framework)

**Waktu belajar:** Nanti kalau sudah mahir React (2-3 minggu kemudian)
**Resource:**
- Webpack.js.org (docs)
- Youtube: Webpack crash course

---

### 7. **Docker** - OPSIONAL (Untuk Deployment) ⭐

**Apa itu Docker?**
Docker adalah **containerization tool** yang "membungkus" aplikasi Anda beserta semua dependencies-nya jadi 1 paket yang bisa jalan di mana aja.

**Analogi sederhana:**
Kayak ngepacking laptop + charger + mouse ke dalam tas. Di mana aja dibuka, tinggal colok dan jalan. Ga perlu install ulang.

**Problem yang dipecahin Docker:**

Tanpa Docker:
```
Developer A: "Kok di laptop gw jalan, di laptop lo error?"
Developer B: "Node version gw beda mungkin..."
Server: "Python nya belum ter-install"
```

Dengan Docker:
```
Developer: "Nih Docker image-nya, tinggal run!"
Server: "OK, jalan!" ✅
```

**Konsep Docker:**

1. **Dockerfile** - Recipe/resep untuk build image
```dockerfile
# Contoh Dockerfile untuk React
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]
```

2. **Docker Image** - Template aplikasi (seperti ISO installer)
3. **Docker Container** - Running instance dari image

**Workflow Docker:**
```
1. Buat Dockerfile
2. Build image: docker build -t employee-frontend .
3. Run container: docker run -p 3000:3000 employee-frontend
4. Aplikasi jalan di http://localhost:3000
```

**Di Kantor:**
Biasanya pakai **docker-compose.yml** untuk orchestrate multiple containers:

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
  
  database:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
```

Jalanin semua: `docker-compose up`

**Kapan perlu belajar Docker?**
- Saat mau deploy ke production
- Setup development environment yang konsisten
- CI/CD pipeline

**Waktu belajar:** 1-2 minggu (setelah mahir React)
**Resource:**
- Docker.com (official docs)
- Youtube: Docker for beginners
- Praktek: Dockerize project ini

---

## 🎓 Roadmap Belajar (Rekomendasi)

### **Fase 1: Foundation (3-4 minggu)**
1. ✅ Modern JavaScript ES6+ (1-2 minggu)
2. ✅ React Fundamentals (2 minggu)
3. ✅ TypeScript Basics (sambil praktek)

**Target:** Bisa bikin CRUD sederhana tanpa styling

---

### **Fase 2: Integration (2-3 minggu)**
4. ✅ Axios & API calls (3-4 hari)
5. ✅ Ant Design components (learning by doing)
6. ✅ State management di React

**Target:** Connect frontend ke Django backend Anda

---

### **Fase 3: Real Project (2-3 minggu)**
7. ✅ Praktek di project Employee Management ini
   - Login/Logout
   - Employee CRUD
   - Form validation
   - Error handling

**Target:** Aplikasi jalan lengkap

---

### **Fase 4: Advanced (Opsional)**
8. Webpack (kalau perlu custom build)
9. Docker (untuk deployment)
10. Testing (Jest, React Testing Library)
11. State management library (Zustand/Redux)

---

## 💡 Tips dari Pengalaman Saya

### 1. **Jangan Langsung Loncat ke Docker/Webpack**
Fokus dulu ke React & API integration. Docker/Webpack itu alat, bukan skill utama.

### 2. **Learning by Doing**
Teori cukup 20%, praktek 80%. Langsung code, error, debug, repeat.

### 3. **Pakai Tools yang Sudah Jadi**
- ✅ Create React App / Vite / Umi.js → sudah setup webpack
- ✅ Ant Design Pro → sudah setup routing & layout
- ❌ Jangan setup webpack manual dulu

### 4. **Mulai dari Yang Simple**
```
Step 1: Tampilkan data dari API ✅
Step 2: Bikin form create ✅
Step 3: Edit & delete ✅
Step 4: Baru pikirin Docker/deployment
```

### 5. **Debugging adalah Skill Penting**
Gunakan:
- Chrome DevTools (Network tab untuk API)
- React DevTools (untuk state)
- Console.log() adalah teman Anda

---

## 📚 Resources Terbaik (Free)

1. **JavaScript:** javascript.info
2. **React:** react.dev (official - WAJIB!)
3. **TypeScript:** typescriptlang.org
4. **Ant Design:** ant.design
5. **Axios:** axios-http.com
6. **Docker:** docs.docker.com
7. **Webpack:** webpack.js.org

**Channel YouTube:**
- Web Dev Simplified
- Traversy Media
- Fireship (untuk overview cepat)

---

## 🚀 Next Steps (Setelah Setup Ini)

1. **Pahami struktur yang sudah saya buat**
   - Lihat `src/api/` - bagaimana axios di-setup
   - Lihat `src/features/auth/LoginPage.tsx` - contoh form
   - Lihat `src/features/employee/EmployeeListPage.tsx` - contoh table

2. **Buat API di Django backend dulu**
   ```
   POST /api/auth/login/
   GET  /api/employees/
   POST /api/employees/
   etc.
   ```

3. **Test API pakai Postman/Thunder Client**
   Pastikan API jalan dulu sebelum connect ke frontend

4. **Jalankan frontend**
   ```bash
   npm install
   npm start
   ```

5. **Connect & Test**
   Login → Employee List → CRUD operations

---

## ❓ FAQ

**Q: Apakah harus belajar Webpack/Docker sekarang?**
A: TIDAK. Fokus React + API dulu. Ant Design Pro sudah handle webpack.

**Q: Berapa lama sampai bisa?**
A: 2-3 bulan untuk comfortable, 6 bulan untuk mahir.

**Q: Lebih prioritas Docker atau Webpack?**
A: Untuk sekarang, TIDAK PERLU KEDUANYA. Fokus React + API integration dulu.

**Q: Kalau di kantor pakai Docker, saya harus belajar sekarang?**
A: Cukup paham konsep dasar (image, container, docker-compose). Detail bisa belajar sambil jalan.

**Q: Build React itu maksudnya apa?**
A: Convert semua file TS/JSX ke plain JS yang bisa dipahami browser. Command: `npm run build`

---

## 🎯 Kesimpulan

**Yang WAJIB sekarang:**
1. ✅ JavaScript ES6+
2. ✅ React (useState, useEffect, components)
3. ✅ TypeScript basics
4. ✅ Axios for API calls
5. ✅ Ant Design (learning by doing)

**Yang NANTI (setelah mahir React):**
6. ⏳ Webpack (opsional, kalau mau custom build)
7. ⏳ Docker (untuk deployment)

**Fokus Anda sekarang:**
→ Bikin backend API dulu
→ Test di Postman
→ Connect frontend (yang sudah saya setup)
→ CRUD Employee dengan Ant Design

Docker & Webpack? **Nanti aja!** Jangan overwhelm diri sendiri.

---

Good luck! 🚀 Kalau ada pertanyaan, tanya aja.
