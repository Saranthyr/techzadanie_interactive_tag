FROM python:3.12.1-slim-bullseye
WORKDIR migr
COPY db ./db
COPY migrations ./migrations
COPY alembic.ini .
RUN pip install --no-cache-dir --upgrade -r db/requirements.txt