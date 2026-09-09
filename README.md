# 🏨 Amfida Backend API

Amfida is a modern accommodation discovery and hostel management backend API built with **Django** and **Django REST Framework (DRF)**. It connects **Landlords** (property owners), **Agents** (listing managers), and **Students/Tenants** (vacancy seekers).

---

## 🌟 Key Features

- **Multi-Role User System**:
  - **Landlords**: Own and manage hostels/properties.
  - **Agents**: Publish, manage, and showcase room listings with media.
  - **Vacancy Seekers (Public Visitors)**: Browse hostels/listings, search by amenities/price, and submit reviews/reports without mandatory signup.
- **Listing & Hostel Management**:
  - Full CRUD operations with strict **Object-Level Authorization (IDOR Protection)**.
  - Media pipelines for uploading **photos** (multipart) and attaching **videos**.
  - Dynamic **amenities** assignment and filtering.
- **Search, Filtering & Pagination**:
  - Keyword search across titles, descriptions, locations, hostel names, and amenities.
  - Multi-criteria filtering by `status`, `hostel`, `area`, `price__gte`, and `price__lte`.
  - Configurable DRF Page-Number Pagination.
- **Interactive API Documentation**:
  - Full OpenAPI 3.0 specification with **Swagger UI** (`/api/docs/`) and **ReDoc** (`/api/redoc/`).
- **Security & Privacy**:
  - JWT Authentication via `djangorestframework-simplejwt`.
  - Sensitive scam reports and reporter contact info protected from public disclosure.
  - Customized Django UserAdmin preventing password hash corruption.

---

## 🛠️ Technology Stack

- **Framework**: Django 6.1, Django REST Framework 3.18
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **API Documentation**: OpenAPI 3.0 with `drf-spectacular`
- **Database**: PostgreSQL (Production & Supabase) / SQLite (Development fallback & Testing)
- **Media Storage**: Cloudflare R2 / AWS S3 (`django-storages`, `boto3`)
- **Email**: Resend (`django-anymail`)
- **Containerization**: Docker & Docker Compose

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- Pipenv or virtualenv
- PostgreSQL (optional for local SQLite development)

### 2. Environment Configuration
Clone the repository and create your `.env` file:
```bash
cp .env.example .env
```

Ensure the following baseline settings are configured:
```ini
DJANGO_ENV=development
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Local Installation (Pipenv)

```bash
# Install dependencies
pipenv install

# Apply database migrations
pipenv run python manage.py migrate

# Create a superuser
pipenv run python manage.py createsuperuser

# Start the development server
pipenv run python manage.py runserver
```

---

## 📖 API Documentation (Swagger UI)

Once the server is running, access the interactive API docs:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **ReDoc UI**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **Raw OpenAPI Schema**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## 🐳 Docker Deployment

To spin up the entire application stack (Web + PostgreSQL):

```bash
# Build and run containers
docker-compose up --build

# Run migrations inside container
docker-compose exec web python manage.py migrate
```

---

## 🧪 Running Automated Tests

Run the complete automated test suite (20 unit and API integration tests):

```bash
pipenv run python manage.py test
```

Test coverage includes:
- Role-based registration (`landlord` vs `agent`)
- User self-service (`/api/user/me/` GET and PATCH)
- Hostel and listing CRUD with IDOR authorization protection
- Listing photo upload and video attachment pipelines
- Writable amenity assignment
- Open reviews and report submission with privacy access controls
- Query search, price filters, and pagination

---

## 🔗 Core API Endpoints

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/token/` | Obtain JWT access & refresh tokens | Public |
| `POST` | `/api/token/refresh/` | Refresh JWT access token | Public |
| `POST` | `/api/user/create/` | Register as Landlord or Agent | Public |
| `GET/PATCH`| `/api/user/me/` | View/update authenticated profile | Authenticated |
| `GET` | `/api/hostels/` | List hostels (search & filter) | Public |
| `POST` | `/api/hostels/create/` | Create a hostel | Landlord |
| `GET` | `/api/listings/` | List room vacancies (search & filter) | Public |
| `POST` | `/api/listings/create/` | Create a vacancy with amenities | Agent |
| `POST` | `/api/listings/<id>/photos/` | Upload listing photo (multipart) | Agent (Owner) |
| `POST` | `/api/listings/<id>/videos/` | Attach video URL | Agent (Owner) |
| `GET/POST`| `/api/amenities/` | List / Create amenities | Public / Admin |
| `GET/POST`| `/api/review/` | List / Submit vacancy reviews | Public |
| `POST` | `/api/report/` | Submit fraud / scam report | Public |
| `GET` | `/api/report/` | List submitted reports | Admin |
| `GET` | `/api/docs/` | Interactive Swagger API Docs | Public |
