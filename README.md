# Django React Template

A production-ready web application template with **all batteries included** for modern full-stack development.

- **Backend**: Django with Django REST Framework
- **Frontend**: React + TypeScript + Vite + Material UI
- **Database**: PostgreSQL  
- **Cache & Message Broker**: Redis
- **Async Tasks**: Celery + Celery Beat (scheduled tasks)
- **Package Management**: uv (Python) + npm (Node.js)
- **Dockerized Setup**: Complete development environment with hot reloading

## Prerequisites
- Docker (>= 24.0.0)
- Node.js (>= 18.0.0) for local development
- uv will be installed automatically by `make setup/local`

## Setup

- Set up local dev environment (installs uv, and python/node dependencies):
```
make setup/local
```

- Update `APP_NAME` in `stacks/.env` and create `stacks/secrets/app.ini` with the following entries (update `SECRET_KEY` and `DATABASE_URL`)
```
SECRET_KEY="..."
DEBUG=True
ALLOWED_HOSTS=localhost
DATABASE_URL=postgres://<APP_NAME>:<APP_NAME>@postgres:5432/<APP_NAME>
REDIS_URL=redis://redis:6379
```

- Build the Docker image (requires Docker >24.0.0):
```
make build
```

- Bring the stack up
```
make up/local
```

- Apply database migrations (first time after build):
```
make exec/web
manage migrate
exit
```

- Bring the stack down
```
make down/local
```

- Exec into a container
```
make exec/<container_name> (e.g. web, celery)
```

- Check container logs
```
make logs/<container_name> (e.g. web, celery)
```

## Running React Dev Server Locally

For active frontend development with hot reloading:

1. Bring the stack up (ensure `DEBUG` is `True` in `app.ini`)
```
make up/local
# Code mounts ensures hot reloading for web and celery containers
```

2. In a separate terminal, start the React dev server
```
cd app/client
npm run dev
```

3. Access the app at `http://localhost:8000` (Django URL)
Django server proxies frontend requests (when `DEBUG` is set) to the Vite dev server running on port 5173, enabling local dev without CORS/CSRF issues
