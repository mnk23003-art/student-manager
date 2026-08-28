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




### Schedule Conflict Detection
Automatically detects when classes overlap and prevents double-booking.

### Task Workload
Tracks estimated time for tasks and shows daily/weekly workload.

### Focus Mode
Pomodoro timer with customizable durations and session tracking.


