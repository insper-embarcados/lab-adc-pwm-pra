import serial
import uinput

ser = serial.Serial('/dev/ttyACM0', 115200)

# Create new mouse device
device = uinput.Device([
    uinput.BTN_LEFT,
    uinput.BTN_RIGHT,
    uinput.REL_X,
    uinput.REL_Y,
])


def parse_data(data):
    axis = data[0]  # 0 for X, 1 for Y
    value = int.from_bytes(data[1:3], byteorder='little', signed=True)  # Convert second byte to signed integer
    print(f"axis: {axis}, value: {value}")
    return axis, value


def move_mouse(axis, value):
    if axis == 0:    # X-axis
        device.emit(uinput.REL_X, value)
    elif axis == 1:  # Y-axis
        device.emit(uinput.REL_Y, value)

try:
    while True:
        # Read 3 bytes from UART
        data = ser.read(4)
        if data[-1] == 0xFF:  # End-of-package indicator
            axis, value = parse_data(data)
            move_mouse(axis, value)
        else:
            print("Erro no protocolo, dados recebidos:")
            print(data)
except KeyboardInterrupt:
    print("Program terminated by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    ser.close()
