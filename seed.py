from app import app, connection

cursor = connection.cursor()
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

# Define an SQL statement to insert data
INSERT_USER_DATA = 'INSERT INTO "user" (email, password) VALUES (%s, %s) RETURNING id;'

# Define an SQL statement to insert data
INSERT_SNIPPET_DATA = (
    "INSERT INTO snippet (language, code, snippet_id) VALUES (%s, %s, %s);"
)

# Data to insert
data_to_insert = [
    {"id": 1, "language": "Python", "code": "print('Hello, World!')"},
    {"id": 2, "language": "Python", "code": "def add(a, b):\n    return a + b"},
    {
        "id": 3,
        "language": "Python",
        "code": "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    def area(self):\n        return 3.14 * self.radius ** 2",
    },
    {"id": 4, "language": "JavaScript", "code": "console.log('Hello, World!');"},
    {
        "id": 5,
        "language": "JavaScript",
        "code": "function multiply(a, b) {\n    return a * b;\n}",
    },
    {"id": 6, "language": "JavaScript", "code": "const square = num => num * num;"},
    {
        "id": 7,
        "language": "Java",
        "code": 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
    },
    {
        "id": 8,
        "language": "Java",
        "code": "public class Rectangle {\n    private int width;\n    private int height;\n\n    public Rectangle(int width, int height) {\n        this.width = width;\n        this.height = height;\n    }\n\n    public int getArea() {\n        return width * height;\n    }\n}",
    },
]

# Create User
cursor.execute(CREATE_USER)
cursor.execute(INSERT_USER_DATA, ("kade@gmail.com", "1234"))
user_id = cursor.fetchone()[0]  # Get the ID of the newly inserted user

# Create Snippet
cursor.execute(CREATE_SNIPPET)

# Loop through the data and execute the INSERT statement
for data in data_to_insert:
    # Use the user_id for each snippet
    values = (data["language"], data["code"], user_id)
    cursor.execute(INSERT_SNIPPET_DATA, values)

# Commit the changes to the database
connection.commit()

# Close the cursor and the database connection
cursor.close()
connection.close()
