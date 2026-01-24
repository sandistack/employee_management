# API Documentation Guide

## 🎯 Akses API Documentation

Setelah menjalankan server Django (`python manage.py runserver`), Anda dapat mengakses dokumentasi API di:

### 1. **Swagger UI** (Interactive API Testing)
```
http://localhost:8000/api/docs/
```
**Fitur:**
- ✅ Interactive testing - bisa langsung test API dari browser
- ✅ Try it out feature - input data dan lihat response langsung
- ✅ Authentication support - bisa login dan test protected endpoints
- ✅ Request/Response examples

**Cara menggunakan:**
1. Buka http://localhost:8000/api/docs/
2. Klik endpoint yang ingin ditest
3. Klik "Try it out"
4. Isi parameter/body
5. Klik "Execute"
6. Lihat response

**Untuk Protected Endpoints:**
1. Login dulu via `/api/v1/login/` untuk dapat JWT token
2. Copy access token
3. Klik tombol "Authorize" (🔒 icon) di kanan atas
4. Masukkan: `Bearer <your-access-token>`
5. Klik "Authorize"
6. Sekarang bisa akses protected endpoints

### 2. **ReDoc** (Beautiful Documentation)
```
http://localhost:8000/api/redoc/
```
**Fitur:**
- ✅ Clean, modern interface
- ✅ Better for reading documentation
- ✅ Grouping by tags
- ✅ Search functionality
- ✅ Three-column layout

**Cocok untuk:**
- Membaca dokumentasi
- Memahami API structure
- Share ke team/client

### 3. **OpenAPI Schema** (JSON/YAML)
```
http://localhost:8000/api/schema/
```
**Fitur:**
- ✅ Raw OpenAPI 3.0 schema
- ✅ Machine-readable format
- ✅ Dapat digunakan untuk code generation

**Cocok untuk:**
- Generate client SDK (JavaScript, Python, etc)
- Import ke Postman/Insomnia
- CI/CD testing
- API versioning

---

## 📋 List API Endpoints Yang Sudah Ada

### Authentication APIs (`/api/v1/`)

#### 1. Register
- **Endpoint:** `POST /api/v1/register/`
- **Permission:** Public (AllowAny)
- **Description:** Daftar user baru
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- **Response:** User data + JWT tokens

#### 2. Login
- **Endpoint:** `POST /api/v1/login/`
- **Permission:** Public (AllowAny)
- **Description:** Login dan dapat JWT token
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password123"
  }
  ```
- **Response:** User data + JWT tokens

#### 3. Logout
- **Endpoint:** `POST /api/v1/logout/`
- **Permission:** Authenticated
- **Description:** Logout dan blacklist refresh token
- **Request Body:**
  ```json
  {
    "refresh": "your-refresh-token"
  }
  ```

#### 4. Refresh Token
- **Endpoint:** `POST /api/v1/token/refresh/`
- **Permission:** Public (AllowAny)
- **Description:** Refresh access token
- **Request Body:**
  ```json
  {
    "refresh": "your-refresh-token"
  }
  ```

#### 5. Profile
- **Endpoint:** `GET /api/v1/profile/`
- **Permission:** Authenticated
- **Description:** Get user profile
- **Response:** Current user data

- **Endpoint:** `PUT /api/v1/profile/`
- **Description:** Update profile

- **Endpoint:** `PATCH /api/v1/profile/`
- **Description:** Partial update profile

#### 6. Change Password
- **Endpoint:** `POST /api/v1/change-password/`
- **Permission:** Authenticated
- **Description:** Ganti password
- **Request Body:**
  ```json
  {
    "old_password": "current_password",
    "new_password": "new_secure_password"
  }
  ```

---

## 🎨 Best Practices untuk API Documentation

### 1. Selalu Gunakan `@extend_schema` Decorator

```python
from drf_spectacular.utils import extend_schema, OpenApiResponse

@extend_schema(
    tags=['Resource Name'],
    summary='Short description',
    description='Detailed description of what this endpoint does',
    request=YourSerializer,
    responses={
        200: YourResponseSerializer,
        400: OpenApiResponse(description='Validation error'),
        404: OpenApiResponse(description='Not found'),
    }
)
class YourViewSet(viewsets.ModelViewSet):
    pass
```

### 2. Group Endpoints dengan Tags

```python
@extend_schema(tags=['Authentication'])  # Group auth endpoints
class LoginView(APIView):
    pass

@extend_schema(tags=['Employees'])  # Group employee endpoints
class EmployeeViewSet(viewsets.ModelViewSet):
    pass
