# Outcome Based Education (OBE) Management System

A small, runnable academic demonstration project built with Python, Flask, SQLite, HTML and CSS. It demonstrates a basic workflow for recording course outcomes and student assessment marks, then viewing a simplified attainment summary.

> **Project status:** MVP / learning prototype. It is not a complete or production-ready college OBE platform.

## Features included in this version

- Dashboard showing course, student and course-outcome counts
- Add courses
- Add Course Outcomes (COs) with a configurable target percentage
- Add fictional student records
- Record or update marks for a student against a CO
- Calculate and display a simplified CO attainment percentage
- View student and marks registers
- Responsive layout for desktop and mobile browsers
- SQLite database created locally on first run

## Technology

- Python 3.10+
- Flask
- SQLite
- HTML and CSS
- Jinja templates

## Requirements

- Windows, macOS or Linux
- Python 3.10 or newer
- Visual Studio Code (recommended) or another code editor

## Run on Windows using VS Code

1. Download and extract this project ZIP.
2. Open the extracted `obe-system-final` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this in the same terminal, then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

6. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

7. Start the application:

   ```powershell
   py app.py
   ```

8. Open `http://127.0.0.1:5000` in your browser.
9. Stop the development server with `Ctrl + C`.

### macOS / Linux

Use `python3 -m venv .venv`, activate with `source .venv/bin/activate`, install using `python -m pip install -r requirements.txt`, and run using `python app.py`.

## Try the application

- The first run creates a local `obe.db` SQLite database and inserts fictional demonstration records.
- Open the dashboard to view the sample course, students, COs and attainment.
- Use the dashboard forms to add a course, CO or student.
- Open **Records** to record or update marks.
- Return to the dashboard to see the attainment summary update.

The sample names and marks are fictional and must not be replaced with real student data in a public demo repository.

## Attainment calculation used in this prototype

For each CO:

1. Each recorded score is converted to a percentage: `(score / maximum score) × 100`.
2. A student is counted as meeting the CO target when their percentage is greater than or equal to that CO's configured target.
3. Attainment is calculated as `(number of students meeting target / number of students with recorded marks) × 100`.

This is a simplified illustrative method only. OBE policies vary by institution. Official reporting may require direct and indirect assessment, assessment-component weights, CO-PO / CO-PSO mapping, attainment levels and institution-approved thresholds. Confirm your college's methodology before using or describing this as an official calculation.

## Security and data handling

- `.gitignore` excludes `.env` files, local SQLite databases, virtual environments and Python cache files.
- No `.env` file, real database, real student data or deployment credential is included in this repository.
- The application uses a temporary random secret key when `SECRET_KEY` is not configured. This is suitable only for local demonstration; sessions may reset when the app restarts.
- For deployment, set a strong `SECRET_KEY` in the hosting environment. Never commit the value to GitHub.
- Do not deploy this prototype with real student information. It does not yet implement authentication, authorization, audit logs or production hardening.

## Known limitations / future improvements

The following features are **not included in this version**:

- Admin, Faculty and Student login with role-based permissions
- Program Outcomes (PO) and Program Specific Outcomes (PSO) management
- CO-PO and CO-PSO mapping matrices
- Multiple assessment components and configurable institutional weighting
- Official attainment levels and institution-specific report formats
- CSV / PDF export
- Automated test suite and deployment configuration
- Production security, audit logging and privacy controls

These are future development items, not features to claim as completed.

## Suggested meaningful Git commits

Make commits after you have actually completed and checked each change. Do not create artificial commits just to increase the commit count.

```bash
git add README.md .gitignore requirements.txt
git commit -m "Add project setup and documentation"

git add app.py
git commit -m "Implement Flask app and SQLite data model"

git add templates/ static/
git commit -m "Build OBE dashboard and records pages"

# After you personally test a change:
git add .
git commit -m "Improve course outcome and marks workflow"
```

## GitHub upload

Create a new empty GitHub repository, for example `outcome-based-education-system`, then run these commands from the project folder:

```bash
git init
git add .
git commit -m "Initial working OBE prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/outcome-based-education-system.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not put passwords or access tokens in source files or command history.

## Academic project note

Before presenting this as a completed final-year project, extend it with the missing modules, test the full workflow, add diagrams and screenshots, and document the exact methodology approved by your institution. Be prepared to explain the code you submit.
