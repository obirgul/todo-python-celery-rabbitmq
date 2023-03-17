FROM python:3.9.7-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ARG GIT_COMMIT_ID
ENV GIT_COMMIT_ID=${GIT_COMMIT_ID}
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD gunicorn -c gunicorn_config.py main:app -k uvicorn.workers.UvicornH11Worker --preload --access-logfile - --error-logfile -

# docker build --platform=linux/amd64 --tag hammer-bid:latest --build-arg GIT_COMMIT_ID=1a2b3c .
# docker run --platform=linux/amd64 --publish 1234:1234 --name hammer-bid hammer-bid:latest
