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
CREATE_USER = """CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email TEXT,
    password TEXT
);"""

CREATE_SNIPPET = """CREATE TABLE IF NOT EXISTS snippet (
    id SERIAL PRIMARY KEY,
    language TEXT,
    code TEXT,
    snippet_id INT,
    FOREIGN KEY(snippet_id) REFERENCES "user"(id) ON DELETE CASCADE
);"""

# Put
# Define an SQL statement to insert data
INSERT_USER_DATA = 'INSERT INTO "user" (email, password) VALUES (%s, %s) RETURNING id;'

# Define an SQL statement to insert data
INSERT_SNIPPET_DATA = (
    "INSERT INTO snippet (language, code, snippet_id) VALUES (%s, %s, %s);"
)

GET_ALL_SNIPPETS = "SELECT * FROM snippet;"
GET_A_SNIPPETS = "SELECT * FROM snippet WHERE id = %s;"
GET_SNIPPETS_BY_LANG = "SELECT * FROM snippet WHERE language = %s"


# Endpoints
# - Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        with connection:
            with connection.cursor as cursor:
                cursor.execute(INSERT_USER_DATA, (email, password))
                user_id = cursor.fetchone()[0]
                connection.commit()

                return (
                    jsonify(
                        {"message": "User created successfully", "user_id": user_id}
                    ),
                    201,
                )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# - Create a new snippet
@app.route("/users/<int:user_id>/snippets", methods=["POST"])
def add_snippet(user_id):
    try:
        data = request.get_json()
        language = data["language"]
        code = data["code"]
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_SNIPPET_DATA, (language, code, user_id))
                connection.commit()

        return (
            jsonify(
                {"message": "User's snippet created successfully", "user_id": user_id}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# - Get all the snippets
@app.route("/users/snippets", methods=["GET"])
def get_all_snippets():
    try:
        with connection:
            with connection.cursor() as cursor:
                # Execute a SQL query to fetch all snippets
                cursor.execute(GET_ALL_SNIPPETS)
                snippets = cursor.fetchall()

        # Convert the snippet data to a list of dictionaries
        snippet_list = []
        for snippet in snippets:
            snippet_dict = {
                "id": snippet[0],
                "language": snippet[1],
                "code": snippet[2],
            }
            snippet_list.append(snippet_dict)

        return jsonify(snippet_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# - Get a specific snippets
@app.route("/users/<int:user_id>/snippets", methods=["GET"])
def get_a_snippet(user_id):
    try:
        with connection:
            with connection.cursor() as cursor:
                # Execute a SQL query to fetch an individual snippet by ID
                cursor.execute(GET_A_SNIPPETS, (user_id,))
                snippet = cursor.fetchone()

        if not snippet:
            return jsonify({"message": "Snippet not found"}), 404

        snippet_dict = {
            "id": snippet[0],
            "language": snippet[1],
            "code": snippet[2],
        }

        return jsonify(snippet_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# - Bonus: Users can make a GET request to e.g. /snippet?lang=python to retrieve all the Python snippets
@app.route("/users/snippets/<string:language>", methods=["GET"])
def get_snippets_by_language(language):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(GET_SNIPPETS_BY_LANG, (language,))
                snippets = cursor.fetchall()

            snippet_list = []
            for snippet in snippets:
                snippet_dict = {
                    "id": snippet[0],
                    "language": snippet[1],
                    "code": snippet[2],
                }
                snippet_list.append(snippet_dict)

            return jsonify(snippet_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
