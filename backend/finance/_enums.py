from project.utils import EnumWithChoices


class TransactionMeans(EnumWithChoices):
    CASH = "Cash"
    MPESA = "M-PESA"
    BANK = "Bank"
    OTHER = "Other"


class TransactionType(EnumWithChoices):
    DEPOSIT = "Deposit"
    PAYMENT = "Payment"
    REFUND = "Refund"


class FeeName(EnumWithChoices):
    LOST_BOOK_PENALTY = "Lost book penalty"
    LATE_BOOK_RETURN_PENALTY = "Late book return penalty"
