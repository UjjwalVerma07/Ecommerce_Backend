# 🛒 FastAPI E-Commerce Backend

A modern, secure, and modular **E-Commerce Backend API** built with **FastAPI**, following industry best practices. This backend supports user authentication, product management, cart operations, order processing, and password reset via email.

---

## 🚀 Features

- 🔐 **JWT Authentication** with Access & Refresh Tokens
- 👥 **Role-based Access Control** (Admin & User)
- 🛍️ **Product CRUD APIs** (Admin only)
- 🌐 **Public Product Listing & Search** with filters and pagination
- 🛒 **Cart Management** (Add, Update, Delete, View)
- 💳 **Checkout API** with automatic order creation
- 📦 **Order History & Detail View**
- ✉️ **Forgot/Reset Password** with Mailhog integration
- 🧱 Clean project structure with `routers`, `schemas`, `models`, and `utils`
- 📋 Fully typed with Pydantic and SQLAlchemy
- 📄 `.env` config with Pydantic `BaseSettings`

---

## 📁 Project Structure

```text
app/
├── main.py
├── auth/
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
│   ├── utils.py
├── products/
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
├── carts/
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
├── orders/
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
├── checkout/
│   ├── routes.py
├── core/
│   ├── config.py
│   ├── database.py
├── utils/
│   ├── email_service.py
│   ├── logging.py
├── middlewares/
├── tests/

📦 Tech Stack
FastAPI 🚀
SQLAlchemy ORM
Pydantic v2
Uvicorn (ASGI server)
PostgreSQL / SQLite
Passlib + Bcrypt
python-jose for JWTs
MailHog for dev email testing
Dotenv for environment configs

🛠️ Installation & Setup
1. Clone the Repository
git clone https://github.com/UjjwalVerma07/Ecommerce_Backend.git
cd Ecommerce_Backend
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Setup .env File
# .env
DATABASE_URL=sqlite:///./blogdatabase.db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
# Email Config for MailHog
mail_host=localhost
mail_port=1025
mail_from=no-reply@ecommerce.local
5. Run Mailhog (for reset-password emails)
# Install Mailhog or use Docker
docker run -d -p 8025:8025 -p 1025:1025 mailhog/mailhog
6. Start the Server
uvicorn app.main:app --reload


📬 API Highlights
Auth
POST /auth/signup
POST /auth/signin
POST /auth/forgot-password
POST /auth/reset-password

Products
GET /products (public)
GET /products/search
POST /admin/products (admin)
PUT /admin/products/{id} (admin)

Cart
POST /cart
GET /cart
PUT /cart/{product_id}
DELETE /cart/{product_id}

Orders
POST /checkout
GET /orders
GET /orders/{order_id}

🧪 Testing
You can use Postman or the built-in Swagger UI at /docs.


🤝 Contributing
Feel free to fork this repo, open issues, or submit PRs.

📜 License
This project is licensed under the MIT License.

💡 Author
Ujjwal Verma
