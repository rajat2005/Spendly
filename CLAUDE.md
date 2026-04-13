# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly - A Flask-based expense tracking web application. This is a student project being built incrementally across multiple steps (database setup, authentication, CRUD operations).

## Commands

```bash
# Run the application
python app.py

# Installs dependencies
pip install -r requirements.txt
```

The Flask app runs on port 5001 with debug mode enabled.

## Architecture

**Stack:** Flask (Python 3.x), SQLite, Jinja2 templates, vanilla CSS/JavaScript

**Structure:**
- `app.py` - Main Flask application with all routes
- `database/db.py` - Database layer (SQLite connections, schema, seed data)
- `templates/` - Jinja2 HTML templates (base.html extends for all pages)
- `static/` - CSS (`css/style.css`) and JavaScript (`js/main.js`)

**Key routes implemented:**
- `/` - Landing page
- `/register`, `/login` - Authentication pages (POST forms)
- `/terms`, `/privacy` - Static pages
- `/logout`, `/profile`, `/expenses/*` - Placeholder routes for future steps

**Database pattern:**
- `get_db()` - Returns SQLite connection with row_factory and foreign keys enabled
- `init_db()` - Creates tables using CREATE TABLE IF NOT EXISTS
- `seed_db()` - Inserts sample development data

## Development Notes

- Virtual environment is in `venv/` (not committed)
- Database file location: typically `expenses.db` in project root (created by init_db)
- No test framework configured yet (pytest in requirements but no tests written)
