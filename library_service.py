from datetime import date, timedelta

from models import NotificationMixin, create_item, create_member


class LibraryManager:
    FINE_PER_DAY = 5

    def __init__(self):
        self.items = {}
        self.members = {}
        self.loans = {}

    def add_item(self, item):
        if item.item_id in self.items:
            raise ValueError("Item ID already exists.")
        self.items[item.item_id] = item

    def add_member(self, member):
        if member.member_id in self.members:
            raise ValueError("Member ID already exists.")
        self.members[member.member_id] = member

    def borrow_item(self, member_id, item_id):
        if member_id not in self.members:
            raise ValueError("Member not found.")
        if item_id not in self.items:
            raise ValueError("Item not found.")

        member = self.members[member_id]
        item = self.items[item_id]

        if not item.available:
            raise ValueError("Item is not available.")
        if not member.can_borrow():
            raise ValueError("Member borrowing limit reached.")
        if item.loan_period_days() == 0:
            raise ValueError("Reference books cannot be borrowed.")

        issue_date = date.today()
        due_date = issue_date + timedelta(days=item.loan_period_days())
        self.loans[item_id] = {
            "member_id": member_id,
            "issue_date": issue_date.isoformat(),
            "due_date": due_date.isoformat(),
        }
        item.borrow()
        member.borrowed_items.append(item_id)

        if isinstance(member, NotificationMixin):
            member.send_notice(f"Return {item.title} by {due_date}.")

        return due_date

    def return_item(self, item_id):
        if item_id not in self.loans:
            raise ValueError("This item is not issued.")

        loan = self.loans[item_id]
        member = self.members[loan["member_id"]]
        due_date = date.fromisoformat(loan["due_date"])
        overdue_days = max(0, (date.today() - due_date).days)
        fine = self.calculate_fine(overdue_days)

        self.items[item_id].return_item()
        member.borrowed_items.remove(item_id)
        del self.loans[item_id]
        return overdue_days, fine

    @staticmethod
    def calculate_fine(overdue_days):
        return overdue_days * LibraryManager.FINE_PER_DAY

    def to_dict(self):
        return {
            "items": [item.to_dict() for item in self.items.values()],
            "members": [member.to_dict() for member in self.members.values()],
            "loans": self.loans,
        }

    @classmethod
    def from_dict(cls, data):
        library = cls()

        for item_data in data.get("items", []):
            library.add_item(create_item(item_data))

        for member_data in data.get("members", []):
            library.add_member(create_member(member_data))

        library.loans = data.get("loans", {})
        for item_id, loan in library.loans.items():
            library.items[item_id].borrow()
            library.members[loan["member_id"]].borrowed_items.append(item_id)

        return library
