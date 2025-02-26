from tools.enums import StrEnum, ValuesEnum


class RightsRole(StrEnum, ValuesEnum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    CAPTAIN = "captain"


class Medal(StrEnum, ValuesEnum):
    NONE = "NONE"
    BRONZE = "🥉"
    SILVER = "🥈"
    GOLD = "🥇"


ALL_ROLES = (*RightsRole.values(), None)
ALL_MEDALS = (*Medal.values(), None)
