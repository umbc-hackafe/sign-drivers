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

const int serialbuffer[bufferSize];
const int img1[ROWS][COLS];
const int img2[ROWS][COLS];

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
    pinMode(CLOCK, OUTPUT);
    pinMode(ROWDATA, OUTPUT);
    pinMode(COLLOW, OUTPUT);
    pinMode(COLHIGH, OUTPUT);
    pinMode(COL0, OUTPUT);
    pinMode(COL2, OUTPUT);
    pinMode(COL4, OUTPUT);

    currentRow = 0;
    serialEnd = 0;
}

extern "C" int main(void) {
  initialize();
  elapsedMillis refresh;
  int* img = img1;
  int* nimg = img2;
  
  Serial.begin(9600);

  while(1) {
    for(int col = 0; col < COLS; col++) {
      digitalWriteFast(ROWDATA, img[row][col] ? HIGH : LOW);
      digitalWriteFast(CLOCK, HIGH);
      digitalWriteFast(CLOCK, LOW);
    }
    setRow(currentRow);
    currentRow++;
    currentRow %= 15;
    while (refresh < 50) {
      if Serial.available() {
        serialbuffer[serialEnd] = Serial.read();
        serialEnd++;
      }
      if (serialEnd == 2) {
        if ((serialbuffer[0] != 0xCA) | (serialbuffer[1] !- 0xFE)) {
          serialEnd = 0;
        }
      }
      if (serialEnd > 2) {
        if (serialbuffer[3] == 0x00) { //Blit frame
          if (img == img1) {
            img = img2;
            nimg = img1;
          } else {
            img = img1;
            nimg = img2;
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
    refresh -= 50;
  }
}
