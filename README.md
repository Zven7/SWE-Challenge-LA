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


## API Usage Examples

The API is exposed under the versioned prefix `/api/v1`.

### GET /api/v1/users

Fetch paginated users, optionally filtered by role and active status.

Query parameters:

- `limit` — number of users returned (default `10`, maximum `100`)
- `skip` — number of users to skip for paging (default `0`)
- `role` — filter users by role, e.g. `admin` or `user`
- `active` — filter users by active status, `true` or `false`

Examples:

```bash
curl "http://localhost:8000/api/v1/users?limit=10&skip=0"
```

```bash
curl "http://localhost:8000/api/v1/users?role=admin&active=true"
```

### POST /api/v1/users

Create a new user.

Required payload:

```json
{
  "username": "jane_doe",
  "email": "jane.doe@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "role": "user",
  "active": true
}
```

Example:

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

### GET /api/v1/users/{user_id}

Retrieve a single user by ID.

Example:

```bash
curl http://localhost:8000/api/v1/users/<user_id>
```

### PUT /api/v1/users/{user_id}

Update existing user fields.

Example payload:

```json
{
  "first_name": "Jane",
  "active": false
}
```

Example:

```bash
curl -X PUT http://localhost:8000/api/v1/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "active": false
  }'
```

### DELETE /api/v1/users/{user_id}

Delete a user by ID.

Example:

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
