"""
Task 2: Persistent Record Management System
Author: sneb18240602
Description: CLI CRUD application with JSON persistence, duplicate ID checks,
             and error handling for corrupted or empty data files.
"""

import json
import os

DATA_FILE = "records.json"

def load_records(filepath: str = DATA_FILE) -> list:
    """Safely load records from a JSON file, handling missing or corrupt files."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print(f"Warning: '{filepath}' was empty or corrupted. Starting with an empty dataset.")
        return []

def save_records(records: list, filepath: str = DATA_FILE) -> bool:
    """Save records to the JSON file safely."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)
        return True
    except OSError as e:
        print(f"Error saving records to file: {e}")
        return False

def get_valid_input(prompt: str, field_name: str, allow_blank: bool = False, default: str = "") -> str:
    """Prompts for input with validation."""
    while True:
        val = input(prompt).strip()
        if not val and allow_blank:
            return default
        if val:
            return val
        print(f"Error: {field_name} cannot be empty.")

def get_valid_int(prompt: str, field_name: str, allow_blank: bool = False, default: int = 0) -> int:
    """Prompts for positive integer input."""
    while True:
        val = input(prompt).strip()
        if not val and allow_blank:
            return default
        if val.isdigit() and int(val) > 0:
            return int(val)
        print(f"Error: {field_name} must be a positive whole number.")

def generate_record_id(records: list) -> str:
    """Auto-generate uniform IDs like FD001, FD002."""
    existing_nums = []
    for r in records:
        rec_id = r.get("id", "")
        if rec_id.startswith("FD") and rec_id[2:].isdigit():
            existing_nums.append(int(rec_id[2:]))
    next_num = max(existing_nums, default=0) + 1
    return f"FD{next_num:03d}"

def add_record(records: list) -> None:
    print("\n--- 1. Add New Record ---")
    rec_id = generate_record_id(records)
    name = get_valid_input("Enter Item Name: ", "Name")
    category = get_valid_input("Enter Category: ", "Category")
    quantity = get_valid_int("Enter Quantity: ", "Quantity")
    location = get_valid_input("Enter Location: ", "Location")
    status = get_valid_input("Enter Status (Available/Claimed) [default: Available]: ", "Status", allow_blank=True, default="Available")

    new_record = {
        "id": rec_id,
        "name": name,
        "category": category,
        "quantity": quantity,
        "location": location,
        "status": status.capitalize()
    }
    records.append(new_record)
    if save_records(records):
        print(f"\nRecord Added Successfully!")
        print(f"ID: {new_record['id']}")
        print(f"Status: {new_record['status']}")

def view_records(records: list) -> None:
    print("\n--- 2. View All Records ---")
    if not records:
        print("No records available.")
        return
    print(f"\n{'ID':<8} | {'Name':<20} | {'Category':<15} | {'Quantity':<10} | {'Location':<15} | {'Status':<10}")
    print("-" * 88)
    for r in records:
        print(f"{r.get('id', 'N/A'):<8} | {r.get('name', 'N/A'):<20} | {r.get('category', 'N/A'):<15} | {r.get('quantity', 0):<10} | {r.get('location', 'N/A'):<15} | {r.get('status', 'N/A'):<10}")

def search_record(records: list) -> None:
    print("\n--- 3. Search Record ---")
    query = get_valid_input("Enter Search ID or Name: ", "Search query").lower()
    matches = [r for r in records if query in r.get("id", "").lower() or query in r.get("name", "").lower()]
    view_records(matches)

def update_record(records: list) -> None:
    print("\n--- 4. Update Record ---")
    rec_id = get_valid_input("Enter ID of record to update (e.g., FD001): ", "Record ID").upper()
    record = next((r for r in records if r.get("id", "").upper() == rec_id), None)

    if not record:
        print(f"Error: Record with ID '{rec_id}' not found.")
        return

    print(f"Updating record {rec_id}. Press Enter to keep current values.")
    record["name"] = get_valid_input(f"Name [{record['name']}]: ", "Name", allow_blank=True, default=record["name"])
    record["category"] = get_valid_input(f"Category [{record['category']}]: ", "Category", allow_blank=True, default=record["category"])
    record["quantity"] = get_valid_int(f"Quantity [{record['quantity']}]: ", "Quantity", allow_blank=True, default=record["quantity"])
    record["location"] = get_valid_input(f"Location [{record['location']}]: ", "Location", allow_blank=True, default=record["location"])
    record["status"] = get_valid_input(f"Status [{record['status']}]: ", "Status", allow_blank=True, default=record["status"]).capitalize()

    if save_records(records):
        print("\nRecord Updated Successfully")
        print(f"ID: {record['id']}")
        print(f"Status: {record['status']}")

def delete_record(records: list) -> None:
    print("\n--- 5. Delete Record ---")
    rec_id = get_valid_input("Enter ID of record to delete (e.g., FD001): ", "Record ID").upper()
    record = next((r for r in records if r.get("id", "").upper() == rec_id), None)

    if not record:
        print(f"Error: Record with ID '{rec_id}' not found.")
        return

    records.remove(record)
    if save_records(records):
        print(f"Record with ID '{rec_id}' deleted successfully.")

def generate_summary(records: list) -> None:
    print("\n--- 6. Generate Summary ---")
    total_records = len(records)
    total_quantity = sum(r.get("quantity", 0) for r in records)
    available = sum(1 for r in records if r.get("status", "").lower() == "available")
    claimed = sum(1 for r in records if r.get("status", "").lower() == "claimed")

    print(f"Total Records: {total_records}")
    print(f"Total Quantity: {total_quantity}")
    print(f"Available Records: {available}")
    print(f"Claimed Records: {claimed}")

def main():
    records = load_records()
    while True:
        print("\n==============================")
        print("  Persistent Management Menu")
        print("==============================")
        print("1. Add Record")
        print("2. View Records")
        print("3. Search Record")
        print("4. Update Record")
        print("5. Delete Record")
        print("6. Generate Summary")
        print("7. Exit")

        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            add_record(records)
        elif choice == "2":
            view_records(records)
        elif choice == "3":
            search_record(records)
        elif choice == "4":
            update_record(records)
        elif choice == "5":
            delete_record(records)
        elif choice == "6":
            generate_summary(records)
        elif choice == "7":
            print("Exiting application. All data is saved.")
            break
        else:
            print("Invalid selection. Please choose an option from 1 to 7.")

if __name__ == "__main__":
    main()
