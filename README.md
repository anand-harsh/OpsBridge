# OpsBridge

A production-grade incident management and response platform inspired by modern reliability engineering tools like PagerDuty and Opsgenie. OpsBridge enables organizations to manage incidents, coordinate responders, track incident lifecycles, and monitor operational health through real-time collaboration and analytics.

---

## Features

### Organization Management
- Create and manage multiple organizations
- Invite and manage members
- Role-Based Access Control (Owner, Admin, Engineer, Viewer)

### Team Management
- Create engineering teams
- Assign team leads
- Manage team members and permissions

### Service Registry
- Register production services
- Associate services with engineering teams
- Track incidents per service

### Incident Management
- Create incidents
- Assign incident commanders
- Update severity and status
- Validate incident state transitions
- Resolve incidents with audit history

### Incident Timeline
- Automatic event logging
- Comment support
- Unified activity timeline
- Complete incident audit trail

### Dashboard & Analytics
- Incident summary metrics
- Severity distribution
- Service-wise incident statistics
- Recent activity feed
- Average resolution time

### Search & Filtering
- Filter by:
  - Status
  - Severity
  - Service
  - Commander
- Search incidents
- Ordering
- Pagination

### Real-Time Collaboration
- Live incident updates using Django Channels
- WebSocket event broadcasting
- Instant synchronization across connected users

---

# Architecture

The project follows a layered architecture separating API, business logic, and data access.

```
Client
   │
   ▼
Views (API Layer)
   │
   ▼
Selectors (Read Operations)
   │
   ▼
Services (Business Logic)
   │
   ▼
Models (Database)
```

Business logic is intentionally kept out of views, making the application easier to maintain, test, and scale.

---

# Tech Stack

## Backend

- Python
- Django
- Django REST Framework
- Django Channels

## Database

- PostgreSQL

## Authentication

- JWT Authentication

## Infrastructure

- Docker
- Docker Compose

## Real-Time

- WebSockets
- ASGI

---

# Project Structure

```
apps/
│
├── accounts/
├── organizations/
├── teams/
├── services/
├── incidents/
└── dashboard/

Each app contains:

models.py
views.py
serializers.py
selectors.py
services.py
permissions.py
urls.py
```

---

# Core Modules

## Accounts

- User registration
- Login
- JWT authentication
- User profile

---

## Organizations

- Create organizations
- Membership management
- Organization roles

---

## Teams

- Team creation
- Team membership
- Team lead assignment

---

## Services

- Register production services
- Associate services with teams
- Service ownership

---

## Incidents

Supports complete incident lifecycle:

```
OPEN
   │
   ▼
INVESTIGATING
   │
   ▼
MONITORING
   │
   ▼
RESOLVED
```

Operations include:

- Create incident
- Assign commander
- Change severity
- Change status
- Add comments
- Resolve incident

---

## Dashboard

Provides:

- Open incidents
- Critical incidents
- Resolved today
- Average resolution time
- Severity analytics
- Service analytics
- Recent activity

---

# Role-Based Access Control

| Role | Permissions |
|------|-------------|
| Owner | Full access |
| Admin | Manage teams, services, incidents |
| Engineer | Create and update incidents |
| Viewer | Read-only access |

---

# API Highlights

## Authentication

```
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
GET  /api/auth/me/
```

---

## Organizations

```
POST /api/organizations/
GET  /api/organizations/
GET  /api/organizations/{slug}/
```

---

## Teams

```
POST /api/teams/
GET  /api/teams/
```

---

## Services

```
POST /api/services/
GET  /api/services/
```

---

## Incidents

```
POST /api/incidents/
GET  /api/incidents/
PATCH /api/incidents/{id}/status/
PATCH /api/incidents/{id}/severity/
PATCH /api/incidents/{id}/commander/
POST /api/incidents/{id}/comments/
GET  /api/incidents/{id}/timeline/
```

---

## Dashboard

```
GET /api/dashboard/
```

---

# Getting Started

## Clone Repository

```bash
git clone https://github.com/your-username/OpsBridge.git

cd OpsBridge
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=opsbridge

DB_USER=postgres

DB_PASSWORD=password

DB_HOST=localhost

DB_PORT=5432
```

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Start Server

```bash
python manage.py runserver
```

---

Visit

```
http://127.0.0.1:8000/
```

---

# Future Improvements

- Email notifications
- Redis caching
- Celery background workers
- Slack integration
- Incident escalation policies
- Service health monitoring
- Kubernetes deployment
- CI/CD pipeline
- Comprehensive test coverage

---

# Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# License

This project is licensed under the MIT License.

---

## ⭐ If you found this project useful, consider giving it a star!
