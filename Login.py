from tkinter import *
import tkinter.messagebox

class LoginPanel:
    def __init__(self):
        self.user = None
        self.key = None
        self.login_frame = None
        self.btn_reg = None
        self.btn_login = None
        self.login_func = login_func
        self.reg_func = reg_func
        self.close_callback = close_callback




        
    def show(self):
        self.login_frame = Tk()
        self.login_frame.configure(background = "#333333")#原：#333333
        screen_width = self.login_frame.winfo_screenwidth()
        screen_height = self.login_frame.winfo_screenheight()
        width = 400
        height = 300
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.login_frame.geometry(gm_str)
        self.login_frame.title("登录")
        self.login_frame.resizable(width=False, height=False)

        title_lable = Label(self.login_frame, text="ICS Chat - LogIn", font=("Helvetica", 16),
                            fg="white", bg="#555555")
        title_lable.grid(row = 0,column = 0)
        
        #登陆表单frame
        form_frame = Frame(self.login_frame,bg = '#222222')#原：#222222
        form_frame.grid(row = 1, column = 0)              
        
        Label(form_frame, text="User：", font=("Helvetica", 12), bg="#222222", fg="white", width = 10, height = 3).grid(row = 1, column = 0) #原： bg="#222222",fg="white"          
        Label(form_frame, text="Password：", font=("Helvetica", 12), bg="#222222", fg="white", width = 10, height = 3).grid(row = 2, column = 0)
            
        self.user = StringVar()
        self.key = StringVar()
        Entry(form_frame, textvariable=self.user, bg="#e3e3e3", width=30).grid(row = 1, column = 1)

        Entry(form_frame, textvariable=self.key, show="*", bg="#e3e3e3", width=30).grid(row = 2, column = 1)
      
        
        #Button Frame
        btn_frame = Frame(self.login_frame, bg = '#333333')
        btn_frame.grid(row = 3,column = 0)
        self.btn_login = Button(btn_frame, text="Log in", bg="lightgreen", fg="black", width=15,
                              font=('Helvetica', 11), command=self.login).grid(row = 5, column = 1)
        self.btn_reg = Button(btn_frame, text = 'Sign up',bg = 'lightgreen',fg = 'black',width = 15,
                              font = ('Helvetica',11), command = None).grid(row = 6, column = 1)
       

        
        self.login_frame.mainloop()
        
        
        
    def login(self):
        tkinter.messagebox.showinfo('Reminder','successfully loged in!')
    
    def close(self):
        if self.login_frame == None:
            print("Panel not shown")
        else:
            self.login_frame.destroy()

    # 获取输入的用户名密码
    def get_input(self):
        return self.user.get(), self.key.get()

'''
a = LoginPanel()
a.show()
''''







    



    






            
        

