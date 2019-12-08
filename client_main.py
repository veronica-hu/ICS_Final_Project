import chat_client_class as chatClient
from tkinter import messagebox
import Login
import Main
import Register
from chat_utils import *
import argparse
import json
#import MD5
from threading import Thread
import time

#  chatting模式， 需要重写
def send_message():
    print("send message:")
    content = main_window.get_send_text()
    if content == "" or content == "\n":
        print("empty message")
        return
    print(content)
    
    main_window.clear_send_text()
    client.send_message(content)

def close_sk():
    print("trying to disconnect socket")
    client.quit()

def close_main_window():
    close_sk()
    main_window.main_window.destroy()

def close_login_window():
    close_sk()
    login_window.login_window.destroy()

# close register and go back to login
def close_reg_window():
    reg_window.close()
    global login_window
    login_window = Login.LoginPanel(login, register, close_login_window)
    login_window.show()

# close login and goto main(chat)
def goto_main_window(user):
    login_window.close()
    global main_window
    main_window = Main.MainPanel()
    #main_window = Main.MainPanel(user, send_message, close_main_window)
    # 新开一个线程专门负责接收并处理数据 --------—-→这个需要吗？？
    # Thread(target=recv_data).start()
    main_window.show()

def login():
    print("click login button")
    user, key = login_window.get_input()
    # key = MD5.gen_md5(key)

    if user == "" or key == "":
        messagebox.showwarning(title="Hint", message="User name or password is empty.")
        return
    print("user: " + user + ", key: " + key)

    # 需要新添login过程中check的步骤（client和servser端）
    result = client.check_user(user, key)
    if result == '0':
        goto_main_window(user)
        client.sm.set_state(S_LOGGEDIN)
        client.sm.set_myname(user)
    elif result == '1':
        messagebox.showerror(title='Error', message='User name does not exist.')
    elif result == '2':
        messagebox.showerror(title="Error", message="User name or password is wrong.")

# from login go to register
def register():
    print("click register button")
    login_window.close()
    global reg_window
    reg_window = Register.RegisterUI(close_reg_window, register_submit, close_reg_window)
    reg_window.show()

# submit register form
def register_submit():
    print("start to register")
    user, key, confirm = reg_window.get_input()

    if user == "" or key == "" or confirm == "":
        messagebox.showwarning("Error", "Please complete the form.")
        return
    if not key == confirm:
        messagebox.showwarning("Error", "Please type in same passwords.")
        return
    # 发送注册请求
    # result = client.register_user(user, MD5.gen_md5(key))

    # 需要新添register申请的步骤（client和server端）
    result = client.register_user(user, key)
    if result == "0":
        messagebox.showinfo("Success", "You have registered successfully.")
        close_reg_window()
    elif result == "1":
        messagebox.showerror("Error", "This username is registered.")

#def handle_command(command): 
    
def start():
    global client
    # 从chat_cmdl_client搬来的, 为了args （argument）
    parser = argparse.ArgumentParser(description='chat client argument')
    parser.add_argument('-d', type=str, default=None, help='server IP addr')
    args = parser.parse_args()

    # 开始仿照chat_client_class的运行顺序
    client = chatClient.Client(args)
    client.init_chat()

    global login_window
    login_window = Login.LoginPanel(login, register, close_login_window)
    login_window.show()


if __name__ == "__main__":
    start()
