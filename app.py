# Business Expense Tracker - REST API
# Built with Flask

from flask import Flask, jsonify, request
from expenses import (
    load_expenses,
    save_expenses,
    add_expense,
    update_expense,
    delete_expense,
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
            "id": e["id"],
            "date": e["date"].strftime("%Y-%m-%d"),
            "category": e["category"],
            "amount": e["amount"],
            "description": e["description"]
        }
        for e in expenses
    ]


# ── GET Routes ────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    """API root — shows available endpoints."""
    return jsonify({
        "message": "Business Expense Tracker API",
        "endpoints": {
            "GET /expenses": "All expense records",
            "GET /expenses/<id>": "Single expense by ID",
            "GET /expenses/category": "Total spent per category",
            "GET /expenses/monthly": "Total spent per month",
            "GET /expenses/summary": "Full summary report",
            "GET /expenses/filter?start=YYYY-MM-DD&end=YYYY-MM-DD": "Filter by date range",
            "POST /expenses": "Add a new expense",
            "PUT /expenses/<id>": "Update an existing expense",
            "DELETE /expenses/<id>": "Delete an expense"
        }
    })


@app.route("/expenses", methods=["GET"])
def get_expenses():
    """Returns all expense records."""
    expenses = load_expenses(FILE_NAME)
    return jsonify({
        "total_records": len(expenses),
        "expenses": serialize_expenses(expenses)
    })


@app.route("/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    """Returns a single expense by ID."""
    expenses = load_expenses(FILE_NAME)
    for e in expenses:
        if e["id"] == expense_id:
            return jsonify(serialize_expenses([e])[0])
    return jsonify({"error": f"Expense with ID {expense_id} not found."}), 404


@app.route("/expenses/category", methods=["GET"])
def get_by_category():
    """Returns total amount spent per category, sorted highest to lowest."""
    expenses = load_expenses(FILE_NAME)
    return jsonify({"total_by_category": total_by_category(expenses)})


@app.route("/expenses/monthly", methods=["GET"])
def get_by_month():
    """Returns total amount spent per month, sorted chronologically."""
    expenses = load_expenses(FILE_NAME)
    return jsonify({"total_by_month": total_by_month(expenses)})


@app.route("/expenses/summary", methods=["GET"])
def get_summary():
    """Returns a full summary report."""
    expenses = load_expenses(FILE_NAME)
    month, amount = most_expensive_month(expenses)
    return jsonify({
        "total_records": len(expenses),
        "total_spent": round(sum(e["amount"] for e in expenses), 2),
        "monthly_average": round(monthly_average(expenses), 2),
        "most_expensive_month": {"month": month, "amount": round(amount, 2)},
        "total_by_category": total_by_category(expenses),
        "total_by_month": total_by_month(expenses)
    })


@app.route("/expenses/filter", methods=["GET"])
def get_filtered():
    """Filters expenses by date range. Params: start, end (YYYY-MM-DD)"""
    start_str = request.args.get("start")
    end_str = request.args.get("end")

    if not start_str or not end_str:
        return jsonify({"error": "Please provide 'start' and 'end' query parameters."}), 400

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


# ── POST Route ────────────────────────────────────────────────────────────────

@app.route("/expenses", methods=["POST"])
def create_expense():
    """
    Adds a new expense.
    Expected JSON body: { "date": "YYYY-MM-DD", "category": "...", "amount": 0.0, "description": "..." }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    required = ["date", "category", "amount", "description"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        expenses = load_expenses(FILE_NAME)
        new_expense = add_expense(
            expenses,
            date_str=data["date"],
            category=data["category"],
            amount=data["amount"],
            description=data["description"]
        )
        save_expenses(FILE_NAME, expenses)
        return jsonify({
            "message": "Expense added successfully.",
            "expense": serialize_expenses([new_expense])[0]
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ── PUT Route ─────────────────────────────────────────────────────────────────

@app.route("/expenses/<int:expense_id>", methods=["PUT"])
def edit_expense(expense_id):
    """
    Updates an existing expense by ID.
    JSON body can include any of: date, category, amount, description.
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    try:
        expenses = load_expenses(FILE_NAME)
        updated = update_expense(
            expenses,
            expense_id,
            date_str=data.get("date"),
            category=data.get("category"),
            amount=data.get("amount"),
            description=data.get("description")
        )

        if updated is None:
            return jsonify({"error": f"Expense with ID {expense_id} not found."}), 404

        save_expenses(FILE_NAME, expenses)
        return jsonify({
            "message": "Expense updated successfully.",
            "expense": serialize_expenses([updated])[0]
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# ── DELETE Route ──────────────────────────────────────────────────────────────

@app.route("/expenses/<int:expense_id>", methods=["DELETE"])
def remove_expense(expense_id):
    """Deletes an expense by ID."""
    expenses = load_expenses(FILE_NAME)
    deleted = delete_expense(expenses, expense_id)

    if deleted is None:
        return jsonify({"error": f"Expense with ID {expense_id} not found."}), 404

    save_expenses(FILE_NAME, expenses)
    return jsonify({
        "message": "Expense deleted successfully.",
        "expense": serialize_expenses([deleted])[0]
    })


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
