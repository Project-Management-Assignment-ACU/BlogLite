# Simple Blog

A lightweight blogging platform built with Django, designed for simplicity and ease of use.

## Features

- Clean, responsive design using Bootstrap 5
- Simple post management with CRUD operations
- User authentication and authorization
- Contact form with email notifications
- Full-text search for blog posts
- Pagination for blog posts list

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Project-Management-Assignment-ACU/BlogLite.git
   cd BlogLite
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Load demo data (optional):
   ```bash
   python manage.py loaddata blog/fixtures/demo.json
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. Visit the following URLs in your browser:
   - Main site: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

- `blog/`: Blog application with models, views, and forms
- `core/`: Core functionality and settings
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)
- `media/`: User-uploaded files
- `docs/`: Project documentation

## Development Workflow

1. Create feature branches for new features or bug fixes
2. Write tests for new functionality
3. Submit pull requests for review
4. Follow the project's coding style and conventions

## License

This project is licensed under the MIT License - see the LICENSE file for details.
