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

Create a `.env` file or use the example below:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=users_db
API_V1_STR=/api/v1
```

## Run locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

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
