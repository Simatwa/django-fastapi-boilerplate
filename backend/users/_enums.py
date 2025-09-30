from project.utils import EnumWithChoices


class UserGender(EnumWithChoices):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
