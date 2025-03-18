from app import create_app
from modules.sqlite import *
import os

app = create_app()

if __name__ == '__main__':
    # Ensure the output directory exists
    if not os.path.exists("output"):
        os.makedirs("output")

    # Ensure the database exists
    if not os.path.exists("output/midnight.db"):
        createDB()
        con = connectDB()
        createTables(con)

    # Start the Flask app
    app.run(debug=True)