# Quick Start Guide - Frontend Development

Panduan cepat untuk mulai develop frontend employee management.

## 🚀 Setup Awal

### 1. Install Dependencies
```bash
cd employee-frontend
npm install
```

### 2. Setup Environment Variables
```bash
# Copy .env.example
cp .env.example .env

# Edit .env
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Run Development Server
```bash
npm start
```

Browser akan otomatis buka di `http://localhost:8000`

---

## 📋 Development Workflow

### Step 1: Buat Backend API Dulu

**Di Django backend:**

```python
# apps/accounts/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user:
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # ...
            }
        })
    
    return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['GET'])
def employee_list(request):
    employees = User.objects.all()
    # Serialize & return
    return Response({
        'count': employees.count(),
        'results': [...]
    })
```

**URLs:**
```python
# config/urls.py
urlpatterns = [
    path('api/auth/login/', login_view),
    path('api/employees/', employee_list),
    # ...
]
```

### Step 2: Test API di Postman

**Test Login:**
```
POST http://localhost:8000/api/auth/login/
Body:
{
    "username": "admin",
    "password": "admin123"
}

Expected Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "username": "admin",
        ...
    }
}
```

**Test Get Employees:**
```
GET http://localhost:8000/api/employees/
Headers:
Authorization: Bearer <access_token>

Expected Response:
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "john",
            "email": "john@example.com",
            ...
        }
    ]
}
```

### Step 3: Connect Frontend

Frontend sudah siap! Tinggal test:

1. **Jalankan backend:**
   ```bash
   cd employee_management
   python manage.py runserver
   ```

2. **Jalankan frontend:**
   ```bash
   cd employee-frontend
   npm start
   ```

3. **Test login:**
   - Buka http://localhost:8000/user/login
   - Input username & password
   - Kalau berhasil → redirect ke employee list

4. **Lihat employee list:**
   - Seharusnya menampilkan table dengan data dari API

---

## 🔍 Debugging Tips

### Problem: CORS Error

**Error:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/...' 
from origin 'http://localhost:8000' has been blocked by CORS policy
```

**Solution - Django:**
```bash
pip install django-cors-headers
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# Development only!
CORS_ALLOW_ALL_ORIGINS = True

# Production:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Problem: 401 Unauthorized

**Check:**
1. Token tersimpan di localStorage?
   - Buka DevTools → Application → Local Storage
   - Cari `access_token` dan `refresh_token`

2. Token valid?
   - Copy token
   - Paste di jwt.io
   - Check expiration time

3. Header correct?
   - Buka DevTools → Network tab
   - Click request
   - Check Headers → Authorization: Bearer <token>

**Fix:**
```typescript
// Sudah di-handle di src/api/axios.ts
// Auto inject token ke setiap request
```

### Problem: Data tidak muncul

**Check:**
1. API response sesuai type definition?
   ```typescript
   // Frontend expect:
   interface PaginatedResponse<T> {
     count: number;
     results: T[];
   }
   
   // Django harus return:
   {
     "count": 10,
     "results": [...]
   }
   ```

2. Console ada error?
   - Buka DevTools → Console
   - Lihat error message

3. Network request berhasil?
   - DevTools → Network
   - Check status code (200 OK?)
   - Check response data

---

## 📝 Develop New Feature

Contoh: Bikin Division CRUD

### 1. Buat API Service

**File:** `src/api/division.api.ts`
```typescript
import axiosInstance from './axios';
import type { PaginatedResponse } from './axios';

export interface Division {
  id: number;
  name: string;
  description: string;
}

export const divisionAPI = {
  getList: async (): Promise<PaginatedResponse<Division>> => {
    const response = await axiosInstance.get('/divisions/');
    return response.data;
  },
  
  create: async (data: Omit<Division, 'id'>): Promise<Division> => {
    const response = await axiosInstance.post('/divisions/', data);
    return response.data;
  },
  
  // update, delete, dll...
};
```

**Export:** `src/api/index.ts`
```typescript
export * from './division.api';
```

### 2. Buat Feature Folder

```bash
mkdir -p src/features/division
```

### 3. Buat List Page

**File:** `src/features/division/DivisionListPage.tsx`
```tsx
import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import { divisionAPI, type Division } from '@/api';

const DivisionListPage: React.FC = () => {
  const [data, setData] = useState<Division[]>([]);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await divisionAPI.getList();
      setData(response.results);
    } catch (error) {
      message.error('Gagal memuat data');
    } finally {
      setLoading(false);
    }
  };
  
  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nama', dataIndex: 'name', key: 'name' },
    { title: 'Deskripsi', dataIndex: 'description', key: 'description' },
  ];
  
  return (
    <Table 
      columns={columns} 
      dataSource={data} 
      loading={loading}
      rowKey="id"
    />
  );
};

export default DivisionListPage;
```

### 4. Tambah Route

**File:** `config/routes.ts`
```typescript
{
  path: '/division',
  name: 'Division',
  icon: 'apartment',
  component: './features/division/DivisionListPage',
},
```

### 5. Test

1. Restart dev server (Ctrl+C, npm start)
2. Buka http://localhost:8000/division
3. Data muncul!

---

## 🎨 Styling Tips

### Menggunakan Ant Design Components

