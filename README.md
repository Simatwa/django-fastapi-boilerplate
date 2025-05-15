# django-fastapi-boilerplate
Repository for quickly jumpstarting web projects that uses both Django &amp; FastAPI frameworks for backend.


# Backend Directory Structure

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

# Frontend Directory Structure

Typical frontend directory structure using React might look like:

```
frontend
├── dist.ready
│   ├── assets
│   │   ├── index-8zeza7Vl.css
│   │   └── index-DrVtJ0P4.js
│   └── index.html
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── postcss.config.js
├── src
│   ├── api
│   │   ├── auth.ts
│   │   ├── client.ts
│   │   ├── routes
│   │   │   ├── account.ts
│   │   │   ├── business.ts
│   │   │   └── core.ts
│   │   └── types
│   │       ├── account.ts
│   │       ├── auth.ts
│   │       ├── business.ts
│   │       └── core.ts
│   ├── App.tsx
│   ├── components
│   │   ├── auth
│   │   │   ├── LoginForm.tsx
│   │   │   ├── PasswordInput.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ResetPasswordForm.tsx
│   │   ├── BookCard.tsx
│   │   ├── BookSearch.tsx
│   │   ├── ContactForm.tsx
│   │   ├── dashboard
│   │   │   ├── BookSuggestions.tsx
│   │   │   ├── BorrowedBooks.tsx
│   │   │   ├── Concerns.tsx
│   │   │   ├── Feedback.tsx
│   │   │   ├── Layout.tsx
│   │   │   └── Messages.tsx
│   │   ├── FAQSection.tsx
│   │   ├── FeedbackCard.tsx
│   │   ├── Modal.tsx
│   │   └── Navbar.tsx
│   ├── index.css
│   ├── main.tsx
│   ├── pages
│   │   ├── AuthPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── HomePage.tsx
│   ├── utils
│   │   ├── auth.ts
│   │   └── format.ts
│   └── vite-env.d.ts
├── tailwind.config.js
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts

12 directories, 48 files
```