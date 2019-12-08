from tkinter import *
import time
import tkinter.messagebox
from chat_utils import *

import indexer

class MainPanel:
    def __init__(self):
    #def __init__(self, username, send_func, close_callback):
        print("Initializing Main Window")
        #self.username = username
        self.friend_list = None
        self.message_text = None
        self.show_text = None
        self.send_text = None
        #self.send_func = send_func # send_message function, 要改，可能不会用
        #self.close_callback = close_callback # close main_window
        self.main_window = None
        self.sonnet = indexer.PIndex("AllSonnets.txt")

    def show(self):
        global main_window
        main_window = Tk()
        main_window.title("Chat Room")
        main_window.geometry('500x500')
        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        #main_window.protocol("WM_DELETE_WINDOW", self.close_callback)

        # 三个frame
        self.function_frame = Frame(main_window, bg='#D8BFD8')
        self.send_frame = Frame(main_window, bg='#FFFFF0')
        self.text_frame = Frame(main_window, bg='#FFEFD5')

        # function区buttons
        self.time_button = Button(self.function_frame, text='Time', command=self.show_time)
        self.time_button.place(x=10,y=10, height=30, width=80)
        self.connect_button = Button(self.function_frame, text='Connect', command=self.connect_peer)
        self.connect_button.place(x=10, y=90, height=30, width=80)
        self.search_button = Button(self.function_frame, text='Search', command=self.show_search)
        self.search_button.place(x=10, y=130, height=30, width=80)
        self.poem_button = Button(self.function_frame, text='Poem Search', command=self.show_poem)
        self.poem_button.place(x=10, y=170, height=30, width=80)
        self.quit_button = Button(self.function_frame, text='Quit', command=main_window.destroy)
        self.quit_button.place(x=10, y=210, height=30, width=80)

        # send区button
        self.send_button = Button(main_window, text='send', 
                                command=self.send_message)
        self.send_button.place(x=430, y=300, height=100, width=70)

        # 文字区
        self.show_text = Text(self.text_frame, bg="#FFEFD5",
            highlightcolor='#FFEFD5', highlightthickness=1)
        self.show_text.place(x=0, y =0, height=300, width=350)
        self.show_text.insert(INSERT, 'Welcome to ICS chatroom\n')
        self.show_text.insert(END, 'Chat away\n\n')
        self.show_text.config(state=DISABLED)  #显示文本区域的文字不可编辑（注意放在最后

        self.send_text = Text(self.send_frame, bg='#FFFFF0', 
            highlightcolor='#FFFFF0', highlightthickness=1)
        self.send_text.place(x=0, y=0, height=200, width=280)

        # frame布局
        self.function_frame.place(x=0,y=0, height=500, width=150)
        self.send_frame.place(x=150,y=300, height=200, width=350)
        self.text_frame.place(x=150,y=0, height=300,width=350)

        self.main_window=main_window
        main_window.mainloop()

    def show_time(self):
        ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
        message = 'Current time is ' + str(ctime)
        tkinter.messagebox.showinfo('Time', message)

    def show_search(self):
        pass

    def show_poem(self):
        poem_window = Tk()
        poem_window.title('Poem')
        poem_window.geometry('450x200')
        label = Label(poem_window,text="Please enter the number of poem you're looking for:")
        label.pack()
        entry = Entry(poem_window, width = 10)
        entry.pack()
        def search_poem():
            poem_idx = int(entry.get())
            poem = self.sonnet.get_poem(poem_idx)
            poem = '\n'.join(poem).strip()
            output_msg = ''
            if (len(poem) > 0):
                output_msg += poem + '\n\n'
            else:
                output_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
            poem_window.destroy()
            tkinter.messagebox.showinfo('Poem'+str(poem_idx), output_msg)

        ok_button = Button(poem_window, text='ok', command = search_poem)
        ok_button.pack()
        poem_window.mainloop()

    def connect_peer(self):
        pass

    def send_message(self):
        self.show_text.config(state=NORMAL)
        mytext = self.send_text.get('0.0', END)
        msg = text_proc(mytext, 'me')
        self.show_text.insert(INSERT, msg)
        self.show_text.insert(END, "\n")
        self.show_text.config(state=DISABLED)
        self.send_text.delete('0.0', END)

if __name__ == "__main__":
    Main = MainPanel()
    Main.show()