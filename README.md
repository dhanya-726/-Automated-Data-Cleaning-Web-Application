# Django Authentication & Data Management System

A Django-based web application that provides user authentication and data upload, analysis, cleaning, and download functionality.

## Features

- User Sign Up, Login, Logout and Password Reset
- Upload CSV and Excel files
- Analyze missing values, duplicates, and data types
- Generic column-wise data cleaning
- Generate and download cleaned datasets
- User-specific file access

## Technologies Used

- Python
- Django
- Pandas
- SQLite
- HTML/CSS

## Data Cleaning

The application:

- Removes duplicate rows
- Handles missing values
- Converts numeric data safely
- Marks missing text values as `"Missing"`
- Removes completely empty rows

## Workflow

```text
Login → Upload File → Analyze Data → Clean Data → Generate Report → Download
```

## How to Run

```bash
pip install django pandas openpyxl
python manage.py migrate
python manage.py runserver
```

The project uses Django's built-in authentication system and Pandas for dataset processing.