```tsx
import { 
  Button, 
  Table, 
  Form, 
  Input, 
  Modal, 
  message,
  Space,
  Card,
  Tag,
  Popconfirm 
} from 'antd';
import { 
  EditOutlined, 
  DeleteOutlined, 
  PlusOutlined 
} from '@ant-design/icons';

// Usage
<Button type="primary" icon={<PlusOutlined />}>
  Tambah
</Button>

<Tag color="green">Aktif</Tag>

<Popconfirm
  title="Yakin hapus?"
  onConfirm={handleDelete}
>
  <Button danger>Hapus</Button>
</Popconfirm>
```

### Custom Styling dengan LESS

**File:** `src/features/employee/EmployeeList.less`
```less
.employee-list {
  padding: 24px;
  
  .search-bar {
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
  }
  
  .table-wrapper {
    background: white;
    padding: 24px;
    border-radius: 8px;
  }
}
```

**Usage:**
```tsx
import styles from './EmployeeList.less';

<div className={styles.employeeList}>
  <div className={styles.searchBar}>
    <Search />
    <Button>Add</Button>
  </div>
</div>
```

---

## 📚 Useful Snippets

### Loading State
```tsx
const [loading, setLoading] = useState(false);

const fetchData = async () => {
  setLoading(true);
  try {
    // API call
  } finally {
    setLoading(false); // Always executed
  }
};
```

### Form Submit
```tsx
const [form] = Form.useForm();

const handleSubmit = async (values: any) => {
  try {
    await employeeAPI.create(values);
    message.success('Berhasil!');
    form.resetFields();
  } catch (error) {
    message.error('Gagal!');
  }
};

<Form form={form} onFinish={handleSubmit}>
  <Form.Item name="username" rules={[{ required: true }]}>
    <Input />
  </Form.Item>
  <Button htmlType="submit">Submit</Button>
</Form>
```

### Modal with Form
```tsx
const [modalVisible, setModalVisible] = useState(false);

<Modal
  title="Tambah Employee"
  open={modalVisible}
  onCancel={() => setModalVisible(false)}
  footer={null}
>
  <Form onFinish={handleSubmit}>
    {/* Form fields */}
  </Form>
</Modal>
```

### Confirmation before Delete
```tsx
<Popconfirm
  title="Hapus data ini?"
  description="Data yang dihapus tidak bisa dikembalikan"
  onConfirm={() => handleDelete(record.id)}
  okText="Ya"
  cancelText="Tidak"
>
  <Button danger icon={<DeleteOutlined />}>
    Hapus
  </Button>
</Popconfirm>
```

---

## 🔥 Common Patterns

### CRUD Pattern

```tsx
// List
const [data, setData] = useState([]);
const fetchData = async () => { /* ... */ };

// Create
const handleCreate = async (values) => {
  await api.create(values);
  fetchData(); // Refresh list
};

// Update
const handleUpdate = async (id, values) => {
  await api.update(id, values);
  fetchData();
};

// Delete
const handleDelete = async (id) => {
  await api.delete(id);
  fetchData();
};
```

### Pagination Pattern

```tsx
const [pagination, setPagination] = useState({
  current: 1,
  pageSize: 10,
  total: 0,
});

const fetchData = async () => {
  const response = await api.getList({
    page: pagination.current,
    page_size: pagination.pageSize,
  });
  
  setData(response.results);
  setPagination({ ...pagination, total: response.count });
};

<Table
  pagination={{
    ...pagination,
    onChange: (page, pageSize) => {
      setPagination({ ...pagination, current: page, pageSize });
    },
  }}
/>
```

---

## ⚡ Performance Tips

### 1. Memo untuk prevent re-render
```tsx
import { memo } from 'react';

const EmployeeCard = memo(({ employee }) => {
  return <div>{employee.name}</div>;
});
```

### 2. useCallback untuk functions
```tsx
import { useCallback } from 'react';

const handleDelete = useCallback((id: number) => {
  // delete logic
}, []); // Dependencies
```

### 3. Lazy load components
```tsx
import { lazy, Suspense } from 'react';

const EmployeeDetail = lazy(() => import('./EmployeeDetail'));

<Suspense fallback={<Spin />}>
  <EmployeeDetail />
</Suspense>
```

---

## 🎯 Checklist Development

Setiap kali develop feature baru:

- [ ] Backend API ready & tested di Postman
- [ ] Buat API service di `src/api/`
- [ ] Buat TypeScript types
- [ ] Buat feature folder & components
- [ ] Add routes di `config/routes.ts`
- [ ] Test di browser
- [ ] Handle loading & error states
- [ ] Add proper validation
- [ ] Test CRUD operations
- [ ] Styling dengan Ant Design
- [ ] Mobile responsive (kalau perlu)

---

## 📞 Need Help?

**Check Documentation:**
1. [00_pengetahuan_dasar.md](./00_pengetahuan_dasar.md) - Fundamental knowledge
2. [01_struktur_folder.md](./01_struktur_folder.md) - Folder structure details
3. [02_cleanup_checklist.md](./02_cleanup_checklist.md) - What's removed

**External Resources:**
- React Docs: https://react.dev
- Ant Design: https://ant.design
- Umi.js: https://umijs.org
- Axios: https://axios-http.com

**Common Issues:**
- CORS error → Setup django-cors-headers
- 401 error → Check token & authentication
- Data not showing → Check API response format
- TypeScript errors → Check type definitions

---

Selamat coding! 🚀
