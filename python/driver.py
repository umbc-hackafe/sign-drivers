import serial

class SerialDriver:
    def __init__(self, port="/dev/ttyACM0"):
        self.serial = serial.Serial(port=port)

    def draw(self, fb):
        self.serial.write(b"\xCA\xFE\x01")
        self.serial.write(bytes(fb))

