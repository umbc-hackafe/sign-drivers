import serial

class SerialDriver:
    def __init__(self, port="/dev/ttyACM0"):
        self.serial = serial.Serial(port=port)

    def draw(self, fb):
        self.serial.write(b"\xCA\xFE\x01")
        self.serial.write(bytes(fb))

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

class DummyDriver:
    def __init__(self, *args, **kwargs):
        pass

    def draw(self, fb):
        for thing in chunks(fb, 112):
            print(''.join(('#' if n else ' ' for n in thing)))
        print()
