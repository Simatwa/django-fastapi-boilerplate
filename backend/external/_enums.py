from project.utils import EnumWithChoices


class FeedbackRate(EnumWithChoices):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    AVERAGE = "Average"
    POOR = "Poor"
    TERRIBLE = "Terrible"


class SenderRole(EnumWithChoices):
    VISITOR = "Visitor"
    CUSTOMER = "Customer"
    MANAGER = "Manager"
    FOUNDER = "Founder"
    INVESTOR = "Investor"


class DocumentName(EnumWithChoices):
    TERMS_OF_USE = "Terms of Service"
    PRIVACY_POLICY = "Privacy Policy"
    COOKIE_POLICY = "Cookie Policy"
    OUR_STORY = "Our story"
