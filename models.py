class LibraryItem:
    def __init__(self, item_id, title, available=True):
        self.item_id = item_id
        self.title = title
        self._available = available

    @property
    def available(self):
        return self._available

    def borrow(self):
        self._available = False

    def return_item(self):
        self._available = True

    def loan_period_days(self):
        return 0

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "item_id": self.item_id,
            "title": self.title,
            "available": self.available,
        }


class Book(LibraryItem):
    def loan_period_days(self):
        return 14


class Magazine(LibraryItem):
    def loan_period_days(self):
        return 7


class ReferenceBook(LibraryItem):
    def loan_period_days(self):
        return 0


class Member:
    def __init__(self, member_id, name, limit=3):
        self.member_id = member_id
        self.name = name
        self.limit = limit
        self.borrowed_items = []

    def can_borrow(self):
        return len(self.borrowed_items) < self.limit

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "member_id": self.member_id,
            "name": self.name,
            "limit": self.limit,
        }


class StudentMember(Member):
    def __init__(self, member_id, name, limit=3):
        super().__init__(member_id, name, limit)


class ResearchStudent(StudentMember):
    def __init__(self, member_id, name, limit=5):
        super().__init__(member_id, name, limit)


class FacultyMember(Member):
    def __init__(self, member_id, name, limit=6):
        super().__init__(member_id, name, limit)


class NotificationMixin:
    def send_notice(self, message):
        print(f"Notice for {self.name}: {message}")


class NotifiedMember(Member, NotificationMixin):
    # Member comes first, so its borrowing methods are used first.
    pass


def create_item(data):
    item_classes = {
        "Book": Book,
        "Magazine": Magazine,
        "ReferenceBook": ReferenceBook,
    }
    item_class = item_classes[data["type"]]
    return item_class(data["item_id"], data["title"], data["available"])


def create_member(data):
    member_classes = {
        "Member": Member,
        "StudentMember": StudentMember,
        "ResearchStudent": ResearchStudent,
        "FacultyMember": FacultyMember,
        "NotifiedMember": NotifiedMember,
    }
    member_class = member_classes[data["type"]]
    return member_class(data["member_id"], data["name"], data["limit"])
