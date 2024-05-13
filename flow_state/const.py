from enum import auto, unique

from .utils.enums import AutoNameLowercaseEnum


@unique
class Environment(AutoNameLowercaseEnum):
    local = auto()
    development = auto()
    staging = auto()
    production = auto()


# After defining the enum, set a static property
Environment.values = [member.value for member in Environment]
