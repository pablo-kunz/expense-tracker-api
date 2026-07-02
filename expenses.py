# Module responsible for loading, processing and analyzing expense data

import csv
from datetime import datetime


def load_expenses(file_name):
    """
    Reads the CSV file and returns a list of dictionaries, each representing an expense.
    If the file doesn't exist or has formatting errors, returns an empty list.
    """
    expenses = []
    try:
        with open(file_name, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    expense = {
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


def export_summary(expenses, output_file):
    """
    Exports a summary report to a new CSV file with totals per category
    and totals per month.
    """
    try:
        category_totals = total_by_category(expenses)
        monthly_totals = total_by_month(expenses)

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(["=== TOTAL BY CATEGORY ==="])
            writer.writerow(["Category", "Total Amount"])
            for category, total in category_totals.items():
                writer.writerow([category, f"{total:.2f}"])

            writer.writerow([])
            writer.writerow(["=== TOTAL BY MONTH ==="])
            writer.writerow(["Month", "Total Amount"])
            for month, total in monthly_totals.items():
                writer.writerow([month, f"{total:.2f}"])

            writer.writerow([])
            writer.writerow(["=== GENERAL SUMMARY ==="])
            writer.writerow(["Total expenses", f"{sum(e['amount'] for e in expenses):.2f}"])
            writer.writerow(["Monthly average", f"{monthly_average(expenses):.2f}"])
            month, amount = most_expensive_month(expenses)
            writer.writerow(["Most expensive month", f"{month} (${amount:.2f})"])

        print(f"Summary exported to '{output_file}' successfully.")
    except Exception as e:
        print(f"Error while exporting the summary: {e}")
