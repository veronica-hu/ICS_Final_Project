import chat_client_class as chatClient
from tkinter import *
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
        self.output_msg = ''
        self.state = None

#=============================================Main Window Commands============================================
    # search in chat history
    def search_history(self):
        search_word = self.main_window.search_entry.get()
        result = self.client.search_history(search_word)
        messagebox.showinfo('Search Result', result)
        self.main_window.search_window.destroy()

    # show your peers
    def show_who(self):
        self.main_window.peer_text.config(state=NORMAL)
        peers = self.client.show_who()
        self.main_window.peer_text.insert(INSERT, peers)
        self.main_window.peer_text.insert(END, '\n')
        self.main_window.peer_text.config(state=DISABLED)

    # 需要show_text文字区显示的文字，交给此function处理
    def output(self):
        if len(self.output_msg)>0:
            self.main_window.show_text.config(state=NORMAL)
            self.main_window.show_text.insert(INSERT,self.output_msg)
            self.main_window.show_text.config(state=DISABLED)
            self.output_msg = ''

#============================================End of Main Window Commands=======================================
    def close_sk(self):
        print("trying to disconnect socket")
        print(self.client.sm.state)
        self.client.sm.set_state(S_OFFLINE)
        print(self.client.sm.state)
        # self.client.quit()

    def close_main_window(self):
        self.close_sk()
        self.main_window.main_window.destroy()

    def close_login_window(self):
        self.close_sk()
        self.login_window.login_frame.destroy()

    # close register and go back to login
    def close_reg_window(self):
        self.reg_window.close()
        self.login_window = Login.LoginPanel(
                            self.login, self.register, self.close_login_window)
        self.login_window.show()
    
    # close login and goto main(chat)
    def goto_main_window(self, user):
        self.login_window.close()
        self.main_window = Main.MainPanel(user, self.close_main_window, self.search_history, 
                                        self.show_who)
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
            self.user = user
            self.client.sm.set_state(S_LOGGEDIN)
            self.client.sm.set_myname(user)
            print('loggedin')
            messagebox.showinfo('Success', 'You have succssfully logged in!')
            self.goto_main_window(user)
        elif result == '1':
            messagebox.showerror(title='Error', message='User name does not exist.')
        elif result == '2':
            messagebox.showerror(title="Error", message="User name or password is wrong.")

    # from login go to register
    def register(self):
        print("click register button")
        self.login_window.close()
        self.reg_window = Register.Register_UI(self.close_reg_window, self.register_submit, self.close_reg_window)
        self.reg_window.show()

    # submit register form
    def register_submit(self):
        print("start to register")
        user, key = self.reg_window.get_input()
        print("getInput", user, key)
    # 加密注册请求
    # result = client.register_user(user, MD5.gen_md5(key))
        result = self.client.register_user(user, key)
        print("the feedback", result)
        if result == "0":
            messagebox.showinfo("Success", "You have registered successfully.")
            self.close_reg_window()
        elif result == "1":
            messagebox.showerror("Error", "This username is registered.")

    def start(self):
    #从chat_cmdl_client搬来的, 为了args （argument）
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()
    # 开始仿照chat_client_class的运行顺序
        self.client = chatClient.Client(args)
        self.client.init_chat()
        self.state = self.client.sm.state

        self.login_window = Login.LoginPanel(self.login, self.register, self.close_login_window)
        self.login_window.show()

    



if __name__ == "__main__":
    ClientGUI = ClientGUI()
    ClientGUI.start()
