# Django Architecture Guide: Where to Put Your Logic 🏗️

## Table of Contents
- [Overview](#overview)
- [The Four Layers](#the-four-layers)
- [Decision Framework](#decision-framework)
- [Real-World Examples](#real-world-examples)
- [Common Mistakes](#common-mistakes)
- [Best Practices](#best-practices)

---

## Overview

Django architecture follows **Separation of Concerns** principle. Each layer has specific responsibilities:

| Layer | Responsibility | When to Use |
|-------|---------------|-------------|
| **Model** | Data structure + Business rules | Single model logic, calculations, validations |
| **Serializer** | Data transformation | API input/output, field formatting, nested data |
| **ViewSet/View** | HTTP handling | Permissions, authentication, response formatting |
| **Service** | Complex workflows | Multi-model operations, external APIs, transactions |

---

## The Four Layers

### 1. MODEL Layer 📦

**Purpose:** Define what data **IS** and what it **CAN DO**

**Responsibilities:**
- Database schema definition
- Business rules and domain logic
- Data validation
- Calculated properties
- State transitions

#### ✅ What Belongs in Model

| Type | Example | Code |
|------|---------|------|
| **Properties** | Role checks, status checks | `@property def is_hr_admin` |
| **Calculations** | Salary, totals, aggregations | `def calculate_monthly_salary()` |
| **State Transitions** | Approve, reject, activate | `def approve(approver)` |
| **Validations** | Business rule checks | `def clean()` |
| **Queries** | Domain-specific queries | `@classmethod get_active_employees()` |

#### Example: Employee Model

```python
class Employee(models.Model):
    name = models.CharField(max_length=100)
    gaji_pokok = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateField()
    
    # ✅ Property: Describe state
    @property
    def is_eligible_for_leave(self):
        """Business rule: 3 months employment required"""
        if not self.hire_date:
            return False
        months = (now().date() - self.hire_date).days / 30
        return months >= 3
    
    # ✅ Calculation: Business logic
    def calculate_monthly_salary(self, month, year):
        """Calculate total salary with bonus, overtime, deductions"""
        bonus = self.bonuses.filter(
            date__month=month, date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        overtime = self._calculate_overtime(month, year)
        deductions = self._calculate_deductions(month, year)
        
        return {
            'gaji_pokok': float(self.gaji_pokok),
            'bonus': float(bonus),
            'overtime': float(overtime),
            'deductions': float(deductions),
            'total': float(self.gaji_pokok + bonus + overtime - deductions)
        }
    
    # ✅ State transition
    def promote_to_manager(self):
        """Promote employee to manager role"""
        if self.status != 'active':
            raise ValidationError("Only active employees can be promoted")
        
        manager_group = Group.objects.get(name='Manager')
        self.groups.add(manager_group)
        self.save()
```

#### Example: Leave Model

```python
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')
    
    # ✅ Business rule: Who can approve?
    def can_be_approved_by(self, user):
        """Check if user can approve this leave"""
        if self.status != 'pending':
            return False
        if user.is_hr_admin:
            return True
        if user.is_manager and self.employee.division == user.division:
            return True
        return False
    
    # ✅ State transition: Approve
    def approve(self, approver):
        """Approve leave request"""
        if self.status != 'pending':
            raise ValidationError("Only pending leaves can be approved")
        
        self.status = 'approved'
        self.approved_by = approver
        self.approved_at = now()
        self.save(update_fields=['status', 'approved_by', 'approved_at'])
        
        # Business side effect
        self._send_approval_notification()
    
    # ✅ Property: Calculated field
    @property
    def duration_days(self):
        """Calculate leave duration in days"""
        return (self.end_date - self.start_date).days + 1
```

---

### 2. SERIALIZER Layer 🔄

**Purpose:** Transform data between Python objects and API format (JSON)

**Responsibilities:**
- Field selection (what to expose in API)
- Data formatting (dates, numbers, nested objects)
- Input validation (API-level)
- Nested serialization

#### ✅ What Belongs in Serializer

| Type | Example | Code |
|------|---------|------|
| **Field Selection** | Choose fields to expose | `fields = ['id', 'name', 'email']` |
| **Formatting** | Date format, nested data | `hire_date = DateField(format='%Y-%m-%d')` |
| **API Validation** | Input checks before model | `def validate(data)` |
| **Computed Fields** | Delegate to model | `def get_salary(obj): return obj.calculate_salary()` |

#### Example: Employee Serializer

```python
class EmployeeSerializer(serializers.ModelSerializer):
    # ✅ Format: Present data nicely
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    division_name = serializers.CharField(source='division.name', read_only=True)
    
    # ✅ Computed field: Delegate to model
    monthly_salary = serializers.SerializerMethodField()
    is_eligible_for_leave = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name', 'email',
            'division_name', 'hire_date', 'monthly_salary',
            'is_eligible_for_leave'
        ]
    
    def get_monthly_salary(self, obj):
        """Get salary from model calculation"""
        return obj.calculate_monthly_salary()  # Delegate to model!
```

#### Example: Leave Serializer with Validation

```python
class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'leave_type', 'reason']
    
    # ✅ API-level validation
    def validate(self, data):
        """Validate input before hitting model"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Check dates
        if end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        
        # Check business rule via model
        employee = self.context['request'].user
        if not employee.is_eligible_for_leave:
            raise serializers.ValidationError(
                'You are not eligible for leave yet (3 months required)'
            )
        
        # Check quota
        duration = (end_date - start_date).days + 1
        if duration > employee.remaining_leave_days:
            raise serializers.ValidationError(
                f'Insufficient leave days. You have {employee.remaining_leave_days} days left.'
            )
        
        return data
```

---

### 3. VIEWSET/VIEW Layer 🚪

**Purpose:** Handle HTTP requests and enforce access control

**Responsibilities:**
- Authentication & authorization
- Permission checks
- Query optimization (select_related, prefetch_related)
- HTTP-specific logic (file uploads, CSV exports)
- Response formatting

#### ✅ What Belongs in ViewSet

| Type | Example | Code |
|------|---------|------|
| **Permissions** | Who can access? | `permission_classes = [IsHRAdmin]` |
| **Filtering** | Role-based data access | `if user.is_hr_admin: return all_data` |
| **HTTP Handling** | File upload, CSV export | `def export_csv(request)` |
| **Query Optimization** | Reduce queries | `select_related('division')` |

#### Example: Leave ViewSet

```python
class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]
    
    # ✅ Filter data based on role
    def get_queryset(self):
        """Role-based data filtering"""
        user = self.request.user
        
        if user.is_hr_admin:
            return Leave.objects.all()
        elif user.is_manager:
            return Leave.objects.filter(
                employee__division=user.division
            )
        else:
            return Leave.objects.filter(employee=user)
    
    # ✅ Custom action: Approve leave
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        POST /api/v1/leaves/{id}/approve/
        Permission: Can approve leaves
        """
        leave = self.get_object()
        
        # ✅ Permission check (API layer)
        if not leave.can_be_approved_by(request.user):
            return APIResponse.forbidden(
                message="You don't have permission to approve this leave"
            )
        
        try:
            # ✅ Delegate business logic to model
            leave.approve(approver=request.user)
            
            # ✅ HTTP response
            return APIResponse.success(
                data=LeaveSerializer(leave).data,
                message="Leave approved successfully"
            )
        except ValidationError as e:
            return APIResponse.error(message=str(e), status_code=400)
    
    # ✅ Custom action: Reject leave
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        POST /api/v1/leaves/{id}/reject/
        Body: { "reason": "Not enough staff coverage" }
        """
        leave = self.get_object()
        
        # ✅ API-level validation
        reason = request.data.get('reason')
        if not reason:
            return APIResponse.error(
                message="Rejection reason is required",
                errors={'reason': 'This field is required'}
            )
        
        # ✅ Permission check
        if not leave.can_be_approved_by(request.user):
            return APIResponse.forbidden(
                message="You don't have permission to reject this leave"
            )
        
        try:
            # ✅ Delegate to model
            leave.reject(rejector=request.user, reason=reason)
            return APIResponse.success(message="Leave rejected")
        except ValidationError as e:
            return APIResponse.error(message=str(e))
```

#### Example: HTTP-Specific Actions

```python
class EmployeeViewSet(viewsets.ModelViewSet):
    # ✅ CSV Export (HTTP-specific)
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """Export employees to CSV file"""
        if not request.user.has_perm('core.export_employee_data'):
            return APIResponse.forbidden()
        
        employees = self.get_queryset()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Email', 'Division'])
        
        for emp in employees:
            writer.writerow([
                emp.employee_id,
                emp.get_full_name(),
                emp.email,
                emp.division.name if emp.division else ''
            ])
        
        return response
    
    # ✅ File Upload (HTTP-specific)
    @action(detail=True, methods=['post'])
    def upload_face_photos(self, request, pk=None):
        """Upload face recognition photos"""
        employee = self.get_object()
        
        # Permission check
        if employee != request.user and not request.user.is_hr_admin:
            return APIResponse.forbidden()
        
        # Validate files
        front = request.FILES.get('front')
        left = request.FILES.get('left')
        right = request.FILES.get('right')
        
        if not all([front, left, right]):
            return APIResponse.error(
                message="All 3 photos are required"
            )
        
        # Save photos
        employee.face_photo_front = front
        employee.face_photo_left = left
        employee.face_photo_right = right
        employee.save()
        
        return APIResponse.success(
            message="Photos uploaded successfully"
        )
```

---

### 4. SERVICE Layer 🎭

**Purpose:** Coordinate complex workflows involving multiple models

**Responsibilities:**
- Multi-model transactions
- Complex business workflows
- External service integration
- Bulk operations
- Async task coordination

#### ✅ When to Use Service

| Scenario | Why Service? | Example |
|----------|-------------|---------|
| **3+ Models** | Coordinate multiple models | Payroll generation |
| **Transactions** | Atomic operations | Leave approval + quota update |
| **External APIs** | Integration logic | Face recognition, email |
| **Bulk Operations** | Process many records | Import 1000 employees |
| **Complex Workflow** | Multi-step process | Check-in with face + location |

#### Example: Payroll Service

```python
# apps/payroll/services.py
from django.db import transaction
from django.core.exceptions import ValidationError


class PayrollService:
    """
    Complex payroll operations
    Coordinates: Employee, Attendance, Bonus, Payroll, Notification
    """
    
    @staticmethod
    @transaction.atomic
    def generate_monthly_payroll(month, year, generated_by):
        """
        Generate payroll for all employees.
        
        Steps:
        1. Validate month/year
        2. Get active employees
        3. Calculate each salary (delegate to model)
        4. Create payroll records
        5. Create payroll items (breakdown)
        6. Send notifications
        7. Log activity
        
        Returns:
            dict: {
                'count': int,
                'total_amount': Decimal,
                'payrolls': list[Payroll]
            }
        """
        # 1. Validation
        if month < 1 or month > 12:
            raise ValidationError("Invalid month")
        
        if Payroll.objects.filter(month=month, year=year).exists():
            raise ValidationError(
                f"Payroll for {month}/{year} already generated"
            )
        
        # 2. Get employees with optimized query
        employees = Employee.objects.filter(
            is_active=True,
            status__in=['active', 'on_leave']
        ).prefetch_related(
            'bonuses', 'attendance_set', 'violations'
        )
        
        payrolls = []
        total_amount = 0
        
        # 3. Process each employee
        for employee in employees:
            # Delegate calculation to model
            salary_data = employee.calculate_monthly_salary(month, year)
            
            # Create payroll record
            payroll = Payroll.objects.create(
                employee=employee,
                month=month,
                year=year,
                gross_salary=salary_data['total'],
                net_salary=salary_data['total'] - salary_data['deductions'],
                generated_by=generated_by
            )
            
            # Create breakdown items
            PayrollService._create_payroll_items(payroll, salary_data)
            
            # Send notification (async)
            PayrollService._notify_employee(payroll)
            
            payrolls.append(payroll)
            total_amount += payroll.net_salary
        
        # 7. Log activity
        ActivityLog.objects.create(
            user=generated_by,
            action='generate_payroll',
            details=f'{len(payrolls)} payrolls for {month}/{year}'
        )
        
        return {
            'count': len(payrolls),
            'total_amount': total_amount,
            'payrolls': payrolls
        }
    
    @staticmethod
    def _create_payroll_items(payroll, salary_data):
        """Helper: Create payroll item breakdown"""
        items = [
            {'type': 'basic_salary', 'amount': salary_data['gaji_pokok']},
            {'type': 'bonus', 'amount': salary_data['bonus']},
            {'type': 'overtime', 'amount': salary_data['overtime']},
            {'type': 'deduction', 'amount': -salary_data['deductions']},
        ]
        
        for item in items:
            if item['amount'] != 0:
                PayrollItem.objects.create(
                    payroll=payroll,
                    item_type=item['type'],
                    amount=item['amount']
                )
    
    @staticmethod
    def _notify_employee(payroll):
        """Helper: Send payslip notification"""
        from apps.notifications.tasks import send_payslip_email
        
        # Async email
        send_payslip_email.delay(payroll.id)
        
        # In-app notification
        Notification.objects.create(
            user=payroll.employee,
            type='payroll_generated',
            message=f'Your payslip for {payroll.month}/{payroll.year} is ready'
        )
```

#### Example: Attendance Check-In Service

```python
# apps/attendance/services.py
class AttendanceService:
    """
    Complex check-in workflow
    Coordinates: Face API, Location API, Attendance, Notification
    """
    
    @staticmethod
    @transaction.atomic
    def process_check_in(employee, check_in_time, location, photo):
        """
        Multi-step check-in process:
        1. Verify face (external API)
        2. Validate location (external API)
        3. Create attendance record
        4. Check if late (business rule)
        5. Send notifications
        
        Raises:
            ValidationError: If verification fails
        """
        # 1. Face recognition (external service)
        from apps.core.services import FaceRecognitionService
        
        if not FaceRecognitionService.verify(employee, photo):
            raise ValidationError("Face verification failed")
        
        # 2. Location validation (external service)
        from apps.core.services import LocationService
        
        if not LocationService.is_in_office(location):
            raise ValidationError("You are not in office area")
        
        # 3. Create attendance
        attendance = Attendance.objects.create(
            employee=employee,
            date=check_in_time.date(),
            check_in=check_in_time.time(),
            location=location
        )
        
        # 4. Check if late (delegate to model)
        if attendance.is_late:
            # Notify employee
            Notification.objects.create(
                user=employee,
                type='late_arrival',
                message=f'You checked in late at {check_in_time.time()}'
            )
            
            # Notify manager
            if employee.division and employee.division.manager:
                Notification.objects.create(
                    user=employee.division.manager,
                    type='employee_late',
                    message=f'{employee.get_full_name()} checked in late'
                )
        
        return attendance
```

#### Using Service in ViewSet

```python
# apps/payroll/views.py
class PayrollViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsHRAdmin]
    
    @action(detail=False, methods=['post'])
    def generate_monthly(self, request):
        """
        POST /api/v1/payrolls/generate_monthly/
        Body: { "month": 1, "year": 2024 }
        
        ✅ ViewSet: Simple HTTP handling
        ✅ Service: Complex logic
        """
        # API validation
        month = request.data.get('month')
        year = request.data.get('year')
        
        if not month or not year:
            return APIResponse.error(
                message="Month and year required"
            )
        
        # Permission check
        if not request.user.has_perm('payroll.generate_payroll'):
            return APIResponse.forbidden()
        
        try:
            # Delegate to service
            result = PayrollService.generate_monthly_payroll(
                month=month,
                year=year,
                generated_by=request.user
            )
            
            return APIResponse.success(
                data={
                    'count': result['count'],
                    'total_amount': str(result['total_amount'])
                },
                message=f"Generated {result['count']} payrolls"
            )
        except ValidationError as e:
            return APIResponse.error(message=str(e))


# apps/attendance/views.py
class AttendanceViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def check_in(self, request):
        """
        POST /api/v1/attendance/check_in/
        Body: { "location": {...}, "photo": "base64..." }
        """
        try:
            # Delegate to service
            attendance = AttendanceService.process_check_in(
                employee=request.user,
                check_in_time=now(),
                location=request.data.get('location'),
                photo=request.data.get('photo')
            )
            
            return APIResponse.success(
                data=AttendanceSerializer(attendance).data,
                message="Check-in successful"
            )
        except ValidationError as e:
            return APIResponse.error(message=str(e))
```

---

## Decision Framework

### Quick Decision Tree

```
Logic X needs to be implemented:
│
├─ Does it involve HTTP/API-specific? (file upload, CSV, auth)
│  └─ YES → VIEWSET ✅
│
├─ Does it transform data for API? (JSON ↔ Model)
│  └─ YES → SERIALIZER ✅
│
├─ Does it coordinate 3+ models with transactions?
│  └─ YES → SERVICE ✅
│
├─ Is it a business rule about THIS model?
│  └─ YES → MODEL ✅
│
└─ Still confused?
   └─ Ask: "Can I do this in Django shell without HTTP?"
      ├─ YES → MODEL or SERVICE
      └─ NO → VIEWSET or SERIALIZER
```

### Comparison Table

| Feature | Model | Serializer | ViewSet | Service |
|---------|-------|------------|---------|---------|
| **Single model logic** | ✅ | ❌ | ❌ | ❌ |
| **Multi-model logic** | ❌ | ❌ | ❌ | ✅ |
| **API formatting** | ❌ | ✅ | ❌ | ❌ |
| **HTTP handling** | ❌ | ❌ | ✅ | ❌ |
| **Permissions** | ❌ | ❌ | ✅ | ❌ |
| **Transactions** | ⚠️ Simple | ❌ | ❌ | ✅ Complex |
| **External APIs** | ❌ | ❌ | ❌ | ✅ |
| **Reusable** | ✅ | ⚠️ | ❌ | ✅ |
| **Testable (no HTTP)** | ✅ | ⚠️ | ❌ | ✅ |

---

## Real-World Examples

### Example 1: Calculate Salary

| Layer | Responsibility | Code Location |
|-------|---------------|---------------|
| **Model** | How to calculate | `employee.calculate_monthly_salary()` |
| **Serializer** | How to show in API | `get_monthly_salary(obj)` delegates to model |
| **ViewSet** | Who can see, when | Permission check, HTTP endpoint |

```python
# Model: Business logic
class Employee(models.Model):
    def calculate_monthly_salary(self, month, year):
        # Complex calculation here
        return {'total': 5000000, 'bonus': 1000000}

# Serializer: Presentation
class EmployeeSerializer(serializers.ModelSerializer):
    monthly_salary = serializers.SerializerMethodField()
    
    def get_monthly_salary(self, obj):
        return obj.calculate_monthly_salary()  # Delegate!

# ViewSet: Access control
class EmployeeViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def salary(self, request, pk=None):
        employee = self.get_object()
        
        # Permission: Only self or HR Admin
        if not (request.user == employee or request.user.is_hr_admin):
            return APIResponse.forbidden()
        
        data = EmployeeSerializer(employee).data
        return APIResponse.success(data=data)
```

### Example 2: Approve Leave

| Layer | Responsibility | Code Location |
|-------|---------------|---------------|
| **Model** | How to approve (business rule) | `leave.approve(approver)` |
| **ViewSet** | Who can approve (permission) | Permission check in endpoint |
| **Service** | Complex approval workflow | Multi-step process with notifications |

```python
# Model: Business logic
class Leave(models.Model):
    def approve(self, approver):
        if self.status != 'pending':
            raise ValidationError("Only pending can be approved")
        self.status = 'approved'
        self.approved_by = approver
        self.save()

# ViewSet: Permission + HTTP
class LeaveViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        
        # Permission check
        if not leave.can_be_approved_by(request.user):
            return APIResponse.forbidden()
        
        # Delegate to model
        leave.approve(request.user)
        return APIResponse.success(message="Approved")

# Service: If workflow is complex
class LeaveService:
    @staticmethod
    @transaction.atomic
    def approve_leave(leave, approver):
        # Complex workflow:
        # 1. Approve leave (delegate to model)
        leave.approve(approver)
        
        # 2. Update quota
        leave.employee.leave_quota.deduct(leave.duration)
        
        # 3. Create approval record
        LeaveApproval.objects.create(leave=leave, approver=approver)
        
        # 4. Send notifications
        NotificationService.send_approval_notification(leave)
        
        # 5. Log activity
        ActivityLog.objects.create(...)
```

### Example 3: Bulk Import Employees

| Layer | Responsibility | Code Location |
|-------|---------------|---------------|
| **Model** | Single employee validation | `User.clean()` |
| **Serializer** | Validate CSV row data | `EmployeeImportSerializer` |
| **Service** | Bulk processing + transaction | `EmployeeService.bulk_import()` |
| **ViewSet** | File upload + permission | HTTP endpoint |

```python
# Service: Bulk operation
class EmployeeService:
    @staticmethod
    def bulk_import_from_csv(csv_file, imported_by):
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                with transaction.atomic():
                    # Validate via serializer
                    serializer = EmployeeImportSerializer(data=row)
                    serializer.is_valid(raise_exception=True)
                    
                    # Create user (model handles business rules)
                    user = User.objects.create_user(...)
                    
                    results['success'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({'row': row, 'error': str(e)})
        
        return results

# ViewSet: HTTP handling
class EmployeeViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        # Permission check
        if not request.user.has_perm('employee.bulk_import'):
            return APIResponse.forbidden()
        
        csv_file = request.FILES.get('file')
        if not csv_file:
            return APIResponse.error("CSV file required")
        
        # Delegate to service
        results = EmployeeService.bulk_import_from_csv(
            csv_file, request.user
        )
        
        return APIResponse.success(data=results)
```

---

## Common Mistakes

### ❌ Mistake 3: Permission Enforcement in Model

```python
# BAD: Permission check in business logic
class Leave(models.Model):
    def approve(self, approver):
        # Permission enforcement in model! ❌
        if not approver.is_hr_admin and not approver.is_manager:
            raise PermissionDenied("You cannot approve")
        
        self.status = 'approved'
        self.save()
```

```python
# GOOD: Permission in view, business rule in model
class Leave(models.Model):
    def can_be_approved_by(self, user):
        """Business rule: who CAN approve (not enforcing)"""
        if self.status != 'pending':
            return False
        return user.is_hr_admin or user.is_manager
    
    def approve(self, approver):
        """Pure business logic"""
        if self.status != 'pending':
            raise ValidationError("Only pending can be approved")
        self.status = 'approved'
        self.save()

class LeaveViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        
        # Permission enforcement at API layer ✅
        if not leave.can_be_approved_by(request.user):
            return APIResponse.forbidden()
        
        leave.approve(request.user)
        return APIResponse.success(...)
```

### ❌ Mistake 4: Not Using Service for Complex Operations

```python
# BAD: Complex multi-model logic in viewset
class PayrollViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def generate_monthly(self, request):
        # Too much happening here! ❌
        employees = Employee.objects.filter(is_active=True)
        
        for emp in employees:
            bonus = emp.bonuses.filter(...).aggregate(...)
            overtime = ...
            
            payroll = Payroll.objects.create(...)
            PayrollItem.objects.create(...)
            PayrollItem.objects.create(...)
            
            send_mail(...)
            Notification.objects.create(...)
        
        return Response({'message': 'Done'})
```

```python
# GOOD: Extract to service
class PayrollService:
    @staticmethod
    @transaction.atomic
    def generate_monthly_payroll(month, year, generated_by):
        """All complex logic here"""
        # ... implementation
        return results

class PayrollViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['post'])
    def generate_monthly(self, request):
        # Clean and simple! ✅
        month = request.data.get('month')
        year = request.data.get('year')
        
        if not month or not year:
            return APIResponse.error("Month and year required")
        
        # Delegate to service
        result = PayrollService.generate_monthly_payroll(
            month, year, request.user
        )
        
        return APIResponse.success(data=result)
```

---

## Best Practices

### 1. Folder Structure

```
your_project/
├── apps/
│   ├── accounts/
│   │   ├── models.py           # User, Division models
│   │   ├── serializers.py      # User serializers
│   │   ├── views.py            # User viewsets
│   │   └── services.py         # Account-related services
│   │
│   ├── payroll/
│   │   ├── models.py           # Payroll, PayrollItem
│   │   ├── serializers.py      # Payroll serializers
│   │   ├── views.py            # Payroll viewsets
│   │   └── services.py         # Payroll generation service
│   │
│   ├── attendance/
│   │   ├── models.py           # Attendance model
│   │   ├── serializers.py      # Attendance serializers
│   │   ├── views.py            # Attendance viewsets
│   │   └── services.py         # Check-in/out services
│   │
│   └── core/
│       ├── models/
│       │   ├── __init__.py
│       │   └── base.py         # Base models (AuditModel, etc)
│       ├── serializers/
│       │   ├── __init__.py
│       │   └── base.py         # Base serializers
│       ├── permissions.py      # Custom permissions
│       ├── responses.py        # APIResponse helper
│       ├── pagination.py       # Custom pagination
│       └── services/
│           ├── __init__.py
│           ├── email.py        # Email service (shared)
│           ├── notification.py # Notification service (shared)
│           └── storage.py      # File storage service (shared)
```

### 2. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| **Model method** | `verb_noun()` | `calculate_salary()`, `approve_leave()` |
| **Model property** | `is_` or `has_` | `is_eligible`, `has_permission` |
| **Service class** | `NounService` | `PayrollService`, `EmailService` |
| **Service method** | `verb_noun()` | `generate_payroll()`, `send_email()` |
| **ViewSet action** | `verb()` | `approve()`, `reject()`, `export_csv()` |

### 3. Code Organization Checklist

**Before writing code, ask:**

| Question | If YES → Use |
|----------|-------------|
| Does it define database schema? | Model |
| Does it calculate/transform model data? | Model method |
| Does it validate business rules? | Model method |
| Does it format data for API? | Serializer |
| Does it validate API input? | Serializer |
| Does it check permissions? | ViewSet/Permission class |
| Does it handle HTTP requests? | ViewSet |
| Does it involve 3+ models? | Service |
| Does it need transactions? | Service |
| Does it call external APIs? | Service |

### 4. Testing Strategy

```python
# ========== MODEL TESTS: Pure business logic ==========
class EmployeeModelTest(TestCase):
    def test_calculate_salary(self):
        """Test salary calculation"""
        employee = Employee.objects.create(
            gaji_pokok=5000000
        )
        Bonus.objects.create(
            employee=employee,
            amount=1000000,
            date=now().date()
        )
        
        # Direct model call, no HTTP needed ✅
        salary = employee.calculate_monthly_salary()
        
        self.assertEqual(salary['total'], 6000000)
    
    def test_leave_approval(self):
        """Test leave approval business rule"""
        leave = Leave.objects.create(status='pending')
        approver = User.objects.create(username='manager')
        
        # Direct model call ✅
        leave.approve(approver)
        
        self.assertEqual(leave.status, 'approved')
        self.assertEqual(leave.approved_by, approver)


# ========== SERIALIZER TESTS: Data transformation ==========
class EmployeeSerializerTest(TestCase):
    def test_serialization(self):
        """Test data formatting"""
        employee = Employee.objects.create(
            first_name='John',
            last_name='Doe'
        )
        
        serializer = EmployeeSerializer(employee)
        data = serializer.data
        
        # Check formatted output ✅
        self.assertEqual(data['full_name'], 'John Doe')
    
    def test_validation(self):
        """Test API input validation"""
        data = {
            'start_date': '2024-01-10',
            'end_date': '2024-01-05'  # Before start!
        }
        
        serializer = LeaveSerializer(data=data)
        
        # Should fail validation ✅
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_date', serializer.errors)


# ========== VIEWSET TESTS: API endpoints ==========
class LeaveViewSetTest(APITestCase):
    def test_approve_permission(self):
        """Test permission check"""
        leave = Leave.objects.create(status='pending')
        staff_user = User.objects.create(username='staff')
        
        # Staff cannot approve ❌
        self.client.force_authenticate(user=staff_user)
        response = self.client.post(f'/api/v1/leaves/{leave.id}/approve/')
        
        self.assertEqual(response.status_code, 403)
    
    def test_approve_success(self):
        """Test successful approval"""
        leave = Leave.objects.create(status='pending')
        hr_admin = User.objects.create(username='hr', is_hr_admin=True)
        
        # HR can approve ✅
        self.client.force_authenticate(user=hr_admin)
        response = self.client.post(f'/api/v1/leaves/{leave.id}/approve/')
        
        self.assertEqual(response.status_code, 200)
        leave.refresh_from_db()
        self.assertEqual(leave.status, 'approved')


# ========== SERVICE TESTS: Complex workflows ==========
class PayrollServiceTest(TestCase):
    def test_generate_monthly_payroll(self):
        """Test payroll generation"""
        # Setup employees
        employee1 = Employee.objects.create(gaji_pokok=5000000)
        employee2 = Employee.objects.create(gaji_pokok=6000000)
        admin = User.objects.create(username='admin')
        
        # Generate payroll
        result = PayrollService.generate_monthly_payroll(
            month=1,
            year=2024,
            generated_by=admin
        )
        
        # Verify results
        self.assertEqual(result['count'], 2)
        self.assertEqual(Payroll.objects.count(), 2)
        
        # Verify notifications sent
        self.assertEqual(Notification.objects.count(), 2)
```

### 5. Documentation Tips

**Model Docstrings:**
```python
class Employee(models.Model):
    """
    Employee model with salary calculation.
    
    Business Rules:
        - Must be employed 3+ months for leave eligibility
        - Salary = Basic + Bonus + Overtime - Deductions
        - Late if check-in after 9:00 AM
    
    Examples:
        >>> employee = Employee.objects.get(id=1)
        >>> salary = employee.calculate_monthly_salary()
        >>> print(salary['total'])
        6500000
    """
    
    def calculate_monthly_salary(self, month=None, year=None):
        """
        Calculate total monthly salary.
        
        Args:
            month (int, optional): Target month (1-12). Defaults to current.
            year (int, optional): Target year. Defaults to current.
        
        Returns:
            dict: {
                'gaji_pokok': Decimal,
                'bonus': Decimal,
                'overtime': Decimal,
                'deductions': Decimal,
                'total': Decimal
            }
        
        Examples:
            >>> salary = employee.calculate_monthly_salary(month=1, year=2024)
            >>> print(f"Total: {salary['total']}")
            Total: 6500000
        """
        pass
```

**Service Docstrings:**
```python
class PayrollService:
    """
    Payroll generation and management service.
    
    Coordinates:
        - Employee model (salary calculation)
        - Attendance model (work hours)
        - Bonus model (bonuses)
        - Payroll model (records)
        - Notification system (alerts)
    
    Thread Safety:
        All methods use database transactions for consistency.
    """
    
    @staticmethod
    @transaction.atomic
    def generate_monthly_payroll(month, year, generated_by):
        """
        Generate payroll for all active employees.
        
        Process:
            1. Validate month/year
            2. Check for duplicates
            3. Calculate each employee salary
            4. Create payroll records
            5. Create item breakdown
            6. Send notifications
            7. Log activity
        
        Args:
            month (int): Month (1-12)
            year (int): Year (e.g., 2024)
            generated_by (User): User generating payroll
        
        Returns:
            dict: {
                'count': int,
                'total_amount': Decimal,
                'payrolls': list[Payroll]
            }
        
        Raises:
            ValidationError: If month invalid or already generated
        
        Examples:
            >>> result = PayrollService.generate_monthly_payroll(
            ...     month=1,
            ...     year=2024,
            ...     generated_by=request.user
            ... )
            >>> print(f"Generated {result['count']} payrolls")
            Generated 150 payrolls
        """
        pass
```

### 6. Performance Optimization

| Layer | Optimization | Example |
|-------|-------------|---------|
| **Model** | Use `select_related()` for FK | `Employee.objects.select_related('division')` |
| **Model** | Use `prefetch_related()` for M2M | `Employee.objects.prefetch_related('bonuses')` |
| **Model** | Use `only()` for specific fields | `Employee.objects.only('id', 'name')` |
| **Model** | Add database indexes | `class Meta: indexes = [Index(fields=['email'])]` |
| **Serializer** | Use `SerializerMethodField` sparingly | Cache heavy calculations |
| **ViewSet** | Optimize queryset in `get_queryset()` | Apply filters early |
| **Service** | Use `bulk_create()` for many records | `User.objects.bulk_create(users)` |
| **Service** | Use `select_for_update()` in transactions | Prevent race conditions |

**Example: Optimized ViewSet**
```python
class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """Optimized query with minimal database hits"""
        return Employee.objects.select_related(
            'division',           # FK: 1 JOIN
            'position'            # FK: 1 JOIN
        ).prefetch_related(
            'bonuses',            # Reverse FK: 1 extra query
            'attendance_set'      # Reverse FK: 1 extra query
        ).only(
            'id', 'employee_id', 'name', 'email',  # Only needed fields
            'division__name',     # From JOIN
            'position__title'     # From JOIN
        )
        # Total: 1 main query + 2 prefetch = 3 queries for ANY number of employees!
```

### 7. Common Patterns Summary

**Pattern: State Machine (Model)**
```python
class Leave(models.Model):
    # States
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    status = models.CharField(max_length=20, default=STATUS_PENDING)
    
    # Transitions
    def approve(self, approver):
        """pending → approved"""
        self._validate_transition('approve')
        self.status = self.STATUS_APPROVED
        self.approved_by = approver
        self.save()
    
    def reject(self, rejector, reason):
        """pending → rejected"""
        self._validate_transition('reject')
        self.status = self.STATUS_REJECTED
        self.rejected_by = rejector
        self.rejection_reason = reason
        self.save()
    
    def _validate_transition(self, action):
        """Validate state transition"""
        if self.status != self.STATUS_PENDING:
            raise ValidationError(
                f"Cannot {action} leave with status '{self.status}'"
            )
```

**Pattern: Query Helpers (Model)**
```python
class Employee(models.Model):
    # Class methods for common queries
    @classmethod
    def get_active_employees(cls):
        """Get all active employees"""
        return cls.objects.filter(is_active=True)
    
    @classmethod
    def get_by_division(cls, division, include_children=False):
        """Get employees by division"""
        if include_children:
            divisions = [division] + division.get_descendants()
            return cls.objects.filter(division__in=divisions)
        return cls.objects.filter(division=division)
    
    @classmethod
    def get_eligible_for_promotion(cls):
        """Get employees eligible for promotion"""
        one_year_ago = now().date() - timedelta(days=365)
        return cls.objects.filter(
            is_active=True,
            hire_date__lte=one_year_ago
        ).exclude(
            promotions__date__gte=one_year_ago
        )
```

**Pattern: Service Factory (Service)**
```python
class NotificationService:
    """Factory for different notification types"""
    
    @staticmethod
    def send_leave_approval(leave):
        """Send leave approval notification"""
        Notification.objects.create(
            user=leave.employee,
            type='leave_approved',
            title='Leave Approved',
            message=f'Your leave request has been approved'
        )
    
    @staticmethod
    def send_payslip_ready(payroll):
        """Send payslip ready notification"""
        Notification.objects.create(
            user=payroll.employee,
            type='payslip_ready',
            title='Payslip Ready',
            message=f'Your payslip for {payroll.month}/{payroll.year} is ready'
        )
    
    @staticmethod
    def send_late_arrival(attendance):
        """Send late arrival notification"""
        Notification.objects.create(
            user=attendance.employee,
            type='late_arrival',
            title='Late Check-In',
            message=f'You checked in late at {attendance.check_in}'
        )
```

---

## Quick Reference Card

### Where Does My Code Go?

| I Need To... | Put It In... |
|-------------|-------------|
| Define database fields | Model |
| Calculate employee salary | Model method |
| Check if user is eligible | Model property |
| Approve/reject leave | Model method |
| Format date for API | Serializer |
| Show nested data | Serializer |
| Validate API input | Serializer |
| Check permissions | ViewSet / Permission class |
| Handle file upload | ViewSet |
| Export to CSV | ViewSet |
| Generate 100 payrolls | Service |
| Process complex check-in | Service |
| Send bulk emails | Service |
| Call external API | Service |

### Decision Flowchart

```
START
  │
  ├─ Is it about data structure?
  │  └─ Model fields
  │
  ├─ Is it a business rule for ONE model?
  │  └─ Model method
  │
  ├─ Is it formatting data for API?
  │  └─ Serializer
  │
  ├─ Is it about HTTP/permissions?
  │  └─ ViewSet
  │
  ├─ Is it coordinating MULTIPLE models?
  │  └─ Service
  │
  └─ Still unsure?
     └─ Ask: "Can I test this without HTTP?"
        ├─ YES → Model or Service
        └─ NO → ViewSet or Serializer
```

### Testing Quick Guide

```python
# Model: No HTTP needed
def test_model():
    obj = MyModel.objects.create()
    result = obj.my_method()
    assert result == expected

# Serializer: No HTTP needed
def test_serializer():
    serializer = MySerializer(data=input_data)
    assert serializer.is_valid()

# ViewSet: HTTP required
def test_viewset():
    self.client.force_authenticate(user=user)
    response = self.client.post('/api/endpoint/')
    assert response.status_code == 200

# Service: No HTTP needed
def test_service():
    result = MyService.my_method(params)
    assert result['success'] == True
```

---

## Conclusion

### Key Takeaways

1. **Model** = Single source of truth for business logic
2. **Serializer** = Data transformation layer (Python ↔ JSON)
3. **ViewSet** = API gateway (HTTP + permissions)
4. **Service** = Complex workflow coordinator

### The Golden Rules

✅ **Model**: "What can this data do?"
✅ **Serializer**: "How to show/receive this?"
✅ **ViewSet**: "Who can access? Via what endpoint?"
✅ **Service**: "How to coordinate multiple things?"

### Remember

- Keep it **SIMPLE**
- One **RESPONSIBILITY** per layer
- Make it **TESTABLE**
- Make it **REUSABLE**

---

## Additional Resources

### Recommended Reading

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django Design Patterns](https://agiliq.com/blog/2015/07/django-design-patterns/)

### Tools

- **Django Debug Toolbar** - Query optimization
- **django-extensions** - Shell Plus, graph models
- **pytest-django** - Better testing
- **black** - Code formatting
- **pylint-django** - Linting

---

**Last Updated:** January 2025
**Version:** 1.0
**Author:** Your Team

---

*Happy Coding! 🚀* Mistake 1: Business Logic in ViewSet

```python
# BAD: Too much logic in viewset
class LeaveViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        
        # Business logic scattered here! ❌
        if leave.status != 'pending':
            return APIResponse.error("Only pending can be approved")
        
        leave.status = 'approved'
        leave.approved_by = request.user
        leave.save()
        
        # Send email
        send_mail(...)
        
        return APIResponse.success(...)
```

```python
# GOOD: Business logic in model
class Leave(models.Model):
    def approve(self, approver):
        if self.status != 'pending':
            raise ValidationError("Only pending can be approved")
        self.status = 'approved'
        self.approved_by = approver
        self.save()

class LeaveViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.approve(request.user)  # Delegate! ✅
        return APIResponse.success(...)
```

### ❌ Mistake 2: Calculations in Serializer

```python
# BAD: Complex calculation in serializer
class EmployeeSerializer(serializers.ModelSerializer):
    monthly_salary = serializers.SerializerMethodField()
    
    def get_monthly_salary(self, obj):
        # Complex logic here! ❌
        bonus = obj.bonuses.filter(...).aggregate(...)
        overtime = ...
        return obj.gaji_pokok + bonus + overtime
```

```python
# GOOD: Calculation in model
class Employee(models.Model):
    def calculate_monthly_salary(self):
        bonus = self.bonuses.filter(...).aggregate(...)
        overtime = ...
        return self.gaji_pokok + bonus + overtime

class EmployeeSerializer(serializers.ModelSerializer):
    monthly_salary = serializers.SerializerMethodField()
    
    def get_monthly_salary(self, obj):
        return obj.calculate_monthly_salary()  # Delegate! ✅
```

### ❌