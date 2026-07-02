# Expense Tracker API 📊

**Personal Project — Python + Flask**
Universidad Tecnológica Nacional (UTN) — Programming Technician Degree

**Developed by:** Pablo Kunz

---

## Description

REST API built with Flask that reads business expense data from a CSV file and exposes it through HTTP endpoints. Returns structured JSON responses ready to be consumed by any frontend, app or external system.

---

## Project Structure

```
├── app.py               # Flask API: routes and endpoints
├── expenses.py          # Core logic: data processing and analysis
└── expenses_data.csv    # Sample expense dataset
```

---

## Requirements

- Python 3.x
- Flask

Install dependencies:

```bash
pip install flask
```

---

## How to Run

1. Clone or download this repository.
2. Make sure all files are in the same folder.
3. Run from the terminal:

```bash
python app.py
```

4. Open your browser at `http://127.0.0.1:5000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API root — lists all available endpoints |
| GET | `/expenses` | Returns all expense records |
| GET | `/expenses/category` | Total spent per category (highest to lowest) |
| GET | `/expenses/monthly` | Total spent per month (chronological) |
| GET | `/expenses/summary` | Full summary report |
| GET | `/expenses/filter?start=YYYY-MM-DD&end=YYYY-MM-DD` | Filter by date range |

---

## Example Response

`GET /expenses/summary`

```json
{
  "monthly_average": 56150.0,
  "most_expensive_month": {
    "amount": 79600.0,
    "month": "2026-04"
  },
  "total_records": 30,
  "total_spent": 336900.0,
  "total_by_category": {
    "Salaries": 135000.0,
    "Raw Materials": 95500.0,
    "Services": 53000.0,
    "Logistics": 28100.0,
    "Supplies": 14900.0,
    "Maintenance": 10400.0
  }
}
```

---

## CSV Format

```
date,category,amount,description
2026-01-05,Raw Materials,15000,Steel sheets
2026-02-25,Salaries,45000,Monthly payroll
```

---

## Key Concepts Applied

- REST API design with Flask
- JSON responses with `jsonify`
- Query parameter handling with `request.args`
- Modular design separating API layer (`app.py`) from business logic (`expenses.py`)
- HTTP error handling with status codes (400)
- CSV data processing with the `csv` and `datetime` modules
