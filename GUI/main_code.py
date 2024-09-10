import sys
import serial
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QDialog
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import serial.tools.list_ports
import time

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

        # Connect the 'Save' button in the side window
        self.ui.btnSave.clicked.connect(self.save_changes)
        # close the dialog box
        self.ui.btnCancel.clicked.connect(self.reject)

        # Access to parent (main window)
        self.main_window = parent

    def save_changes(self):
        # Get the new D_t value from the QLineEdit
        try:
            new_D_t = float(self.ui.lineEdit_Dt.text())
            self.main_window.D_t = new_D_t  # Update the D_t value in the main window
            self.main_window.ui.messageDisplay.append(f'D_t updated to {new_D_t} seconds')
            self.accept()  # Close the side window after saving
        except ValueError:
            self.main_window.ui.messageDisplay.append('Invalid input for D_t')
        self.main_window.get_bytes() # print out number of bytes

# calss for main window functionality
class TemperaturePlot(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Load the GUI from the .ui file
        self.ui = Ui_MainWindow()  
        self.ui.setupUi(self)

        # Serial port configuration
        self.serial_port = 'COM3'  # Update with your serial port
        self.baud_rate = 9600
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)

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
        self.time_data = []
        self.temperature_data = []
        self.time_step = 0
        self.D_t = 30  # Example: 30 seconds time window
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

        # Shortcuts for the buttons
        self.ui.btnMoveLeft.setShortcut('Left')
        self.ui.btnMoveRight.setShortcut('Right')

        # Continously read data to prevent the growth of the buffer (delay between the measurement and diplay)
        self.latest_temperature = None  # Stores the most recent temperature value
        
        # Timer for continuous serial reading
        self.serial_read_timer = QTimer()
        self.serial_read_timer.setInterval(100)  # Read every 100ms
        self.serial_read_timer.timeout.connect(self.read_serial_data) # funciton read_serial_data defined bellow
        self.serial_read_timer.start()

    # Function to continuously read data from the serial port (help with delays)
    def read_serial_data(self):
        if self.ser.is_open: # only read if the serial port is open
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
        if not self.measurement_active:
            # important!!
            self.ser.flushInput() # Flush the input buffer - fixing delayed temperature response
            self.ui.messageDisplay.append("Measurement started...") # print a message to let the user know the measurement has started
            self.get_bytes() # print out number of bytes
            self.measurement_active = True

            # If the measurement was previously stopped, account for the time elapsed during the stop
            if self.stop_time is not None:
                elapsed_time = time.time() - self.stop_time
                self.time_step += int(elapsed_time)  # Adjust time_step by the time that passed
                self.stop_time = None  # Reset stop_time

            # Timer to update the plot every second
            self.timer = QTimer()
            self.timer.setInterval(1000)  # 1 second interval
            self.timer.timeout.connect(self.update_plot)
            self.timer.start()

    # Function triggered by pressing the btnStopDetection
    def stop_measurement(self):
        if self.measurement_active:
            self.measurement_active = False
            self.ui.messageDisplay.append("Measurement stoped...")
            self.get_bytes() # print out number of bytes
            
            # Record the time when the measurement was stopped
            self.stop_time = time.time()

    # Save measurement data to a user-specified location.
    def save_measurement(self):
        # stop measurement if it is running
        self.stop_measurement()
        # Open a file dialog to choose the save location
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # Optional, can remove this line
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Measurement Data", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            # Prepare data for saving
            # self.time_data = np.array([self.time_data])  # Convert to appropriate format
            # self.temperature_data = np.array([self.temperature_data])
            data = np.hstack((np.rot90(np.array([self.time_data]) , k=3), np.rot90(np.array([self.temperature_data]), k=3)))  # Rotate rows -> columns + merge columns
            
            # Save the data to the selected file location
            np.savetxt(file_name, data)
            self.ui.messageDisplay.append(f"Data saved to {file_name}")
            self.get_bytes() # print out number of bytes

    def clear_data(self):
        # clear all data
        self.time_data = []
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
        self.ui.messageDisplay.append("Data cleared.")
        self.get_bytes() # print out number of bytes
        self.stop_time = None # set back to None so that it starts measureing from zero

    def open_param_window(self):
        self.param_window = ParamWindow(self)
        self.param_window.show()

    def move_left(self):
        if (self.time_step > self.D_t):
            self.scroll_offset += 5 # one press left key -> 5s back
            self.current_view = 'scrolling'
            self.update_scroll_view()
    
    def move_right(self):
        if (self.scroll_offset > 0):
            self.scroll_offset -= 5 # one press left key -> 5s back
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
        # Log the number of bytes in the input buffer (chech if it is growing over time - could lead to delay)
        buffer_size = self.ser.in_waiting
        self.ui.messageDisplay.append(f"Buffer size: {buffer_size} bytes")
    
    def update_plot(self):
        self.time_data.append(self.time_step)
        if self.measurement_active: # control the measurement with the START/STOP buttons
            self.temperature_data.append(self.latest_temperature) # display latest temperature, which is now always being updated
            # Print temperature in the QTextEdit
            self.ui.dataDisplay.append(f'{self.time_step}s: {self.latest_temperature}°C')
            # # Log the number of bytes in the input buffer (chech if it is growing over time - could lead to delay)
            # self.get_bytes()
            # Increment time step
            self.time_step += 1
            if self.current_view == 'realtime': 
                # Update the plot
                self.ax.clear()
                self.ax.plot(self.time_data, self.temperature_data, label="Temperature (°C)")
                # Keep the x-axis showing only the last D_t seconds
                if self.time_step > self.D_t:
                    self.ax.set_xlim(left=(self.time_step - self.D_t), right=self.time_step)
                else:
                    self.ax.set_xlim(left=0, right=self.D_t)
                self.ax.set_xlabel("Time (s)")
                self.ax.set_ylabel("Temperature (°C)")
                self.ax.legend(loc='upper right')
                # Redraw the canvas
                self.canvas.draw()
        else:
            # make sure to add the last temeparture so the dimentions of the lists match
            if len(self.temperature_data) == 0:
                self.temperature_data.append(self.latest_temperature)
            else:
                repeat_temperature = self.temperature_data[-1]
                self.temperature_data.append(repeat_temperature)

    def closeEvent(self, event):
        # Close the serial port properly when the window is closed
        if self.ser.is_open:
            self.ser.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperaturePlot()
    window.show()
    sys.exit(app.exec_())
