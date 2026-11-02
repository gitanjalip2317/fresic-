FRESIC - Fruit & Vegetable Delivery Demo
=========================================

START (Windows)
1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. In the installer, tick "Add Python to PATH".
3. Extract this ZIP to a folder you can find easily, e.g. Desktop\FRESIC_Project.
4. Double-click START.bat. First run needs internet to install Flask.
5. The website should open at http://127.0.0.1:5000.
6. Keep the black command window open while using the site. Close it to stop the server.

ADMIN DASHBOARD
Open http://127.0.0.1:5000/admin/login
Demo username: admin
Demo password: fresic123

IMPORTANT SECURITY NOTE:
These are demo login details for a local learning project. Before putting the site online, change them using environment variables FRESIC_ADMIN_USER and FRESIC_ADMIN_PASSWORD and set a strong FRESIC_SECRET_KEY. Do not publish the demo credentials.

FEATURES
- Product catalogue with categories and search
- Shopping cart and checkout form
- Orders saved locally in fresic.db (SQLite database is created automatically)
- Admin dashboard to view orders and update status
- Order confirmation page

WHATSAPP
This starter does NOT automatically send WhatsApp messages. Automatic sending needs Meta WhatsApp Business Platform/Cloud API setup, a registered business phone number, access token, phone-number ID, and any required approved template. A normal WhatsApp account alone is not enough. No secret credentials are included in this ZIP.

This project is a local demo and is not yet a production-ready public store. It has no online payments, delivery integration, customer accounts, or public hosting setup.
