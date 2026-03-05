import enum


class LevelEnum(enum.Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"


class ModuleTypeEnum(enum.Enum):
    CORE = "CORE"
    DOMAIN = "DOMAIN"
    READING = "READING"
    WRITING = "WRITING"
    SPEAKING = "SPEAKING"
