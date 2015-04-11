#!/usr/bin/env python2
from __future__ import print_function
import argparse
import cwiid
import time

def get_wiimote():
    wm = None
    while(wm is None):
        try:
            wm = cwiid.Wiimote()
        except RuntimeError as e:
            print(e)
            print('Trying again...')
            
    print('Connected!')
    wm.rpt_mode = cwiid.RPT_BTN
    wm.rumble = True
    time.sleep(0.25)
    wm.rumble = False

    wm.led = 11

    return wm

def main(args):
    with open(args.fifo, 'wb', buffering=0) as fifo:
        wm = get_wiimote()

        old_buttons = wm.state['buttons']
        while True:
            buttons = wm.state['buttons']
            
            if (buttons & cwiid.BTN_RIGHT) and not (old_buttons & cwiid.BTN_RIGHT):
                fifo.write('D')
            if (buttons & cwiid.BTN_LEFT) and not (old_buttons & cwiid.BTN_LEFT):
                fifo.write('A')
            if (buttons & cwiid.BTN_UP) and not (old_buttons & cwiid.BTN_UP):
                fifo.write('W')
            if (buttons & cwiid.BTN_DOWN) and not (old_buttons & cwiid.BTN_DOWN):
                fifo.write('S')
                
            if (old_buttons & cwiid.BTN_RIGHT) and not (buttons & cwiid.BTN_RIGHT):
                fifo.write('d')
            if (old_buttons & cwiid.BTN_LEFT) and not (buttons & cwiid.BTN_LEFT):
                fifo.write('a')
            if (old_buttons & cwiid.BTN_UP) and not (buttons & cwiid.BTN_UP):
                fifo.write('w')
            if (old_buttons & cwiid.BTN_DOWN) and not (buttons & cwiid.BTN_DOWN):
                fifo.write('s')
                
            old_buttons = buttons

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fifo')
    parser.add_argument('--delay', type=float, default=0.25)
    main(parser.parse_args())
