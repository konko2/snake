from tkinter import *
from tkinter.messagebox import showerror

from constraints import Speed, LengthConfines, HeightConfines
from exceptions import InitialDataError, SmallLengthError, SmallHeightError, BigLengthError, BigHeightError, \
    WrongLengthError, WrongHeightError, QuitError


WELCOME_TEXT = """
    This is a snake game.\n
    Choose some preference and press 'Start!'.\n
    To quit press 'Quit'.
    """


class _WindowState:
    def __init__(self, window, speed_box, length_box, height_box):
        self.window = window
        self.speed_box = speed_box
        self.length_box = length_box
        self.height_box = height_box

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
        length = self.length_box.get()
        height = self.height_box.get()

        if not length.isnumeric():
            raise WrongLengthError

        length = int(length)
        if length < LengthConfines.MINIMAL.value:
            raise SmallLengthError
        if length > LengthConfines.MAXIMAL.value:
            raise BigLengthError

        if not height.isnumeric():
            raise WrongHeightError

        height = int(height)
        if height < HeightConfines.MINIMAL.value:
            raise SmallHeightError
        if height > HeightConfines.MAXIMAL.value:
            raise BigHeightError

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
