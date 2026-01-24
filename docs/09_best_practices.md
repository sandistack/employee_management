# Django Best Practices - Senior Developer Guide (10+ Years Experience)

## 🏗️ Architecture Principles

### 1. Project Structure (Yang Anda Sudah Gunakan - BAGUS! ✅)

```
project/
├── apps/                    # Django apps (business logic)
│   ├── accounts/           # User management
│   ├── core/               # Shared utilities
│   └── employees/          # Future: Employee management
├── api/                     # API layer (separated from business logic)
│   ├── shared/             # Shared API utils
│   └── v1/                 # API versioning
│       └── accounts/
│           ├── serializers/    # Separate serializers
│           ├── viewsets/       # Separate viewsets
│           └── urls.py
├── config/                  # Project settings
└── docs/                    # Documentation
```

**Kenapa ini BAGUS:**
- ✅ Separation of concerns (apps vs api)
- ✅ API versioning (v1, v2, etc)
- ✅ Modular structure
- ✅ Easy to scale
- ✅ Easy to test

---

## 📐 Design Patterns yang Wajib Dipakai

### 1. Fat Models, Thin Views, Skinny Serializers

#### ❌ WRONG (Logic di View):
```python
class EmployeeViewSet(viewsets.ModelViewSet):
    def create(self, request):
        # DON'T: Business logic di view
        employee = Employee.objects.create(**request.data)
        employee.code = f"EMP{employee.id:05d}"
        employee.save()
        
        # Send email
        send_mail(...)
        
        # Log activity
        Log.objects.create(...)
        
        return Response(...)
```

#### ✅ CORRECT (Logic di Model/Manager):
```python
# models/employee.py
class EmployeeManager(models.Manager):
    def create_employee(self, **kwargs):
        """Business logic here"""
        employee = self.create(**kwargs)
        employee.generate_code()
        employee.send_welcome_email()
        employee.log_creation()
        return employee

class Employee(models.Model):
    objects = EmployeeManager()
    
    def generate_code(self):
        """Single responsibility"""
        if not self.code:
            self.code = f"EMP{self.id:05d}"
            self.save(update_fields=['code'])
    
    def send_welcome_email(self):
        """Another responsibility"""
        send_mail(
            subject='Welcome',
            message=f'Welcome {self.name}',
            recipient_list=[self.email]
        )
    
    def log_creation(self):
        """Yet another responsibility"""
        Log.objects.create(
            action='employee_created',
            employee=self
        )

# viewsets/employee.py
class EmployeeViewSet(viewsets.ModelViewSet):
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Simple, clean view
        employee = Employee.objects.create_employee(
            **serializer.validated_data
        )
        
        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_201_CREATED
        )
```

### 2. Use Custom Managers & QuerySets

```python
# models/employee.py
class EmployeeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status='active')
    
    def by_division(self, division):
        return self.filter(division=division)
    
    def with_full_details(self):
        """Optimize queries"""
        return self.select_related(
            'division',
            'position',
            'user'
        ).prefetch_related(
            'skills',
            'projects'
        )

class EmployeeManager(models.Manager.from_queryset(EmployeeQuerySet)):
    pass

class Employee(models.Model):
    objects = EmployeeManager()
    
    # Now you can chain:
    # Employee.objects.active().by_division(div).with_full_details()
```

### 3. Use Services Layer untuk Complex Logic

```python
# apps/accounts/services/user_service.py
class UserService:
    @staticmethod
    def register_user(email, password, **extra_fields):
        """Complex registration logic"""
        # Validate email domain
        if not UserService._is_valid_email_domain(email):
            raise ValidationError("Invalid email domain")
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        
        # Create profile
        Profile.objects.create(user=user)
        
        # Send verification email
        UserService._send_verification_email(user)
        
        # Log registration
        UserService._log_registration(user)
        
        return user
    
    @staticmethod
    def _is_valid_email_domain(email):
        domain = email.split('@')[1]
        return domain in settings.ALLOWED_EMAIL_DOMAINS
    
    @staticmethod
    def _send_verification_email(user):
        # Email logic
        pass
    
    @staticmethod
    def _log_registration(user):
        # Logging logic
        pass

# In view:
from apps.accounts.services.user_service import UserService

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = UserService.register_user(**serializer.validated_data)
        
        return Response(UserSerializer(user).data)
```

---

