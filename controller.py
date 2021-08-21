import serial

control_code = {
'RelayOnMotorOn'    : b'a',
'RelayOnMotorOff'   : b'b',
'RelayOffMotorOn'   : b'c',
'RelayOffMotorOff'  : b'd'
}


class Controller:

    def __init__(self, port, state='RelayOffMotorOff', baud=9600):
        self.serial = serial.Serial(port, baud)
        self.update(state)
        self.state = state

    def update(self, state):
        code = control_code.get(state, 'RelayOffMotorOff')

        while True:
            self.serial.write(code)
            echo = self.serial.read()
            print("echo %s" % echo)
            print("code %s" % code)
            print('-------')
            if echo == code:
                break

        self.state = state
        return state

    def close(self):
        self.serial.close()


if __name__=="__main__":
    controller = Controller('/dev/ttyUSB0')
    print(controller.update('RelayOnMotorOn'))
    print(controller.update('RelayOffMotorOn'))
    print(controller.update('RelayOnMotorOff'))
 
    
