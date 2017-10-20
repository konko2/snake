from constraints import HeightConfines, LengthConfines


class InitialDataError(Exception):
    code = 1
    message = ''


class SmallLengthError(InitialDataError):
    code = 11
    message = "Too small length, please choose bigger than " + str(LengthConfines.MINIMAL.value)


class BigLengthError(InitialDataError):
    code = 12
    message = "Too big length, please choose smaller than " + str(LengthConfines.MAXIMAL.value)


class WrongLengthError(InitialDataError):
    code = 13
    message = "Please write integer length"


class SmallHeightError(InitialDataError):
    code = 14
    message = "Too small height, please choose bigger than " + str(HeightConfines.MINIMAL.value)


class BigHeightError(InitialDataError):
    code = 15
    message = "Too big height, please choose smaller than " + str(HeightConfines.MAXIMAL.value)


class WrongHeightError(InitialDataError):
    code = 16
    message = "Please write integer height"


class QuitError(Exception):
    code = 2


class ImagesDimensionError(Exception):
    code = 3
