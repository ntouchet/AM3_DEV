

String innit_message = "ADR1";
String recieved_message = "";
String position_message = "";
volatile long encoder_count = 0;
volatile uint8_t encoder_status = 0;



void setup() {
  attachInterrupt(digitalPinToInterrupt(2),encoder_isr,CHANGE);
  attachInterrupt(digitalPinToInterrupt(3),encoder_isr,CHANGE);
  encoder_status = (PIND & 0b1100);
  
  Serial.begin(9600);
//  recieved_message = Serial.readStringUntil('\r');
//  while(recieved_message != innit_message){
//    recieved_message = Serial.readStringUntil('\r');
//  }
//  
//  message_handler(recieved_message);
}

void loop() {
//  // put your main code here, to run repeatedly:
//  if( Serial.available()){
//    recieved_message = Serial.readStringUntil('\r');
//    message_handler(recieved_message);
//  }
//}
//
//void message_handler(String message){
// if (message.indexOf("CP?")!=-1){
//    
//    Serial.print("CP ");
//    Serial.println(encoder_count);
// }else if (message.indexOf("ADR1") != -1){
//  Serial.println("connected");
//  }else if (message.indexOf("SZ") != -1){
//    encoder_count = 0;
//  }
 Serial.println(encoder_count);
}


void encoder_isr(){
  static int8_t position_addition_values[] = {0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0};
  
  static uint8_t pinstate = 0;

  Serial.println("Hello");
  encoder_status = encoder_status >> 2;
  pinstate = PIND & 0b1100;
  encoder_status = encoder_status | pinstate;
  encoder_count = encoder_count + position_addition_values[encoder_status & 0b1111];
}
