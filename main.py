from pathlib import Path

from library_service import LibraryManager
from models import Book, FacultyMember, Magazine, NotifiedMember, ReferenceBook, ResearchStudent, StudentMember
from storage import load_data, save_data


DATA_FILE = Path(__file__).with_name("data.json")


def register_item(library):
    print("1. Book  2. Magazine  3. Reference book")
    item_types = {"1": Book, "2": Magazine, "3": ReferenceBook}
    item_class = item_types.get(input("Item type: "))

    if item_class is None:
        print("Invalid choice.")
        return

    try:
        item = item_class(input("Item ID: "), input("Title: "))
        library.add_item(item)
        print("Item registered successfully.")
    except ValueError as error:
        print(error)


def register_member(library):
    print("1. Student  2. Research student  3. Faculty  4. Notified member")
    member_types = {
        "1": StudentMember,
        "2": ResearchStudent,
        "3": FacultyMember,
        "4": NotifiedMember,
    }
    member_class = member_types.get(input("Member type: "))

    if member_class is None:
        print("Invalid choice.")
        return

    try:
        member = member_class(input("Member ID: "), input("Name: "))
        library.add_member(member)
        print("Member registered successfully.")
    except ValueError as error:
        print(error)


def borrow_item(library):
    try:
        member_id = input("Member ID: ")
        item_id = input("Item ID: ")
        due_date = library.borrow_item(member_id, item_id)
        print(f"Borrow successful: {item_id} issued to {member_id}")
        print(f"Due date: {due_date}")
    except ValueError as error:
        print(f"Borrow failed: {error}")


def return_item(library):
    try:
        item_id = input("Item ID: ")
        overdue_days, fine = library.return_item(item_id)
        print("Return successful.")
        print(f"Overdue days: {overdue_days}")
        print(f"Fine: Rs. {fine}")
    except ValueError as error:
        print(f"Return failed: {error}")


def view_reports(library):
    print(f"\nAll items: {len(library.items)}")
    for item in library.items.values():
        status = "Available" if item.available else "Issued"
        print(f"{item.item_id} | {item.title} | {status}")

    print(f"\nAvailable items: {sum(item.available for item in library.items.values())}")

    print(f"\nActive loans: {len(library.loans)}")
    for item_id, loan in library.loans.items():
        print(f"{item_id} | {loan['member_id']} | Due: {loan['due_date']}")

    print("\nMembers:")
    for member in library.members.values():
        print(f"{member.member_id} | {member.name} | Borrowed: {len(member.borrowed_items)}")


def main():
    library = load_data(DATA_FILE)

    while True:
        print("\n1. Register book  2. Register member")
        print("3. Borrow item    4. Return item")
        print("5. View reports   6. Exit")
       
        choice = input("Choice: ")

        if choice == "1":
            register_item(library)
        elif choice == "2":
            register_member(library)
        elif choice == "3":
            borrow_item(library)
        elif choice == "4":
            return_item(library)
        elif choice == "5":
            view_reports(library)
        elif choice == "6":
            save_data(library, DATA_FILE)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice.")

        save_data(library, DATA_FILE)


if __name__ == "__main__":
     main()
