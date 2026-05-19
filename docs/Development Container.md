### Development Container

### Context
Services are top-level functionalities of this container

#### API
The current API uses FastAPI to allows the front-end side to access back-end services, like accessing database, using back-end calculations, etc.

#### Development Container
The current development is done within Docker container with all depenedencies inside the containers. (No dependencies available outside of container)


#### Synchronization between container and host
> During CI/Production, the local host (developer) need the container (Docker) to update its image and dependencies.

##### Synchronization  on build
`Dockerfile` is executed when Docker is asked to build an image. This triggers an copy from the host `src` file to the containers `/app/src`.


Futher synchronization is triggered through the `watch:` and also the port of current environment is linked to the port of the container (allowing for database access)

```
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app/src"]
```

```{yml}
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: wowberg-api
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: requirements.txt
        - action: rebuild
          path: Dockerfile
    ports:
      - "8000:8000"
    environment:
      APP_ENV: development
      DB_HOST: db
      DB_PORT: "5432"
      DB_NAME: wowberg
      DB_USER: wowberg
      DB_PASSWORD: wowberg
    depends_on:
      - db

  db:
    image: timescale/timescaledb:latest-pg16
    container_name: wowberg-db
    environment:
      POSTGRES_DB: wowberg
      POSTGRES_USER: wowberg
      POSTGRES_PASSWORD: wowberg
    ports:
      - "5432:5432"
    volumes:
      - wowberg-db-data:/var/lib/postgresql/data

volumes:
  wowberg-db-data:
````
