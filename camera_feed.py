import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600) # Replace 'COM3' with the appropriate serial port
time.sleep(2) # Wait for the serial connection to establish

while True:
    # Send a message to Arduino
    message = {"remarks" : "Default",
                "instruction": "NO",
                "product_map": "YES",}
    ser.write(str(message).encode())
    #ser.close()
    #time.sleep(5)
    
    # Wait for a response from Arduino
    while ser.in_waiting == 0:
        pass

    message1 = ser.readline().decode().strip()
    print(message1)
    