```

### 3. Document Request/Response Examples

```python
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    examples=[
        OpenApiExample(
            'Valid Example',
            value={
                'email': 'user@example.com',
                'password': 'password123'
            },
            request_only=True,
        ),
    ]
)
```

### 4. Describe Query Parameters

```python
from drf_spectacular.utils import OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            type=str,
            description='Search by name or email',
            required=False,
        ),
        OpenApiParameter(
            name='status',
            type=str,
            enum=['active', 'inactive'],
            description='Filter by status',
        ),
    ]
)
```

---

## 🚀 Workflow Development dengan API Docs

### Untuk Backend Developer:
1. Buat model & serializer
2. Buat viewset/view dengan `@extend_schema`
3. Test di Swagger UI
4. Review di ReDoc
5. Update documentation jika ada perubahan

### Untuk Frontend Developer:
1. Buka ReDoc untuk lihat available endpoints
2. Buka Swagger UI untuk test API
3. Test authentication flow
4. Test dengan real data
5. Handle error cases

### Untuk Testing:
1. Download OpenAPI schema
2. Import ke Postman/Insomnia
3. Setup environment variables
4. Create test collections
5. Automate dengan newman/CI

---

## 📦 Export API Documentation

### 1. Export Schema ke File
```bash
python manage.py spectacular --file schema.yml
```

### 2. Generate untuk Postman
```bash
python manage.py spectacular --format openapi-json --file api-schema.json
```
Kemudian import `api-schema.json` ke Postman

### 3. Generate Client SDK
```bash
# Install openapi-generator
npm install @openapitools/openapi-generator-cli -g

# Generate TypeScript client
openapi-generator-cli generate -i schema.yml -g typescript-axios -o ./client
```

---

## 🔧 Tips & Tricks

### 1. Automatic Schema Generation
drf-spectacular akan automatic generate documentation dari:
- Serializers
- ViewSets
- Permissions
- Filter backends
- Pagination

### 2. Custom Schema
Jika auto-generate tidak sesuai:
```python
@extend_schema(
    request=CustomRequestSerializer,
    responses={
        200: CustomResponseSerializer,
    }
)
```

### 3. Exclude dari Documentation
```python
@extend_schema(exclude=True)
class InternalAPIView(APIView):
    pass
```

### 4. Version API Documentation
```python
SPECTACULAR_SETTINGS = {
    'VERSION': '1.0.0',  # Update ini saat ada breaking changes
}
```

---

## 🎓 Kenapa drf-spectacular? (Senior Developer Perspective)

### ✅ Advantages:
1. **OpenAPI 3.0 Standard** - More modern than Swagger 2.0
2. **Auto-generated** - Less maintenance
3. **Type-safe** - Better with Python type hints
4. **Django-native** - Deep integration with DRF
5. **Client generation** - Generate SDK untuk berbagai language
6. **CI/CD friendly** - Easy to test schema validity

### ⚠️ Alternatives (NOT Recommended):
- ❌ **drf-yasg** - Uses Swagger 2.0 (outdated)
- ❌ **Manual Swagger** - Too much maintenance
- ❌ **Postman Collections** - Not auto-generated
- ❌ **API Blueprint** - Less popular

### 💡 Industry Standard:
- Google uses OpenAPI
- Stripe uses OpenAPI
- GitHub uses OpenAPI
- Semua major tech companies menggunakan OpenAPI 3.0

---

## 📝 Next Steps

### Immediate:
1. ✅ Jalankan `python manage.py runserver`
2. ✅ Buka http://localhost:8000/api/docs/
3. ✅ Test register & login endpoints
4. ✅ Test authenticated endpoints

### Soon:
1. 📝 Add more endpoints (Employees, Divisions, Positions)
2. 📝 Add filtering & searching documentation
3. 📝 Add pagination documentation
4. 📝 Add file upload examples
5. 📝 Add bulk operations

### Production:
1. 🔒 Disable Swagger UI in production (optional)
2. 🔒 Add API rate limiting
3. 🔒 Add API versioning
4. 🔒 Setup API monitoring
5. 🔒 Generate client SDKs

---

## 🐛 Troubleshooting

### Schema generation error?
```bash
python manage.py spectacular --validate
```

### Swagger UI not showing?
Check if 'drf_spectacular' in INSTALLED_APPS

### Authentication not working in Swagger?
Click "Authorize" button and use: `Bearer <access-token>`

### Schema tidak update?
Hard refresh browser (Ctrl+Shift+R) atau clear cache
