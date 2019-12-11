import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm


import threading

class Client:
    def __init__(self, args, receive_gui):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        #self.peer_msg = ''
        self.args = args
        self.socket = None
        self.name = ''
        self.is_peer = True

        self.receive_gui = receive_gui

    def get_peer(self):
        return self.is_peer

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        #reading_thread = threading.Thread(target=self.read_input)
        #reading_thread.daemon = True
        #reading_thread.start()

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        #my_msg = ''
        peer_msg = []
        
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        #if len(self.console_input) > 0:
            #my_msg = self.console_input.pop(0)
            #pop功能使my_msg的[]永远只有最新的消息
            
        if self.socket in read:
            peer_msg = self.recv()
            
        return peer_msg
        #return peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.system_msg = ''

    # 没用到
    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)

#====================================================New Added Commands==================================================
    def receive(self):
        while True:
            while self.sm.state != S_OFFLINE and self.is_peer == True:
                peer_msg = self.get_msgs()
                #peer_msg = self.recv()
                if len(peer_msg) > 0:
                    result = self.sm.proc('', peer_msg)
                    print('be connected result', result)
                    time.sleep(CHAT_WAIT)
                    self.receive_gui(result)
                else:
                    self.receive_gui('')

    def connect(self, peer_name):
        self.is_peer = False
        msg = json.dumps({'action': 'connect', 'target': peer_name})
        self.send(msg)
        result = json.loads(self.recv())['status']
        if result == 'success':
            self.sm.state = S_CHATTING
            self.is_peer = True
            print('connected to', peer_name)
            return '0'
        elif result == 'self':
            self.is_peer = True
            return '1'
        else:
            self.is_peer = True
            return '2'
    
    def send_mine(self, send_content):
        print(send_content)
        if send_content == 'bye\n':
            msg = json.dumps({'action':'disconnect'})
            self.send(msg)
            self.sm.state = S_LOGGEDIN
            return '0'
        else:
            msg = json.dumps({'action':'exchange', "from":"[" + self.name + "]", "message":send_content})
            self.send(msg)
            return '1'

    # search in chat history
    def search_history(self, search_word):
        self.is_peer = False
        msg = json.dumps({"action":"search", "target":search_word})
        self.send(msg)
        result = json.loads(self.recv())['results']
        if (len(result)) > 0:
            self.is_peer = True
            return result + '\n\n'
        else:
            self.is_peer = True
            return '\'' + search_word + '\'' + ' not found\n\n'
    
    # show peers list
    def show_who(self):
        self.is_peer = False
        msg = json.dumps({"action":"list"})
        self.send(msg)
        response = json.loads(self.recv())
        self.is_peer = True
        logged_in = response["results"]
        return logged_in

    # check login username & password
    def check_user(self, user, key):
        msg = json.dumps({'action':'login', 'name': user, 'password': key})
        self.send(msg)
        response = json.loads(self.recv())
        if response['status']=='ok':
            self.name = user
            return '0'
        elif response['status']=='nouser':
            return '1'
        elif response['status']=='incorrect':
            return '2'
        elif response['status'] == 'duplicate':
            return '3'


    # check register username & password
    def register_user(self, user, key):
        #print("user and key", type(user), type(key))
        msg = json.dumps({'action':'register', 'name':user, 'password':key})
        self.send(msg)
        response = json.loads(self.recv())
        if response['status'] == 'duplicate':
            return '1'
        elif response['status'] == 'ok':
            return '0'
#======================================================================================================================
    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1]
            self.console_input.append(text) # no need for lock, append is thread safe

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output() #print system_msg 并清零
        while self.login() == False:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()

        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
            
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
