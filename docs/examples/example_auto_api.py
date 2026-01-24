# CONTOH: API Tanpa Decorator - Tetap Muncul di Swagger!
# ========================================================

from rest_framework import viewsets, serializers
from apps.accounts.models import User

# 1. Buat Serializer biasa
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

# 2. Buat ViewSet biasa (TANPA DECORATOR!)
class UserViewSet(viewsets.ModelViewSet):
    """
    API untuk manage users.
    
    Ini cuma docstring biasa, tapi drf-spectacular baca ini!
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    # OTOMATIS muncul di Swagger:
    # - GET /api/v1/users/          (list)
    # - POST /api/v1/users/         (create)
    # - GET /api/v1/users/{id}/     (retrieve)
    # - PUT /api/v1/users/{id}/     (update)
    # - PATCH /api/v1/users/{id}/   (partial_update)
    # - DELETE /api/v1/users/{id}/  (destroy)

# 3. Tambahkan ke urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls

# ✅ SELESAI! Swagger otomatis show 6 endpoints!
# ✅ Request/Response format otomatis dari UserListSerializer!
# ✅ Authentication otomatis dari REST_FRAMEWORK settings!
