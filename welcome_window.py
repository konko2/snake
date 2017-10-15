from tkinter import *
from tkinter.messagebox import showerror

from constraints import Speed, WidthConfines, LengthConfines
from exceptions import InitialDataError, SmallWidthError, SmallLengthError, BigWidthError, BigLengthError, \
    WrongLengthError, WrongWidthError, QuitError


WELCOME_TEXT = """
    This is a snake game.\n
    Choose some preference and press 'Start!'.\n
    To quit press 'Quit'.
    """


class _WindowState():
    def __init__(self, window, speed_box, width_box, length_box):
        self.window = window
        self.speed_box = speed_box
        self.width_box = width_box
        self.length_box = length_box

    def pressing_start(self):
        try:
            self.check_values()
            self.window.destroy()
        except InitialDataError as error:
            showerror('', error.message)

    def pressing_quit(self):
        self.quit = True
        self.window.destroy()

    def check_values(self):
        width = self.width_box.get()
        length = self.length_box.get()

        if not width.isnumeric():
            raise WrongWidthError

        width = int(width)
        if width < WidthConfines.MINIMAL.value:
            raise SmallWidthError
        if width > WidthConfines.MAXIMAL.value:
            raise BigWidthError

        if not length.isnumeric():
            raise WrongLengthError

        length = int(length)
        if length < LengthConfines.MINIMAL.value:
            raise SmallLengthError
        if length > LengthConfines.MAXIMAL.value:
            raise BigLengthError

        str_speed = self.speed_box.get()
        speed = next(s for s in Speed if str(s) == str_speed),
        self.checked_values = speed, width, length

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

    Label(tk, text="Width: ").grid(row=1, column=2)
    Label(tk, text="Length: ").grid(row=2, column=2)
    width_box, length_box = Entry(tk), Entry(tk)
    width_box.insert(0, "20"), length_box.insert(0, "20")
    width_box.grid(row=1, column=3), length_box.grid(row=2, column=3)

    state = _WindowState(tk, speed_box, width_box, length_box)
    Button(tk, text="Start!", command=state.pressing_start).grid(row=3, column=0, columnspan=2)
    Button(tk, text="Quit", command=state.pressing_quit).grid(row=3, column=2, columnspan=2)

    tk.mainloop()

    if state.quit:
        raise QuitError

    return state.checked_values


if __name__ == '__main__':
    try:
        print(create_preference_window())
    except QuitError:
        print('Done')
