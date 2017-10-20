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
        return self.name.title()


# TODO: make maximal confine counting by display preference
class LengthConfines(Enum):
    MINIMAL = 4
    MAXIMAL = 100


# TODO: make maximal confine counting by display preference
class HeightConfines(Enum):
    MINIMAL = 4
    MAXIMAL = 50


class Direction(Enum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4

    def find_symmetric_direction(self):
        if self == Direction.RIGHT:
            return Direction.LEFT

        if self == Direction.UP:
            return Direction.DOWN

        if self == Direction.LEFT:
            return Direction.RIGHT

        if self == Direction.DOWN:
            return Direction.UP

    def is_symmetric(self, direction):
        if direction == self.find_symmetric_direction():
            return True
        return False


@unique
class ImagesPath(Enum):
    SNAKE_HEAD_RIGHT = r'./images/head_right.gif'
    SNAKE_TAIL_RIGHT = r'./images/tail_right.gif'
    SNAKE_BODY_VERTICAL = r'./images/body_vertical.gif'
    SNAKE_BODY_RIGHT_DOWN = r'./images/body_right_down.gif'
    EGG = r'./images/egg.gif'
