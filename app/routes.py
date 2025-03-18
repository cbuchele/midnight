from flask import Blueprint, render_template, request, jsonify, Response, stream_with_context
import subprocess
import threading
from tor_proxy import TorProxy

import sqlite3
from sqlite3 import Error

def connectDB():
    """Connect to the SQLite database."""
    try:
        # Connect to the database (or create it if it doesn't exist)
        con = sqlite3.connect("output/midnight.db")
        print("Connected to SQLite database")
        return con
    except Error as e:
        print(f"Error connecting to SQLite database: {e}")
        return None
    

def createDB():
    """Create the SQLite database if it doesn't exist."""
    try:
        con = sqlite3.connect("output/midnight.db")
        print("Database created successfully")
        con.close()
    except Error as e:
        print(f"Error creating database: {e}")

def createTables(con):
    """Create tables in the SQLite database."""
    try:
        cursor = con.cursor()

        # Example table creation query
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deep_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                url_dir TEXT NOT NULL,
                html TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deep_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_url TEXT NOT NULL,
                source_dir TEXT NOT NULL,
                target_url TEXT NOT NULL,
                target_dir TEXT NOT NULL
            )
        """)

        con.commit()
        print("Tables created successfully")
    except Error as e:
        print(f"Error creating tables: {e}")


# Ensure the Blueprint is named 'main'
main_bp = Blueprint('main', __name__)

# Global variables
scan_status = "idle"
tor_proxy = TorProxy()  # Initialize Tor proxy settings

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/start_scan', methods=['POST'])
def start_scan():
    global scan_status
    if scan_status == "idle":
        scan_status = "running"
        threading.Thread(target=run_midnight_scan, args=(tor_proxy.get_proxy(),)).start()
        return jsonify({"status": "Scan started!"})
    else:
        return jsonify({"status": "Scan is already running!"})

@main_bp.route('/scan_status', methods=['GET'])
def get_scan_status():
    global scan_status
    return jsonify({"status": scan_status})

@main_bp.route('/search', methods=['POST'])
def search():
    term = request.form['search_term']
    con = connectDB()
    if con:
        results = searchFTS(term, con)
        con.close()
        return render_template('results.html', results=results, term=term)
    else:
        return "Error connecting to the database", 500


def searchFTS(term, con):
    """Search the database using Full-Text Search (FTS)."""
    try:
        cursor = con.cursor()

        # Example FTS query
        cursor.execute("""
            SELECT * FROM deep_data
            WHERE html LIKE ?
        """, (f"%{term}%",))

        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error searching database: {e}")
        return []


@main_bp.route('/logs')
def stream_logs():
    def generate():
        process = subprocess.Popen(
            ["python3", "midnight.py"],  # Replace with the actual command
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        for line in process.stdout:
            yield f"data: {line}\n\n"
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

def run_midnight_scan(proxy_settings):
    global scan_status
    try:
        print("[DEBUG] Starting midnight scan...")
        from midnight import run_midnight_scan as scan
        scan(proxy_settings['http'].split('//')[1].split(':')[0], int(proxy_settings['http'].split(':')[2]))
        scan_status = "completed"
        print("[DEBUG] Midnight scan completed.")
    except Exception as e:
        scan_status = f"error: {str(e)}"
        print(f"[DEBUG] Error in midnight scan: {e}")