## 🚀 Performance Best Practices

### 1. Query Optimization

#### Always Use select_related & prefetch_related

```python
# ❌ BAD: N+1 queries problem
employees = Employee.objects.all()
for emp in employees:
    print(emp.division.name)  # Query on each iteration
    print(emp.position.title)  # Another query!

# ✅ GOOD: 1 query with JOIN
employees = Employee.objects.select_related(
    'division',
    'position'
).all()
for emp in employees:
    print(emp.division.name)  # No additional query
    print(emp.position.title)  # No additional query

# ✅ GOOD: For Many-to-Many
employees = Employee.objects.prefetch_related(
    'skills',
    'projects'
).all()
```

#### Use only() & defer() untuk Reduce Data

```python
# ❌ BAD: Fetch all columns
employees = Employee.objects.all()

# ✅ GOOD: Only needed columns
employees = Employee.objects.only('id', 'name', 'email')

# ✅ GOOD: Exclude heavy columns
employees = Employee.objects.defer('photo', 'resume')
```

### 2. Database Indexing

```python
class Employee(models.Model):
    email = models.EmailField(unique=True, db_index=True)  # ✅
    code = models.CharField(max_length=20, db_index=True)  # ✅
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        db_index=True  # ✅ Often filtered
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['division', 'status']),  # Composite index
            models.Index(fields=['created_at']),
            models.Index(fields=['-updated_at']),  # Descending
        ]
```

### 3. Caching Strategy

```python
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# Cache view for 5 minutes
@method_decorator(cache_page(60 * 5), name='dispatch')
class EmployeeListView(APIView):
    pass

# Cache queryset
def get_divisions():
    cache_key = 'divisions_all'
    divisions = cache.get(cache_key)
    
    if divisions is None:
        divisions = list(Division.objects.all().values('id', 'name'))
        cache.set(cache_key, divisions, 60 * 60)  # 1 hour
    
    return divisions

# Cache expensive computation
from django.core.cache import cache

class Employee(models.Model):
    def get_total_projects(self):
        cache_key = f'employee_{self.id}_total_projects'
        total = cache.get(cache_key)
        
        if total is None:
            total = self.projects.count()
            cache.set(cache_key, total, 60 * 15)  # 15 minutes
        
        return total
```

---

## 🔒 Security Best Practices

### 1. Always Validate Input

```python
# serializers/employee.py
from rest_framework import serializers
from apps.core.validators import validate_phone_number

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Employee.objects.all())]
    )
    phone = serializers.CharField(validators=[validate_phone_number])
    
    class Meta:
        model = Employee
        fields = '__all__'
    
    def validate_email(self, value):
        """Custom email validation"""
        if not value.endswith('@company.com'):
            raise serializers.ValidationError(
                "Only company emails are allowed"
            )
        return value.lower()
    
    def validate(self, attrs):
        """Cross-field validation"""
        if attrs.get('start_date') > attrs.get('end_date'):
            raise serializers.ValidationError(
                "Start date must be before end date"
            )
        return attrs
```

### 2. Use Permissions Properly

```python
# api/v1/accounts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission: Owner can edit, others can only read"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsManagerOrReadOnly(permissions.BasePermission):
    """Only managers can edit"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_manager

# In viewset
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
```

### 3. Rate Limiting

```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='100/h'), name='dispatch')
class LoginView(APIView):
    pass
```

---

## 📊 Monitoring & Logging

### 1. Structured Logging

```python
# config/settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

```python
# In your code
import logging

logger = logging.getLogger(__name__)

class EmployeeViewSet(viewsets.ModelViewSet):
    def create(self, request):
        logger.info(f"Creating employee: {request.data.get('email')}")
        try:
            # ... code ...
            logger.info(f"Employee created successfully: {employee.id}")
        except Exception as e:
            logger.error(f"Error creating employee: {str(e)}", exc_info=True)
            raise
```

### 2. Audit Trail

```python
# apps/core/models/audit.py
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    object_id = models.IntegerField()
    changes = models.JSONField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['model', 'object_id']),
            models.Index(fields=['-timestamp']),
        ]

