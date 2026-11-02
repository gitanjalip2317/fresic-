from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
from functools import wraps

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "fresic.db")
app = Flask(__name__)
app.secret_key = os.environ.get("FRESIC_SECRET_KEY", "change-this-local-demo-key")

PRODUCTS = [
    {"id": 1, "name": "Fresh Apples", "category": "Fruits", "price": 140, "unit": "kg", "emoji": "🍎", "desc": "Crisp, sweet and handpicked"},
    {"id": 2, "name": "Bananas", "category": "Fruits", "price": 60, "unit": "dozen", "emoji": "🍌", "desc": "Naturally sweet everyday fruit"},
    {"id": 3, "name": "Oranges", "category": "Fruits", "price": 90, "unit": "kg", "emoji": "🍊", "desc": "Juicy citrus goodness"},
    {"id": 4, "name": "Strawberries", "category": "Fruits", "price": 180, "unit": "box", "emoji": "🍓", "desc": "Bright, sweet seasonal berries"},
    {"id": 5, "name": "Tomatoes", "category": "Vegetables", "price": 35, "unit": "kg", "emoji": "🍅", "desc": "Ripe and full of flavour"},
    {"id": 6, "name": "Carrots", "category": "Vegetables", "price": 45, "unit": "kg", "emoji": "🥕", "desc": "Crunchy farm-fresh carrots"},
    {"id": 7, "name": "Broccoli", "category": "Vegetables", "price": 70, "unit": "piece", "emoji": "🥦", "desc": "Fresh green goodness"},
    {"id": 8, "name": "Potatoes", "category": "Vegetables", "price": 30, "unit": "kg", "emoji": "🥔", "desc": "Kitchen essentials, picked fresh"},
    {"id": 9, "name": "Spinach", "category": "Vegetables", "price": 25, "unit": "bunch", "emoji": "🥬", "desc": "Tender leafy greens"},
    {"id": 10, "name": "Capsicum", "category": "Vegetables", "price": 55, "unit": "kg", "emoji": "🫑", "desc": "Colourful, crisp and fresh"},
    {"id": 11, "name": "Mangoes", "category": "Fruits", "price": 160, "unit": "kg", "emoji": "🥭", "desc": "Seasonal sunshine in every bite"},
    {"id": 12, "name": "Onions", "category": "Vegetables", "price": 32, "unit": "kg", "emoji": "🧅", "desc": "Fresh daily cooking staple"},
]

STATUSES = ["Pending", "Confirmed", "Preparing", "Out for Delivery", "Delivered", "Cancelled"]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL
            )
        """)

init_db()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)

@app.route("/checkout", methods=["POST"])
def checkout():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    raw_items = request.form.get("items_json", "[]")
    import json
    try:
        cart = json.loads(raw_items)
    except (ValueError, TypeError):
        cart = []
    if not name or not phone or not address or not isinstance(cart, list) or not cart:
        flash("Please fill all details and add at least one item.", "error")
        return redirect(url_for("index"))
    product_map = {p["id"]: p for p in PRODUCTS}
    order_lines = []
    total = 0
    for entry in cart:
        try:
            pid = int(entry.get("id"))
            qty = int(entry.get("qty"))
        except (ValueError, TypeError, AttributeError):
            continue
        if pid not in product_map or qty < 1 or qty > 100:
            continue
        p = product_map[pid]
        line_total = p["price"] * qty
        total += line_total
        order_lines.append(f'{p["name"]} x {qty} = ₹{line_total}')
    if not order_lines:
        flash("Your cart is empty. Please add products first.", "error")
        return redirect(url_for("index"))
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO orders (customer_name, phone, address, items, total, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, phone, address, "\n".join(order_lines), total, "Pending", datetime.now().strftime("%d %b %Y, %I:%M %p"))
        )
        order_id = cur.lastrowid
    return render_template("success.html", order_id=order_id, name=name, phone=phone, total=total)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        expected_user = os.environ.get("FRESIC_ADMIN_USER", "admin")
        expected_password = os.environ.get("FRESIC_ADMIN_PASSWORD", "fresic123")
        if username == expected_user and password == expected_password:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Wrong username or password.", "error")
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    with get_db() as conn:
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template("admin.html", orders=orders, statuses=STATUSES)

@app.route("/admin/update/<int:order_id>", methods=["POST"])
@admin_required
def update_status(order_id):
    status = request.form.get("status", "")
    if status not in STATUSES:
        flash("Invalid order status.", "error")
    else:
        with get_db() as conn:
            conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
        flash(f"Order #{order_id} status updated to {status}.", "success")
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
