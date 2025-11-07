# Healthcare WebApp Backend - CureNet

This is the backend of the Healthcare Web Application project for 6th semester Web Engineering course.

## Project Overview

CureNet is a Django-based healthcare management system with Role-Based Access Control (RBAC) supporting three user roles:
- **Patient**: Can register, create profile, and access patient dashboard
- **Doctor**: Can register, create profile (pending admin approval), and access doctor dashboard after approval
- **Admin**: Can manage users, approve doctors, assign clinics, and access admin panel

## Features

- ✅ Custom User Model with RBAC (Patient, Doctor, Admin)
- ✅ Patient Profile Management
- ✅ Doctor Profile Management with Admin Approval
- ✅ Clinic Management
- ✅ Doctor Approval Workflow
- ✅ Beautiful Bootstrap UI Templates
- ✅ Django Admin Interface
- ✅ Secure Authentication System

## Tech Stack

- **Framework**: Django 5.2.7
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5.3.0
- **Python**: 3.x

## Project Structure

```
Healthcare-WebApp-backend/
├── curenet/                 # Main Django project
│   ├── accounts/            # Accounts app (Users, Profiles, Clinics)
│   │   ├── models.py        # User, PatientProfile, DoctorProfile, Clinic models
│   │   ├── views.py         # Authentication and profile views
│   │   ├── forms.py         # Registration and profile forms
│   │   ├── admin.py         # Django admin configuration
│   │   ├── urls.py          # URL routing
│   │   └── management/      # Custom management commands
│   │       └── commands/
│   │           └── createadmin.py  # Create admin user command
│   ├── curenet/             # Project settings
│   │   ├── settings.py      # Django settings
│   │   ├── urls.py          # Main URL configuration
│   │   └── wsgi.py          # WSGI configuration
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   └── accounts/        # Account-related templates
│   ├── static/              # Static files (CSS, JS, images)
│   ├── db.sqlite3           # SQLite database (not in git)
│   └── manage.py            # Django management script
├── .gitignore               # Git ignore file
├── README.md                # This file
├── ADMIN_SETUP.md           # Admin setup guide
└── pip_requirements.txt     # Python dependencies
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ninja-hatori-340/Healthcare-WebApp-backend.git
cd Healthcare-WebApp-backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r pip_requirements.txt

# Or install Django directly
pip install django
```

### Step 4: Database Setup

```bash
# Navigate to project directory
cd curenet

# Run migrations
python manage.py migrate

# Create admin user (see Admin Setup section below)
python manage.py createadmin
```

### Step 5: Run Development Server

```bash
# Make sure you're in the curenet directory
python manage.py runserver

# Server will start on http://127.0.0.1:8000/
```

## Admin Setup

### Method 1: Using Management Command (Recommended)

```bash
cd curenet
python manage.py createadmin

# Or with arguments
python manage.py createadmin --username admin --email admin@curenet.com --password admin123
```

### Method 2: Using Django Createsuperuser

```bash
cd curenet
python manage.py createsuperuser
```

Then edit the user in Django admin to set:
- Role: ADMIN
- Staff status: ✓
- Superuser status: ✓

For detailed admin setup instructions, see [ADMIN_SETUP.md](ADMIN_SETUP.md).

## Usage Guide

### Accessing the Application

1. **Home Page**: `http://127.0.0.1:8000/`
2. **Login**: `http://127.0.0.1:8000/accounts/login/`
3. **Register**: `http://127.0.0.1:8000/accounts/register/`
4. **Admin Panel**: `http://127.0.0.1:8000/admin/`

### User Registration Flow

#### Patient Registration
1. Go to `/accounts/register/`
2. Select "Patient" role
3. Fill in registration details
4. Complete patient profile form
5. Access patient dashboard

#### Doctor Registration
1. Go to `/accounts/register/`
2. Select "Doctor" role
3. Fill in registration details
4. Complete doctor profile form (specialization, qualification, experience)
5. Wait for admin approval
6. Admin assigns clinic and approves doctor
7. Doctor can now login

#### Admin Access
- Create admin account using management command (see Admin Setup)
- Login at `/accounts/login/` or `/admin/`
- Access admin panel for user and clinic management

### Admin Responsibilities

1. **Manage Clinics**
   - Add/edit/delete clinics in Django admin
   - View all clinics

2. **Approve Doctors**
   - Go to Django admin → Doctor Profiles
   - View pending doctor profiles
   - Assign clinic to doctor
   - Approve doctor (`is_approved=True`)
   - Doctors must have clinic assigned before approval

3. **Manage Users**
   - View all users (patients, doctors, admins)
   - Edit user information
   - Activate/deactivate accounts

## Database Models

### User Model
- Extends Django's AbstractUser
- Roles: PATIENT, DOCTOR, ADMIN
- Email is unique and required

### PatientProfile Model
- One-to-one relationship with User
- Fields: date_of_birth, gender, phone_number, address
- Soft delete: is_active flag

### DoctorProfile Model
- One-to-one relationship with User
- Fields: clinic (ForeignKey), specialization, qualification, experience_years
- Admin approval: is_approved flag
- Soft delete: is_active flag

### Clinic Model
- Fields: name, address, phone_number, email
- Soft delete: is_active flag

## Development

### Running Migrations

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Creating Superuser

```bash
python manage.py createsuperuser
```

### Django Shell

```bash
python manage.py shell
```

### Running Tests

```bash
python manage.py test
```

## Git Workflow

### Initial Setup (First Time)

```bash
# Navigate to repository root
cd /home/sanzid/projects/6th_sem_web_Engineering/Healthcare-WebApp-backend

# Check current status
git status

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: RBAC system with patient, doctor, and admin roles"

# Push to remote
git push -u origin main
# Or if your branch is named 'master':
# git push -u origin master
```

### Regular Workflow

```bash
# Check status
git status

# Add specific files
git add curenet/accounts/models.py
git add curenet/templates/

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "Add doctor approval workflow and clinic assignment"

# Push to remote
git push origin main
# Or: git push origin master
```

### Viewing Changes

```bash
# See what files changed
git status

# See detailed changes
git diff

# See commit history
git log
```

## Important Notes

- **Database**: SQLite is used for development. For production, use PostgreSQL or MySQL
- **Secret Key**: Change `SECRET_KEY` in `settings.py` for production
- **DEBUG**: Set `DEBUG = False` in production
- **Static Files**: Run `python manage.py collectstatic` before deployment
- **Doctor Approval**: Doctors cannot login until admin approves and assigns clinic

## Troubleshooting

### Migration Issues
```bash
# Reset migrations (CAUTION: Deletes database)
rm db.sqlite3
rm -rf accounts/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r pip_requirements.txt
```

### Permission Issues
```bash
# Fix file permissions
chmod +x manage.py
```

## Contributors

- Project for 6th Semester Web Engineering Course

## License

This project is for educational purposes.

## Support

For issues and questions, please contact the project maintainers.
