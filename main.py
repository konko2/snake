from tkinter import *
from random import choice

from objects import Snake, Apple, Board
from constraints import Direction
from welcome_window import create_preference_window
from exceptions import QuitError


try:
    speed, length, height = create_preference_window()

    # TODO: button quit in upper menu, button 'back to preference window'
    tk = Tk()
    tk.resizable(False, False)

    canvas = Canvas(tk)
    board = Board(canvas, length, height)
    canvas.configure(width=length * board.pixels_in_field, height=height * board.pixels_in_field)
    canvas.pack()

    snake = Snake(board, board.find_center_coords())
    apple = Apple(board, choice(board.find_free_fields_coords(snake)))

    def start_next_step(tk, snake):
        tk.quit()
        snake.move()

    while True:
        tk.after(speed, lambda: start_next_step(tk, snake))

        # TODO: if snakes body takes all board, then free fields doesn't exist, so apple can't be created
        if snake.is_eat(apple):
            snake.is_growing = True
            del apple
            apple = Apple(board, choice(board.find_free_fields_coords(snake)))
        else:
            snake.delete_bitten_tail()
        tk.bind('<Up>', lambda _: snake.change_direction(Direction.UP))
        tk.bind('<Down>', lambda _: snake.change_direction(Direction.DOWN))
        tk.bind('<Left>', lambda _: snake.change_direction(Direction.LEFT))
        tk.bind('<Right>', lambda _: snake.change_direction(Direction.RIGHT))
        tk.mainloop()

except QuitError:
    pass
