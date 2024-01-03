from serial import Serial
from loadyaml import loadyaml
import math
import time
import os

class arduino():
    def __init__(self):
        current_directory = os.getcwd()
        self.config = loadyaml(os.path.join(current_directory, "config.yaml"))
        self.serial_port = self.config["arduino"]["serial_port"]
        self.initialization_message = b"connected"
        self.arduino_connection = Serial(self.serial_port)
        time.sleep(1.5)
        self.arduino_connection.write(b"ADR1")
        self.mr = self.arduino_connection.read_until(b"\r\n")
        print(self.mr.decode())

    def set_direction(self, direction):
        if direction == "Clockwise":
           self.arduino_connection.write(b"NDCL\r")
        if direction == "CounterClockwise":
            self.arduino_connection.write(b"NDCC\r")

       
    def get_value(self,message):
        self.arduino_connection.write(message.encode()+b"\r")
        message_recieved = self.arduino_connection.read_until(b"\r")
        return message_recieved

    def request_encoder_position(self):
        binary_encoder_position_message = self.get_value("CP?")  
        encoder_position_message = binary_encoder_position_message.decode()
        encoder_position = int(encoder_position_message.split()[1])
        position_in_meters = 100*(encoder_position/self.config["encoder"]["pulses_per_revolution"])*2*math.pi*self.config["encoder"]["diameter_cm"]
        return position_in_meters
    
    def set_current_position_as_zero(self):
        current_position = self.get_value("SZ")
        time.sleep(1.5)
        
       
        return current_position
        


            
