# Student Manager

A comprehensive personal student management system built with Django.

## Features

- **Dashboard** - Smart overview with today's schedule, tasks, exams, and stats
- **Semesters** - Manage academic semesters with progress tracking
- **Subjects** - Track courses with grades, attendance, and notes
- **Schedule** - Full weekly schedule with conflict detection
- **Tasks** - Task management with priorities, deadlines, and workload tracking
- **Grades** - Grade tracking with weighted averages and GPA calculation
- **Attendance** - Attendance monitoring with per-subject statistics
- **Exams** - Exam management with countdown timers
- **Calendar** - Unified calendar for classes, tasks, exams, and events
- **Notes** - Note-taking with search, tags, and subject filtering
- **Goals** - Semester goals with progress tracking
- **Focus Mode** - Pomodoro timer for productive study sessions
- **Notifications** - Smart notifications for deadlines and exams
- **Statistics** - Academic analytics and insights
- **Dark Mode** - Full dark theme support
- **Responsive** - Works on desktop, tablet, and mobile
- **i18n** - English and Russian language support

## Tech Stack

- Python 3.12+
- Django 5.x
- SQLite
- Django Templates + HTMX
- CSS3 with CSS Variables
- JavaScript (minimal)

## Quick Start

### 1. Clone and setup

```bash
cd student_manager
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set:
- `SECRET_KEY` - Generate a random secret key
- `DEBUG` - Set to `True` for development

### 3. Initialize database

```bash
python manage.py migrate
```

### 4. Create demo data (optional)

```bash
python manage.py seed_demo
```

Demo credentials: `demo` / `demo1234`

### 5. Run development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Project Structure

```
student_manager/
├── config/              # Django configuration
│   ├── settings/        # Settings module
│   ├── urls.py          # Root URLs
│   ├── wsgi.py
│   └── asgi.py
├── apps/                # Django applications
│   ├── accounts/        # User auth & profiles
│   ├── dashboard/       # Main dashboard
│   ├── semesters/       # Semester management
│   ├── subjects/        # Subject management
│   ├── schedule/        # Weekly schedule
│   ├── tasks/           # Task management
│   ├── grades/          # Grade tracking
│   ├── attendance/      # Attendance tracking
│   ├── exams/           # Exam management
│   ├── calendar/        # Unified calendar
│   ├── notes/           # Note-taking
│   ├── goals/           # Goal tracking
│   ├── productivity/    # Pomodoro/Focus mode
│   ├── notifications/   # Notification system
│   └── core/            # Shared utilities
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # User uploads
├── tests/               # Test suite
├── manage.py
├── requirements.txt
└── README.md
```

## Management Commands

```bash
# Create demo data
python manage.py seed_demo

# Clear demo data
python manage.py clear_demo
```

## Features Detail

### Grade Calculation
Supports multiple grading systems:
- Percentage (0-100)
- 5-Point scale
- 10-Point scale
- GPA 4.0

### Schedule Conflict Detection
Automatically detects when classes overlap and prevents double-booking.

### Task Workload
Tracks estimated time for tasks and shows daily/weekly workload.

### Focus Mode
Pomodoro timer with customizable durations and session tracking.

## Testing

```bash
pytest
```

## Production Deployment

```bash
# Set environment variables
export DEBUG=False
export SECRET_KEY=your-secure-secret-key
export ALLOWED_HOSTS=yourdomain.com

# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn config.wsgi:application
```

## License

MIT License
