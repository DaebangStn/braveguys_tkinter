import tkinter as tk

from kafka import KafkaConsumer
from json import loads
#hi
class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Frame_start)

    def switch_frame(self, frame_class):
        frame_new = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = frame_new
        self._frame.pack()


class Frame_start(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Start!", font=
                 ('Helvetica', 18, "bold")).pack(side="top")
        tk.Button(self, text="Next", command=
                  lambda: master.switch_frame(Frame_qr)).pack()


class Frame_qr(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Please scan Qr", font=
                 ('Helvetica', 12)).pack(side="top")

        self.list_qr = []
        self.str_qr = tk.StringVar()
        tk.Label(self, textvariable=self.str_qr, font=
                 ('Helvetica', 12)).pack(side="bottom")

        tk.Button(self, text="Scan bottle", command=
                  lambda: master.switch_frame(Frame_wait)).pack()

        self.bind('<Key>', self.handler_qr)
        self.focus_set()

    def handler_qr(self, event):
        c = event.char
        if c is '\r':
            temp_str = ''.join(self.list_qr)
            self.str_qr.set(temp_str)
            self.list_qr = []

            print(temp_str + ' logged in')
        else:
            self.list_qr.append(c)


class Frame_wait(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        tk.Label(self, text="Scan your bottle", font=
                 ('Helvetica', 12)).pack(side="top")
 
        tk.Button(self, text="Next", command=
                  lambda: master.switch_frame(Frame_done)).pack()
        
        tk.Button(self, text="scan", command=deepstream_hang(master)).pack()
        master.switch_frame(Frame_done)

    '''
    def deepstream_hang(self, master):
        consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

        for message in consumer:
            print("%s:%d:%d: key=%s value=%s" % 
                  (message.topic, message.partition, message.offset, 
                   message.key, message.value))
            consumer.close()

        master.switch_frame(Frame_done)
    '''


class Frame_done(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Done!", font=
                 ('Helvetica', 12)).pack(side="top")
        tk.Button(self, text="Go First", command=
                  lambda: master.switch_frame(Frame_start)).pack()

def deepstream_hang(master):
    consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])
    print("hell")
    for message in consumer:
         print("%s:%d:%d: key=%s value=%s" % 
              (message.topic, message.partition, message.offset, 
               message.key, message.value))
         consumer.close()

    master.switch_frame(Frame_done)


if __name__ == "__main__":
    root = Application()
    root.title("Brave guys")
    root.geometry("400x400")
    root.mainloop()
