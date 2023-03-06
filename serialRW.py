import serial
import time

baudrate = 115200
port = '/dev/ttyACM0'
message = ""


def write_line(baudrate, port, message):
    with serial.Serial() as ser:
        ser.baudrate = baudrate
        ser.port = port
        ser.open()
        time.sleep(3)
        ser.write(message.encode(encoding='utf-8'))

def read_line(baudrate, port):
    with serial.Serial() as ser:
        ser.baudrate = baudrate
        ser.port = port
        ser.open()
        #time.sleep(0)
        message = ser.readline().decode().replace("\r\n","")
        return message

"""
while True:
    message = read_line(baudrate, port)
    print(message)

"""