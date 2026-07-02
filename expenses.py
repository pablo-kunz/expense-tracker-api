# Module responsible for loading, processing and analyzing expense data

import csv
from datetime import datetime


def load_expenses(file_name):
    """
    Reads the CSV file and returns a list of dictionaries, each representing an expense.
    Automatically assigns an incremental ID to each record.
    If the file doesn't exist or has formatting errors, returns an empty list.
    """
    expenses = []
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for index, row in enumerate(reader, start=1):
                try:
                    expense = {
                        "id": index,
                        "date": datetime.strptime(row["date"].strip(), "%Y-%m-%d"),
                        "category": row["category"].strip(),
                        "amount": float(row["amount"]),
                        "description": row["description"].strip()
                    }
                    expenses.append(expense)
                except (ValueError, KeyError):
                    print(f"Warning: skipped a row with invalid format: {row}")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"Unexpected error while reading the file: {e}")

    return expenses


def save_expenses(file_name, expenses):
    """
    Saves the full expense list back to the CSV file.
    """
    try:
        with open(file_name, "w", newline="", encoding="utf-8") as f:
            fields = ["date", "category", "amount", "description"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for e in expenses:
                writer.writerow({
                    "date": e["date"].strftime("%Y-%m-%d"),
                    "category": e["category"],
                    "amount": e["amount"],
                    "description": e["description"]
                })
    except Exception as e:
        print(f"Error while saving the file: {e}")


def add_expense(expenses, date_str, category, amount, description):
    """
    Creates a new expense and adds it to the list.
    Returns the new expense or raises ValueError if data is invalid.
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category or not description:
        raise ValueError("Category and description cannot be empty.")

    new_id = max((e["id"] for e in expenses), default=0) + 1
    new_expense = {
        "id": new_id,
        "date": date,
        "category": category.strip(),
        "amount": float(amount),
        "description": description.strip()
    }
    expenses.append(new_expense)
    return new_expense


def update_expense(expenses, expense_id, date_str=None, category=None, amount=None, description=None):
    """
    Updates an existing expense by ID.
    Only updates the fields that are provided.
    Returns the updated expense or None if not found.
    """
    for expense in expenses:
        if expense["id"] == expense_id:
            if date_str:
                expense["date"] = datetime.strptime(date_str, "%Y-%m-%d")
            if category:
                expense["category"] = category.strip()
            if amount is not None:
                if amount <= 0:
                    raise ValueError("Amount must be greater than zero.")
                expense["amount"] = float(amount)
            if description:
                expense["description"] = description.strip()
            return expense
    return None


def delete_expense(expenses, expense_id):
    """
    Deletes an expense by ID.
    Returns the deleted expense or None if not found.
    """
    for i, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            return expenses.pop(i)
    return None


def total_by_category(expenses):
    """
    Returns a dictionary with the total amount spent per category,
    sorted from highest to lowest.
    """
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))


def total_by_month(expenses):
    """
    Returns a dictionary with the total amount spent per month (YYYY-MM format),
    sorted chronologically.
    """
    totals = {}
    for expense in expenses:
        month = expense["date"].strftime("%Y-%m")
        totals[month] = totals.get(month, 0) + expense["amount"]
    return dict(sorted(totals.items()))


def most_expensive_month(expenses):
    """Returns the month with the highest total spending."""
    monthly = total_by_month(expenses)
    if not monthly:
        return None, 0
    month = max(monthly, key=monthly.get)
    return month, monthly[month]


def monthly_average(expenses):
    """Calculates the average monthly spending."""
    monthly = total_by_month(expenses)
    if not monthly:
        return 0
    return sum(monthly.values()) / len(monthly)


def filter_by_date_range(expenses, start_date, end_date):
    """
    Returns only the expenses between start_date and end_date (inclusive).
    Dates must be datetime objects.
    """
    return [
        e for e in expenses
        if start_date <= e["date"] <= end_date
    ]
