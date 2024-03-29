"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import indexer
import json
import pickle as pkl
from chat_utils import *
import chat_group as grp


class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        self.user_password = {}

    def new_client(self, sock):
        # add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        # read the msg that should have login code plus username
        #msg = json.loads(myrecv(sock))
        #print(msg["action"])
        try:
            msg = json.loads(myrecv(sock))
            #print(len(msg))
            if len(msg) > 0:
                #print(len(msg))
                if msg["action"] == "login":
                    name = msg["name"]
                    password = msg['password']
                    if name not in self.user_password.keys():
                        mysend(sock, json.dumps({"action": "login", "status": "nouser"}))
                    elif self.group.is_member(name) == True:
                        mysend(sock, json.dumps({'action': 'login', 'status':'duplicate'}))
                    elif name in self.user_password.keys() and self.group.is_member(name) != True: 
                        if self.user_password[name] == password:
                            # move socket from new clients list to logged clients
                            self.new_clients.remove(sock)
                            # add into the name to sock mapping
                            self.logged_name2sock[name] = sock
                            self.logged_sock2name[sock] = name
                            
                            # load chat history of that user   
                            if name not in self.indices.keys():
                                try:
                                    self.indices[name] = pkl.load(
                                        open(name + '.idx', 'rb'))
                                except IOError:  # chat index does not exist, then create one
                                    self.indices[name] = indexer.Index(name)
                            
                            print(name + ' logged in')
                            self.group.join(name)
                            mysend(sock, json.dumps({"action": "login", "status": "ok"}))
                        else:
                            mysend(sock, json.dumps({"action": "login", "status": "incorrect"}))

                elif msg['action'] == 'register':
                    user_name = msg['name']
                    password = msg['password']
                    #print("server user_name and password", user_name, password)
                    if user_name not in self.user_password.keys():
                        mysend(sock, json.dumps(
                            {'action':'register', 'status': 'ok'}))
                        print(user_name, 'registered')
                        self.user_password[user_name] = password
                    else:
                        mysend(sock, json.dumps(
                            {'action':'register', 'status': 'duplicate'}))
                
                else:
                    print('wrong code received')
            else:  # client died unexpectedly
                self.logout(sock)
        except Exception as err:
            print("error occured", err)
            self.all_sockets.remove(sock)

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(name + '.idx', 'wb'))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

# ==============================================================================
# main command switchboard
# ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        msg = myrecv(from_sock)

        if len(msg) > 0:
            # ==============================================================================
            # handle connect request this is implemented for you
            # ==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action": "connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name): #即to_name在login用户中，且不是本人
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps({"action": "connect", "status": "success"})
                    print('one connection success')
                    for g in the_guys[1:]:
                        print('group member:', g)
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps(
                            {"action": "connect", "status": "request", "from": from_name}))
                    print('message sent to group member')
                        #把线递给其他被请求的peer (注意：没有被请求的peer是不会被递线的)
                        
                else: #即to_name不在login用户中
                    msg = json.dumps(
                        {"action": "connect", "status": "no-user"})
                    
                mysend(from_sock, msg) #把线递还给本人（更新状态）
# ==============================================================================
# handle messeage exchange: IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "exchange":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                said2 = text_proc(msg['message'], from_name)
                # text_proc 来源于chat_utils.py
                self.indices[from_name].add_msg_and_index(said2)
                
                for g in the_guys[1:]:
                    to_sock = self.logged_name2sock[g]
                    self.indices[g].add_msg_and_index(said2)
                    mysend(to_sock, json.dumps(
                            {'action':'exchange', 'from': msg['from'], 'message': msg['message']}))
                
                if '@' in msg['message']:
                    idx = msg['message'].rstrip('\n').index('@') + 1
                    notify_name = msg['message'].rstrip('\n')[idx:]
                    if len(notify_name)>0 and notify_name != from_name and notify_name in the_guys:
                        to_sock_notify = self.logged_name2sock[notify_name]
                        mysend(to_sock_notify, json.dumps(
                            {'action':'@', 'from': from_name }))
# ==============================================================================
# the "from" guy has had enough (talking to "to")!
# ==============================================================================
            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(to_sock, json.dumps(
                        {"action": "disconnect", "message": "\n everyone left, you are alone \n"}))
# ==============================================================================
#                 listing available peers: IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "list":
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all(from_name)
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": msg}))
# ==============================================================================
#             retrieve a sonnet : IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "poem":
                poem_num = int(msg['target'])
                from_name = self.logged_sock2name[from_sock]
                print(from_name, 'asks for', poem_num)
                poem = self.sonnet.get_poem(poem_num)
                poem = '\n'.join(poem).strip()
                # join func, 在poem中每个element之间插入\n
                print('here:\n', poem)
                mysend(from_sock, json.dumps(
                    {"action": "poem", "results": poem}))
# ==============================================================================
#                 time 可以直接在gui端解决
# ==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps(
                    {"action": "time", "results": ctime}))
# ==============================================================================
#                 search: : IMPLEMENT THIS
# ==============================================================================
            elif msg["action"] == "search":
                term = msg['target']
                
                from_name = self.logged_sock2name[from_sock]
                print('search for', from_name, 'for', term)
                search_rslt = '\n'.join(
                    [x[-1] for x in self.indices[from_name].search(term)])
                
                #for i in self.indices[from_name].search(msg['target']):
                    #search_rslt.append(i[1])
                #问题：句末不能加标点，不然句末单词搜不出
                
                print('server side search:', search_rslt)
                mysend(from_sock, json.dumps(
                    {"action": "search", "results": search_rslt}))

# ==============================================================================
#                 the "from" guy really, really has had enough
# ==============================================================================
        else:
            # client died unexpectedly
            self.logout(from_sock)
# ==============================================================================
# main loop, loops *forever*
# ==============================================================================
    def run(self):
        print('starting server...')
        while(1):
            read, write, error = select.select(self.all_sockets, [], [])
            print('checking logged clients..')
            
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
                    
            print('checking new clients..')
            
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
                    
            print('checking for new connections..')
            
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()
