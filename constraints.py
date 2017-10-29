from enum import Enum, unique

from PIL import Image

MINIMAL_LENGTH = 10
MINIMAL_HEIGHT = 10
MAXIMAL_LENGTH = None
MAXIMAL_HEIGHT = None


@unique
class ImagesPath(Enum):
    SNAKE_HEAD_RIGHT = r'./images/head_right.gif'
    SNAKE_TAIL_RIGHT_L = r'./images/tail_right_turned_left.gif'
    SNAKE_BODY_VERTICAL_L = r'./images/body_vertical_left.gif'
    SNAKE_BODY_RIGHT_DOWN = r'./images/body_right_down.gif'
    EGG = r'./images/egg.gif'


_set_of_sizes = {Image.open(path.value).size for path in ImagesPath}
if len(_set_of_sizes) != 1:
    raise Exception('Different image dimensions')
_length, _height = _set_of_sizes.pop()
if _length != _height:
    raise Exception('Non-square images')

PIXELS_IN_FIELD = _length


@unique
class Speed(Enum):
    HIGH = 100
    NORMAL = 250
    LOW = 500

    def __str__(self):
        return self.name.title()


class Direction(Enum):
    RIGHT = 1
    UP = 2
    LEFT = 3
    DOWN = 4

    def find_reverse_direction(self):
        if self == self.__class__.RIGHT:
            return self.__class__.LEFT

        if self == self.__class__.UP:
            return self.__class__.DOWN

        if self == self.__class__.LEFT:
            return self.__class__.RIGHT

        if self == self.__class__.DOWN:
            return self.__class__.UP

    def is_reverse(self, direction):
        if direction == self.find_reverse_direction():
            return True
        return False
