FROM python:3.9-alpine
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
ENV FLASK_APP=app.py
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]