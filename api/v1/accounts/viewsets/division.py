"""
Division ViewSet - OTOMATIS muncul di Swagger!

Cukup buat ViewSet biasa, drf-spectacular auto-detect semuanya:
- URL patterns
- HTTP methods
- Request/Response format dari serializer
- Authentication requirements
- Filters & search
"""
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.accounts.models import Division
from api.v1.accounts.serializers.division import (
    DivisionSerializer,
    DivisionWriteSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary='List all divisions',
        description='Get paginated list of all divisions with employee count',
        tags=['Divisions'],
    ),
    retrieve=extend_schema(
        summary='Get division detail',
        description='Get detailed information of a specific division',
        tags=['Divisions'],
    ),
    create=extend_schema(
        summary='Create new division',
        description='Create a new division with code, name, and description',
        tags=['Divisions'],
    ),
    update=extend_schema(
        summary='Update division',
        description='Update all fields of a division',
        tags=['Divisions'],
    ),
    partial_update=extend_schema(
        summary='Partially update division',
        description='Update specific fields of a division',
        tags=['Divisions'],
    ),
    destroy=extend_schema(
        summary='Delete division',
        description='Delete a division (soft delete if has employees)',
        tags=['Divisions'],
    ),
)
class DivisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk manage divisions.
    
    **Otomatis generate 6 endpoints:**
    - GET /api/v1/divisions/ - List divisions
    - POST /api/v1/divisions/ - Create division
    - GET /api/v1/divisions/{id}/ - Detail division
    - PUT /api/v1/divisions/{id}/ - Update division
    - PATCH /api/v1/divisions/{id}/ - Partial update
    - DELETE /api/v1/divisions/{id}/ - Delete division
    
    **Features:**
    - Pagination (20 items per page)
    - Search (by name, code)
    - Filter (by name)
    - Ordering (by name, created_at, etc)
    """
    
    queryset = Division.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    
    # Filter & search - otomatis muncul di Swagger!
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    
    def get_serializer_class(self):
        """
        2 Serializers approach - SIMPLE & RECOMMENDED!
        
        Read operations (GET) → DivisionSerializer
        Write operations (POST/PUT/PATCH) → DivisionWriteSerializer
        """
        # Write operations
        if self.action in ['create', 'update', 'partial_update']:
            return DivisionWriteSerializer
        
        # Read operations (list & retrieve)
        return DivisionSerializer
    
    def perform_create(self, serializer):
        """Auto set created_by ke current user"""
        serializer.save(created_by=self.request.user)
    
    def perform_destroy(self, instance):
        """
        Soft delete jika ada employees.
        Hard delete jika kosong.
        """
        if instance.user_set.exists():
            instance.is_active = False
            instance.save()
        else:
            instance.delete()
    
    # ============================================
    # Custom Actions - Juga OTOMATIS muncul!
    # ============================================
    
    @extend_schema(
        summary='Get division statistics',
        description='Get statistical data for a specific division',
        responses={200: {
            'type': 'object',
            'properties': {
                'employee_count': {'type': 'integer'},
                'active_employees': {'type': 'integer'},
                'inactive_employees': {'type': 'integer'},
            }
        }},
        tags=['Divisions'],
    )
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """
        Custom action: GET /api/v1/divisions/{id}/statistics/
        
        Return: {
            "employee_count": 10,
            "active_employees": 8,
            "inactive_employees": 2
        }
        """
        division = self.get_object()
        employees = division.user_set.all()
        
        return Response({
            'employee_count': employees.count(),
            'active_employees': employees.filter(is_active=True).count(),
            'inactive_employees': employees.filter(is_active=False).count(),
        })
    
    @extend_schema(
        summary='Get employees in division',
        description='Get list of all employees in this division',
        tags=['Divisions'],
    )
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """
        Custom action: GET /api/v1/divisions/{id}/employees/
        
        Return list of employees in this division
        """
        division = self.get_object()
        employees = division.user_set.all()
        
        # Import UserSerializer untuk serialize employees
        from api.v1.accounts.serializers.user import UserSerializer
        serializer = UserSerializer(employees, many=True)
        
        return Response(serializer.data)

