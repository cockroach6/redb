#!/bin/python3

# https://github.com/python273/vk_api/blob/master/examples
# https://github.com/python273/vk_api


import os
import sys

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def reply(uid, msg):
	if (msg != '\n' and len(msg) > 0):
		vk_session.method("messages.send", {'user_id': uid, 'message' : msg, 'random_id' : 0})

def send_msg(uid, msg):
	msg = msg.strip()
	if msg != '':
		vk_session.method("messages.send", {'user_id': uid, 'message' : msg, 'random_id' : 0})

def send_photo(uid, photo):
	pass

def send_audio(uid, audio):
	pass


try:
	with open("token.txt") as f:
		token = f.read().strip('\n')
	if token == '':
		raise
except:
	print("error: vkcomm: file token.txt is empty or does not exist")
	sys.exit(1)

vk_session = vk_api.VkApi(token = token)
