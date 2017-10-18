from enum import Enum, unique


@unique
class Speed(Enum):
    '''
    Duration of one step in milliseconds
    '''
    HIGH = 100
    NORMAL = 250
    LOW = 500

    def __str__(self):
        return self._name_.title()


# TODO: make maximal confine counting by display preference
class LengthConfines(Enum):
    MINIMAL = 10
    MAXIMAL = 100


# TODO: make maximal confine counting by display preference
class HeightConfines(Enum):
    MINIMAL = 10
    MAXIMAL = 50


class Direction(Enum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4


@unique
class ImagesPath(Enum):
    SNAKE = r'./images/red.gif'
    APPLE = r'./images/blue.gif'
