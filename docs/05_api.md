# 05. API Documentation

> Daftar endpoint RESTful API, format request/response, dan contoh penggunaan.

## 📋 Overview

Dokumen ini menjelaskan endpoint utama, authentication, dan contoh request/response.

## 🔑 Authentication

- JWT (djangorestframework-simplejwt)
- Token di header: `Authorization: Bearer <token>`

## 📚 Endpoint List

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET    | /api/v1/users/ | List users |
| POST   | /api/v1/users/ | Create user |
| ...    | ...      | ...       |

## 📦 Contoh Request/Response

```http
GET /api/v1/users/
Authorization: Bearer <token>
```

```json
{
  "results": [
    {"id": 1, "username": "admin"}
  ]
}
```

## 📝 Lanjutkan ke:
- [06_testing.md](06_testing.md) - Testing strategy
- [guides/README.md](guides/README.md) - Step-by-step development
