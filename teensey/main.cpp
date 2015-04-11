#include "teensy3/WProgram.h"
#include "teensy3/core_pins.h"
#include "teensy3/usb_serial.h"

#define ROWS 15
#define COLS 112

#define CLK 11
#define DAT 12
#define HIBANK 3
#define LOBANK 4
#define BIT0 0
#define BIT1 1
#define BIT2 2

#define bufferSize 512

int serialbuffer[bufferSize];
int img1[ROWS][COLS];
int img2[ROWS][COLS];

int currentRow;
int serialEnd;

void setRow(int row) {
  if (row < 8 & row < 16) {
    digitalWriteFast(HIBANK, LOW);
    digitalWriteFast(LOBANK, HIGH);
  } else if (row < 16) {
    digitalWriteFast(HIBANK, HIGH);
    digitalWriteFast(LOBANK, LOW);
  } else {
    digitalWriteFast(HIBANK, LOW);
    digitalWriteFast(LOBANK, LOW);
  }
  digitalWriteFast(BIT0, row & 1);
  digitalWriteFast(BIT1, row & 2);
  digitalWriteFast(BIT2, row & 4);
}

void initialize() {
    pinMode(CLK, OUTPUT);
    pinMode(DAT, OUTPUT);
    pinMode(LOBANK, OUTPUT);
    pinMode(HIBANK, OUTPUT);
    pinMode(BIT0, OUTPUT);
    pinMode(BIT1, OUTPUT);
    pinMode(BIT2, OUTPUT);

    currentRow = 0;
    serialEnd = 0;
}

extern "C" int main(void) {
  initialize();
  elapsedMillis refresh = 0;
  int* img = (int*)img1;
  int *nimg = (int*)img2;
  
  Serial.begin(9600);

  while(1) {
    for(int col = 0; col < COLS; col++) {
      digitalWriteFast(DAT, img[currentRow*ROWS + col] ? HIGH : LOW);
      digitalWriteFast(CLK, HIGH);
      digitalWriteFast(CLK, LOW);
    }
    setRow(currentRow);
    currentRow++;
    currentRow %= 15;
    while (refresh < 10) {
      if (Serial.available()) {
        serialbuffer[serialEnd] = Serial.read();
        serialEnd++;
      }
      if (serialEnd == 2) {
        if ((serialbuffer[0] != 0xCA) | (serialbuffer[1] != 0xFE)) {
          serialEnd = 0;
        }
      }
      if (serialEnd > 2) {
        if (serialbuffer[3] == 0x00) { //Blit frame
          if (img == (int*)img1) {
            img = (int*)img2;
            nimg = (int*)img1;
          } else {
            img = (int*)img1;
            nimg = (int*)img2;
          }
          serialEnd = 0;
          currentRow = 0;
        }
        if ((serialbuffer[3] == 0x01) & (serialEnd == COLS*ROWS+3)) {
          for (int i=0; i<COLS*ROWS; i++) {
            nimg[i] = serialbuffer[i+3];
          }
        }
      }
      if (serialEnd > bufferSize) {
        serialEnd = 0;
      }
    } 
    setRow(16);
    refresh -= 10;
  }
}
