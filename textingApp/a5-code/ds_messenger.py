'''Ds_messenger protocol is a module used for storing sending and recieving messages'''
import socket
import time
import json
import ds_protocol


class DirectMessage:
    '''Direct message stores the messages that are sent to you'''
    def __init__(self, recipient, message, timestamp):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    '''Direct messenger class that stores info on token, server, username, and password'''
    def __init__(self, dsuserver ='168.235.86.101', username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    
    def send(self, message:str, recipient:str) -> bool:
        '''Sends a message and returns true or false'''
        self.server_connection()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver,3021))
            send = client.makefile('w')
            recv = client.makefile('r')
            post_msg = json.dumps({"token":self.token, "directmessage": {"entry": message,
                                                                         "recipient": recipient,
                                                                         "timestamp": time.time()}})
            send.write(post_msg + '\r\n')
            send.flush()
            resp = recv.readline()
            x_1 = ds_protocol.extract_send(resp)
            if x_1.type == 'ok':
                return True
            else:
                return False


    def retrieve_new(self) -> list:
        '''Must return a list of DirectMessage objects containing all new messages'''
        self.server_connection()
        obj_list = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, 3021))
            send = client.makefile('w')
            recv = client.makefile('r')
            post_msg = json.dumps({"token":self.token, "directmessage": "new"})
            send.write(post_msg + '\r\n')
            send.flush()
            resp = recv.readline()
            x_1 = ds_protocol.recieve_message(resp)
            for values in x_1["Message"]:
                values = 1
                obj_list.append(DirectMessage(x_1['Name'],x_1['Message'], x_1['time']))
            return obj_list


    def retrieve_all(self) -> list:
        '''Must return a list of DirectMessage objects containing all messages'''
        self.server_connection()
        obj_list = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver, 3021))
            send = client.makefile('w')
            recv = client.makefile('r')
            post_msg = json.dumps({"token": self.token, "directmessage": "all"})
            send.write(post_msg + '\r\n')
            send.flush()
            resp = recv.readline()
            x_1 = ds_protocol.recieve_message(resp)
            for values in x_1["Message"]:
                values = 1
                obj_list.append(DirectMessage(x_1['Name'],x_1['Message'], x_1['time']))
            return obj_list


    def server_connection(self):
        '''Server connection function that connects and collects user token'''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((self.dsuserver,3021))
            send = client.makefile('w')
            recv = client.makefile('r')
            join_msg = json.dumps({"join": {"username": self.username,
                                            "password": self.password,
                                            "token": ''}})
            send.write(join_msg + '\r\n')
            send.flush()
            resp = recv.readline()
            message_extraction = ds_protocol.extract_json(resp)
            self.token = message_extraction.token
