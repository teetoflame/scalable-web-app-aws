import os
from flask import Flask
import pymysql

app = Flask(__name__)

# RDS Configuration from Environment Variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Database Connection
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT content FROM messages")
            result = cursor.fetchall()
            messages = [row["content"] for row in result]
            return "<br>".join(messages)
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
