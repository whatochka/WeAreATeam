from tools.enums import StrEnum, ValuesEnum


class RightsRole(StrEnum, ValuesEnum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    CAPTAIN = "captain"


ALL_ROLES = (*RightsRole.values(), None)
