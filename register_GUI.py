# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 14:37:31 2019

@author: re_be
"""

import tkinter as tk
import tkinter.messagebox as mbox

#
import Login
import chat_client_class as chatClient
import argparse
import client_main_modified
#


class Register_UI(tk.Frame):
    def __init__(self, quit_func, reg_func, close_callback, master = None):
        tk.Frame.__init__(self, master)
        self.quit_func = quit_func
        self.reg_func = reg_func
        self.close_callback = close_callback
        self.master.title('New user: welcome to ICS chat system!')
        self.master.geometry('500x400')
        self.master.config(background = "#FFC0CB")

        self.createWidgets()
        
# create Widgets
    def createWidgets(self):      
        '''
        self.photo = tk.PhotoImage(file="test2.png")
        self.Artwork = tk.Label(self.master, image=self.photo)
        self.Artwork.photo = self.photo
        self.Artwork.pack()
        #picture at the top
        '''
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

        self.Label_name.place(x = 50, y = 200, width = 100, height = 30)        
        self.entry_name.place(x = 150, y = 200, width = 100, height = 30)
        self.Label_psw.place(x = 50, y = 240, width = 100, height = 30)
        self.entry_psw.place(x = 150, y = 240, width = 200, height = 30)
        self.Label_psw_confirm.place(x = 50, y = 280, width = 200, height = 30)
        self.entry_psw_confirm.place(x = 250, y = 280, width = 200, height = 30)        
        self.clickButton_fine.place(x = 180, y = 330, width = 100, height = 30)     
        #locating widgets(labels, text entries, button)
        

        
    def finish(self):
        if self.entry_psw.get() != self.entry_psw_confirm.get():
            mbox.showinfo("Failure","Two entries of password are not the same, please register again!")
        elif self.entry_name.get() == '':
            mbox.showinfo("Failure","The username can't be empty, please try again!")
        elif self.entry_psw.get() == '':
            mbox.showinfo("Failure", "The password can't be empty, please try again!")
        else:
            self.reg_func()
        
    def get_input(self):
        return self.entry_name.get(), self.entry_psw.get()
    
    def close(self):
        self.master.destroy()

    def show(self):
        self.master.mainloop()
#===testing code, if no need, just delete it========================================
def close_reg_window():
    reg_window.close()
    global login_window
    login_window = Login.LoginPanel(Login.login, Login.register, Login.close_login_window)
    login_window.show()
    
def register_submit():
    print("start to register")
    user, key = reg_window.get_input()
    # 需要新添register申请的步骤（client和server端）
    #====copied from client_main.py to define client here======================
    result = client.register_user(user, key)
    if result == "0":
        mbox.showinfo("Success", "You have registered successfully.")
        close_reg_window()
    elif result == "1":
        mbox.showerror("Error", "This username is registered.")

reg_window = Register_UI(close_reg_window, register_submit, close_reg_window)
reg_window.show()
#======end of test code==================================
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
