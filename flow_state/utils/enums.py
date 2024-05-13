from enum import Enum


class AutoNameLowercaseEnum(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name.lower()


class AutoNameUppercaseEnum(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values) -> str:
        return name.upper()
