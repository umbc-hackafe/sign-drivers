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
    def __init__(self, *args, **kwargs):
        pass

    def draw(self, fb):
        print("+" + "-"*112, "+")
        for thing in chunks(list(fb), 112):
            print('|' + ''.join(('#' if n else ' ' for n in thing)) + '|')
        print("+" + "-"*112, "+")
        print()
