## Setup

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

- Apply database migrations (first time only):
```
make exec/web
manage migrate
exit 
# Restart the stack
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

For active development with hot reloading:

1. Bring the stack up (ensure `DEBUG` is `True` in `app.ini`)
```
make up/local
# Volume mounts in `docker-compose-local.yml` ensure web and celery containers reflect code changes in real time
```

2. In a separate terminal, navigate to the client directory and start the React dev server
```
cd app/client
npm install  # first time only
npm run dev
```

3. Access the app at `http://localhost:8000` (Django URL)
Django server proxies frontend requests (when `DEBUG` is set) to the Vite dev server running on port 5173, enabling local dev without CORS/CSRF issues
