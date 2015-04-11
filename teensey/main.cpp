#include "teensy3/WProgram.h"
#include "teensy3/core_pins.h"
#include "teensy3/usb_serial.h"

#define ROWS 15
#define COLS 112

#define SYNC 10
#define CLK 11
#define DAT 12
#define HIBANK 3
#define LOBANK 4
#define BIT0 0
#define BIT1 1
#define BIT2 2

#define bufferSize 2048

int serialbuffer[bufferSize];
int img1[ROWS][COLS];
int img2[ROWS][COLS];

int currentRow;
int serialEnd;

void setRow(int row) {
  digitalWrite(LOBANK, HIGH);
  digitalWrite(HIBANK, HIGH);
  digitalWrite(BIT0, row & 1);
  digitalWrite(BIT1, row & 2);
  digitalWrite(BIT2, row & 4);
  if ((row < 8) & (row < 16) & (row >= 0)) {
    digitalWrite(HIBANK, LOW);
  } else if ((row >= 8) & (row < 16)) {
    digitalWrite(LOBANK, LOW);
  }
}

void initialize() {
    pinMode(CLK, OUTPUT);
    pinMode(DAT, OUTPUT);
    pinMode(LOBANK, OUTPUT);
    pinMode(HIBANK, OUTPUT);
    pinMode(BIT0, OUTPUT);
    pinMode(BIT1, OUTPUT);
    pinMode(BIT2, OUTPUT);
    pinMode(SYNC, OUTPUT);
    pinMode(13, OUTPUT);

    currentRow = 0;
    serialEnd = 0;
}

extern "C" int main(void) {
  initialize();
  elapsedMillis refresh = 0;
  int* img = (int*)img1;
  int *nimg = (int*)img2;
  
  int ledState = 0;

  Serial.begin(9600);

  while(1) {
    setRow(16);
    digitalWrite(SYNC, currentRow);
    for(int col = 0; col < COLS; col++) {
      digitalWrite(DAT, img[currentRow*COLS + col] ? HIGH : LOW);
      digitalWrite(CLK, LOW);
      delayMicroseconds(2);
      digitalWrite(CLK, HIGH);
    }
    setRow(ROWS - currentRow - 1);
    currentRow++;
    currentRow %= 16;
    for (int i=0; i<118; i++) {
      if (Serial.available()) {
        digitalWrite(13, HIGH);
        serialbuffer[serialEnd] = Serial.read();
        serialEnd++;
      }
      if (serialEnd == 1) {
        if (serialbuffer[0] != 0xCA) {
          digitalWrite(13, LOW);
          serialEnd = 0;
        }
      }
      if (serialEnd == 2) {
        if (serialbuffer[1] != 0xFE) {
          digitalWrite(13, LOW);
          serialEnd = 0;
        }
      }
      if (serialEnd > 2) {
        if (serialbuffer[2] == 0x00) { //Blit frame
          digitalWrite(13, LOW);
          if (img == (int*)img1) {
            img = (int*)img2;
            nimg = (int*)img1;
          } else {
            img = (int*)img1;
            nimg = (int*)img2;
          }
          serialEnd = 0;
        }
        if ((serialbuffer[2] == 0x01) & (serialEnd == COLS*ROWS+3)) {
          for (int i=0; i<COLS*ROWS; i++) {
            nimg[i] = serialbuffer[i+3];
          }
          digitalWrite(13, LOW);
          serialEnd = 0;
        }
      }
      if (serialEnd > bufferSize) {
        digitalWrite(13, LOW);
        serialEnd = 0;
      }
    } 
    refresh = 0;
  }
}
