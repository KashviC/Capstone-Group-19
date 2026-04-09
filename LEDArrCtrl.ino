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

// chord tables
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
Serial.println("assign chord indexes");
for(int i=0; i < 3; i++) {
  astrin[i] = FrtList[7][i];
  Serial.println(astrin[i]);
  delay(1000);
  emstrin[i] = FrtList[9][i];
  Serial.println(emstrin[i]);
  delay(1000);
  dmstrin[i] = FrtList[10][i];
  cstrin[i] = FrtList[4][i];
}
Serial.println("chord indices finished");
chordAddr(dmstrin, DmStr);
delay(1000);
chordAddr(cstrin, CStr);
delay(1000);
chordAddr(astrin, AStr);
delay(1000);
chordAddr(emstrin,EmStr);
delay(1000);
chordAddr(dmstrin, DmStr);
delay(1000);
chordAddr(cstrin, CStr);
delay(1000);
chordAddr(astrin, AStr);
delay(1000);
chordAddr(emstrin,EmStr);
delay(1000);
}

void chordAddr(byte chord[], byte strings[][6]) { //  'b' counts from 0 to 2...
  strip.clear();
  int pixel = 0;
  int start = 0;
  for(int i=0; i<3; i++) {
    if(chord[i] != 0) {
      for(int s=0; s<6; s++) {
        if(strings[i][s] == 1) {
          pixel = (6*(chord[i]-1)) + s*(chord[i]%2)+(5-s)*((chord[i]+1)%2);
          Serial.println(pixel);
          Serial.println(chord[i]);
          strip.setPixelColor(pixel, 255, 0, 255);
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

