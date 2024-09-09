import sys
import serial
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

# Import the generated Python GUI class
from temp_sensor_mian_window import Ui_MainWindow  # Replace with your .ui converted Python file

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

        # Timer to update the plot every second
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second interval
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Read data from the serial port
        line = self.ser.readline().decode('utf-8').strip()

        try:
            # Extract temperature value and convert it to float
            temperature = float(re.findall("\d+\.\d+", line)[0])
            self.time_data.append(self.time_step)
            self.temperature_data.append(temperature)

            # Print temperature in the QTextEdit
            self.ui.textDisplay.append(f'{self.time_step}s: {temperature}°C')

            # Increment time step
            self.time_step += 1

            # Update the plot
            self.ax.clear()
            self.ax.plot(self.time_data, self.temperature_data, label="Temperature (°C)")

            # Keep the x-axis showing only the last D_t seconds
            if self.time_step > self.D_t:
                self.ax.set_xlim([self.time_step - self.D_t, self.time_step])
            else:
                self.ax.set_xlim([0, self.D_t])

            self.ax.set_xlabel("Time (s)")
            self.ax.set_ylabel("Temperature (°C)")
            self.ax.legend(loc='upper right')

            # Redraw the canvas
            self.canvas.draw()

        except (IndexError, ValueError):
            # Skip invalid lines
            pass

    def closeEvent(self, event):
        # Close the serial port when the window is closed
        self.ser.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TemperaturePlot()
    window.show()
    sys.exit(app.exec_())
