# PetCare AI

PetCare AI is a Django-based web application designed as a lightweight intelligent pet-care dialogue platform. The project includes standard Django pages, static assets, media upload directories, and a core application module for back-end logic and interaction handling.

This repository can be used for local development, demonstration, and future deployment to a server or containerized environment.

## Requirements

- Python 3.9 or later
- `pip` and `venv` (or Conda)
- Git for version control

## Project Structure

```text
petcare/
├─ manage.py
├─ db.sqlite3
├─ 1/                       # Sample CSV data
├─ cwyl/                    # Core application logic (models, views, urls)
├─ media/uploads/           # Uploaded media files
├─ static/                  # Static assets (CSS, JS, images)
├─ templates/               # HTML templates
└─ petcare/                 # Project settings and configuration
```

## Features

- Django-based web application architecture
- Intelligent question-answering style interaction flow
- Static and media file support
- Django Admin support for management and testing

## Quick Start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install django
```

If you use additional libraries such as `pandas` or `django-import-export`, install them as needed:

```bash
pip install pandas django-import-export
```

### 3. Apply database migrations

```bash
python manage.py migrate
```

### 4. Create an admin user

```bash
python manage.py createsuperuser
```

### 5. Start the development server

```bash
python manage.py runserver
```

Then open:

- Main site: `http://127.0.0.1:8000/`
- Admin dashboard: `http://127.0.0.1:8000/admin/`

Actual routes depend on the URL configuration in `petcare/urls.py` and `cwyl/urls.py`.

## Static and Media Files

- Static assets are served from `static/` during development
- Uploaded files are stored in `media/uploads/`
- In production, you should run:

```bash
python manage.py collectstatic
```

## GitHub Setup

If you want to publish the project to GitHub:

```bash
git init
git add .
git commit -m "chore: initial commit"
git branch -M main
git remote add origin https://github.com/yourname/petcare.git
git push -u origin main
```

Suggested `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
*.sqlite3
.venv/
staticfiles/
media/
.vscode/
.idea/
*.log
```

## Common Issues

- SQLite file lock issues: stop any running processes that are using the database
- Static files not loading: verify template static tags and static configuration
- Encoding issues on systems with Chinese paths: ensure UTF-8 terminal encoding or move the project to a path without non-ASCII characters

## License

No license is currently specified. Add a `LICENSE` file if you plan to open-source the project.

## Contribution

Issues and pull requests are welcome. Before submitting changes, please make sure:

- the project still runs correctly
- the change is clearly described
- dependency changes are reflected in the documentation
