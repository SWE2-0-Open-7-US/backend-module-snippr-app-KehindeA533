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
