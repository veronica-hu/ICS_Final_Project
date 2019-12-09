import chat_client_class as chatClient
from tkinter import messagebox
import Login
import Main
import register_GUI as Register
from chat_utils import *
import argparse
#import MD5

class ClientGUI:
    def __init__(self):
        self.main_window = None
        self.login_window = None
        self.register_window = None
        self.client = None
        self.user = None

    def close_sk(self):
        print("trying to disconnect socket")
        self.client.quit()

    def close_main_window(self):
        self.close_sk()
        self.main_window.main_window.destroy()

    def close_login_window(self):
        self.close_sk()
        self.login_window.login_frame.destroy()

    # close register and go back to login
    def close_reg_window(self):
        self.reg_window.close()
        #global login_window
        self.login_window = Login.LoginPanel(self.login, self.register, self.close_login_window)
        self.login_window.show()
    
    # close login and goto main(chat)
    def goto_main_window(self, user):
        self.login_window.close()
        #global main_window
        self.main_window = Main.MainPanel(user, self.close_main_window)
        #main_window = Main.MainPanel(user, send_message, close_main_window)
        # 新开一个线程专门负责接收并处理数据 --------—-→这个需要吗？？
        # Thread(target=recv_data).start()
        self.main_window.show()

    def login(self):
        print("click login button")
        user, key = self.login_window.get_input()

    # key = MD5.gen_md5(key)
        if user == "" or key == "":
            messagebox.showwarning(title="Hint", message="User name or password is empty.")
            return

        result = self.client.check_user(user, key)
        if result == '0':
            messagebox.showinfo('Success', 'You have succssfully logged in!')
            self.user = user
            self.goto_main_window(user)
            self.client.sm.set_state(S_LOGGEDIN)
            self.client.sm.set_myname(user)
        elif result == '1':
            messagebox.showerror(title='Error', message='User name does not exist.')
        elif result == '2':
            messagebox.showerror(title="Error", message="User name or password is wrong.")

    # from login go to register
    def register(self):
        print("click register button")
        self.login_window.close()
        #global reg_window
        self.reg_window = Register.Register_UI(self.close_reg_window, self.register_submit, self.close_reg_window)
        self.reg_window.show()

    # submit register form
    def register_submit(self):
        print("start to register")
        user, key = self.reg_window.get_input()
        print("getInput", user, key)

    #if user == "" or key == "" or confirm == "":
        #messagebox.showwarning("Error", "Please complete the form.") 
    #if not key == confirm:
        #messagebox.showwarning("Error", "Please type in same passwords.")
        
    # 发送注册请求
    # result = client.register_user(user, MD5.gen_md5(key))

    # 需要新添register申请的步骤（client和server端）
        result = self.client.register_user(user, key)
        print("the feedback", result)
        if result == "0":
            messagebox.showinfo("Success", "You have registered successfully.")
            self.close_reg_window()
        elif result == "1":
            messagebox.showerror("Error", "This username is registered.")

    def start(self):
        #global client
    # 从chat_cmdl_client搬来的, 为了args （argument）
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()

    # 开始仿照chat_client_class的运行顺序
        self.client = chatClient.Client(args)
        self.client.init_chat()

        #global login_window
        self.login_window = Login.LoginPanel(self.login, self.register, self.close_login_window)
        self.login_window.show()


if __name__ == "__main__":
    ClientGUI = ClientGUI()
    ClientGUI.start()
