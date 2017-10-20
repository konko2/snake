from tkinter import *
from random import choice

from objects import Snake, Board
from constraints import Direction
from welcome_window import create_preference_window
from exceptions import QuitError


try:
    speed, length, height = create_preference_window()

    # TODO: button quit in upper menu, button 'back to preference window'
    tk = Tk()
    tk.title("snake")
    tk.resizable(False, False)

    board = Board(tk, length, height)
    board.pack()

    snake = Snake(board, board.find_center_field())

    free_fields = board.find_free_fields(snake)
    egg = board.create_image(choice(free_fields), board.images['egg'])


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

except QuitError:
    pass
