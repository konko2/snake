from tkinter import PhotoImage

from constraints import Direction, ImagesPath
from exceptions import ImagesError


class Board:
    def __init__(self, canvas_widget, length, height):
        self.canvas = canvas_widget
        self.length = length
        self.height = height

        self.images, self.pixels_in_field = Board.loading_images()

        self.length_px = length * self.pixels_in_field
        self.height_px = height * self.pixels_in_field

    @staticmethod
    def loading_images():
        images = dict()
        images['snake'] = PhotoImage(file=ImagesPath.SNAKE.value)
        images['apple'] = PhotoImage(file=ImagesPath.APPLE.value)

        images_size = set((image.width(), image.height()) for image in images.values())
        size = images_size.pop()

        if images_size or size[0] != size[1]:
            raise ImagesError

        return images, size[0]

    def find_neighbour_field_coords(self, direction, field):
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
        busy_fields = [tuple(map(int, self.canvas.coords(field))) for field in snake]
        return [i for i in self.all_fields_coords() if i not in busy_fields]

    min_field_coords = (3, 3)


class Snake:
    def __init__(self, board, head_field_coords, length=3):
        self.board = board

        self.image = board.images['snake']
        self.body = [board.canvas.create_image(*head_field_coords, image=self.image, anchor='nw'), ]
        for _ in range(length-1):
            self.body.append(board.canvas.create_image(
                *board.find_neighbour_field_coords(Direction.LEFT, board.canvas.coords(self.body[-1])),
                image=self.image,
                anchor='nw'
            ))

    def __iter__(self):
        return iter(self.body)

    def change_direction(self, new_direction):
        if self.is_direction_changed:
            return

        right_and_left = (Direction.RIGHT, Direction.LEFT)
        up_and_down = (Direction.UP, Direction.DOWN)

        if self.direction in right_and_left and new_direction in right_and_left:
            return

        if self.direction in up_and_down and new_direction in up_and_down:
            return

        self.is_direction_changed = True
        self.changed_direction = new_direction

    def is_eat(self, obj):
        if self.board.canvas.coords(self.body[0]) == self.board.canvas.coords(obj.body):
            return True
        return False

    def delete_bitten_tail(self):
        try:
            head_coords = self.board.canvas.coords(self.body[0])
            index_of_eaten_field = [
                self.board.canvas.coords(field) for field in self.body[1:]
            ].index(head_coords)
            for field in self.body[index_of_eaten_field:]:
                self.board.canvas.delete(field)
            self.body = self.body[:index_of_eaten_field]
        except ValueError:
            return

    def move(self):
        if self.is_growing:
            del self.is_growing
        else:
            self.board.canvas.delete(self.body[-1])
            del self.body[-1]

        if self.is_direction_changed:
            del self.is_direction_changed

            self.direction = self.changed_direction
            del self.changed_direction

        self.body.insert(0, self.board.canvas.create_image(
            self.board.find_neighbour_field_coords(self.direction, self.board.canvas.coords(self.body[0])),
            image=self.image,
            anchor='nw'
        ))

    is_growing = False
    is_direction_changed = False
    changed_direction = None
    direction = Direction.RIGHT


class Apple:
    def __init__(self, board, field_px):
        self.board = board
        self.image = board.images['apple']
        self.body = board.canvas.create_image(*field_px, image=self.image, anchor='nw')

    def __del__(self):
        self.board.canvas.delete(self.body)
