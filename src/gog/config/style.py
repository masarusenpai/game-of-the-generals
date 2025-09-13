from typing import Callable


BOLD: Callable[[str], str] = lambda target: "\x1b[1m" + target + "\x1b[22m"
BLINK: Callable[[str], str] = lambda target: "\x1b[5m" + target + "\x1b[25m"

BLUE: Callable[[str], str] = lambda target: "\x1b[34m" + target + "\x1b[0m"
GREEN: Callable[[str], str] = lambda target: "\x1b[32m" + target + "\x1b[0m"
RED: Callable[[str], str] = lambda target: "\x1b[31m" + target + "\x1b[0m"
YELLOW: Callable[[str], str] = lambda target: "\x1b[33m" + target + "\x1b[0m"
WHITE: Callable[[str], str] = lambda target: "\x1b[37m" + target + "\x1b[0m"
