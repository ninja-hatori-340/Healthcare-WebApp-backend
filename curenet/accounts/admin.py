from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, PatientProfile, DoctorProfile, Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    """Admin interface for Clinic model."""
    list_display = ['name', 'phone_number', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email', 'phone_number', 'address']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'phone_number', 'email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model with role-based access."""
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['date_joined', 'last_login']
        return []


class PatientProfileInline(admin.StackedInline):
    """Inline admin for PatientProfile."""
    model = PatientProfile
    can_delete = False
    verbose_name_plural = 'Patient Profile'
    fields = ('date_of_birth', 'gender', 'phone_number', 'address', 'is_active')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    """Admin interface for PatientProfile."""
    list_display = ['user', 'gender', 'date_of_birth', 'phone_number', 'is_active', 'created_at']
    list_filter = ['gender', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'phone_number', 'address')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.append('user')
        return readonly


class DoctorProfileInline(admin.StackedInline):
    """Inline admin for DoctorProfile."""
    model = DoctorProfile
    can_delete = False
    verbose_name_plural = 'Doctor Profile'
    fields = ('specialization', 'qualification', 'experience_years', 'clinic', 'is_approved', 'is_active')


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """Admin interface for DoctorProfile."""
    list_display = ['user', 'specialization', 'clinic', 'qualification', 'experience_years', 'is_approved', 'is_active', 'created_at']
    list_filter = ['specialization', 'is_approved', 'is_active', 'clinic', 'created_at']
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'specialization', 'qualification', 'clinic__name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Professional Information', {
            'fields': ('specialization', 'qualification', 'experience_years'),
            'description': 'Doctor submitted information.'
        }),
        ('Admin Assignment', {
            'fields': ('clinic',),
            'description': 'Assign clinic to doctor when approving. Clinic assignment is required for approval.'
        }),
        ('Status', {
            'fields': ('is_approved', 'is_active'),
            'description': 'Admin must approve doctors and assign a clinic before they can login.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    actions = ['approve_doctors', 'reject_doctors']
    
    def approve_doctors(self, request, queryset):
        """Admin action to approve selected doctors."""
        # Check for doctors without clinic assignment
        doctors_without_clinic = queryset.filter(clinic__isnull=True)
        if doctors_without_clinic.exists():
            self.message_user(
                request, 
                f'Warning: {doctors_without_clinic.count()} doctor(s) do not have a clinic assigned. '
                f'Please assign clinics individually before approving.',
                level='warning'
            )
            return
        
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} doctor(s) approved successfully.')
    approve_doctors.short_description = 'Approve selected doctors (requires clinic assignment)'
    
    def reject_doctors(self, request, queryset):
        """Admin action to reject selected doctors."""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} doctor(s) rejected.')
    reject_doctors.short_description = 'Reject selected doctors'

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.append('user')
        return readonly
