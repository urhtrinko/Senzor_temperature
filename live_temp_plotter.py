import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re
from functools import partial
import numpy as np

# Serial port configuration
serial_port = 'COM3'  # Replace with your Arduino's serial port
baud_rate = 9600  # Match the baud rate in your Arduino code

# Open the serial connection
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Lists to store data
time_data = []
temperature_data = []
time_step = 0

# Define time window
D_t = 60*3 # [seconds] time interval that is constant for the graph
current_view = 'realtime' # initially realtime viewing
scroll_offset = 0 # when this non zero the user has scolled away from realtime viewing

# Set up the plot
plt.style.use('fivethirtyeight')
fig, ax = plt.subplots(1, 1, figsize=(6, 4), layout='constrained')
# ax.set_title("Real-time Temperature Plot")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")

# Update the plot dynamically
def update(frame, D_t): # time interval which is displayed on the graph
    global time_step
    global scroll_offset
    global current_view
   
    line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
    
    try:
        temperature = re.findall("\d+\.\d+", line)[0] # if no temeperature in line then the list is empty amd the line is passed (except)
        time_data.append(time_step)
        print('{}: temperatura je {}°C'.format(time_step, temperature)) # print temperature at the same time
        temperature_data.append(float(temperature))
        time_step += 1

        # only do this if the user is in 'realtime'
        if current_view == 'realtime':
            ax.clear()
            ax.plot(time_data, temperature_data, '-', label="Temperature (°C)")
            # ax.set_title("Real-time Temperature Plot")
            ax.set_xlabel("Čas (s)")
            ax.set_ylabel("Temperatura (°C)")
            if time_step > D_t:
                ax.set_xlim(left=time_step - D_t, right=time_step)
            else:
                ax.set_xlim(0, D_t)
            ax.legend(loc='upper right')

    except IndexError:
        # If the data is not a number, we skip it
        pass

def update_scroll_view():
    ax.clear()
    start_time = max(0, time_step - D_t - scroll_offset)
    end_time = start_time + D_t
    ax.plot(time_data, temperature_data, '-', label='Temperatura (°C)')
    ax.set_xlim(left=start_time, right=end_time)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (°C)")
    ax.legend(loc='upper right')
    plt.draw()

# function for when the user presses some keys
def on_key(event):
    global current_view
    global scroll_offset

    if (event.key == 'left') and (time_step > D_t): # scroll back only if there is already some history
        # scroll back
        scroll_offset += 5 # one press left key -> 5s back
        current_view = 'scrolling'
        update_scroll_view()
    elif (event.key == 'right') and (scroll_offset > 0): # move right only if we are not in 'realtime'
        # scroll forward
        scroll_offset -= 5 # one press right key -> 5s forward
        if scroll_offset == 0:
            current_view = 'realtime'
        update_scroll_view()

# Connect the key press event and the figure
fig.canvas.mpl_connect('key_press_event', on_key)

# Create the animation
ani = FuncAnimation(fig, partial(update, D_t=D_t), interval=1000, cache_frame_data=False)  # Evry second call the function update()

# Display the plot
plt.show()

# Close the serial port when done
ser.close()

# save data to a text file
name = input('Shrani meritve kot:')
time_data = np.array([time_data]) # prevedeno v ustrezbo obliko
temperature_data = np.array([temperature_data])
podatki = np.hstack((np.rot90(time_data, k=3), np.rot90(temperature_data, k=3))) # rotacija vrstica -> stolpec + pravi vrstni red in združitev stolpcev
np.savetxt(f'Meritve/{name}.txt', podatki)
