# Advance Weather Project - FastAPI Backend

This is the backend API for the Advance Weather Project. It is built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT authentication, and Docker.

The API supports user authentication, weather search, saved cities, admin user management, activity tracking, and analytics.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn
- Docker and Docker Compose

## Project Structure

```text
app/
  api/V1/
    dependencies/     Auth, database, and RBAC dependencies
    routes/           Weather, saved cities, admin, and analytics routes
  core/               Config, security, middleware, response, and exceptions
  db/                 Database session, base metadata, and seed data
  models/             SQLAlchemy database models
  schemas/            Pydantic request and response schemas
  services/           Business logic
alembic/
  versions/           Database migration files
  env.py              Alembic migration environment
alembic.ini           Alembic configuration
docker-compose.yml    App and PostgreSQL services
Dockerfile            Backend container image
requirements.txt      Python dependencies
```

## Main API Routes

- `GET /` - Health/root endpoint
- `POST /auth/register` - Register a user
- `POST /auth/login` - Login and receive a bearer token
- `GET /weather/search` - Search weather data
- `POST /saved-cities/` - Save a city
- `GET /saved-cities/` - List saved cities
- `DELETE /saved-cities/{saved_city_id}` - Delete a saved city
- `GET /analytics/activities` - View activity analytics
- `GET /analytics/top-cities` - View top searched/saved cities
- `GET /admin/users` - Admin user list
- `POST /admin/users` - Admin create user
- `DELETE /admin/users/{user_id}` - Admin delete user

FastAPI also provides interactive API docs after the server starts:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/weather_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
WEATHER_API_KEY=your-weather-api-key
```

For local development without Docker, use `localhost` instead of `db` in `DATABASE_URL`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/weather_db
```

Important: the FastAPI app reads the database URL from `.env`, but Alembic reads it from `alembic.ini`.

For Docker, this value is already configured in `alembic.ini`:

```ini
sqlalchemy.url = postgresql://postgres:postgres@db:5432/weather_db
```

For local development, change it to:

```ini
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/weather_db
```

## Run With Docker

This is the easiest way to run the project because Docker Compose starts both the FastAPI app and PostgreSQL database.

```bash
docker compose up --build
```

The backend will be available at:

```text
http://localhost:8000
```

The Docker command in this project runs database migrations before starting the API:

```bash
alembic upgrade head
```

To stop the containers:

```bash
docker compose down
```

To stop the containers and remove the database volume:

```bash
docker compose down -v
```

## Run Locally Without Docker

Install PostgreSQL first and create a database named `weather_db`.

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Update `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/weather_db
```

Update `alembic.ini`:

```ini
sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/weather_db
```

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:

```text
http://localhost:8000/docs
```

## Database Migrations

Alembic is used to manage database schema changes.

Apply all migrations:

```bash
alembic upgrade head
```

Create a new migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

Rollback the last migration:

```bash
alembic downgrade -1
```

View migration history:

```bash
alembic history
```

View the current database revision:

```bash
alembic current
```

## Seed Users

The seed file is located at:

```text
app/db/seed.py
```

It creates default users with these roles:

- `ADMIN`
- `ANALYST`
- `USER`

Default password:

```text
123456
```

To run the seed function manually:

```bash
python -c "from app.db.seed import run_seed; run_seed()"
```

If you are running inside Docker:

```bash
docker exec -it weather_app python -c "from app.db.seed import run_seed; run_seed()"
```

## Authentication

Login returns a bearer token. Use this token for protected endpoints:

```http
Authorization: Bearer your_access_token
```

Some routes require specific roles, such as admin or analyst permissions.

## Useful Docker Commands

Run containers:

```bash
docker compose up --build
```

Run containers in the background:

```bash
docker compose up -d --build
```

View app logs:

```bash
docker logs -f weather_app
```

Open a shell inside the app container:

```bash
docker exec -it weather_app sh
```

Run migrations inside the app container:

```bash
docker exec -it weather_app alembic upgrade head
```

## Notes

- PostgreSQL runs in Docker as the `db` service.
- The app container uses `db` as the database hostname.
- Local development should use `localhost` as the database hostname.
- Always run Alembic migrations after changing database models.
- Keep `.env` private and do not commit real secrets or API keys.
