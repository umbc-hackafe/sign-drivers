#!/usr/bin/env python3

import threading
import argparse
import curses
import graphics
import driver
import time
import importlib
import sys
import os

class Play(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.screen = graphics.Display()
        
        self.games = {}
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), "games")):
            if filename.endswith('.py'):
                modname = filename[:-3]
                self.games[modname] = (lambda modname: lambda: importlib.import_module('games.' + modname))(modname)
        

    def fifo_thread(self, fifo):
        with open(fifo) as f:
            while True:
                i = f.read(1)
                if i:
                    self.game.send_input(i)
                else:
                    time.sleep(.01)

    def stdin_thread(self):
        while True:
            chars = input()
            for char in chars:
                self.game.send_input(char)

    def exec_game(self, name):
        self.game.stop()
        self.game_name = name

    def run(self, args):
        if args.dummy:
            self.serial = driver.DummyDriver(self.stdscr)
        elif args.flaschen:
            self.serial = driver.FlaschenDriver(args.flaschen)
        else:
            self.serial = driver.SerialDriver(args.serial_port)

        self.game_name = args.game
        
        if args.fifo:
            self.input_thread = threading.Thread(target=self.fifo_thread, args=(args.fifo,), daemon=True)
            self.input_thread.start()
        elif args.stdin:
            self.input_thread = threading.Thread(target=self.stdin_thread, daemon=True)
            self.input_thread.start()

        while True:
            self.game = self.games[self.game_name]().GAME(self.screen, self.serial, self.stdscr, self)
            self.game.run()

def main(stdscr, argv):
    stdscr.nodelay(True)

    play = Play(stdscr)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--serial-port", "-s", help="The serial port the teensy is connected to", type=str, default="/dev/ttyACM0")
    parser.add_argument("--fifo", "-f", help="The path to a fifo to use for input", type=str)
    parser.add_argument("--stdin", "-i", help="Read input from stdin", action="store_true")
    parser.add_argument("--game", "-g", help="The game to play", choices=play.games.keys(), default='menu')
    parser.add_argument("--dummy", "-d", help="Use a dummy terminal output", action="store_true")
    parser.add_argument("--flaschen", "-t", help="Output to a flaschen-taschen server", type=str, default="")

    args = parser.parse_args(argv)

    play.run(args)

if __name__ == "__main__":
    curses.wrapper(main, sys.argv[1:])
