from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, PatientProfileForm, DoctorProfileForm
from .models import User, PatientProfile, DoctorProfile


def register_view(request):
    """Registration view with role selection."""
    if request.user.is_authenticated:
        return redirect('accounts:profile_redirect')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Redirect to profile creation based on role
                if user.role == User.Role.PATIENT:
                    return redirect('accounts:create_patient_profile')
                elif user.role == User.Role.DOCTOR:
                    return redirect('accounts:create_doctor_profile')
                elif user.role == User.Role.ADMIN:
                    return redirect('accounts:profile_redirect')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Custom login view with doctor approval check."""
    if request.user.is_authenticated:
        return redirect('accounts:profile_redirect')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is a doctor and if they're approved
            if user.role == User.Role.DOCTOR:
                try:
                    doctor_profile = user.doctor_profile
                    if not doctor_profile.is_approved:
                        messages.error(request, 'Your account is pending admin approval. Please wait for approval before logging in.')
                        return render(request, 'accounts/login.html', {'error': 'Account pending approval'})
                    if not doctor_profile.is_active:
                        messages.error(request, 'Your account has been deactivated. Please contact admin.')
                        return render(request, 'accounts/login.html', {'error': 'Account deactivated'})
                except DoctorProfile.DoesNotExist:
                    # Doctor registered but profile not created yet
                    return redirect('accounts:create_doctor_profile')
            
            # Check if user is a patient and profile exists
            if user.role == User.Role.PATIENT:
                try:
                    patient_profile = user.patient_profile
                    if not patient_profile.is_active:
                        messages.error(request, 'Your account has been deactivated. Please contact admin.')
                        return render(request, 'accounts/login.html', {'error': 'Account deactivated'})
                except PatientProfile.DoesNotExist:
                    # Patient registered but profile not created yet
                    return redirect('accounts:create_patient_profile')
            
            # All checks passed, log in
            login(request, user)
            return redirect('accounts:profile_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def create_patient_profile(request):
    """Create patient profile after registration."""
    # Check if profile already exists
    if hasattr(request.user, 'patient_profile'):
        messages.info(request, 'Profile already exists.')
        return redirect('accounts:profile_redirect')
    
    # Check if user is a patient
    if request.user.role != User.Role.PATIENT:
        messages.error(request, 'Access denied.')
        return redirect('accounts:profile_redirect')
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile created successfully!')
            return redirect('accounts:profile_redirect')
    else:
        form = PatientProfileForm()
    
    return render(request, 'accounts/create_patient_profile.html', {'form': form})


@login_required
def create_doctor_profile(request):
    """Create doctor profile after registration."""
    # Check if profile already exists
    if hasattr(request.user, 'doctor_profile'):
        messages.info(request, 'Profile already exists.')
        return redirect('accounts:profile_redirect')
    
    # Check if user is a doctor
    if request.user.role != User.Role.DOCTOR:
        messages.error(request, 'Access denied.')
        return redirect('accounts:profile_redirect')
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(
                request, 
                'Profile created successfully! Your account is pending admin approval. You will be able to login once approved.'
            )
            # Log out the doctor since they need approval
            logout(request)
            return redirect('accounts:login')
    else:
        form = DoctorProfileForm()
    
    return render(request, 'accounts/create_doctor_profile.html', {'form': form})


@login_required
def profile_redirect(request):
    """Redirect user based on their role and profile status."""
    user = request.user
    
    if user.role == User.Role.PATIENT:
        try:
            profile = user.patient_profile
            return render(request, 'accounts/patient_dashboard.html', {
                'user': user,
                'profile': profile
            })
        except PatientProfile.DoesNotExist:
            return redirect('accounts:create_patient_profile')
    
    elif user.role == User.Role.DOCTOR:
        try:
            profile = user.doctor_profile
            if profile.is_approved:
                return render(request, 'accounts/doctor_dashboard.html', {
                    'user': user,
                    'profile': profile
                })
            else:
                messages.warning(request, 'Your account is pending admin approval.')
                return render(request, 'accounts/pending_approval.html', {'user': user})
        except DoctorProfile.DoesNotExist:
            return redirect('accounts:create_doctor_profile')
    
    elif user.role == User.Role.ADMIN:
        return redirect('admin:index')
    
    return redirect('accounts:login')


@login_required
def patient_dashboard(request):
    """Patient dashboard view."""
    if request.user.role != User.Role.PATIENT:
        messages.error(request, 'Access denied.')
        return redirect('accounts:profile_redirect')
    
    try:
        profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        return redirect('accounts:create_patient_profile')
    
    return render(request, 'accounts/patient_dashboard.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def doctor_dashboard(request):
    """Doctor dashboard view."""
    if request.user.role != User.Role.DOCTOR:
        messages.error(request, 'Access denied.')
        return redirect('accounts:profile_redirect')
    
    try:
        profile = request.user.doctor_profile
        if not profile.is_approved:
            messages.warning(request, 'Your account is pending admin approval.')
            return render(request, 'accounts/pending_approval.html', {'user': request.user})
    except DoctorProfile.DoesNotExist:
        return redirect('accounts:create_doctor_profile')
    
    return render(request, 'accounts/doctor_dashboard.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Custom logout view that handles both GET and POST requests."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
