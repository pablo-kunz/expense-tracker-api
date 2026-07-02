Expense Tracker API 📊

Personal Project — Python + Flask
Universidad Tecnológica Nacional (UTN) — Programming Technician Degree

Developed by: Pablo Kunz


Description

REST API built with Flask that reads business expense data from a CSV file and exposes it through HTTP endpoints. Returns structured JSON responses ready to be consumed by any frontend, app or external system.


Project Structure

├── app.py               # Flask API: routes and endpoints
├── expenses.py          # Core logic: data processing and analysis
└── expenses_data.csv    # Sample expense dataset


Requirements


Python 3.x
Flask


Install dependencies:

bashpip install flask


How to Run


Clone or download this repository.
Make sure all files are in the same folder.
Run from the terminal:


bashpython app.py


Open your browser at http://127.0.0.1:5000



API Endpoints

MethodEndpointDescriptionGET/API root — lists all available endpointsGET/expensesReturns all expense recordsGET/expenses/categoryTotal spent per category (highest to lowest)GET/expenses/monthlyTotal spent per month (chronological)GET/expenses/summaryFull summary reportGET/expenses/filter?start=YYYY-MM-DD&end=YYYY-MM-DDFilter by date range


Example Response

GET /expenses/summary

json{
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


CSV Format

date,category,amount,description
2026-01-05,Raw Materials,15000,Steel sheets
2026-02-25,Salaries,45000,Monthly payroll


Key Concepts Applied


REST API design with Flask
JSON responses with jsonify
Query parameter handling with request.args
Modular design separating API layer (app.py) from business logic (expenses.py)
HTTP error handling with status codes (400)
CSV data processing with the csv and datetime modules
