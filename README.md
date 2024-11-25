# Student Attendance Management System

A comprehensive system for tracking and managing student attendance, generating reports, and sending notifications. Built with Django and FastAPI.

## Features

- **Attendance Management**
- **Reporting**
- **Notifications**
- **User Management**
- **Student managemet** 
- **Class management**


## Technology Stack

- **Backend Framework:** Django 4.2
- **API Framework:** FastAPI 0.100.0
- **Database:** PostgreSQL
- **Authentication:** JWT
- **Dependency Management:** Pipenv

## Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Pipenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Viateur-akimana/School-attendance-management-system.git
cd School-attendance-management-system
```

2. Install dependencies using Pipenv:
```bash
pipenv install
```

3. Create and activate virtual environment:
```bash
pipenv shell
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Initialize the database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Start the development server:
```bash
# Start Django server
python manage.py runserver

# In a separate terminal, start FastAPI server
uvicorn api.main:app --reload
```

## Development Setup

### Database Configuration
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'attendance_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables
```plaintext
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/attendance_db
REDIS_URL=redis://localhost:6379
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## API Documentation

The API documentation is available at:
- Django Admin: `http://localhost:8000/admin/`
- FastAPI Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## Deployment

1. Set up production environment variables
2. Configure NGINX/Apache
3. Set up SSL certificates
4. Configure Gunicorn

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email akimanaviateur94@gmail.com or create an issue in the repository.
