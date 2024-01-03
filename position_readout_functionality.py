from position_readout import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from arduino_dev_AM3 import arduino
from loadyaml import loadyaml
import time
import os


class functional_app(Ui_MainWindow):
    def setup_functionality(self):
        current_directory = os.getcwd()
        self.config = loadyaml(os.path.join(current_directory,"config.yaml"))
        self.position_reporting_status = 0
        self.direction = "Clockwise"
        self.old_direction = self.direction
        self.set_zero_bit = 0
        self.arduino = arduino()
        self.encoder_timer = QtCore.QTimer()
        self.encoder_timer.timeout.connect(self.position_report_loop)
        self.begin_button.clicked.connect(self.toggle_position_reporting)
        self.zero_button.clicked.connect(self.set_zero)
        self.direction_button.clicked.connect(self.set_direction)
        self.readout_display.display(0.0)
        self.setup_set_zero_popup()
        self.setup_set_direction_popup()

    def position_report_loop(self):
        if self.old_direction != self.direction:
            self.arduino.set_direction(self.direction)
        if self.set_zero_bit == 1:
            current_position = self.arduino.set_current_position_as_zero()
            
            self.set_zero_bit = 0
        encoder_position = self.arduino.request_encoder_position()
        self.readout_display.display(encoder_position)

    def toggle_position_reporting(self):
        self.position_reporting_status=self.position_reporting_status^1
        if self.position_reporting_status == 1 :
            self.position_report_loop()
            self.encoder_timer.start(self.config["arduino"]["period_between_samples_mili_seconds"])
            self.begin_button.setText("Stop Reporting Position")

        elif self.position_reporting_status == 0:
            self.begin_button.setText("Start Reporting Position")
            self.encoder_timer.stop()
    
    def set_zero(self):
        self.zero_popup_box.exec_()
    
    def set_direction(self):
        self.direction_popup_box.exec()
    
    def setup_set_zero_popup(self):
        self.zero_popup_box = QtWidgets.QMessageBox()
        self.zero_popup_box.setText("Would you like to set the current encoder position as Zero?")
        self.zero_popup_box.setIcon(QtWidgets.QMessageBox.Question)
        self.zero_popup_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.zero_popup_box.setDefaultButton(QtWidgets.QMessageBox.No)
        self.zero_popup_box.buttonClicked.connect(self.set_zero_popup_button_handler)
    
    def setup_set_direction_popup(self):
        self.direction_popup_box = QtWidgets.QMessageBox()
        self.direction_popup_box.setText("What Direction is the motor rotating in?")
        clockwise_button = self.direction_popup_box.addButton("Clockwise", QtWidgets.QMessageBox.AcceptRole)
        counterclockwise_button = self.direction_popup_box.addButton("Counter Clockwise", QtWidgets.QMessageBox.RejectRole)
        self.direction_popup_box.buttonClicked.connect(self.set_direction_popup_button_handler)

    def set_direction_popup_button_handler(self,button_pressed):
        self.old_direction = self.direction
        if button_pressed == "Clockwise":
            self.direction = "Clockwise"
            print("lol")
        elif button_pressed == "Counter Clockwise":
            self.direction = "CounterClockwise"

    def set_zero_popup_button_handler(self, button_pressed):
        if button_pressed == "Yes":
            self.set_zero_bit = 1
            print("lol")
        elif button_pressed == "No":
            self.zero_popup_box.close()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = functional_app()
    ui.setupUi(MainWindow)
    
    MainWindow.show()
    ui.setup_functionality()
    sys.exit(app.exec_())      



