// include the library code:
#include <LiquidCrystal.h>
#include <math.h>

float serial_time = 0.5; // # of seconds to wait before printing to serial.
float last_serial_time = 0.;
int x = 0;
int currx = 1023;
String btnStr = "None";
float frac_saved = 0.01;//# of saved 
float frac_saved_deriv = 0.001;//# of saved 
float running_temp=75.0;
float running_temp_old=0.0;
float running_deriv = 0.0;
int counter = 0;
float t_setpoint = 75.0;
int outpin = 13;
float p=6.0;
float kI = .00025;
float kD = 30000;
float integral = 0.0;
float deriv = 0.0;
float num_sec = 10.0;
float timers = millis();
float timers0 = millis();
float timers_last = millis();
float controlvar = 0.0;
float current_controlvar = 0.0;
int controlmode = 0;
float percent = 0;
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.clear();
  lcd.setCursor(0,0);
  //lcd.print("Analog 0: ");
  //lcd.print(currx);
  //lcd.setCursor(0,1);
  //lcd.print(btnStr);
  Serial.begin(9600);
  timers = millis();
  Serial.println(timers);
  pinMode(outpin, OUTPUT);
  digitalWrite(outpin, HIGH);
}

void loop() {
  timers_last = timers;
  timers = millis();
  
  int sensorValue = analogRead(A1);
  // print out the value you read:
  float voltage = sensorValue / 1024. * 5.0;
  float resistance = voltage/5.0*10000.0 / (1-voltage/5.0);
  float temperature = 6.547E3 / (log(resistance / 4.9E-2))-459.0;
  running_temp_old = running_temp;
  running_temp = running_temp*(1-frac_saved)+frac_saved*temperature;
  running_deriv = running_deriv*(1-frac_saved_deriv)+frac_saved_deriv*(running_temp - running_temp_old); //Should probably divide the deltaT by the delta time to normalize performance
  deriv = kD*running_deriv;/// (timers - timers_last);
  integral = integral + kI*(timers - timers_last)*(t_setpoint - running_temp);
  if(integral>100){
    integral = 100;
  }
  else  if(integral<=-100){
    integral = -100;
  }
  if(deriv>100){
    deriv=100;
  }
  else if(deriv<=-100){
    deriv=-100;
  }
  controlvar = p*(t_setpoint - running_temp)+integral - deriv;//p*(t_setpoint - running_temp)*(1-frac_saved)+frac_saved*controlvar;
  if(controlvar>100){
    controlvar=100.;
  }
  else if(controlvar<=0){
    controlvar=0;
  }
  if(controlmode==1){
    controlvar = percent;
  }
  //millis()num_sec; timers;
  

  if((timers-timers0)>=num_sec*1000){
    timers0 = timers;
    current_controlvar = controlvar;
  }
  else if((timers - timers0)>num_sec*1000*current_controlvar/100.){
    digitalWrite(outpin, LOW);
  }
  else if((timers - timers0)<num_sec*1000*current_controlvar/100.){
    digitalWrite(outpin, HIGH);
  }
  
//  if(timers-last_serial_time>serial_time*1000.){
//    last_serial_time = timers;
//    Serial.print(timers/1000.);
//    Serial.print(",");
//    Serial.print(t_setpoint);
//    Serial.print(",");
//    Serial.print(running_temp);
//    Serial.print(",");
//    Serial.print(p*(t_setpoint - running_temp));
//    Serial.print(",");
//    Serial.print(integral);
//    Serial.print(",");
//    Serial.print(deriv);
//    Serial.print(",");
//    Serial.print(controlvar);
//    Serial.println(",");
//  }





  if(counter==50){
    lcd.clear();
    
    if(controlmode==0){
      lcd.setCursor(0,0);
      lcd.print("T_read(F): ");
      lcd.print(running_temp);
      lcd.setCursor(0,1);
      lcd.print("T_stpt(F): ");
      //  lcd.setCursor(0,1);
      lcd.print(t_setpoint);
    }
    else{
      lcd.setCursor(0,1);
      lcd.print("% on: ");
    }
    counter=0;
  }
  else{
    counter++;
  }

  x = analogRead(A0); // the buttons are read from the analog0 pin

  // Check if x has changed
  if (x != 1023){
    // && (x != currx))

    //update screen and change currx
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("T_read(F): ");
      lcd.print(running_temp);
      currx = x;

  }
  
  
    if (currx > 620 && currx < 660){
      btnStr="Select";
      Serial.println("5");
      if(controlmode==0){
        controlmode=1;
      }
      else {
        controlmode=0; 
      }
      
    } 
    else if (currx > 400 && currx < 420){

      btnStr="Left";

    } 
    else if (currx < 40){

      btnStr="Right";

    } 
    else if (currx > 90 && currx < 110){

      btnStr="Up";
      if(controlmode==0){
        t_setpoint = t_setpoint + 0.1;
      }
      else{
        percent = percent+1;
      }
        
    } 
    else if (currx > 250 && currx < 270){

      btnStr="Down";
      if(controlmode==0){
      t_setpoint = t_setpoint - 0.1;
      }
      else{
        percent = percent-1;
      }
    }
  
    

    //update button pressed
    lcd.setCursor(0,1);
    if(controlmode==0){
      lcd.print("T_stpt(F): ");
      lcd.print(t_setpoint);
    }
    else {
      lcd.print("%on: ");
      lcd.print(percent);
    }
    
    //  lcd.setCursor(0,1);
  

  

  Serial.println(controlmode);
  delay(10);

}

