import ds_protocol
import socket
import json
import time

def test_case1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect(('168.235.86.101',3021))
      send = client.makefile('w')
      recv = client.makefile('r')
      post_msg = json.dumps({"token": '5845d99e-7ed7-41da-a22a-504feea15985', "directmessage": {"entry": 'Test for milky', "recipient": 'Milky',
                                                                       "timestamp": time.time()}})
      send.write(post_msg + '\r\n')
      send.flush()
      resp = recv.readline()
      x = ds_protocol.extract_send(resp)
      assert x.message == 'Direct message sent'
      assert x.type == 'ok'
      
def test_case2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect(('168.235.86.101',3021))
      send = client.makefile('w')
      recv = client.makefile('r')
      join_msg = json.dumps({"join": {"username": 'Milky',
                                      "password": 'John',
                                      "token": ''}})
      send.write(join_msg + '\r\n')
      send.flush()
      resp = recv.readline()
      message_extraction = ds_protocol.extract_json(resp)
      assert message_extraction.message == "Welcome back, Milky"
      assert message_extraction.token == '5845d99e-7ed7-41da-a22a-504feea15985'
if __name__ == '__main__':
    test_case1()
    test_case2()
    
