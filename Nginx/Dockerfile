FROM python:3.12-alpine
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
ENV FLASK_APP=app.py
CMD ["gunicorn", "app:app", "--bind", "8080"]