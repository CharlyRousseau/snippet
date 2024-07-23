FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "snippet_project.wsgi:application"]
