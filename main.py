from tkinter import *
from random import choice

from objects import Snake, Egg, Board
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

    snake = Snake(board, board.find_center_coords())
    egg = Egg(board, choice(board.find_free_fields_coords(snake)))

    def finish_step(master, snake):
        master.quit()
        snake.move()

    while True:
        tk.after(speed, lambda: finish_step(tk, snake))

        # TODO: if snakes body takes all board, then free fields doesn't exist, so egg can't be created
        if snake.is_eat(egg):
            snake.is_growing = True
            del egg
            egg = Egg(board, choice(board.find_free_fields_coords(snake)))
        else:
            snake.delete_bitten_tail()
        tk.bind('<Up>', lambda _: snake.change_direction(Direction.UP))
        tk.bind('<Down>', lambda _: snake.change_direction(Direction.DOWN))
        tk.bind('<Left>', lambda _: snake.change_direction(Direction.LEFT))
        tk.bind('<Right>', lambda _: snake.change_direction(Direction.RIGHT))
        tk.mainloop()

except QuitError:
    pass
