# Django Development Environment Rules

This document defines the rules and best practices for setting up and running Django projects for **Kilocode**. Following these ensures consistency, security, and efficient development workflow.

## Guidelines

### 1. Virtual Environment
- Activate the environment before installing any dependencies or running any python manage.py related function:

```bash
# Linux/macOS
source tbuenv/bin/activate

```

- Never install packages globally; keep all dependencies project-specific.

### 2. Dependencies
- Maintain a `requirements.txt` file for all dependencies:

```bash
pip freeze > requirements.txt
```

- Install dependencies using:

```bash
pip install -r requirements.txt
```

- Update dependencies carefully to avoid breaking changes.

### 3. Database Setup
- Run migrations after setting up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

- Use the Django shell for database queries when needed:

```bash
python manage.py shell
```




### 4. Running the Development Server
- Run the server inside the virtual environment:

```bash
python manage.py runserver
```


### 5. Static & Media Files
- Collect static files only when needed:

```bash
python manage.py collectstatic
```

- Keep separate directories for media uploads during development to avoid conflicts.

### 6. Git & Version Control
- Use a `.gitignore` file to exclude unnecessary or sensitive files:
Every time you complete a task prompt me whether you should do git processes i.e git add, git commit, and git push. You will then give me three options, "Yes, do git add, commit, and push",
"No, skip git processes for now", "Not yet, let me do something else and prompt me again"

When I confirm do all those processes. Use the task request and conversation to deliver the git commit message


- Commit meaningful code only; avoid committing secrets or environment files.

### 7. Coding & Project Standards
- Follow PEP8 coding style guidelines.
- Keep code modular and reusable.
- Document important functionality, environment setup, and steps for new developers.
- Use meaningful commit messages and branch names.

### 8. Testing & Debugging
- Write tests for new features using Django’s pytest framework.


```bash
Use pytest for all testing
```

