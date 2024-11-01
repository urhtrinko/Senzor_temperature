import sys
import serial
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QDialog, QMessageBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# trying to imporve .exe loading time by using the Agg backend, wich dosen't have the as many user
# interaction capabilities.
import matplotlib
matplotlib.use('Agg')  # Switch to Agg backend for faster rendering
import matplotlib.pyplot as plt
import serial.tools.list_ports
import time
import random
from datetime import datetime

# Import the generated Python GUI class
from parameters_dialog_box import Ui_Dialog
# from parameters_widget import Ui_Form # Widget
from temp_sensor_main_window import Ui_MainWindow # Main window

# class for dialog box functionality
class ParamWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()  # Initialize the side window
        self.ui.setupUi(self)
    
        # Access to parent (main window)
        self.main_window = parent
        
        # self.port = str(self.ui.lineEdit_serialPort.text())
        # self.baud_rate = int(self.ui.lineEdit_baudRate.text())

        # parameters written in qLineEdit
        self.ui.lineEdit_serialPort.setText(str(self.main_window.port))
        self.ui.lineEdit_baudRate.setText(str(self.main_window.baud_rate))
        self.ui.lineEdit_Dt.setText(str(self.main_window.D_t))
        self.ui.lineEdit_measureInterval.setText(str(self.main_window.measure_interval/1000)) # get value in secs
        if self.main_window.simulation_mode:
            self.ui.radioButton_simOn.setChecked(True)
        else:
            self.ui.radioButton_simOff.setChecked(True)

        # Connect the 'Save' button in the side window
        self.ui.btnSave.clicked.connect(self.save_changes)
        # close the dialog box
        self.ui.btnCancel.clicked.connect(self.reject)
    
    # Function to update measure_interval and restart the timer
    def update_measure_interval(self, new_interval):
        # Stop the current timer
        self.main_window.timer.stop()

        # Update the measure_interval
        self.main_window.measure_interval = new_interval

        # Restart the timer with the new interval
        self.main_window.timer.setInterval(int(self.main_window.measure_interval))  # Set the new interval
        self.main_window.timer.start()  # Start the timer again with the new interval

    def save_changes(self):
        # save new parameters
        try:
            # check radio buttons, which determine if the data is being simulated (True) or measured (False)
            if self.ui.radioButton_simOff.isChecked(): # measurement
                self.main_window.simulation_mode = False
            else: # simulation
                self.main_window.simulation_mode = True
            # new serial port
            new_port = str(self.ui.lineEdit_serialPort.text())
            if new_port != self.main_window.port:
                self.main_window.port = new_port
            new_baud_rate = int(self.ui.lineEdit_baudRate.text())
            if new_baud_rate != self.main_window.baud_rate:
                self.main_window.baud_rate = new_baud_rate
            # Pass the settings back to the main window and close the dialog
            self.main_window.update_serial_settings(self.main_window.port, self.main_window.baud_rate)
            # new time window
            new_D_t = float(self.ui.lineEdit_Dt.text())
            if new_D_t != self.main_window.D_t: # only print message when there is a change
                self.main_window.D_t = new_D_t  # Update the D_t value in the main window
                self.main_window.ui.messageDisplay.append(f'Time window updated to {new_D_t} seconds.\n')
            # new measurement interval
            new_measure_interval = float(self.ui.lineEdit_measureInterval.text()) # in secs
            if new_measure_interval*1000 != self.main_window.measure_interval:
                # self.main_window.measure_interval = new_measure_interval*1000 # in msecs !
                self.update_measure_interval(new_measure_interval*1000)
                self.main_window.ui.messageDisplay.append(f'Measure interval updated to {new_measure_interval} seconds.\n')
            # Close the side window after saving
            self.accept()
        except ValueError:
            self.main_window.ui.messageDisplay.append('Invalid input\n')

