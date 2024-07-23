FROM        --platform=$BUILDPLATFORM python:3.12-bullseye

LABEL       author="CCFV" maintainer="Livecampus EAN/EDL P2024"
LABEL       org.opencontainers.image.source="https://github.com/CharlyRousseau/snippet"
LABEL       org.opencontainers.image.licenses="CC BY-NC-ND 4.0"

RUN         apt-get update \
            && apt-get install -y ca-certificates curl ffmpeg g++ gcc git openssl sqlite3 tar tzdata \
            && useradd -ms /bin/bash container

USER        container
ENV         USER=container HOME=/home/container
WORKDIR     /home/container

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /home/container/
RUN pip install -r requirements.txt && python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "snippet_project.wsgi:application"]
