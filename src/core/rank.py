from enum import Enum, auto


class Rank(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()

    @staticmethod
    def value_of(value: int | str):
        if str(value) == "1":
            return Rank.ONE
        elif str(value) == "2":
            return Rank.TWO
        elif str(value) == "3":
            return Rank.THREE
        elif str(value) == "4":
            return Rank.FOUR
        elif str(value) == "5":
            return Rank.FIVE
        else:
            raise ValueError(f"Invalid rank: {value}")

    @property
    def short_name(self) -> str:
        if self is Rank.ONE:
            return "1"
        elif self is Rank.TWO:
            return "2"
        elif self is Rank.THREE:
            return "3"
        elif self is Rank.FOUR:
            return "4"
        elif self is Rank.FIVE:
            return "5"

    @property
    def number_value(self) -> int:
        if self is Rank.ONE:
            return 1
        if self is Rank.TWO:
            return 2
        if self is Rank.THREE:
            return 3
        if self is Rank.FOUR:
            return 4
        if self is Rank.FIVE:
            return 5

    def __repr__(self) -> str:
        return self.short_name
