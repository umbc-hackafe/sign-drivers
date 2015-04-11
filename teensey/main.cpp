#define CLOCK 1
#define ROWDATA 2

#define col(i) (i - COLLOW)
#define COLLOW 3
#define COLHIGH 4
#define COL4 5
#define COL2 6
#define COL0 7

#define ROWS 15
#define COLS 112

const int output[][] = {
    {HIGH,  LOW,  LOW,  LOW,  LOW},
    {HIGH,  LOW,  LOW,  LOW, HIGH},
    {HIGH,  LOW,  LOW, HIGH,  LOW},
    {HIGH,  LOW,  LOW, HIGH, HIGH},
    {HIGH,  LOW, HIGH,  LOW,  LOW},
    {HIGH,  LOW, HIGH,  LOW, HIGH},
    {HIGH,  LOW, HIGH, HIGH,  LOW},
    {HIGH,  LOW, HIGH, HIGH, HIGH},
    { LOW, HIGH,  LOW,  LOW,  LOW},
    { LOW, HIGH,  LOW,  LOW, HIGH},
    { LOW, HIGH,  LOW, HIGH,  LOW},
    { LOW, HIGH,  LOW, HIGH, HIGH},
    { LOW, HIGH, HIGH,  LOW,  LOW},
    { LOW, HIGH, HIGH,  LOW, HIGH},
    { LOW, HIGH, HIGH, HIGH,  LOW},
    { LOW, HIGH, HIGH, HIGH, HIGH},
};

const int img[ROWS][COLS];

int row;

void setup() {
    pinModeFast(CLOCK, OUTPUT);
    pinModeFast(ROWDATA, OUTPUT);
    pinModeFast(COLLOW, OUTPUT);
    pinModeFast(COLHIGH, OUTPUT);
    pinModeFast(COL0, OUTPUT);
    pinModeFast(COL2, OUTPUT);
    pinModeFast(COL4, OUTPUT);

    row = 0;
}

void loop() {
    for(int col = 0; col < COLS; col++) {
        digitalWriteFast(ROWDATA, img[row][col] ? HIGH : LOW);
        digitalWriteFast(CLOCK, HIGH);
        digitalWriteFast(CLOCK, LOW);
    }

    digitalWriteFast(COLLOW, output[row][col(COLLOW)]);
    digitalWriteFast(COLHIGH, output[row][col(COLHIGH)]);
    digitalWriteFast(COL0, output[row][col(COL0)]);
    digitalWriteFast(COL2, output[row][col(COL2)]);
    digitalWriteFast(COL4, output[row][col(COL4)]);

    delay(100);

    digitalWriteFast(COLLOW, LOW);
    digitalWriteFast(COLHIGH, LOW);
    digitalWriteFast(COL0, LOW);
    digitalWriteFast(COL2, LOW);
    digitalWriteFast(COL4, LOW);
}
