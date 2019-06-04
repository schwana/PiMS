#include                 <LiquidCrystal.h>

char inData[2];
byte index = 0;
int holeNumber = 0;
int res = 0;
// initialize the library with the numbers of the interface pins (4-9 used for LCD)
LiquidCrystal           lcd(8, 9, 4, 5, 6, 7);
int incoming = 0;
String str;

int GlobalX;
int GlobalY;

int CurX;
int CurY;

int Xlocations[3] = {100, 200, 300};
int Ylocations[3] = {100, 100, 100};

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.print("Waiting....setup");
  Serial.begin(9600);
  CurX = 0;
  CurY = 0;
  lcd.setCursor(0, 1);
  lcd.print("X:");
  lcd.print(CurX);
  lcd.print(" Y:");
  lcd.print(CurY);
  lcd.setCursor(0, 0);
  delay(3000);
  //On Startup calibrate and move to first standard hole
  //insert function call
}

void loop() {
  int i = 0;
  delay(10);
  //Serial.read();

  while (Serial.available() > 0)
  {
    lcd.clear();
    char inChar = Serial.read();

    if (inChar == '\n')
    {
      index = 0;
      //inData[index] = NULL;
      inData[index] = 0;
    }
    else
    {
      inData[index] = inChar;
      index++;
      inData[index] = '\0';
      int char1 = inData[0] - '0';
      int char2 = inData[1] - '0';
      holeNumber = 10 * char1 + char2;
    }
    if (i == 2)
    {
      lcd.print("Moving to ");
      lcd.print(holeNumber);
      res = sampleMove(holeNumber);

      if (res = 1)
      {
        
        Serial.println('1');

        lcd.print(" ");
        lcd.print(i);
        delay(5000);
        lcd.clear();
        lcd.print("Sample Moved");
        delay(5000);
        lcd.clear();
        lcd.print("waiting...loop");

        lcd.setCursor(0, 1);
        lcd.print("X: ");
        lcd.print(CurX);
        lcd.print(" Y: ");
        lcd.print(CurY);
      }

      
      res = 0;
    }
    i++;

  }

}

int sampleMove(int S)
{
  lcd.setCursor(0, 1);

  int reqX = Xlocations[S - 10];
  int reqY = Ylocations[S - 10];

  int XtoMove = reqX - CurX;
  int YtoMove = reqY - CurY;

  //Dummy stage move code
  do
  {
    delay(500);

    CurX = CurX + 10;
    lcd.setCursor(0, 1);
    lcd.print("X: ");
    lcd.print(CurX);
    lcd.print(" Y: ");
    lcd.print(CurY);
  } while (CurX < XtoMove);

  do
  {
    delay(500);

    CurY = CurY + 10;
    lcd.setCursor(0, 1);
    lcd.print("X: ");
    lcd.print(CurX);
    lcd.print(" Y: ");
    lcd.print(CurY);
  } while (CurY < YtoMove);

  lcd.clear();

  lcd.setCursor(0, 1);
  lcd.print("X: ");
  lcd.print(CurX);
  lcd.print(" Y: ");
  lcd.print(CurY);



  lcd.setCursor(0, 0);
  lcd.print("SampleMove: ");
  lcd.print(S);

  return 1;
}


