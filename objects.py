from tkinter import Canvas
from PIL import Image
from PIL.ImageTk import PhotoImage

from constraints import Direction, ImagesPath


class Board(Canvas):
    def __init__(self, master, length, height, *args, **kwargs):
        self.length = length
        self.height = height

        self.pixels_in_field = ImagesPath.get_images_size()
        self.images = Board.loading_images()

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

        images = {'egg': PhotoImage(image=egg)}
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

        return images

    def create_image(self, coords, image):
        return super().create_image(*coords, image=image, anchor='nw')

    def find_next_field(self, direction, field):
        new_field = list(field)

        if direction == Direction.RIGHT:
            new_field[0] += self.pixels_in_field

        elif direction == Direction.UP:
            new_field[1] -= self.pixels_in_field

        elif direction == Direction.LEFT:
            new_field[0] -= self.pixels_in_field

        elif direction == Direction.DOWN:
            new_field[1] += self.pixels_in_field

        return [new_field[0] % self.length_px, new_field[1] % self.height_px]

    def find_center_field(self):
        return [
            self.min_field[0] + self.pixels_in_field * (self.length // 2),
            self.min_field[1] + self.pixels_in_field * (self.height // 2)
        ]

    def all_fields(self):
        return [[
            self.min_field[0] + i * self.pixels_in_field,
            self.min_field[1] + j * self.pixels_in_field,
        ] for i in range(self.length) for j in range(self.height)]

    def find_free_fields(self, list_of_obj):
        busy_fields = [self.coords(obj) for obj in list_of_obj]
        return [i for i in self.all_fields() if i not in busy_fields]

    min_field = [3, 3]


class Snake(list):
    def __init__(self, board, head_field):
        self.board = board
        self.images = board.images['snake']

        reverse_direction = self.direction.find_reverse_direction()

        body_fields = [head_field, ]
        for _ in range(2):
            body_fields += [board.find_next_field(
                reverse_direction,
                body_fields[-1]
            )]

        body = map(
            lambda field, body_part: board.create_image(
                field,
                self.images[body_part][self.direction]
            ),
            body_fields,
            ['head', 'body', 'tail']
        )

        super().__init__(body)

    def __delitem__(self, key):
        if isinstance(key, slice):
            self.board.delete(*self[key])
            tail_index = key.start - 1
        else:
            self.board.delete(self[key])
            tail_index = key - 1

        body_direction = self.get_body_direction(tail_index)
        self.board.itemconfigure(
            self[tail_index],
            image=self.images['tail'][body_direction]
        )

        super().__delitem__(key)

    def get_body_direction(self, index):
        if index == 1 or index == -len(self):
            return self.direction

        field = self.board.coords(self[index])
        next_field = self.board.coords(self[index-1])
        direction_to_neighbors = {
            tuple(self.board.find_next_field(d, field)): d for d in Direction
        }

        return direction_to_neighbors[tuple(next_field)]

    def change_direction(self, new_direction):
        if self.is_direction_changed:
            return
        elif self.direction == new_direction:
            return
        elif self.direction.is_reverse(new_direction):
            return

        self.is_direction_changed = True
        self.changed_direction = new_direction

    def is_eat(self, obj):
        if self.board.coords(self[0]) == self.board.coords(obj):
            return True
        return False

    def delete_bitten_tail(self):
        head_field, *body_fields = [self.board.coords(field) for field in self]
        try:
            eaten_field_index = body_fields.index(head_field)
            del self[eaten_field_index:]
        except ValueError:
            return

    def move(self):
        if self.is_growing:
            del self.is_growing
        else:
            del self[-1]

        image_field_after_head = self.images['body'][self.direction]

        if self.is_direction_changed:
            body_reverse_direction = self.direction.find_reverse_direction()
            body_corners = frozenset((body_reverse_direction, self.changed_direction))
            image_field_after_head = self.images['body'][body_corners]

            self.direction = self.changed_direction
            del self.changed_direction, self.is_direction_changed

        next_head_field = self.board.find_next_field(
            self.direction,
            self.board.coords(self[0])
        )
        head = self.board.create_image(
            next_head_field,
            self.images['head'][self.direction]
        )
        self.insert(0, head)

        self.board.itemconfigure(self[1], image=image_field_after_head)

    is_growing = False
    is_direction_changed = False
    changed_direction = None
    direction = Direction.RIGHT
