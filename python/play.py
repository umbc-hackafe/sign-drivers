#!/usr/bin/env python3

import threading
import argparse
import graphics
import driver
import imp
import sys
import os

def fifo_thread(fifo, game):
    with open(fifo) as f:
        while True:
            game.send_input(f.read(1))

def load(path):
    sys.path.insert(0, os.path.abspath(path))

    print("Loading from {}".format(path))
    files = []
    for _, _, f in os.walk(path):
        files.extend(f)
        break

    modules = {}
    for f in files:
        if f.startswith(".") or f.endswith("~") or f.endswith("#"):
            continue
        name = os.path.splitext(f)[0]
        modules[name] = imp.load_source(name, os.path.join(path, f))
    return modules

def main(argv):
    print(os.path.join(os.path.dirname(__file__), 'games'))
    games = load(os.path.join(os.path.dirname(__file__), "games"))

    parser = argparse.ArgumentParser()
    parser.add_argument("--serial-port", "-s", help="The serial port the teensy is connected to", type=str, default="/dev/ttyACM0")
    parser.add_argument("--fifo", "-f", help="The path to a fifo to use for input", type=str)
    parser.add_argument("--game", "-g", help="The game to play", choices=games.keys())
    parser.add_argument("--dummy", "-d", help="Use a dummy terminal output", action="store_true")

    args = parser.parse_args(argv)

    if args.dummy:
        serial = driver.DummyDriver()
    else:
        serial = driver.SerialDriver(args.serial_port)

    screen = graphics.Display()
    game = games[args.game].GAME(screen, serial)

    if args.fifo:
        input_thread = threading.Thread(target=fifo_Thread, args=(args.fifo, game), daemon=True)
        input_thread.start()

    game.run()

if __name__ == "__main__":
    main(sys.argv[1:])
