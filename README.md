# Portfolio User Management System

A modern full-stack web application featuring a stunning Glassmorphism UI combined with an interactive 3D background powered by Three.js. Built with Python, Flask, SQLite3, and vanilla JS/CSS.

## Features

- **Modern UI**: Apple VisionOS & Windows 11 inspired Glassmorphism interface
- **3D Background**: Interactive Three.js background with floating glass spheres and crystal objects
- **User Authentication**: Secure register/login with Werkzeug password hashing
- **User Dashboard**: Profile management for standard users
- **Admin Dashboard**: Full CRUD management over all users
- **Responsive Design**: Flawlessly adapts to Desktop, Tablet, and Mobile views
- **Secure**: Utilizes Flask sessions, CSRF protection, and parameterized queries

## Folder Structure

```
PortfolioUserManagement/
│
├── app.py                  # Main Flask application
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── users.db                # SQLite database (generated)
│
├── database/
│   └── create_db.py        # Database initialization script
│
├── templates/              # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── admin_dashboard.html
│   └── edit_user.html
│
├── static/
│   ├── css/                # Stylesheets (Glassmorphism & animations)
│   │   ├── style.css
│   │   ├── login.css
│   │   ├── dashboard.css
│   │   └── admin.css
│   ├── js/                 # Client-side scripts
│   │   ├── app.js
│   │   ├── validation.js
│   │   └── threeScene.js
│   └── images/             # Static images
│
└── uploads/                # User uploaded content
```

## Installation & Requirements

Ensure you have Python 3 installed.

1. **Clone/Navigate to the directory**:
   ```bash
   cd path/to/PortfolioUserManagement
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

## Database Creation

Run the database creation script to initialize the SQLite database and create the default admin user:

```bash
python database/create_db.py
```

*Default Admin Credentials:*
- **Username:** `admin`
- **Email:** `admin@gmail.com`
- **Password:** `admin123`

## Running the Project

Start the Flask development server:

```bash
python app.py
```

Navigate to `http://127.0.0.1:5000` in your web browser.
