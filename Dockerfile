FROM python:3.12.0-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Command to run the Django app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "snippet_project.wsgi:application"]
