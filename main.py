from flask import Flask, render_template, request, redirect, flash, send_from_directory
import psycopg2
import os
from werkzeug.utils import secure_filename
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "database": os.getenv("POSTGRES_DB", "feedback_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password")
}

@app.route('/')
def home():
    try:
        conn = psycopg2.connect(**DB_PARAMS, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute("SELECT * FROM feedback ORDER BY created_at DESC;")
        feedback = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error connecting to database: {e}", "danger")
        feedback = []
    return render_template("index.html", feedback=feedback)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    department = request.form.get('department')
    category = request.form.get('category')
    rating = request.form.get('rating')
    feedback_text = request.form.get('feedback')
    attachment = request.files.get('attachment')

    if not all([name, email, department, category, rating, feedback_text]):
        flash("Please fill in all required fields!", "warning")
        return redirect('/')

    filename = None
    if attachment and attachment.filename != "":
        filename = secure_filename(f"{datetime.now().timestamp()}_{attachment.filename}")
        attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO feedback (name, email, department, category, rating, feedback, attachment, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (name, email, department, category, rating, feedback_text, filename, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
        flash("Feedback submitted successfully!", "success")
    except Exception as e:
        flash(f"Database error: {e}", "danger")

    return redirect('/')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
