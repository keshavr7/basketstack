FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y netcat-traditional curl

# Install Node.js
ENV NODE_VERSION=23.9.0
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

COPY requirements.txt /code/

RUN pip install -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY ./app /code/app/

WORKDIR /code/app

# Build frontend
RUN cd client && npm install && npm run commit-to-django && rm -rf node_modules

# Collect static files
RUN python manage.py collectstatic --noinput