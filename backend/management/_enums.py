from project.utils import EnumWithChoices


class MessageCategory(EnumWithChoices):
    GENERAL = "General"
    PAYMENT = "Payment"
    MAINTENANCE = "Maintenance"
    PROMOTION = "Promotion"
    WARNING = "Warning"
    OTHER = "Other"


class ConcernStatus(EnumWithChoices):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class UtilityName(EnumWithChoices):
    CURRENCY = "Currency"
    LIBRARY_OPENING_HOURS = "Library Opening Hours"
    LIBRARY_CLOSING_HOURS = "Library Closing Hours"
    BOOKS_BORROWING_LIMIT = "Books borrowing limit"
