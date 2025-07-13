<h1 align="center">django-fastapi-boilerplate</h1>

<p align="center">
  <a href="#"><img alt="Python Version" src="https://img.shields.io/static/v1?logo=python&color=Blue&message=3.13&label=Python"/></a>
  <a href="#"><img alt="Backend Admin - Django" src="https://img.shields.io/static/v1?logo=django&color=Blue&message=v5.1.6&label=Django"/></a>
  <a href="#"><img alt="Backend API - FastAPI" src="https://img.shields.io/static/v1?logo=fastapi&color=Blue&message=v0.115.11&label=FastAPI"/></a>
  <!--
  <a href="#"><img alt="Frontend - React" src="https://img.shields.io/static/v1?logo=react&color=Blue&message=Frontend&label=React"/></a>
  <a href="https://github.com/Simatwa/house-rental-management-system/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=MIT&color=Blue&message=GPLv3&label=License"/></a>
  -->
</p>

Repository for quickly jumpstarting web projects that uses both Django &amp; FastAPI frameworks for backend.

| Page       |   Screenshot   |
|------------|----------------|
| Landing    | ![Landin page demo](https://raw.githubusercontent.com/Simatwa/management-systems/refs/heads/main/assets/django-fastapi-boilerplate/landing-page.png)  |
| Admin      |     ![Admin page demo](https://raw.githubusercontent.com/Simatwa/management-systems/refs/heads/main/assets/django-fastapi-boilerplate/dashboard.png) |
| OpenAPI Docs | ![OpenAPI docs page demo](https://raw.githubusercontent.com/Simatwa/management-systems/refs/heads/main/assets/django-fastapi-boilerplate/openapi-docs.png) |

# Features

- Common django apps ie.
    - [Users](backend/users) - User accounts
    - [Management](backend/management) - Message management, crucial app info etc.
    - [Finance](backend/finance) - Money related stuff
    - [External](backend/external) - App information etc
- FastAPI endpoints
    - [Business](backend/api/v1/business) - Provides app information
    - [Account](backend/api/v1/account) - User account creation & management
    - [Core](backend/api/v1/core) - User level actions - *templated*
- Admin dashboard using [Django-Jazzmin](https://github.com/farridav/django-jazzmin)

<details>

<summary>

<h3>Backend Directory Structure</h3>

</summary>

```
backend
├── api
│   ├── cli.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── README.md
│   ├── tests
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── test_accounts.py
│   │       ├── test_business.py
│   │       └── test_core.py
│   ├── v1
│   │   ├── account
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   ├── business
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── utils.py
│   └── VERSION
├── db.sqlite3
├── env.example
├── external
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   └── external
│   │       ├── css
│   │       ├── img
│   │       │   └── logo.png
│   │       └── js
│   ├── tests.py
│   └── views.py
├── files
│   ├── exports
│   ├── media
│   │   └── default
│   │       ├── logo.png
│   │       └── user.png
│   └── static
├── finance
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── templatetags
│   │   └── my_filters.py
│   ├── tests.py
│   └── views.py
├── Makefile
├── management
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── project
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── dev.py
│   │   ├── __init__.py
│   │   └── prod.py
│   ├── urls.py
│   ├── utils
│   │   ├── admin.py
│   │   └── __init__.py
│   └── wsgi.py
├── requirements.txt
├── templates
│   ├── api
│   │   └── v1
│   │       └── email
│   │           ├── message_received_confirmation.html
│   │           └── password_reset_token.html
│   ├── success.html
│   └── user_creation.html
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── wsgi.py

30 directories, 76 files

```

</details>

> [!IMPORTANT]
> The frontend directory declared in [.env](env.example) must have `index.html` file.