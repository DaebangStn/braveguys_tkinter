import tkinter as tk

from kafka import KafkaConsumer
from json import loads

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.my_text = tk.StringVar()
        self.my_text.set("Test")
        self.my_label = tk.Label(self, textvariable=self.my_text)
        self.my_label.pack()

    def say_hi(self):
        consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

        for message in consumer:
            self.my_text.set("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                message.offset, message.key, message.value))
            break

root = tk.Tk()
root.title("Brave guys")
#root.geometry("600x400")
app = Application(master=root)
app.mainloop()
