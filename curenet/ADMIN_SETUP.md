# Admin Account Setup Guide

## How to Create an Admin Account

There are two ways to create an admin account in CureNet:

### Method 1: Using Django Management Command (Recommended)

This is the easiest way to create an admin account:

```bash
# Activate your virtual environment first
source /path/to/.venv/bin/activate

# Navigate to project directory
cd /home/sanzid/projects/6th_sem_web_Engineering/Healthcare-WebApp-backend/curenet

# Run the createadmin command
python manage.py createadmin
```

The command will prompt you for:
- Username
- Email
- Password

**Example:**
```bash
python manage.py createadmin --username admin --email admin@curenet.com --password admin123
```

### Method 2: Using Django Admin Createsuperuser

You can also use Django's built-in createsuperuser command, but you'll need to manually set the role:

```bash
python manage.py createsuperuser
```

After creating the user, you need to:
1. Go to Django admin at `/admin/`
2. Find the user you just created
3. Edit the user and set:
   - Role: ADMIN
   - Staff status: ✓ (checked)
   - Superuser status: ✓ (checked)

### Method 3: Register via Web Interface

You can also register as ADMIN through the registration page at `/accounts/register/`, but this requires that you manually set `is_staff=True` and `is_superuser=True` in the database or Django admin after registration.

## Accessing Admin Panel

Once you have an admin account:

1. **Via Web Interface:**
   - Go to `/accounts/login/`
   - Login with your admin credentials
   - You'll be redirected to `/admin/` automatically

2. **Direct Admin Access:**
   - Go to `/admin/`
   - Login with your admin credentials

## Admin Responsibilities

As an admin, you can:

1. **Manage Clinics:**
   - Add/edit/delete clinics
   - View all clinics

2. **Approve Doctors:**
   - View pending doctor profiles
   - Assign clinics to doctors
   - Approve/reject doctors
   - Doctors must have a clinic assigned before approval

3. **Manage Users:**
   - View all users (patients, doctors, admins)
   - Edit user information
   - Activate/deactivate accounts

4. **Manage Profiles:**
   - View patient and doctor profiles
   - Edit profile information

## Important Notes

- **Doctor Approval Process:**
  - Doctors register and create their profile
  - Admin must assign a clinic to the doctor
  - Admin must approve the doctor (`is_approved=True`)
  - Only after approval can doctors login

- **Clinic Assignment:**
  - Doctors cannot select their clinic during registration
  - Admin assigns clinic when approving doctor
  - Clinic assignment is required for approval

