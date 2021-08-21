import tkinter as tk

from kafka import KafkaConsumer
from json import loads

from controller import Controller


DEV_PATH_ARDUINO_LINUX  = '/dev/ttyUSB0'
DEV_PATH_ARDUINO_WIN    = 'COM3'

MS_PASS_TO_RESTORE      = 5000
MS_RESTORE_TO_QR        = 2000
class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.controller = Controller(DEV_PATH_ARDUINO_WIN)

        self.switch_frame(Frame_restore)

    def switch_frame(self, frame_class):
        frame_new = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = frame_new
        self._frame.pack()


class Frame_qr(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Please scan Qr", font=
                 ('Helvetica', 12)).pack(side="top")

        self.bind('<Key>', self.handler_qr)
        self.focus_set()

        master.controller.update('RelayOnMotorOff')

        self.list_qr = []
        self.str_qr = tk.StringVar()
        tk.Label(self, textvariable=self.str_qr, font=
                 ('Helvetica', 12)).pack(side="bottom")


    def handler_qr(self, event):
        c = event.char
        if c == '\r':
            temp_str = ''.join(self.list_qr)
            self.str_qr.set(temp_str)
            self.list_qr = []

            print(temp_str + ' logged in')
            self.master.after(MS_RESTORE_TO_QR, self.master.switch_frame, Frame_wait)
        else:
            self.list_qr.append(c)


class Frame_wait(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Wait until scanned", font=
                 ('Helvetica', 12)).pack(side="top")
 
        tk.Button(self, text="Scan bottle", command=
                  lambda: master.switch_frame(Frame_pass)).pack(side="bottom")

#        tk.Button(self, text="scan", command=self.deepstream_hang()).pack()

    def deepstream_hang(self):
        consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

        for message in consumer:
            print("%s:%d:%d: key=%s value=%s" % 
                  (message.topic, message.partition, message.offset, 
                   message.key, message.value))
            consumer.close()

        self.master.switch_frame(Frame_pass)


class Frame_pass(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Video passed", font=
                 ('Helvetica', 12)).pack(side="top")

        self.timer = MS_PASS_TO_RESTORE
        self.str_timer = tk.StringVar()
        self.str_timer.set("%d sec remain" % (self.timer / 1000))

        tk.Label(self, textvariable=self.str_timer, font=
                 ('Helvetica', 12)).pack(side="bottom")

        master.controller.update('RelayOffMotorOn')
        self.update_clock()
        self.master.after(MS_PASS_TO_RESTORE, self.master.switch_frame, Frame_restore)

    def update_clock(self):
        if self.timer > 999:
            self.timer -= 1000
            print(self.timer)
            self.str_timer.set("%d sec remain" % (self.timer / 1000))
            self.after(1000, self.update_clock)
            

class Frame_restore(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Restoring", font=
                 ('Helvetica', 18, "bold")).pack(side="top")

        self.timer = MS_RESTORE_TO_QR
        self.str_timer = tk.StringVar()
        self.str_timer.set("%d sec remain" % (self.timer / 1000))

        tk.Label(self, textvariable=self.str_timer, font=
                 ('Helvetica', 12)).pack(side="bottom")

        master.controller.update('RelayOffMotorOff')
        self.update_clock()
        self.master.after(MS_RESTORE_TO_QR, self.master.switch_frame, Frame_qr)

    def update_clock(self):
        if self.timer > 999:
            self.timer -= 1000
            print(self.timer)
            self.str_timer.set("%d sec remain" % (self.timer / 1000))
            self.after(1000, self.update_clock)



if __name__ == "__main__":
    root = Application()
    root.title("Brave guys")
    root.geometry("400x400")
    root.mainloop()
