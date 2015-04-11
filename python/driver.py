import serial

class SerialDriver:
    def __init__(self, port="/dev/ttyACM0"):
        self.serial = serial.Serial(port=port)

    def draw(self, fb):
        self.serial.write(b"\xCA\xFE\x01")
        self.serial.write(bytes(fb))
        self.serial.write(b"\xCA\xFE\x00")

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

class DummyDriver:
    def __init__(self, stdscr, *args, **kwargs):
        self.stdscr = stdscr

    def draw(self, fb):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "+" + "-" * 112 + "+")
        for i, thing in enumerate(chunks(list(fb), 112), start=1):
            self.stdscr.addstr(i, 0, '|' + ''.join(('#' if n else ' ' for n in thing)) + '|')
        self.stdscr.addstr(16, 0, "+" + "-" * 112 + "+")
        self.stdscr.refresh()

