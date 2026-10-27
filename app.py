import os
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_NAME = "spice_garden.db"

# EMAIL CONFIGURATION (Set environment variables or edit fallback defaults)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "your-restaurant-email@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "your-app-password")
OWNER_EMAIL = os.environ.get("OWNER_EMAIL", "owner@spicegarden.com")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        items TEXT NOT NULL,
        total_amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
    conn.commit()
    conn.close()

    
init_db()

def send_feedback_email(name, user_email, rating, message):
    if SENDER_EMAIL == "your-restaurant-email@gmail.com":
        print("[Simulated Email] Email credentials not configured. Skipping live SMTP dispatch.")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🌶️ New Spice Garden Feedback from {name}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = OWNER_EMAIL

        body_text = f"New Feedback Received:\n\nName: {name}\nEmail: {user_email}\nRating: {rating}/5 Stars\nMessage: {message}"
        body_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
            <div style="background-color: #3b1f0f; color: #f5b041; padding: 15px; text-align: center; border-radius: 8px 8px 0 0;">
              <h2>Spice Garden - Customer Feedback</h2>
            </div>
            <div style="padding: 20px; border: 1px solid #ddd; border-radius: 0 0 8px 8px; background-color: #fffaf5;">
              <p><strong>Customer Name:</strong> {name}</p>
              <p><strong>Customer Email:</strong> {user_email}</p>
              <p><strong>Rating:</strong> {'⭐' * int(rating)} ({rating}/5)</p>
              <p><strong>Feedback Message:</strong></p>
              <blockquote style="background-color: #fff2dc; padding: 15px; border-left: 4px solid #f5b041; margin: 10px 0;">
                {message}
              </blockquote>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, OWNER_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/menu")
def menu():
    return render_template("menu.html", page="menu")

@app.route("/team")
def team():
    return render_template("team.html", page="team")

@app.route("/about")
def about():
    return render_template("about.html", page="about")

@app.route("/contact")
def contact():
    return render_template("contact.html", page="contact")

@app.route("/api/feedback", methods=["POST"])
def handle_feedback():
    data = request.get_json() or request.form
    name = data.get("name")
    email = data.get("email")
    rating = data.get("rating", 5)
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"success": False, "error": "All required fields must be filled out."}), 400

    # 1. Save feedback into SQLite database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)",
        (name, email, rating, message)
    )
    conn.commit()
    conn.close()

    # 2. Dispatch email notification to owner
    send_feedback_email(name, email, rating, message)

    return jsonify({"success": True, "message": "Thank you for your feedback! It has been recorded."})

@app.route("/api/order", methods=["POST"])
def submit_order():
    data = request.get_json() or request.form
    order_id = data.get("order_id")
    items = data.get("items")
    total = data.get("total")

    if not order_id or not items:
        return jsonify({"success": False, "error": "Invalid order data."}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (order_id, items, total_amount) VALUES (?, ?, ?)",
        (order_id, str(items), total)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Items from the cart sent to our kitchen!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)