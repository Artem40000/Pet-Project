FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /All_Know_In-Project
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:8000