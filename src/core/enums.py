from tools.enums import StrEnum, ValuesEnum


class RightsRole(StrEnum, ValuesEnum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    PARTICIPANT = "participant"


ALL_ROLES = (*RightsRole.values(), None)
