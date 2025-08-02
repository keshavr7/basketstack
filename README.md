## Dev Setup

- Create `stacks/secrets/app.ini` with the following entries, and update `SECRET_KEY` and `DATABASE_URL`
```
SECRET_KEY="..."
DEBUG=True
ALLOWED_HOSTS=localhost
DATABASE_URL=postgres://$APP_NAME:$APP_NAME@postgres:5432/$APP_NAME
REDIS_URL=redis://redis:6379
```

- Build the Docker image (requires Docker >24.0.0):
```
make build
```

- Bring up the stack:
```
make up/local
```

- Run database migrations (first time only):
```
make exec/web
python manage.py migrate
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
