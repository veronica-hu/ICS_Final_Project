from tkinter import *
import time
import tkinter.messagebox
from chat_utils import *

import indexer

class MainPanel:
    def __init__(self, user, close_callback, search_history, 
                show_who):
    #def __init__(self, user):
        print("Initializing Main Window")
        self.user = user
        self.close_callback = close_callback # close main_window
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        self.search_history = search_history #引入的func
        self.show_who = show_who #引入的func

        #self.click_connect_button = False
        #self.click_send_button = False

        #下面的不确定要不要写
        #self.connect_entry = None
        self.show_text = None
        self.send_text = None
        self.main_window = None

    def show(self):
        global main_window
        main_window = Tk()
        main_window.title(self.user + "----Chat Room")

        # 使window居中显示
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        width = 600
        height = 500
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        main_window.geometry(gm_str)

        # 设置窗口关闭按钮回调，用于退出时关闭socket连接
        main_window.protocol("WM_DELETE_WINDOW", self.close_callback)

        # 三个frame
        self.function_frame = Frame(main_window, bg='#D8BFD8')
        self.send_frame = Frame(main_window, bg='#FFFFF0')
        self.text_frame = Frame(main_window, bg='#DCDCDC')

        # function区buttons
        #self.quit_button = Button(self.function_frame, text='Quit', command=self.close_callback) #直接点左上角就可以了
        #self.quit_button.place(x=35, y=20, height=30, width=80)
        self.time_button = Button(self.function_frame, text='Time', command=self.show_time)
        self.time_button.place(x=35,y=20, height=30, width=80)
        self.poem_button = Button(self.function_frame, text='Poem', command=self.show_poem)
        self.poem_button.place(x=35, y=65, height=30, width=80)
        self.search_button = Button(self.function_frame, text='Search', command=self.show_search)
        self.search_button.place(x=35, y=110, height=30, width=80)
        self.connect_button = Button(self.function_frame, text='Conncet', command=self.connect_peer)
        self.connect_button.place(x=35, y=155, height=30, width=80)
        self.connect_button = Button(self.function_frame, text='Who', command=self.show_who)
        self.connect_button.place(x=35, y=200, height=30, width=80)

        # send区button
        self.send_button = Button(main_window, text='send', 
                                command=self.send_message)
        self.send_button.place(x=480, y=350, height=75, width=120)

        # 文字区
        self.show_text = Text(self.text_frame, bg="#DCDCDC",
            highlightcolor='#DCDCDC', highlightthickness=1)
        self.show_text.place(x=0, y =0, height=350, width=450)
        self.show_text.insert(INSERT, 'Welcome to ICS chatroom\n')
        self.show_text.insert(END, 'Chat away!\n\n')
        self.show_text.config(state=DISABLED)  #显示文本区域的文字不可编辑（注意放在最后

        self.send_text = Text(self.send_frame, bg='#FFFFF0', 
            highlightcolor='#FFFFF0', highlightthickness=1)
        self.send_text.place(x=0, y=0, height=150, width=280)

            #左侧显示who的文字区
        self.peer_text = Text(self.function_frame, bg='white', 
            highlightcolor='white', highlightthickness=1)
        self.peer_text.place(x=0,y=240, height=260, width=150)
        self.show_text.config(state=DISABLED)

        # show_text的滚动条
        show_scr = Scrollbar(self.text_frame)
        show_scr.pack(side=RIGHT, fill=Y)
        show_scr.config(command=self.show_text.yview)
        self.show_text.config(yscrollcommand=show_scr)

        # frame布局
        self.function_frame.place(x=0,y=0, height=500, width=150)
        self.send_frame.place(x=150,y=350, height=150, width=450)
        self.text_frame.place(x=150,y=0, height=350,width=450)

        self.main_window=main_window
        main_window.mainloop()

#======================End of GUI Setting, Start of commands======================================================
    def connect_peer(self):
        self.connect_window = Tk()
        self.connect_window.title('Connect a peer')
        self.connect_window.geometry('450x100')
        connect_label = Label(self.connect_window, text="Please enter the peer's name\n you want to connect with")
        connect_label.pack()
        self.connect_entry = Entry(self.connect_window, width = 10)
        self.connect_entry.pack()
        
        ok_button = Button(self.connect_window, text='ok', command=None)
        ## 现在okbutton点击后没有用
        ok_button.pack()

        self.connect_window.mainloop()
        

    def show_time(self):
        ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
        message = 'Current time is ' + str(ctime)
        tkinter.messagebox.showinfo('Time', message)

    def show_search(self):
        self.search_window = Tk()
        self.search_window.title('Search in History')
        self.search_window.geometry('450x100')
        search_label = Label(self.search_window, text="Please enter the keyword you're searching for")
        search_label.pack()
        self.search_entry = Entry(self.search_window, width = 10)
        self.search_entry.pack()
        ok_button = Button(self.search_window, text='ok', command = self.search_history )
        ok_button.pack()
        self.search_window.mainloop()
        
    def show_poem(self):
        poem_window = Tk()
        poem_window.title('Poem')
        poem_window.geometry('450x100')
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

    def send_message(self):
        self.show_text.config(state=NORMAL)
        mytext = self.send_text.get('0.0', END)
        msg = text_proc(mytext, self.user)
        self.show_text.insert(INSERT, msg)
        self.show_text.insert(END, "\n")
        self.show_text.config(state=DISABLED)
        self.send_text.delete('0.0', END)


if __name__ == "__main__":
    Main = MainPanel('me')
    Main.show()
