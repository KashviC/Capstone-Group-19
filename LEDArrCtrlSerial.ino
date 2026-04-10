#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1:
#define LED_PIN    6

// How many NeoPixels are attached to the Arduino?
#define LED_COUNT 144

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
String InBytes;
// chord tables
byte AbStr[2][6] = {
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
  {1,3,4}, // Eb
  {2,3,0}, // G
  {1,2,3}, // C
  {2,3,0}, // D
  {1,2,0}, // E
  {2,0,0}, // A
  {1,2,0}, // Am
  {2,0,0}, // Em
  {1,2,3} // Dm
};

void setup() {
  strip.begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
  strip.show();            // Turn OFF all pixels ASAP
  strip.setBrightness(70); // Set BRIGHTNESS to about 1/5 (max = 255)
  Serial.begin(9600);
}

void loop() {
byte astrin[3] = {0,0,0};
byte emstrin[3] = {0,0,0};
byte dmstrin[3] = {0,0,0};
byte cstrin[3] = {0,0,0};

if (Serial.available()>0) {
  InBytes = Serial.readStringUntil('\n');
  int chordInt = 0;
  if (InBytes == NULL) {
    digitalWrite(LED_BUILTIN,LOW);
    Serial.write("Led off, chord detected:");
    strip.clear();
    strip.show();
  }
  else {
    digitalWrite(LED_BUILTIN,HIGH);
    Serial.write("Led on, chord detected:");
    chordInt = InBytes.toInt(); 
  }
  switch (chordInt) {
    case 0:
      strip.clear();
      strip.show();
      break;
    case 1:
      chordAddr(FrtList[0], AbStr);
      break;
    case 2:
      chordAddr(FrtList[1], FmStr);
      break;
    case 3:
      chordAddr(FrtList[2], EbStr);
      break;
    case 4:
      chordAddr(FrtList[3], GStr);
      break;
    case 5:
      chordAddr(FrtList[4], CStr);
      break;
    case 6:
      chordAddr(FrtList[5], DStr);
      break;
    case 7:
      chordAddr(FrtList[6], EStr);
      break;
    case 8:
      chordAddr(FrtList[7], AStr);
      break;
    case 9:
      chordAddr(FrtList[8], AmStr);
      break;
    case 10:
      chordAddr(FrtList[9], EmStr);
      break;
    case 11:
      chordAddr(FrtList[10], DmStr);
      break;
  }

}
}

void chordAddr(byte chord[], byte strings[][6]) { //  'b' counts from 0 to 2...
  strip.clear();
  int pixel = 0;
  int start = 0;
  int r;
  int b;
  int g;

  for(int i=0; i<3; i++) {
    if(chord[i] != 0) {
      for(int s=0; s<6; s++) {
        if(strings[i][s] == 1) {
          pixel = (6*(chord[i]-1)) + s*(chord[i]%2)+(6-s-1)*((chord[i]+1)%2);
          Serial.println(pixel);
          Serial.println(chord[i]);
          switch (s*(chord[i]%2)+(6-s-1)*((chord[i]+1)%2)) {
          case 0:
              r=255;
              g=0;
              b=0;
              break; 
          case 1:
              r=255;
              g=255;
              b=0;
              break;
          case 2:
              r=0;
              g=0;
              b=255;
              break; 
          case 3:
              r=255;
              g=90;
              b=0;
              break;
          case 4:
              r=0;
              g=255;
              b=0;
              break; 
          case 5:
              r=128;
              g=0;
              b=128;
          break;}
          strip.setPixelColor(pixel,r ,g ,b );
          strip.show();
        } else {
          continue;
        }
      } 
    }
    else {
      continue;
    }
  }
}



