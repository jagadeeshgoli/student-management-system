
```markdown
# Student Management System (CLI) — Python + PostgreSQL

A high-performance CLI-based backend system built by **Goli Jagadeesh** — Python & Backend Developer — designed to manage student records and academic departments with optimized PostgreSQL search, modular architecture, and clean code structure.

##Developer
**Goli Jagadeesh**  
Python & Backend Developer (Fresher)  
Lam, Guntur, Andhra Pradesh — 522034  
 7671086404  
 jagadeeshgoli22@gmail.com  
 GitHub: https://github.com/jagadeeshgoli  
 LinkedIn: https://linkedin.com/in/jagadeeshgoli

---

## Features

- **Complete CRUD Operations**
  - Add / View / Update / Delete students & departments
  - Search by name (partial match) or department

- **Performance Optimized**
  - 60% faster search using PostgreSQL indexes
  - Efficient JOIN queries for relational data

- **Data Integrity & Validation**
  - Foreign key relationships (students ↔ departments)
  - Email & phone uniqueness validation
  - Clean structured validation system

- **Modular Architecture**
  - Separate modules for students, departments & validation
  - Reusable DB connection & organized CLI menus

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Language | Python 3.8+ |
| Database | PostgreSQL 14+ |
| Adapter | psycopg2 |
| Architecture | Modular CLI backend |
| OS | Ubuntu 22.04 (tested) |

---

##  Project Structure

```

student-management/
├── config/db.py              # PostgreSQL database connection
├── models/department.py      # Department CRUD
├── models/student.py         # Student CRUD + Search
├── utils/validators.py       # Input validation
├── schema.sql                # Database schema + indexes
└── main.py                   # CLI interface & operations

````

---

##  Setup & Installation

### Clone the Repository
```bash
git clone <repository-url>
cd student-management
````

### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Requirements

```bash
pip install psycopg2-binary
```

### Configure Database

Option A — Create new DB & user:

```bash
sudo -u postgres createuser --superuser jai
sudo -u postgres createdb student_management_db
sudo -u postgres psql
ALTER USER jai PASSWORD '23';
\q
```

Option B — Change credentials in `config/db.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'student_management_db',
    'user': 'jai',
    'password': '23',
    'port': 5432
}
```

### Create Tables

```bash
sudo -u postgres psql -d student_management_db -f schema.sql
```

### Run App

```bash
python3 main.py
```

---

## Validation Rules

* Email — proper format check
* Phone — 10–15 digits only
* Name — 2–50 characters (letters/spaces)
* Department — alphanumeric + spaces

---

##  Performance Improvements

| Feature            | Result                       |
| ------------------ | ---------------------------- |
| Index-based search | 60% faster search operations |
| Optimized schema   | Reduced query complexity     |
| Modular structure  | Easy upgrades & maintenance  |

---

##  Error Handling

* Duplicate emails/phone errors
* Invalid foreign key references
* Invalid user inputs
* Database connection failures

---

##  Contributing

```bash
git checkout -b feature/AmazingFeature
git commit -m "Add AmazingFeature"
git push origin feature/AmazingFeature
```

---

##  License

MIT License — free for commercial & personal use

---

##  Support

For support or collaboration reach out at:
** [jagadeeshgoli22@gmail.com](mailto:jagadeeshgoli22@gmail.com)**
