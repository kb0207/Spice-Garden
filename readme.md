# 🌶️ Spice Garden — Interactive Multi-Page Restaurant Web Application

Welcome to **Spice Garden**, a modern, multi-page web application designed for a contemporary dining experience. Built with a **Flask (Python)** backend, **SQLite** database persistence, and an interactive front-end powered by **HTML5, CSS3, and JavaScript**, this project elevates standard restaurant menus into a dynamic digital dining platform.

---

## 🌟 Key Features & "X-Factor"

### 1. 🌶️ Custom Spice & Taste Engine (The X-Factor)
- Dynamic filtering engine on the Menu page that allows users to instantly filter dishes based on their preferred taste profile (`Mild / Kids`, `Medium Spice`, `Hot & Spicy`, and `Sweet Tooth`).
- Real-time DOM manipulation updates the displayed menu items without reloading the page.

### 2. 🛒 Interactive Order Tray & Real-Time Bill Calculator
- Guests can add dishes directly to their live tray.
- Automatically calculates total pricing on the fly.
- Unique Order ID Generation: Every session generates a unique tracking code (e.g., `SG-9X2K7A`) using `Math.random().toString(36)`.

### 3. 🍳 Kitchen Relay System
- Submitting an order sends a JSON payload via an AJAX request to the Flask backend.
- Saves the order against the unique Order ID into the SQLite database (`orders` table).
- Displays instant visual feedback to the user: `"Items from the cart sent to our kitchen!"`.

### 4. 📬 Owner Feedback & Automated Email Dispatch
- Interactive 5-star rating system with real-time state highlighting.
- All feedback submissions are written directly to the `feedback` table in SQLite.
- Includes Python `smtplib` dispatch to automatically email incoming feedback directly to the restaurant owner.

### 5. 📄 Modular Multi-Page Architecture
- Built using Jinja2 template inheritance (`base.html`) to ensure consistent design across all pages while keeping code DRY (Don't Repeat Yourself).
- **Pages**:
  - `index.html`: Hero introduction & restaurant branding.
  - `menu.html`: Interactive menu, taste engine, and live order tray.
  - `team.html`: Kitchen crew showcase ("Chef Brigade").
  - `about.html`: Restaurant story and mission.
  - `contact.html`: Interactive feedback form & star rating system.

---

## 🗄️ Database Schema (`spice_garden.db`)

The application uses an **SQLite3** relational database with two core tables created automatically on app startup:

### 1. `orders` Table
Stores customer orders sent from the interactive tray.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `order_id` | TEXT | Unique session-generated ID (e.g., `SG-A1B2C3`) |
| `items` | TEXT | JSON string of selected dishes & prices |
| `total_amount` | REAL | Total bill amount in INR (₹) |
| `created_at` | TIMESTAMP | Submission timestamp |

### 2. `feedback` Table
Stores customer reviews and ratings from the contact page.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `name` | TEXT | Customer name |
| `email` | TEXT | Customer email address |
| `rating` | INTEGER | Rating out of 5 stars |
| `message` | TEXT | Detailed feedback message |
| `created_at` | TIMESTAMP | Submission timestamp |

---

## 📁 Project Structure

```text
Restaurant-Menu/
│
├── app.py                   # Python Flask backend & API routes
├── spice_garden.db          # SQLite database (auto-generated)
├── requirements.txt         # Dependencies list
│
├── templates/               # Jinja2 HTML Templates
│   ├── base.html            # Core layout template (Navbar, Footer, CSS links)
│   ├── index.html           # Home page
│   ├── menu.html            # Interactive menu & order tray
│   ├── team.html            # Kitchen crew profile page
│   ├── about.html           # Restaurant info page
│   └── contact.html         # Feedback form
│
└── static/                  # Static assets
    ├── css/
    │   └── style.css        # Responsive custom stylesheet
    └── img/
        ├── jai-kumar.jpg    # Chef photos
        ├── joy-malik.jpg
        └── karan-bhura.jpg