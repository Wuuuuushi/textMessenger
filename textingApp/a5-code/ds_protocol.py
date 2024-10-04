'''Module that will parse responses given in a json format'''

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Rudy Xie
# rudyx@uci.edu
# 95455194

import json
from collections import namedtuple
from Profile import Profile

DataTuple = namedtuple('DataTuple', ['message', 'token'])

SendTuple = namedtuple('SendTuple', ['message', 'type'])

def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object

    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''
    json_obj = json.loads(json_msg)
    try:
        json_obj = json.loads(json_msg)
        message = json_obj['response']['message']
        token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return False
    return DataTuple(message, token)


def recieve_message(json_msg: str):
    try:
        y = Profile()
        message_dict = {"Message":[],"Name":[], "time":[]}
        json_obj = json.loads(json_msg)
        for messages in json_obj['response']['messages']:
            message_dict["Message"].append(messages['message'])
            message_dict["Name"].append(messages['from'])
            message_dict["time"].append(messages['timestamp'])
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return False
    return message_dict

def extract_send(json_msg: str) -> DataTuple:
    '''
    Same process as extract_json but will have more variables
    '''
    json_obj = json.loads(json_msg)
    try:
        json_obj = json.loads(json_msg)
        message = json_obj['response']['message']
        message_type = json_obj['response']['type']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return False
    return SendTuple(message, message_type)
