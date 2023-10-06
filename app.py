from flask import Flask, request, jsonify
import os
import psycopg2

from dotenv import load_dotenv

## Load Environment Variables
load_dotenv()
password = os.getenv("DATABASE_PASSWORD")

# Initialize Flask app
app = Flask(__name__)

# Establish a database connection
connection = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password=password,
)

# Define SQL queries
# CREATE
CREATE_USER = """CREATE TABLE IF NOT EXISTS user (
    id SERIAL PRIMARY KEY,
    email TEXT,
    password TEXT
);"""

CREATE_SNIPPET = """cREATE TABLE IF NOT EXISTS snippet (
    id SERIAL PRIMARY KEY,
    language TEXT,
    code TEXT,
    snippet_id INT
    FOREIGN KEY(snippEt_id) REFERENCES user(id) ON DELETE CASCADE
);"""


#
# Endpoints
# - Create a new snippet
# - Get all the snippets
# - Get a specific snippets

# - Bonus: Users can make a GET request to e.g. /snippet?lang=python to retrieve all the Python snippets
