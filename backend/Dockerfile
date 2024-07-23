FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add Flask and SQLAlchemy to the requirements
RUN pip install --no-cache-dir Flask Flask-SQLAlchemy Werkzeug psycopg2-binary

CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000"]

