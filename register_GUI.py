# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:37:31 2019

@author: re_be
"""

import tkinter as tk
import tkinter.messagebox as mbox
#from PIL import ImageTk, Image

# 定义MainUI类表示应用/窗口，继承Frame类
class Register_UI(tk.Frame):
# Application构造函数，master为窗口的父控件
    def __init__(self, master = None):
# 初始化Application的Frame部分 
        tk.Frame.__init__(self, master)
        #self.grid()
# 创建控件
        self.createWidgets()
        

# 创建控件
    def createWidgets(self):      
        self.photo = tk.PhotoImage(file="test2.png")
        self.Artwork = tk.Label(self.master, image=self.photo)
        self.Artwork.photo = self.photo
        self.Artwork.pack()
        #picture at the top
        self.Label_name = tk.Label(self.master,text="Username:", font=('Helvetica', 12))
        self.Label_psw = tk.Label(self.master, text = "Password:", font=('Helvetica', 12))
        self.Label_psw_confirm = tk.Label(self.master, text = "Confirm your password:", font=('Helvetica', 12))
        #labels representing username, password, password confirmation
        
        default = ''
        self.entry_name = tk.Entry(self.master, textvariable = default)
        self.entry_psw = tk.Entry(self.master, show = "*", textvariable = default)
        self.entry_psw_confirm = tk.Entry(self.master, show = "*", textvariable = default)
        #text entries of username, password, password confirmation
        
        self.clickButton_fine = tk.Button(self.master, text = "Submit", font=('Helvetica', 12), command = self.finish)
        #submission button

        self.Label_name.place(x = 100, y = 420, width = 100, height = 30)        
        self.entry_name.place(x = 200, y = 420, width = 180, height = 30)
        self.Label_psw.place(x = 100, y = 460, width = 100, height = 30)
        self.entry_psw.place(x = 200, y = 460, width = 180, height = 30)
        self.Label_psw_confirm.place(x = 100, y = 500, width = 170, height = 30)
        self.entry_psw_confirm.place(x = 270, y = 500, width = 180, height = 30)        
        self.clickButton_fine.place(x = 250, y = 540, width = 100, height = 30)     
        #locating widgets(labels, text entries, button)
        

        
    def finish(self):
        if self.entry_psw.get() != self.entry_psw_confirm.get():
            mbox.showinfo("Failure","Two entries of password are not the same, please register again!")
        elif self.entry_name.get() == '':
            mbox.showinfo("Failure","The username can't be empty, please try again!")
        elif self.entry_psw.get() == '':
            mbox.showinfo("Failure", "The password can't be empty, please try again!")
        else:
            mbox.showinfo("Success","You have registered as a member. Congratulations!")
        
    def get(self):
        return self.entry_name.get(), self.entry_psw.get()
    
    def close(self):
        self.master.destroy()

def show():
    root = tk.Tk()
    root.geometry("800x600")
    root.title('New user: welcome to ICS chat system!')
# 创建一个MainUI对象

#mycolor = '#%02x%02x%02x' % (255, 0, 238)
    app = Register_UI(root)
# 设置窗口标题
    app.master.title('New user: welcome to ICS chat system!')
# 设置窗体大小
    app.master.geometry('600x600')
# 主循环开始
    root.config(background = "#FFC0CB")
    root.mainloop()

show()
#GUI
#Function 1: @
#Function 2:表情
#Function 3:登录注册
#Function 4:上传&下载文件
#Function 5:字体？颜色？
#Function 6:聊天背景
#(Function 7:种树)

#Funtion 1: @
#1. user type "@someone"
#2. user send a message of notifying someone especially
#3. socket received the message, and then send everyone with the message, and when it comes to "someone", the system adds "someone @ you" at the front
