from random import choice
from tkinter import Tk, TclError

from constraints import Direction
from objects import Snake, Board
from welcome_window import create_preference_window

try:
    speed, length, height = create_preference_window()

    tk = Tk()
    tk.title("snake")
    tk.resizable(False, False)

    board = Board(tk, length, height)
    board.pack()

    snake = Snake(board, board.find_center_field())
    egg = None

    def finish_step():
        tk.quit()
        snake.move()

    while True:
        tk.after(speed, finish_step)

        if egg and snake.is_eat(egg):
            snake.is_growing = True

            board.delete(egg)
            egg = None
        else:
            snake.delete_bitten_tail()

        if not egg:
            free_fields = board.find_free_fields(snake)
            if free_fields:
                egg = board.create_image(choice(free_fields), board.images['egg'])

        tk.bind('<Up>', lambda _: snake.change_direction(Direction.UP))
        tk.bind('<Down>', lambda _: snake.change_direction(Direction.DOWN))
        tk.bind('<Left>', lambda _: snake.change_direction(Direction.LEFT))
        tk.bind('<Right>', lambda _: snake.change_direction(Direction.RIGHT))
        tk.mainloop()

except TclError:
    pass
