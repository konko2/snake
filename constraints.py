from enum import Enum, unique


@unique
class Speed(Enum):
    HIGH = 1
    NORMAL = 2
    LOW = 3

    def __str__(self):
        return self._name_.title()


# TODO: make maximal confine counting by display preference
class WidthConfines(Enum):
    MINIMAL = 10
    MAXIMAL = 50


# TODO: make maximal confine counting by display preference
class LengthConfines(Enum):
    MINIMAL = 10
    MAXIMAL = 100


if __name__ == '__main__':
    print(Speed.HIGH)
    print(LengthConfines.MINIMAL.value)
