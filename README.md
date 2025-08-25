### Hexlet tests and linter status:
[![Actions Status](https://github.com/Anik0000000/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Anik0000000/python-project-52/actions)

[![CI](https://github.com/Anik0000000/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/Anik0000000/python-project-52/actions/workflows/pyci.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Anik0000000_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Anik0000000_python-project-52)

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