# calss for main window functionality
class TemperaturePlot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load the GUI from the .ui file
        self.ui = Ui_MainWindow()  
        self.ui.setupUi(self)

        # # Serial port configuration
        # self.serial_port = 'COM3'  # Update with your serial port
        # self.baud_rate = 9600
        # self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)

        # Set up the plot
        plt.style.use('fivethirtyeight')
        self.fig, self.ax = plt.subplots(1, 1, layout='constrained')
        self.canvas = FigureCanvas(self.fig)
        
        # Check if plotWidget already has a layout
        if self.ui.plotWidget.layout() is None:
            # Add a layout to plotWidget if it doesn't have one
            layout = QVBoxLayout(self.ui.plotWidget)
            self.ui.plotWidget.setLayout(layout)
        
        self.ui.plotWidget.layout().addWidget(self.canvas)  # Add canvas to GUI plotWidget (QWidget placeholder)

        # Data for plotting
        self.port = 'COM3'
        self.baud_rate = 9600
        self.time_data = []
        self.current_time_list = []
        self.temperature_data = []
        self.time_step = 0
        self.D_t = 5*60  # At start: 300 seconds time window
        self.measure_interval = 60*1000 # interval for updating the plot, in miliseconds, At start: 60 000 miliseconds
        self.stop_time = None  # To track when the measurement was stopped

        # initialize the measurement status
        self.measurement_active = False

        # parameters used for user enabled scroling in time
        self.scroll_offset = 0
        self.current_view = 'realtime'

        # BUTTON CONNECTIONS (set up what each button does)
        self.ui.btnStartDetection.clicked.connect(self.start_measurement)
        self.ui.btnStopDetection.clicked.connect(self.stop_measurement)
        self.ui.btnSave.clicked.connect(self.save_measurement)
        self.ui.btnClear.clicked.connect(self.clear_data)
        self.ui.btnMoveLeft.clicked.connect(self.move_left)
        self.ui.btnMoveRight.clicked.connect(self.move_right)
        self.ui.btnParameters.clicked.connect(self.open_param_window)

        # Disable all buttons (except btnParameters) until the proper serial connection is established
        self.ui.btnStartDetection.setEnabled(False)
        self.ui.btnStopDetection.setEnabled(False)
        self.ui.btnSave.setEnabled(False)
        self.ui.btnClear.setEnabled(False)
        self.ui.btnMoveLeft.setEnabled(False)
        self.ui.btnMoveRight.setEnabled(False)

        # Shortcuts for the buttons
        self.ui.btnMoveLeft.setShortcut('Left')
        self.ui.btnMoveRight.setShortcut('Right')

        # Continously read data to prevent the growth of the buffer (delay between the measurement and diplay)
        self.latest_temperature = None  # Stores the most recent temperature value

        # Marker for establshing the serial connection 
        self.already_connected = False

        # timer for updating the plot
        self.timer = QTimer()
        
        # Timer for continuous serial reading
        self.serial_read_timer = QTimer()
        self.serial_read_timer.setInterval(100)  # Read every 100ms
        self.serial_read_timer.timeout.connect(self.read_serial_data) # funciton read_serial_data defined bellow
        # self.serial_read_timer.start() # only start the timer when the user specifies the port, baud rate

        # Flag to determine when to simulate data instead of reading it
        self.simulation_mode = False

        # Flag to warn the user when the data hasn't yet been saved
        self.already_saved = False

    def establish_serial_connection(self, port, baud_rate):
        if not self.simulation_mode:
            try:
                # Initialize the serial connection with selected settings
                self.ser = serial.Serial(port, baud_rate, timeout=1)
                # print(f"Serial connection established on {port} at {baud_rate} baud.")
                self.ui.messageDisplay.append(f"Serial connection established on {port} at {baud_rate} baud.\n")
                self.get_bytes() # print out number of bytes
                self.serial_read_timer.start() # start continously reading the serial port
                self.already_connected = True
            except serial.SerialException as e:
                # Handle connection error
                if not self.already_connected:
                    self.error_message(f"Failed to connect: {str(e)}")
        else:
            self.ui.messageDisplay.append(f"Simulation mode on.\n")

    def update_serial_settings(self, port, baud_rate):
        # Update the main window with the new settings
        self.serial_port = port
        self.baud_rate = baud_rate
        # Now try to establish the serial connection
        self.establish_serial_connection(self.serial_port, self.baud_rate)
        # enable the buttons when the serial connection is established
        self.ui.btnStartDetection.setEnabled(True)
        self.ui.btnStopDetection.setEnabled(True)
        self.ui.btnSave.setEnabled(True)
        self.ui.btnClear.setEnabled(True)
        self.ui.btnMoveLeft.setEnabled(True)
        self.ui.btnMoveRight.setEnabled(True)

    # Function to continuously read data from the serial port (help with delays)
    def read_serial_data(self):
        if self.ser and self.ser.is_open: # only read if the serial connection is properly established
            # Continuously read data from the serial port, regardless of whether measurement is active
            line = self.ser.readline().decode('utf-8').strip()
            try:
                # Extract temperature value and store the latest value
                temperature = float(re.findall("\d+\.\d+", line)[0])
                self.latest_temperature = temperature  # Update the latest temperature value
            except (IndexError, ValueError):
                # Skip invalid lines
                pass

    # Function triggered by pressing the btnStartDetection to begin the measurement.
    def start_measurement(self):
        self.already_saved = False
        if self.simulation_mode or (self.ser and self.ser.is_open):  # allow starting in simulation mode
            if not self.measurement_active:
                if not self.simulation_mode:
                    self.ser.flushInput()  # Flush the input buffer only for real Arduino data
                self.ui.messageDisplay.append("Measurement started...\n")
                self.get_bytes() if not self.simulation_mode else None  # Only print bytes if using the serial connection
                self.measurement_active = True

                if self.stop_time is not None:
                    elapsed_time = time.time() - self.stop_time
                    self.time_step += int(elapsed_time)
                    self.stop_time = None
                
                self.start_time = None
                # Update plot immediately as the start_measurement button is pressed
                self.update_plot()
                # Timer to update the plot time interval equal to the parameter 'measure_interval'
                self.timer = QTimer()
                self.timer.setInterval(int(self.measure_interval))  # 'measure_interval' determines the time interval for updatign the plot
                self.timer.timeout.connect(self.update_plot)
                self.timer.start()

    # Function triggered by pressing the btnStopDetection
    def stop_measurement(self):
        if self.measurement_active:
            self.measurement_active = False
            self.ui.messageDisplay.append("Measurement stoped...\n")
            self.get_bytes() if not self.simulation_mode else None  # Only print bytes if using the serial connection
            
            # stop the timer for plotting the data
            if self.timer.isActive():
                self.timer.stop()

            # Record the time when the measurement was stopped
            self.stop_time = time.time()

    # Save measurement data to a user-specified location.
    def save_measurement(self):
        # stop measurement if it is runningS
        self.stop_measurement()

        # Open a file dialog to choose the save location
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Optional, can remove this line
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Measurement Data", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            if file_name:
                # Open the file in write mode to save the file manually
                with open(file_name, 'w') as f:
                    # Write header
                    f.write("# Live time[s] Current time   Temperature[°C]\n")
                    # Iterate over the data and write each pair to the file
                    for live_time, current_time, temp in zip(self.time_data, self.current_time_list, self.temperature_data):
                        f.write(f"{live_time:.2f}   {current_time}  {temp:.2f}\n")
            
            # Notify user of the successful save
            self.ui.messageDisplay.append(f"Data saved to {file_name}\n")
            self.get_bytes() if not self.simulation_mode else None  # Only print bytes if using the serial connection
            self.already_saved = True


    def clear_data(self):
        self.measurement_active = False # stops the measurement
        if not self.already_saved:
            reply = QMessageBox.question(self, 'Unsaved Data', 
                                        "You have unsaved data. Are you sure you want to clear the data?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return  # Exit the function without clearing data
        self.start_time = None  # Reset the start time when starting new measurements
        # clear all data
        self.time_data = []
        self.current_time_list = []
        self.temperature_data = []
        self.time_step = 0
        # clear the plot
        self.ax.clear()
        self.canvas.draw()
        # clear the data and message Display
        self.ui.dataDisplay.clear()
        self.ui.messageDisplay.clear()
        # stop measurement if it is running
        if self.measurement_active:
            self.measurement_active = False
        self.ui.messageDisplay.append("Data cleared.\n")
        self.get_bytes() if not self.simulation_mode else None  # Only print bytes if using the serial connection
        self.stop_time = None # set back to None so that it starts measureing from zero
        
    def open_param_window(self):
        self.stop_measurement()
        self.param_window = ParamWindow(self)
        self.param_window.show()

    def move_left(self):
        if (self.time_step > self.D_t):
            self.scroll_offset += self.measure_interval/1000 # one press left key -> 5s back
            self.current_view = 'scrolling'
            self.update_scroll_view()
    
    def move_right(self):
        if (self.scroll_offset > 0):
            self.scroll_offset -= self.measure_interval/1000 # one press left key -> 5s back
            if self.scroll_offset == 0:
                self.current_view = 'realtime'
            self.update_scroll_view()

    def update_scroll_view(self):
        self.ax.clear()
        start_time = max(0, self.time_step - self.D_t - self.scroll_offset) # makes sure the user dosen't go to negative time
        end_time = start_time + self.D_t
        self.ax.plot(self.time_data, self.temperature_data, '-', label='Temperatura (°C)')
        self.ax.set_xlim(left=start_time, right=end_time)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.legend(loc='upper right')
        # Redraw the canvas
        self.canvas.draw()

    def get_bytes(self):
        if self.ser and self.ser.is_open: # only execute when the serial connection is properly established
            # Log the number of bytes in the input buffer (chech if it is growing over time - could lead to delay)
            buffer_size = self.ser.in_waiting
            self.ui.messageDisplay.append(f"Buffer size: {buffer_size} bytes\n")
    
    def error_message(self, message):
        # Create a message box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Error')
        msg.setText('An error occurred!')
        msg.setInformativeText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Display the message box
        msg.exec_()
    
    def update_plot(self):
        self.time_data.append(self.time_step)
        # add another list fot the time measurements in the format HH:MM:SS
        current_time = self.get_local_time()
        self.current_time_list.append(current_time)
        if self.measurement_active:  # control the measurement with the START/STOP buttons
            if self.simulation_mode:
                simulated_temperature = self.generate_simulated_data()
                self.temperature_data.append(simulated_temperature)
                # self.ui.dataDisplay.append(f'{self.time_step}s: {simulated_temperature}°C')
                self.ui.dataDisplay.append(f'{current_time}: {simulated_temperature}°C')
            else:
                self.temperature_data.append(self.latest_temperature)
                self.ui.dataDisplay.append(f'{current_time}: {self.latest_temperature}°C')

            # self.get_bytes() if not self.simulation_mode else None  # Only print bytes if using the serial connection
            
            self.time_step += self.measure_interval/1000 # in secs
            # # Fix step-like behaviour
            # if self.start_time is None:
            #     self.start_time = time.time()  # Record the start time once
            # current_time = time.time()
            # self.time_step = current_time - self.start_time  # Use the real elapsed time

            if self.current_view == 'realtime':
                self.ax.clear()
                self.ax.plot(self.time_data, self.temperature_data, label="Temperature (°C)")
                if self.time_step > self.D_t:
                    self.ax.set_xlim(left=(self.time_step - self.D_t), right=self.time_step)
                else:
                    self.ax.set_xlim(left=0, right=self.D_t)
                self.ax.set_xlabel("Time (s)")
                self.ax.set_ylabel("Temperature (°C)")
                self.ax.legend(loc='upper right')
                self.canvas.draw()
        else:
            if len(self.temperature_data) == 0:
                self.temperature_data.append(self.latest_temperature)
            else:
                repeat_temperature = self.temperature_data[-1]
                self.temperature_data.append(repeat_temperature)
    
    # Used for testing the GUI when there is now connection to the arduino
    def generate_simulated_data(self):
        # Simulate temperature values between 20°C and 30°C
        return round(random.uniform(20.0, 30.0), 2)
    
    def get_local_time(self):
        c = datetime.now()
        # get just the time in hours:munutes_seconds
        current_time = c.strftime('%H:%M:%S')
        return current_time
    
    def closeEvent(self, event):
        if not self.already_saved and (self.temperature_data != []):
            reply = QMessageBox.question(self, 'Unsaved Data', 
                                        "You have unsaved data. Are you sure you want to exit without saving?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                event.ignore()  # Ignore the close event
                return  # Exit the function to prevent closing
        else:
            # Close the serial port properly when the window is closed
            try:
                if self.ser.is_open:
                    self.ser.close()
                    self.ser.flushInput() # Flush the input buffer - fixing delayed temperature response
            except Exception as e:
                pass
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperaturePlot()
    window.show()
    sys.exit(app.exec_())
