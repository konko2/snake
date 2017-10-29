from tkinter import Tk, TclError, Label, Spinbox, Entry, Button
from tkinter.messagebox import showerror

from constraints import Speed, PIXELS_IN_FIELD, MINIMAL_LENGTH, MAXIMAL_LENGTH, MINIMAL_HEIGHT, MAXIMAL_HEIGHT

WELCOME_TEXT = """
    This is a snake game. \n
    Choose some preference and press 'Start!'.
    To quit press 'Quit'.
    """

MESSAGE_SMALL_LENGTH = "Too small length, please choose bigger than {}"
MESSAGE_BIG_LENGTH = "Too big length, please choose smaller than {}"
MESSAGE_NON_INT_LENGTH = "Please write integer length"
MESSAGE_SMALL_HEIGHT = "Too small height, please choose bigger than {}"
MESSAGE_BIG_HEIGHT = "Too big height, please choose smaller than {}"
MESSAGE_NON_INT_HEIGHT = "Please write integer height"


class InitialDataError(Exception):
    def __init__(self, message, confine=None):
        self.message = message
        self.confine = confine

    def __str__(self):
        return self.message.format(self.confine)


class _WindowState:
    def __init__(self, window, speed_box, length_box, height_box):
        self.window = window
        self.speed_box = speed_box
        self.length_box = length_box
        self.height_box = height_box

        self.minimal_length = MINIMAL_LENGTH
        self.minimal_height = MINIMAL_HEIGHT
        self.maximal_length = MAXIMAL_LENGTH if MAXIMAL_LENGTH else \
            window.winfo_screenwidth() // PIXELS_IN_FIELD
        self.maximal_height = MAXIMAL_HEIGHT if MAXIMAL_HEIGHT else \
            window.winfo_screenheight() // PIXELS_IN_FIELD

    def pressing_start(self):
        try:
            self.check_values()
            self.window.destroy()
        except InitialDataError as error:
            showerror('', str(error))

    def pressing_quit(self):
        self.quit = True
        self.window.destroy()

    def check_values(self):
        length = self.length_box.get()
        height = self.height_box.get()

        if not length.isnumeric():
            raise InitialDataError(MESSAGE_NON_INT_LENGTH)

        length = int(length)
        if length < self.minimal_length:
            raise InitialDataError(MESSAGE_SMALL_LENGTH, self.minimal_length)
        if length > self.maximal_length:
            raise InitialDataError(MESSAGE_BIG_LENGTH, self.maximal_length)

        if not height.isnumeric():
            raise InitialDataError(MESSAGE_NON_INT_HEIGHT)

        height = int(height)
        if height < self.minimal_height:
            raise InitialDataError(MESSAGE_SMALL_HEIGHT, self.minimal_height)
        if height > self.maximal_height:
            raise InitialDataError(MESSAGE_BIG_HEIGHT, self.maximal_height)

        str_speed = self.speed_box.get()
        speed = next(s for s in Speed if str(s) == str_speed).value
        self.checked_values = speed, length, height

    checked_values = None
    quit = False


def create_preference_window():
    tk = Tk()
    tk.title("snake")
    tk.resizable(False, False)

    Label(tk, text=WELCOME_TEXT).grid(row=0, column=0, columnspan=4)

    Label(tk, text="Speed: ").grid(row=1, column=0)
    speed_box = Spinbox(tk, values=list(Speed), state='readonly')
    while speed_box.get() != str(Speed.NORMAL):
        speed_box.invoke('buttonup')
    speed_box.grid(row=1, column=1)

    Label(tk, text="Length: ").grid(row=1, column=2)
    Label(tk, text="Height: ").grid(row=2, column=2)
    length_box, height_box = Entry(tk), Entry(tk)
    length_box.insert(0, "20"), height_box.insert(0, "20")
    length_box.grid(row=1, column=3), height_box.grid(row=2, column=3)

    state = _WindowState(tk, speed_box, length_box, height_box)
    Button(
        tk,
        text="Start!",
        command=state.pressing_start
    ).grid(row=3, column=0, columnspan=2)
    Button(
        tk,
        text="Quit",
        command=state.pressing_quit
    ).grid(row=3, column=2, columnspan=2)

    tk.mainloop()

    if state.quit:
        raise TclError

    return state.checked_values


if __name__ == '__main__':
    try:
        print(create_preference_window())
    except TclError:
        print('Done')
