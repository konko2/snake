from welcome_window import create_preference_window
from exceptions import QuitError


try:
    speed, width, length = create_preference_window()
except QuitError:
    pass
