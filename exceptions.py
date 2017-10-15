from constraints import WidthConfines, LengthConfines


class InitialDataError(Exception):
    code = 1
    message = ''


class SmallWidthError(InitialDataError):
    code = 11
    message = "Too small width, please choose bigger than " + str(WidthConfines.MINIMAL.value)


class BigWidthError(InitialDataError):
    code = 12
    message = "Too big width, please choose smaller than " + str(WidthConfines.MAXIMAL.value)


class WrongWidthError(InitialDataError):
    code = 13
    message = "Please write integer width"


class SmallLengthError(InitialDataError):
    code = 14
    message = "Too small length, please choose bigger than " + str(LengthConfines.MINIMAL.value)


class BigLengthError(InitialDataError):
    code = 15
    message = "Too big length, please choose smaller than " + str(LengthConfines.MAXIMAL.value)


class WrongLengthError(InitialDataError):
    code = 16
    message = "Please write integer length"


class QuitError(Exception):
    code = 2
