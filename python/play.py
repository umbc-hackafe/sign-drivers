#!/usr/bin/env python3

import threading
import argparse
import driver
import games
import sys

def fifo_thread(fifo, game):
    with open(fifo) as f:
        while True:
            game.send_input(f.read(1))

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--serial-port", "-s", help="The serial port the teensy is connected to", type=str, default="/dev/ttyACM0")
    parser.add_argument("--fifo", "-f", help="The path to a fifo to use for input", type=str)
    parser.add_argument("--game", "-g", help="The game to play", choices=games.all.keys())
    parser.add_argument("--dummy", "-d", help="Use a dummy terminal output", action="store_true")

    args = parser.pasre_args(argv)

    if args.dummy:
        serial = driver.DummyDriver()
    else:
        serial = driver.SerialDriver(args.serial_port)

    graphics = graphics.Display()
    game = games.all[args.game](graphics, serial)

    if args.fifo:
        input_thread = threading.Thread(target=fifo_Thread, args=(args.fifo, game), daemon=True)
        input_thread.start()

    game.run()

if __name__ == "__main__":
    main(sys.argv[1:])
