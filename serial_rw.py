import serial


class Serial:
    def __init__(self, port, baudrate=115200, timeout=1.0):
        self._ser = serial.Serial(port, baudrate, timeout)

    def read(self):
        while True:
            if self._ser.in_waiting > 0:
                line = self._ser.readline()
                return line

    def write(self, x, y):
        self._ser.write("!".encode())
        # print("X=")
        # print(x)
        self._ser.write(str(int(x)).encode())
        self._ser.write("|".encode())

        self._ser.write("@".encode())
        # print("Y=")
        # print(y)
        self._ser.write(str(int(y)).encode())
        self._ser.write("|".encode())
        
        self._ser.write("\r\n".encode())
