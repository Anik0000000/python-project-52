### Hexlet tests and linter status:
[![Actions Status](https://github.com/Anik0000000/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Anik0000000/python-project-52/actions)

[![CI](https://github.com/Anik0000000/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/Anik0000000/python-project-52/actions/workflows/pyci.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Anik0000000_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Anik0000000_python-project-52)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Anik0000000_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Anik0000000_python-project-52)

## Demo
[Deployed application](https://python-project-52-j8mu.onrender.com/)

## Features

### User Management
- User registration, login, logout
- User profile management (only own profile)
- User list (public access)
- User protection (cannot delete if has tasks)

### Status Management
- Create, view, update, and delete statuses
- Status protection (cannot delete if used by tasks)
- Login required for all status operations

### Task Management
- Create, view, update, and delete tasks
- Task detail view with full information
- Automatic author assignment on creation
- Only task author can delete tasks
- Login required for all task operations
- Foreign key relationships (status, author, executor)
- Many-to-many relationship with labels

### Label Management
- Create, view, update, and delete labels
- Label protection (cannot delete if used by tasks)
- Many-to-many relationship with tasks
- Multiple label selection for tasks
- Login required for all label operations

## Technology Stack

### Backend
- Python 3.10+
- Django 5.0+ - Web framework
- PostgreSQL - Production database
- SQLite - Development database
- Gunicorn - WSGI HTTP Server
- Rollbar - Error tracking

### Frontend
- Bootstrap 5 - CSS framework
- Django templates - Server-side rendering

### DevOps & Tools
- UV - Fast Python package installer and resolver
- Coverage.py - Code coverage analysis
- Pytest - Testing framework
- Ruff - Fast Python linter
- GitHub Actions - CI/CD
- SonarQube - Code quality and security
- Render.com - Deployment platform

## Setup and Installation

### Prerequisites
- Python 3.10 or higher
- UV package manager

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anik0000000/python-project-52.git
   cd python-project-52
   ```

2. **Install dependencies**
   ```bash
   make dev-install
   ```

3. **Apply migrations**
   ```bash
   make migrate
   ```

4. **Run the development server**
   ```bash
   make run
   ```

5. **Run tests**
   ```bash
   make test
   ```

6. **Run linting**
   ```bash
   make lint
   ```

7. **Generate coverage report**
   ```bash
   make coverage
   ```

### Production Deployment

This application is configured for deployment on Render.com:

1. **Environment Variables**
   - `SECRET_KEY`: Django secret key
   - `DATABASE_URL`: PostgreSQL connection string
   - `ROLLBAR_TOKEN`: Rollbar access token
   - `DEBUG`: Set to False in production

2. **Build Command**
   ```bash
   make build
   ```

3. **Start Command**
   ```bash
   make render-start
   ```