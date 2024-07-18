FROM python:3.10


ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip
RUN pip install gunicorn

RUN pip install -r requirements.txt

COPY ./weather /app/
RUN python manage.py collectstatic --no-input
CMD ["gunicorn", "weather.wsgi:application", "--bind", "0:8000" ]