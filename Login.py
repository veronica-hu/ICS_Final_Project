from tkinter import *
import tkinter.messagebox

class LoginPanel:
    def __init__(self, login_func, reg_func, close_callback):
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
        
        self.login_frame.protocol("WM_DELETE_WINDOW", self.close_callback)
        
        #窗口尺寸已修改
        screen_width = self.login_frame.winfo_screenwidth()
        screen_height = self.login_frame.winfo_screenheight()
        width = 500
        height = 400
        gm_str = "%dx%d+%d+%d" % (width, height, (screen_width - width) / 2,
                                  (screen_height - 1.2 * height) / 2)
        self.login_frame.geometry(gm_str)
        
        self.login_frame.title("Login")
        self.login_frame.resizable(width=False, height=False)

        title_lable = Label(self.login_frame, text="ICS Chat - LogIn", font=("Calibri", 16),
                            fg="white", bg="#555555")
        title_lable.pack(ipady = 10, fill = X)
        
        #登陆表单frame
        form_frame = Frame(self.login_frame,bg = '#222222')#原：#222222
        form_frame.pack(fill=X, padx=20, pady=10)
        user_img = PhotoImage(file="user.png", master=self.login_frame)
        key_img = PhotoImage(file="key.png", master=self.login_frame)
        user_img_label = Label(form_frame, image=user_img, width=30, height=30, bg="#333333")
        key_img_label = Label(form_frame, image=key_img, width=30, height=30, bg="#333333")
        user_img_label.grid(row=0, column=0, padx=5)
        key_img_label.grid(row=1, column=0, padx=5)

        
        Label(form_frame, text="User：", font=("Calibri", 12), bg="#222222", fg="white", width = 10, height = 3).grid(row=0, column=1, pady=20) #原： bg="#222222",fg="white"          
        Label(form_frame, text="Password：", font=("Calibri", 12), bg="#222222", fg="white", width = 10, height = 3).grid(row=1, column=1, pady=20)
            
        self.user = StringVar()
        self.key = StringVar()
        Entry(form_frame, textvariable=self.user, bg="#e3e3e3", width=30).grid(row=0, column=2, ipady=1)

        Entry(form_frame, textvariable=self.key, show="*", bg="#e3e3e3", width=30).grid(row=1, column=2, ipady=1)
      
        #Button Frame
        btn_frame = Frame(self.login_frame, bg = '#333333')
        btn_frame.pack(fill=X, padx=20, pady=20)
        self.btn_login = Button(btn_frame, text="Log in", bg="lightgreen", fg="black", width=15,
                              font=('Calibri', 11), command=self.login_func).pack(side=LEFT, ipady=3)
        self.btn_reg = Button(btn_frame, text = 'Sign up',bg = 'lightgreen',fg = 'black',width = 15,
                              font = ('Calibri',11), command = self.reg_func).pack(side=RIGHT, ipady=3)
       
        self.login_frame.mainloop()
    
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
'''







    



    






            
        

