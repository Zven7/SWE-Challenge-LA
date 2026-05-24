# LATAM SWE Challenge

FastAPI user management API with MongoDB and CRUD operations.

## Features

- Create, read, update, delete users
- Input validation with Pydantic
- MongoDB data storage using Beanie and Motor
- OpenAPI documentation via FastAPI
- Request logging middleware
- Basic error handling

## Environment

This project loads environment variables from `.env` via `pydantic-settings`.

Create a `.env` file or use one of the environment-specific files below:

```env
MONGODB_URL=mongodb://mongo:27017
MONGODB_DB_NAME=users_db
API_V1_STR=/api/v1
DEBUG=true
```

Available settings:

- `MONGODB_URL` — MongoDB connection URL
- `MONGODB_DB_NAME` — Database name
- `API_V1_STR` — API version prefix
- `DEBUG` — Enable debug mode when running locally

The repository includes these Compose environment files:

- `.env` — default development settings
- `.env.development` — explicit development settings
- `.env.production` — explicit production settings

## Run locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker

The `Dockerfile` uses a multi-stage build with Python 3.12 slim and installs dependencies into an isolated virtual environment under `/app/.venv`.

Build and run with Docker:

```bash
docker build -t swe-api .
```

```bash
docker run --rm -p 8000:8000 swe-api
```

Build and run with Docker Compose:

```bash
docker compose up --build
```

By default, `docker compose` uses the `.env` file in the repository, which is configured for development.

To run a specific environment file explicitly:

```bash
docker compose --env-file .env.development up --build
```

```bash
docker compose --env-file .env.production up --build
```

Then open:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Docker Compose configuration

The `docker-compose.yml` file defines two services:

- `api`
  - builds the local application image from `.`
  - maps port `8000` on the host to `8000` in the container
  - runs `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
  - mounts the workspace into `/app` for live code reload
  - mounts `/app/.venv` to preserve the virtual environment across container restarts
  - depends on the `mongo` service

- `mongo`
  - uses `mongo:7`
  - exposes port `27017`
  - persists data in the `mongo_data` named volume

Compose service environment defaults:

- `MONGODB_URL=mongodb://mongo:27017`
- `MONGODB_DB_NAME=users_db`
- `API_V1_STR=/api/v1`
- `DEBUG=true`

## API Usage Examples

### Create user

```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane_doe",
    "email": "jane.doe@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "user",
    "active": true
  }'
```

### List users

```bash
curl "http://localhost:8000/api/v1/users?limit=10&skip=0&role=admin&active=true"
```

### Get user by ID

```bash
curl http://localhost:8000/api/v1/users/<user_id>
```

### Update user

```bash
curl -X PUT http://localhost:8000/api/v1/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "active": false
  }'
```

### Delete user

```bash
curl -X DELETE http://localhost:8000/api/v1/users/<user_id>
```

## Edge cases covered

- Duplicate username or email returns `409 Conflict`
- Invalid object IDs return `404 Not Found`
- Invalid request payloads return `422 Unprocessable Entity`
- Missing user returns `404 Not Found`

## Testing

```bash
pytest -q
```

## API documentation

FastAPI automatically serves OpenAPI docs for this API at:

- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — ReDoc

Use these endpoints to explore request schemas, responses, and payload examples.
