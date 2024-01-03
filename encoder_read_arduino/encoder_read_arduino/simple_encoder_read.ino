volatile long encoder_count = 0;
unsigned int  direction = 1;

void setup() {
    attachInterrupt(2,encoder_isr, HIGH);
    Serial.begin(9600);
}

void loop() {
    Serial.println(encoder_count);
}

void encoder_isr() {
    if(direction == 1){
        encoder_count = encoder_count + 1;
    }else if(direction == 0){
        encoder_count = encoder_count - 1;
    }
    
}