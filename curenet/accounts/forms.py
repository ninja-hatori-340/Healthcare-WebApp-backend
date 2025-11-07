from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User, PatientProfile, DoctorProfile, Clinic


class UserRegistrationForm(UserCreationForm):
    """Registration form with role selection."""
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.RadioSelect,
        required=True
    )
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class PatientProfileForm(forms.ModelForm):
    """Form for patient profile creation."""
    class Meta:
        model = PatientProfile
        fields = ('date_of_birth', 'gender', 'phone_number', 'address')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DoctorProfileForm(forms.ModelForm):
    """Form for doctor profile creation."""
    class Meta:
        model = DoctorProfile
        fields = ('specialization', 'qualification', 'experience_years')
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Cardiology'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MD, MBBS'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

