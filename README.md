# Secure Student Records API (Lab Activity)

This project is a Django REST Framework API that implements a **Secure Student Records System**. It focuses on API security, using JSON Web Tokens (JWT) for authentication and Role-Based Access Control (RBAC) to manage granular permissions for different types of users.

## 🚀 Features & Role-Based Permissions

The API strictly enforces access control based on three user groups:

**1. Administrator (`Admin` Group)**
* Has full access to the system.
* Can create and delete student records.
* Can manage users, classes, and grading timeframes.

**2. Faculty (`Faculty` Group)**
* Can view profiles of students assigned to their classes.
* Can create and update grades, but **only** for students in their assigned classes.
* Can only modify grades if the current date falls within an active `GradingTimeframe`.
* Cannot delete records or access system settings.

**3. Student (`Student` Group)**
* Can view their own profile and their enrolled subjects.
* Can view their own grades.
* Can update limited personal information (Contact Number and Email).
* Can change their own password via a dedicated endpoint.
* **Cannot** view other students' data, modify grades, or access Admin/Faculty endpoints.

## 🛠️ Technology Stack
* Python
* Django
* Django REST Framework
* djangorestframework-simplejwt (JWT Authentication)

## ⚙️ Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Zsxcylliope/Module-4-Security-Integrated-Systems.git
   cd Module-4-Security-Integrated-Systems/core
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install django djangorestframework djangorestframework-simplejwt
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 📡 API Endpoints

### Authentication
* `POST /api/token/` - Obtain JWT access and refresh tokens.
* `POST /api/change-password/` - (Students) Change password.

### Core Endpoints
*(Must pass `Authorization: Bearer <token>` in headers)*
* `GET/POST/PUT/DELETE /api/student-records/` - Manage student profiles (Permissions vary by role).
* `GET/POST/PUT/DELETE /api/classes/` - Manage Course Classes (Admin/Faculty only).
* `GET/POST/PUT/DELETE /api/timeframes/` - Manage Grading Timeframes (Admin/Faculty only).
* `GET/POST/PUT/DELETE /api/grades/` - Manage student grades (Permissions vary by role).
