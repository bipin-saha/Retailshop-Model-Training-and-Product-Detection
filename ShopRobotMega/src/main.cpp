#include<Arduino.h>
#include<ArduinoJson.h>

void setup() {
  Serial.begin(9600);  
}


void loop() 
{
  
  if (Serial.available()) {
    String message = "";    
    while (Serial.available()) 
    {
      message += (char)Serial.read();
      delay(10);
    }
    
    String message_string = String(message);

    DynamicJsonDocument command(4096);
    deserializeJson(command, message_string);
    
    String instruction = command["instruction"];
    String product_map = command["product_map"];
    String remarks = command["remarks"];

    Serial.println(remarks);
    Serial.println(product_map);
    Serial.println(instruction);    
    
  }
}