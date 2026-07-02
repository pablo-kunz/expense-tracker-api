# Business Expense Tracker - REST API
# Built with Flask

from flask import Flask, jsonify, request
from expenses import (
    load_expenses,
    total_by_category,
    total_by_month,
    most_expensive_month,
    monthly_average,
    filter_by_date_range
)
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "expenses_data.csv"


# ── Helper ────────────────────────────────────────────────────────────────────

def serialize_expenses(expenses):
    """Converts expense list to JSON-serializable format (dates to strings)."""
    return [
        {
            "date": e["date"].strftime("%Y-%m-%d"),
            "category": e["category"],
            "amount": e["amount"],
            "description": e["description"]
        }
        for e in expenses
    ]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    """API root — shows available endpoints."""
    return jsonify({
        "message": "Business Expense Tracker API",
        "endpoints": {
            "GET /expenses": "All expense records",
            "GET /expenses/category": "Total spent per category",
            "GET /expenses/monthly": "Total spent per month",
            "GET /expenses/summary": "Full summary report",
            "GET /expenses/filter?start=YYYY-MM-DD&end=YYYY-MM-DD": "Filter by date range"
        }
    })


@app.route("/expenses")
def get_expenses():
    """Returns all expense records."""
    expenses = load_expenses(FILE_NAME)
    return jsonify({
        "total_records": len(expenses),
        "expenses": serialize_expenses(expenses)
    })


@app.route("/expenses/category")
def get_by_category():
    """Returns total amount spent per category, sorted highest to lowest."""
    expenses = load_expenses(FILE_NAME)
    totals = total_by_category(expenses)
    return jsonify({
        "total_by_category": totals
    })


@app.route("/expenses/monthly")
def get_by_month():
    """Returns total amount spent per month, sorted chronologically."""
    expenses = load_expenses(FILE_NAME)
    totals = total_by_month(expenses)
    return jsonify({
        "total_by_month": totals
    })


@app.route("/expenses/summary")
def get_summary():
    """Returns a full summary report."""
    expenses = load_expenses(FILE_NAME)

    month, amount = most_expensive_month(expenses)

    return jsonify({
        "total_records": len(expenses),
        "total_spent": round(sum(e["amount"] for e in expenses), 2),
        "monthly_average": round(monthly_average(expenses), 2),
        "most_expensive_month": {
            "month": month,
            "amount": round(amount, 2)
        },
        "total_by_category": total_by_category(expenses),
        "total_by_month": total_by_month(expenses)
    })


@app.route("/expenses/filter")
def get_filtered():
    """
    Filters expenses by date range.
    Query params: start (YYYY-MM-DD), end (YYYY-MM-DD)
    Example: /expenses/filter?start=2026-01-01&end=2026-03-31
    """
    start_str = request.args.get("start")
    end_str = request.args.get("end")

    if not start_str or not end_str:
        return jsonify({"error": "Please provide 'start' and 'end' query parameters (YYYY-MM-DD)."}), 400

    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if start > end:
        return jsonify({"error": "Start date cannot be after end date."}), 400

    expenses = load_expenses(FILE_NAME)
    filtered = filter_by_date_range(expenses, start, end)

    return jsonify({
        "start": start_str,
        "end": end_str,
        "total_records": len(filtered),
        "total_spent": round(sum(e["amount"] for e in filtered), 2),
        "expenses": serialize_expenses(filtered)
    })


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
