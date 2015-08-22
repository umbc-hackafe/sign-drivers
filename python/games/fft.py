import json
import graphics
import driver
import game
import alsaaudio
import numpy as np
import collections
import sys
import time
import math

rows = 15
cols = 112

class FFT(game.Game):
    def __init__(self, *args, **kwargs):
        self.plotMax = 2
        self.offset = 9
        self.plotStart = 5
        self.plotEnd = 100
        self.periodsize = 2400
        self.bufferLength = 4800
        self.sampleRate = 48000
        self.buffer = collections.deque(self.bufferLength*[0], self.bufferLength)

        card = 'default:CARD=Set'
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
        self.inp.setchannels(1)
        self.inp.setrate(self.sampleRate)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.periodsize = self.inp.setperiodsize(self.periodsize)

        for i in range(0, int(self.bufferLength/self.periodsize)):
            self.buffer.extend(np.fromstring(self.inp.read()[1], dtype=">h"))

        with open("./fft_data", "r") as datafile:
            self.noiseOffset = json.loads(datafile.read())

        super().__init__(*args, **kwargs)

    def loop(self):
        datalength, data = self.inp.read()
        if (datalength != self.periodsize):
            return
        self.buffer.extend(np.fromstring(data, dtype="<h"))
        fftData = np.absolute(np.fft.rfft(self.buffer))
        buckets = []
        for i in range(len(fftData)):
            buckets.append(fftData[i]*math.log(i+1))
        buckets = np.array_split(fftData, cols)
        buckets = [math.log(sum(x)/(len(x)+1)+1)-self.offset for x in buckets]
#        with open("./fft_data", "w") as datafile:
#            datafile.write(json.dumps(buckets))
        for i in range(len(buckets)):
            buckets[i] -= self.noiseOffset[i]
        buckets = [min(int((x*rows)/self.plotMax),self.plotMax*rows) for x in buckets]
        self.graphics.buffer = []
        for i in range(rows):
            self.graphics.buffer.append([x>=i for x in buckets])
        self.graphics.buffer.reverse()

        self.graphics.draw(self.serial)

GAME = FFT
