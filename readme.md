# 🏋️‍♀️ Fitness Class Booking API

A RESTful API built using Django and Django REST Framework that allows clients to:

- View upcoming fitness classes
- Book a slot in a class
- View all their bookings

---

## ✨ Features

- ✅ **Class & Booking APIs**
- ✅ **API Versioning support (e.g., /api/v1/classes/) using Django REST Framework versioning schemes**
- ✅ **Swagger API Documentation** (`drf-yasg`)
- ✅ **Unit Testing** using `APITestCase`
- ✅ **Management Script** for creating sample classes
- ✅ **Atomic Transactions** to prevent overbooking
- ✅ **Validation & Integrity Handling**
- ✅ **PEP8 Compliant** clean code structure

---


## 🧰 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-project.git
cd your-project
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Run Management Scripts

```bash
python manage.py create_fitness_classes

```

### 6. Run the Development Server

```bash
python manage.py runserver

```


## 📁 API Endpoints

### 📌 `v1/classes/` `GET`

List all upcoming fitness classes.  
Returns: `name`, `datetime`, `instructor`, and `available_slots`.
```json
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-15T07:30:00Z",
    "instructor": "Alice Smith",
    "available_slots": 15
  },
  {
    "id": 2,
    "name": "Zumba",
    "datetime": "2025-06-16T18:00:00Z",
    "instructor": "Bob Johnson",
    "available_slots": 20
  },
  {
    "id": 3,
    "name": "HIIT",
    "datetime": "2025-06-17T06:00:00Z",
    "instructor": "Clara Lee",
    "available_slots": 12
  }
]
```

---

### 📝 `v1/book/<int:class_id>/` `POST`

Book a class.

#### Request Body:
```json
{
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
```

### 📝 `/bookings/?email=john@example.com` `GET`

Fetch all bookings made by a specific email address.
Returns: `client_name`, `client_email`, `fitness_class`, and `id`.