# apps/core/mixins.py
class AuditMixin:
    def perform_create(self, serializer):
        instance = serializer.save()
        AuditLog.objects.create(
            user=self.request.user,
            action='CREATE',
            model=instance.__class__.__name__,
            object_id=instance.id,
            changes=serializer.validated_data,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        return instance
    
    def perform_update(self, serializer):
        old_data = model_to_dict(serializer.instance)
        instance = serializer.save()
        new_data = model_to_dict(instance)
        
        changes = {
            k: {'old': old_data[k], 'new': new_data[k]}
            for k in old_data
            if old_data[k] != new_data[k]
        }
        
        AuditLog.objects.create(
            user=self.request.user,
            action='UPDATE',
            model=instance.__class__.__name__,
            object_id=instance.id,
            changes=changes,
            ip_address=self.request.META.get('REMOTE_ADDR')
        )
        return instance
```

---

## 🧪 Testing Strategy

### 1. Test Structure

```python
# tests/api/v1/test_employee.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_user(db):
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    return user

@pytest.fixture
def authenticated_client(api_client, authenticated_user):
    api_client.force_authenticate(user=authenticated_user)
    return api_client

@pytest.mark.django_db
class TestEmployeeAPI:
    def test_create_employee_success(self, authenticated_client):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
        }
        response = authenticated_client.post('/api/v1/employees/', data)
        
        assert response.status_code == 201
        assert response.data['name'] == 'John Doe'
    
    def test_create_employee_unauthorized(self, api_client):
        response = api_client.post('/api/v1/employees/', {})
        assert response.status_code == 401
```

---

## 📦 Dependency Management

### 1. requirements.txt Structure (Yang Anda Sudah Punya - BAGUS!)

```
requirements/
├── base.txt          # Production dependencies
├── development.txt   # Dev dependencies
└── testing.txt       # Test dependencies
```

### 2. Use Docker untuk Consistency

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: employee_management
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_ENGINE=postgresql
      - DB_NAME=employee_management
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_HOST=db

volumes:
  postgres_data:
```

---

## 🎯 Summary: Must-Have Features

### ✅ Yang Sudah Anda Punya (BAGUS!):
1. ✅ API Versioning (v1/)
2. ✅ Separated API layer
3. ✅ JWT Authentication
4. ✅ drf-spectacular for docs
5. ✅ Django Filter
6. ✅ Custom User model
7. ✅ Modular structure

### 📝 Yang Perlu Ditambahkan:
1. ⏳ Caching (Redis)
2. ⏳ Celery for async tasks
3. ⏳ Rate limiting
4. ⏳ Audit logging
5. ⏳ Comprehensive tests
6. ⏳ Docker setup
7. ⏳ CI/CD pipeline

### 🚀 Production Checklist:
1. Use PostgreSQL (not SQLite)
2. Setup Redis for caching
3. Use Celery for background tasks
4. Setup monitoring (Sentry)
5. Use environment variables
6. Setup CI/CD
7. Use Docker
8. Setup logging
9. Add rate limiting
10. Security headers (django-cors-headers, django-csp)

---

## 📚 Recommended Packages

### Must Have (Production):
```
Django==5.0.0                      # ✅ You have this
djangorestframework==3.14.0        # ✅ You have this
drf-spectacular==0.27.1            # ✅ You have this
djangorestframework-simplejwt==5.3.1  # ✅ You have this
django-filter==23.5                # ✅ You have this
django-cors-headers==4.3.1         # ✅ You have this
psycopg[binary]==3.1.19           # ✅ You have this

# Add these:
celery==5.3.4                      # Async tasks
redis==5.0.1                       # Caching
django-redis==5.4.0                # Redis cache backend
gunicorn==21.2.0                   # Production server
whitenoise==6.6.0                  # Static files
sentry-sdk==1.38.0                 # Error tracking
django-health-check==3.17.0        # Health checks
```

### Development:
```
django-debug-toolbar==4.2.0        # Debugging
django-extensions==3.2.3           # ✅ You have this
ipython==8.18.1                    # Better shell
```

### Testing:
```
pytest==7.4.3                      # ✅ You have this
pytest-django==4.7.0               # ✅ You have this
pytest-cov==4.1.0                  # Coverage
factory-boy==3.3.0                 # Test fixtures
faker==20.1.0                      # Fake data
```

---

**Kesimpulan:** Struktur project Anda sudah SANGAT BAGUS untuk scalable application. Yang perlu dilakukan tinggal implement best practices di setiap layer dan tambahkan monitoring/caching untuk production readiness.
