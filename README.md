# Dev Portal Backend

A comprehensive Django REST API backend for managing developers, their skills, projects, and AI-powered project analysis. This system provides intelligent developer matching and skill level tracking based on project experience.

## 🚀 Features

- **Developer Management**: Complete CRUD operations for developer profiles
- **Skill Tracking**: Hierarchical skill areas and individual skills management
- **Project Management**: Developer project tracking with skill associations
- **AI Integration**: Gemini-powered project analysis and developer recommendations
- **Skill Level System**: Automatic skill level calculation based on project experience
- **JWT Authentication**: Secure API access with token-based authentication
- **RESTful API**: Well-structured API endpoints with pagination support

## 🛠️ Tech Stack

- **Framework**: Django 5.2.6
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (Simple JWT)
- **AI Integration**: Google Gemini API
- **CORS**: django-cors-headers
- **Environment**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Backend_new
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   pip install djangorestframework
   pip install djangorestframework-simplejwt
   pip install django-cors-headers
   pip install psycopg2-binary
   pip install python-dotenv
   pip install google-generativeai
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   ENVIRONMENT=Development
   DB_NAME=dev_portal_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Initialize Skill Levels** (for existing data)
   ```bash
   python manage.py init_skill_levels
   ```

7. **Create Superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication
The API uses JWT authentication. Include the token in your requests:
```
Authorization: Bearer <your_jwt_token>
```

### Main Endpoints

#### Developers
- `GET /api/developers/` - List all developers
- `POST /api/developers/` - Create a new developer
- `GET /api/developers/{id}/` - Get developer details with skills and projects
- `PUT /api/developers/{id}/` - Update developer
- `POST /api/developers/add_dev_skills/` - Add skills to developer

#### Skill Areas
- `GET /api/skill-areas/` - List skill areas
- `POST /api/skill-areas/` - Create skill area
- `GET /api/skill-areas/{id}/` - Get skill area with skills
- `POST /api/skill-areas/add_skills/` - Add skills to skill area

#### Developer Projects
- `GET /api/developer-projects/` - List developer projects
- `POST /api/developer-projects/` - Create developer project
- `GET /api/developer-projects/{id}/` - Get project details
- `PUT /api/developer-projects/{id}/` - Update project

#### Project Categories
- `GET /api/projects/` - List project categories
- `POST /api/projects/` - Create project category
- `GET /api/projects/{id}/` - Get category details
- `POST /api/projects/add_required_skills/` - Add required skills to category

#### AI Agent
- `POST /api/agent/query/` - Simple AI query
- `POST /api/agent/analyze-project/` - Analyze project and suggest developers

For detailed API documentation, see [API_Integration_Guide.md](API_Integration_Guide.md)

## 🎯 Skill Level System

The system automatically tracks developer skill levels based on project experience:

- **Level 0 - Basic Knowledge**: No projects completed
- **Level 1 - Beginner**: 1 project completed
- **Level 2 - Advanced**: 2-3 projects completed  
- **Level 3 - Expert**: 4+ projects completed

For detailed information, see [SKILL_LEVEL_SYSTEM.md](SKILL_LEVEL_SYSTEM.md)

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run specific test cases:
```bash
python manage.py test developers.tests.SkillLevelTestCase
```

## 📁 Project Structure

```
Backend_new/
├── agent/                 # AI agent functionality
├── developers/           # Developer management app
├── projects/             # Project categories app
├── dev_portal/          # Main Django project settings
├── manage.py            # Django management script
├── API_Integration_Guide.md
├── SKILL_LEVEL_SYSTEM.md
└── Dev Portal.postman_collection.json
```

## 🔐 Security Features

- JWT token authentication with rotation
- CORS configuration for frontend integration
- Environment-based configuration
- Input validation and sanitization
- Secure database connections

## 🚀 Deployment

### Production Environment Variables
```env
SECRET_KEY=your-production-secret-key
ENVIRONMENT=Production
DB_NAME=production_db_name
DB_USER=production_db_user
DB_PASSWORD=production_db_password
DB_HOST=your-production-db-host
DB_PORT=5432
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
GEMINI_API_KEY=your-production-gemini-key
```

### Production Commands
```bash
python manage.py collectstatic
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the API documentation in `API_Integration_Guide.md`
- Review the skill level system in `SKILL_LEVEL_SYSTEM.md`
- Use the provided Postman collection for API testing

## 🔄 API Response Format

All API responses follow this consistent format:
```json
{
  "details": "Success/Error message",
  "data": {},
  "pagination": {
    "count": 25,
    "next": "http://example.com/api/endpoint/?page=3",
    "previous": "http://example.com/api/endpoint/?page=1",
    "current_page": 2,
    "page_size": 10
  }
}
```

## 📊 Key Features

- **Pagination**: All list endpoints support pagination (10 items per page)
- **Filtering**: Developer projects can be filtered by developer name
- **File Upload**: AI agent accepts PDF/DOCX files for project analysis
- **Automatic Updates**: Skill levels update automatically when projects change
- **Comprehensive Testing**: Full test coverage for core functionality

---

Built with ❤️ using Django and Django REST Framework
