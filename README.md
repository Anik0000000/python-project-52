### Hexlet tests and linter status:
[![Actions Status](https://github.com/Anik0000000/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Anik0000000/python-project-52/actions)

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