# Spec: Registration

## Overview
Implement the user registration feature for Spendly expense tracker. This step allows new users to create an account by providing their name, email, and password. The registration form validates input, checks for duplicate emails, hashes passwords securely, and stores the user in the database. This is the first step of the authentication system, enabling personalized expense tracking in subsequent steps.

## Depends on
- Step 01 (Database Setup) — requires the `users` table and `get_db()` function to be implemented

## Routes
- `GET /register` - render registration form - public (already exists as stub, upgrade it)
- `POST /register` — handles registration form submission — public

## Database changes
No database changes — uses the `users` table created in Step 01

## Templates
- **Create:** `templates/register.html` — registration form with name, email, password fields
- **Modify:** None

## Files to change
- `app.py` — add POST handler for `/register` route

## Files to create
- `templates/register.html` — registration form template

## New dependencies
No new dependencies

## Rules for implementation
- No SQLAlchemy or ORMs — use raw SQLite with parameterized queries only
- Passwords must be hashed with `werkzeug.security.generate_password_hash`
- All templates must extend `base.html`
- Use CSS variables for styling — never hardcode hex values
- Email must be checked for uniqueness before insert
- Name must not be empty or whitespace-only (name.strip() must be non-empty); maximum 100 characters
- Password must be at least 8 characters long
- Display clear error messages for validation failures
- On successful registration, flash a success message ("Account created. Please log in.") and redirect to the login page



## Definition of done
- [ ] Registration form loads at GET /register with name, email, and password fields.
- [ ] Form validates that all fields are filled (name must not be whitespace-only)
- [ ] Form validates name is 100 characters or fewer
- [ ] Form validates email format (contains @)
- [ ] Form rejects duplicate emails with error message
- [ ] Form validates password is at least 8 characters
- [ ] Form rejects duplicate emails with a clear error message
- [ ] Password is hashed before storing in database
- [ ] Successful registration flashes "Account created. Please log in." and redirects to login page
- [ ] Error states re-render the form with the error message and preserve previously entered values (except password)
- [ ] User can verify new user exists in database after registration
- [ ] All SQL queries use parameterized statements (no string formatting)
