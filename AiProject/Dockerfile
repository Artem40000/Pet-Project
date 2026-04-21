FROM python:3.12-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /AiProject
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py runserver 0.0.0.0:8