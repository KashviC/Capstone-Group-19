byte Abstr[2][6] = {
  {0,0,1,1,1,0},
  {0,0,0,0,0,1}
};
byte FmStr[2][6] = {
  {1,1,1,1,1,1},
  {0,1,1,0,0,0}
};
byte EbStr[3][6] = {
  {0,0,1,0,0,0},
  {0,0,0,1,0,1},
  {0,0,0,0,1,0}
};
byte GStr[2][6] = {
  {0,1,0,0,0,0},
  {1,0,0,0,0,1}
};
byte CStr[3][6] = {
  {0,0,0,0,1,0},
  {0,0,1,0,0,0},
  {0,1,0,0,0,0}
};
byte DStr[2][6] = {
  {0,0,0,1,0,1},
  {0,0,0,0,1,0}
};
byte EStr[2][6] = {
  {0,0,0,1,0,0},
  {0,1,1,0,0,0}
};
byte AStr[1][6] = {
  {0,0,1,1,1,0}
};
byte AmStr[2][6] = {{0,0,0,0,1,0},{0,0,1,1,0,0}};
byte EmStr[1][6] = {
  {0,1,1,0,0,0}
};
byte DmStr[3][6] = {
  {0,0,0,0,0,1},
  {0,0,0,1,0,0},
  {0,0,0,0,1,0}
};
byte FrtList [11][3] = {
  {1,4,0}, // Ab
  {1,3,0}, // Fm
  {1,3,4}, //Eb
  {2,3,0}, // G
  {1,2,3}, // C
  {2,3,0}, // D
  {1,2,0}, // E
  {2,0,0}, // A
  {1,2,0}, // Am
  {2,0,0}, // Em
  {1,2,3} // Dm
};

int pinArray[6] = {5,6,7,8,9,10};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); 
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}

void loop() {
  for (byte j=0; j < 6; j++) {
    int pinInd = pinArray[j];
    int stringVal = AStr[0][j];
    if (stringVal == 1) {
      digitalWrite(pinInd, HIGH);
    }
    delay(100);
  }
  delay(10000);
}
