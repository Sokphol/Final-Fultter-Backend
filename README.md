# Final-Fultter-Backend

<p align="center">
  <strong>SonicFlow</strong> — E-Commerce REST API Backend for Flutter Mobile & Web Storefront.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-3.0+-000000?logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.1+-D71F00?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/JWT-Auth-black?logo=jsonwebtokens" alt="JWT" />
  <img src="https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite-00758F?logo=mysql&logoColor=white" alt="Database" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

## 📌 Overview

A production-ready e-commerce RESTful API backend engineered using **Flask, SQLAlchemy, Marshmallow, and JWT Extended**. It serves the [Final-Mobile-Frontend](https://github.com/Sokphol/Final-Mobile-Frontend) audio storefront with comprehensive catalog endpoints, authentication, shopping cart persistence, customer reviews, order tracking, and administration capabilities.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- MySQL 8.x or SQLite (for local zero-setup development)

### 2. Setup Virtual Environment & Install Dependencies

```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the example `.env` file and configure your credentials:

```bash
copy .env.example .env    # On Windows
cp .env.example .env      # On Linux/macOS
```

Sample `.env`:
```env
FLASK_ENV=development
SECRET_KEY=your-secure-app-secret-key
JWT_SECRET_KEY=your-secure-jwt-secret-key

# MySQL Connection (Default)
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/headphone_shop?charset=utf8mb4

# SQLite Alternative (No database installation required)
# DATABASE_URL=sqlite:///headphone_shop.db

UPLOAD_FOLDER=uploads
```

### 4. Seed Database & Run Server

```bash
# Create database tables and seed demo headphone products
python seed.py

# Start the Flask development server
python run.py
```

- **Base Server URL:** `http://localhost:5000`
- **Product API Endpoint:** `http://localhost:5000/api/v1/products/`

---

## 📁 Project Structure

```text
backend/
├── app/
│   ├── __init__.py               # App factory (create_app)
│   ├── config.py                 # Dev / Test / Prod configs
│   ├── extensions.py             # Flask extensions (db, jwt, cors, migrate)
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py       # Blueprint registry
│   │       ├── auth/routes.py    # Register, Login, Token Refresh, Current User
│   │       ├── users/routes.py   # User profile management
│   │       ├── addresses/routes.py
│   │       ├── categories/routes.py
│   │       ├── brands/routes.py
│   │       ├── products/routes.py
│   │       ├── cart/routes.py
│   │       ├── orders/routes.py
│   │       ├── payments/routes.py
│   │       ├── reviews/routes.py
│   │       ├── wishlist/routes.py
│   │       └── admin/routes.py   # Admin management dashboard
│   ├── models/
│   │   ├── user.py
│   │   ├── address.py
│   │   ├── category.py
│   │   ├── brand.py
│   │   ├── product.py            # Product, ProductImage, ProductVariant
│   │   ├── cart.py               # Cart, CartItem
│   │   ├── order.py              # Order, OrderItem
│   │   ├── payment.py
│   │   ├── review.py
│   │   └── wishlist.py
│   ├── schemas/                  # Marshmallow validation schemas
│   ├── services/                 # Business logic and database operations
│   └── utils/
│       ├── response.py           # Unified JSON response helper
│       ├── security.py           # Password hashing & verification
│       ├── decorators.py         # @admin_required, @active_required
│       ├── pagination.py         # Query pagination helper
│       ├── slugify.py            # URL slug generator
│       └── upload.py             # File upload handler
├── tests/                        # Pytest suite
├── seed.py                       # Demo data seeder
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container configuration
├── .env.example                  # Environment variable template
└── .gitignore                    # Git ignore specifications
```

---

## 🔑 REST API Reference

### Authentication
| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `POST` | `/api/v1/auth/register` | Public | Register new user account |
| `POST` | `/api/v1/auth/login` | Public | Login with email/password to retrieve JWT |
| `POST` | `/api/v1/auth/refresh` | Refresh Token | Refresh expired access token |
| `GET` | `/api/v1/auth/me` | JWT | Get current logged-in user profile |
| `PUT` | `/api/v1/auth/change-password` | JWT | Change user password |
| `POST` | `/api/v1/auth/logout` | JWT | Invalidate token session |

### Catalog & Products
| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `GET` | `/api/v1/products/` | Public | List products (with search, filter, sort, pagination) |
| `GET` | `/api/v1/products/featured` | Public | Get featured products for hero/promotions |
| `GET` | `/api/v1/products/<id>` | Public | Get single product by ID |
| `GET` | `/api/v1/products/slug/<slug>` | Public | Get single product by URL slug |
| `GET` | `/api/v1/products/<id>/related` | Public | Fetch recommended related products |
| `POST` | `/api/v1/products/` | Admin | Create new product |
| `PUT` | `/api/v1/products/<id>` | Admin | Update existing product |
| `DELETE` | `/api/v1/products/<id>` | Admin | Soft delete product |
| `POST` | `/api/v1/products/<id>/variants`| Admin | Add color/spec variant |

**Product Query Parameters:**
- Search: `?search=Sony`
- Category: `?category_id=1`
- Sorting: `?sort=popular` (`newest` | `price_asc` | `price_desc` | `rating` | `popular`)
- Filters: `&min_price=50&max_price=300&noise_cancellation=true&connectivity=Bluetooth`
- Pagination: `&page=1&per_page=12`

### Cart & Orders
| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `GET` | `/api/v1/cart/` | JWT | Retrieve current user shopping cart |
| `POST` | `/api/v1/cart/items` | JWT | Add product to cart `{product_id, quantity, variant_id?}` |
| `PUT` | `/api/v1/cart/items/<id>` | JWT | Update item quantity |
| `DELETE` | `/api/v1/cart/items/<id>` | JWT | Remove item from cart |
| `DELETE` | `/api/v1/cart/clear` | JWT | Clear all items from cart |
| `GET` | `/api/v1/orders/` | JWT | List authenticated user orders |
| `POST` | `/api/v1/orders/` | JWT | Place new order `{address_id, payment_method, notes?}` |
| `GET` | `/api/v1/orders/<id>` | JWT | Order detail with status & timeline |
| `PATCH` | `/api/v1/orders/<id>/cancel`| JWT | Cancel pending order |

### Reviews & Wishlist
| Method | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `GET` | `/api/v1/reviews/product/<id>` | Public | Fetch customer reviews for a product |
| `GET` | `/api/v1/reviews/product/<id>/summary` | Public | Rating summary (average & stars breakdown) |
| `POST` | `/api/v1/reviews/` | JWT | Post a product review `{product_id, rating, comment}` |
| `GET` | `/api/v1/wishlist/` | JWT | Get user wishlist |
| `POST` | `/api/v1/wishlist/<product_id>` | JWT | Add product to wishlist |
| `DELETE`| `/api/v1/wishlist/<product_id>` | JWT | Remove product from wishlist |

---

## 📦 Standard Response Schema

### Success Response
```json
{
  "success": true,
  "message": "Products fetched",
  "data": {
    "items": [...],
    "pagination": {
      "total": 50,
      "page": 1,
      "per_page": 12,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Invalid email or password",
  "data": null
}
```

---

## 🔐 Authentication & JWT

Requests requiring authentication require a Bearer token in the request header:

```http
Authorization: Bearer <access_token>
```

- Access tokens are valid for **2 hours**.
- Refresh tokens are valid for **30 days**.

---

## 🧪 Testing

Execute the test suite using `pytest`:

```bash
pytest tests/ -v
```

---

## 🌱 Demo Credentials (Generated via `python seed.py`)

| Role | Email | Password |
|:---|:---|:---|
| **Admin** | `admin@headphoneshop.com` | `admin123` |
| **Customer** | `john@example.com` | `password123` |

---

## 🐳 Docker Support

Build and run using Docker:

```bash
docker build -t final-flutter-backend:latest .
docker run -d -p 5000:5000 --env-file .env final-flutter-backend:latest
```

---

## 👥 Related Repositories

- **Frontend Client (Flutter):** [Final-Mobile-Frontend](https://github.com/Sokphol/Final-Mobile-Frontend)
