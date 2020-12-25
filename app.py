from tkinter import Tk, StringVar, Frame, Label, Button
from main import Deezer
from threading import Thread

class Window:
    button_main = None

    def __init__(self):
        self.message = "программа готова"

    def starting_main(self, string_msg):
        self.button_main['state'] = "disabled"
        spotify = Deezer(string_msg)
        Thread(target=spotify.main).start()


    def app(self):

        windows = Tk()
        windows.geometry("500x250")
        windows.configure(background='#313131')
        windows.title('spotify')
        string_var = StringVar()
        string_var.set(self.message)

        frame = Frame(windows, background='#313131', pady=30)

        data = string_var.set

        button = Button(frame, text='Start', command=lambda data = data :self.starting_main(data),
                        fg="black",font=("Tahoma",10), width = 20, background='#807175',
                        highlightbackground="black")

        self.button_main = button
        button.grid(row=0, columnspan=2, pady=(0,10))

        status_label = Label(frame, text='status: ',fg="#b98694",font=("Tahoma",10),background='#313131')
        status_label.grid(row=1, column=0)

        message_lable = Label(frame, textvariable=string_var, fg="#a89da0",font=("Tahoma",10),background='#313131')
        message_lable.grid(row=1, column=1)

        frame.pack(pady=(60, 0))


        windows.mainloop()


if __name__ == '__main__':
    s = Window()
    s.app()