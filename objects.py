from tkinter import Canvas
from PIL import Image
from PIL.ImageTk import PhotoImage

from constraints import Direction, ImagesPath
from exceptions import ImagesDimensionError


class Board(Canvas):
    def __init__(self, master, length, height, *args, **kwargs):
        self.length = length
        self.height = height

        self.images, self.pixels_in_field = Board.loading_images()

        self.length_px = length * self.pixels_in_field
        self.height_px = height * self.pixels_in_field

        kwargs.pop('length', None)
        kwargs.pop('height', None)
        super().__init__(
            master,
            *args,
            width=self.length_px,
            height=self.height_px,
            **kwargs
        )

    @staticmethod
    def loading_images():

        head_right = Image.open(ImagesPath.SNAKE_HEAD_RIGHT.value)
        body_vertical = Image.open(ImagesPath.SNAKE_BODY_VERTICAL.value)
        body_right_down = Image.open(ImagesPath.SNAKE_BODY_RIGHT_DOWN.value)
        tail_right = Image.open(ImagesPath.SNAKE_TAIL_RIGHT.value)
        egg = Image.open(ImagesPath.EGG.value)

        images = dict()
        images['snake'] = {
            'head': {
                Direction.RIGHT: PhotoImage(image=head_right),
                Direction.UP: PhotoImage(image=head_right.rotate(90)),
                Direction.LEFT: PhotoImage(image=head_right.rotate(180)),
                Direction.DOWN: PhotoImage(image=head_right.rotate(270))
            },
            'body': {
                Direction.UP: PhotoImage(image=body_vertical),
                Direction.DOWN: PhotoImage(image=body_vertical),
                Direction.LEFT: PhotoImage(image=body_vertical.rotate(90)),
                Direction.RIGHT: PhotoImage(image=body_vertical.rotate(90)),
                frozenset((Direction.RIGHT, Direction.DOWN)): PhotoImage(image=body_right_down),
                frozenset((Direction.UP, Direction.RIGHT)): PhotoImage(image=body_right_down.rotate(90)),
                frozenset((Direction.LEFT, Direction.UP)): PhotoImage(image=body_right_down.rotate(180)),
                frozenset((Direction.DOWN, Direction.LEFT)): PhotoImage(image=body_right_down.rotate(270))
            },
            'tail': {
                Direction.RIGHT: PhotoImage(image=tail_right),
                Direction.UP: PhotoImage(image=tail_right.rotate(90)),
                Direction.LEFT: PhotoImage(image=tail_right.rotate(180)),
                Direction.DOWN: PhotoImage(image=tail_right.rotate(270))
            }
        }
        images['egg'] = PhotoImage(image=egg)

        list_of_images = \
            [images['egg'], ] + \
            list(images['snake']['head'].values()) + \
            list(images['snake']['body'].values())
        images_size = set((image.width(), image.height()) for image in list_of_images)
        size = images_size.pop()

        if images_size or size[0] != size[1]:
            raise ImagesDimensionError

        return images, size[0]

    @staticmethod
    def rotate_image(image):
        pass

    def create_image(self, coords, image):
        return super().create_image(*coords, image=image, anchor='nw')

    def find_next_field_coords(self, direction, field):
        result = list(field)

        if direction == Direction.RIGHT:
            result[0] += self.pixels_in_field

        elif direction == Direction.UP:
            result[1] -= self.pixels_in_field

        elif direction == Direction.LEFT:
            result[0] -= self.pixels_in_field

        elif direction == Direction.DOWN:
            result[1] += self.pixels_in_field

        result = result[0] % self.length_px, result[1] % self.height_px
        return result

    def find_center_coords(self):
        return (
            self.min_field_coords[0] + self.pixels_in_field * (self.length // 2),
            self.min_field_coords[1] + self.pixels_in_field * (self.height // 2)
        )

    def all_fields_coords(self):
        return [(
            self.min_field_coords[0] + i * self.pixels_in_field,
            self.min_field_coords[1] + j * self.pixels_in_field,
        ) for i in range(self.length) for j in range(self.height)]

    def find_free_fields_coords(self, snake):
        busy_fields = [tuple(map(int, self.coords(field))) for field in snake]
        return [i for i in self.all_fields_coords() if i not in busy_fields]

    min_field_coords = (3, 3)


class Snake(list):
    def __init__(self, board, head_field_coords, length=3):
        self.board = board
        self.images = board.images['snake']

        body = [board.create_image(head_field_coords, self.images['head'][self.direction]), ]
        for _ in range(length-1):
            body.append(board.create_image(
                board.find_next_field_coords(Direction.LEFT, board.coords(body[-1])),
                self.images['body'][Direction.LEFT],
            ))
        board.itemconfigure(body[-1], image=self.images['tail'][self.direction])
        super().__init__(body)

    def __delitem__(self, key):
        if isinstance(key, slice):
            self.board.delete(*self[key])
            first_field_index = key.start
        else:
            self.board.delete(self[key])
            first_field_index = key

        snakes_tail_direction = next(
            direction for direction in Direction
            if tuple(
                int(coord) for coord in self.board.coords(self[first_field_index-2])
            ) == self.board.find_next_field_coords(
                direction,
                self.board.coords(self[first_field_index-1])
            )
        )
        self.board.itemconfigure(self[first_field_index-1], image=self.images['tail'][snakes_tail_direction])

        super().__delitem__(key)

    def change_direction(self, new_direction):
        if self.is_direction_changed or self.direction == new_direction or self.direction.is_symmetric(new_direction):
            return

        self.is_direction_changed = True
        self.changed_direction = new_direction

    def is_eat(self, obj):
        if self.board.coords(self[0]) == self.board.coords(obj.body):
            return True
        return False

    # TODO: if snake eat tail, one field don't need to delete
    def delete_bitten_tail(self):
        try:
            head_coords = self.board.coords(self[0])
            index_of_eaten_field = [
                self.board.coords(field) for field in self[1:]
            ].index(head_coords)

            del self[index_of_eaten_field:]
        except ValueError:
            return

    def move(self):
        image_field_after_head = self.images['body'][self.direction]

        if self.is_growing:
            del self.is_growing
        else:
            del self[-1]

        if self.is_direction_changed:
            image_field_after_head = self.images['body'][
                frozenset((self.direction.find_symmetric_direction(), self.changed_direction))]

            self.direction = self.changed_direction
            del self.changed_direction, self.is_direction_changed

        self.board.itemconfigure(self[0], image=image_field_after_head)

        self.insert(0, self.board.create_image(
            self.board.find_next_field_coords(self.direction, self.board.coords(self[0])),
            self.images['head'][self.direction]
        ))

    is_growing = False
    is_direction_changed = False
    changed_direction = None
    direction = Direction.RIGHT


class Egg:
    def __init__(self, board, field_coords):
        self.board = board
        self.image = board.images['egg']
        self.body = board.create_image(field_coords, self.image)

    def __del__(self):
        self.board.delete(self.body)
