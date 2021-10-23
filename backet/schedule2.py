#!/usr/bin/python3


import os
import sys
import time
from datetime import datetime


# FIXME: cockroach
# all these functions have to return empty string in case of error

RIGHT_NOW = datetime.now().strftime("%d-%m %Hh")
# print(RIGHT_NOW)
# sys.exit(0)


sched_fname = "schedule.txt"
sched_file = open(sched_fname, "r")
if sched_file == None:
	print("error: redb: could not open schedule file")
	os.exit(1)


def sched_get_line():
	global sched_file;
	global sched_fname;
	line = sched_file.readline()
	# print(">>line ", line, end='')
	if line:
		return line
	else:
		print("schedule: end of file")
		sched_file.close()
		sys.exit(0)


def sched_skip_task():
	parse_datatype1()
	parse_datatype2()
	parse_datatype3()
	parse_datatype4()
	parse_datatype5()
	pass


# return
# 1 - perform task
# 0 - skip current task (it's not time)
def parse_date():
	line = sched_get_line().strip('\n')
	if line[:2] == "> ":
		line = line[2:]
		if line == RIGHT_NOW:
			print("sched: do perform this task: {line}".format(line=line))
			return 1
		else:
			print("sched: do NOT perform this task: {line}".format(line=line))
			return 0
	else:
		return 0


def parse_datatype1():
	line = sched_get_line().strip('\n')
	key, value = line.split(": ")
	if (key == "datatype1"):
		return value
	else:
		return None

# read file
def parse_datatype2():
	line = sched_get_line().strip('\n')
	key, value = line.split(": ")
	if (key == "datatype2"):
		with open(value, "r") as f:
			content = f.read()
		return content
	else:
		return None

def parse_datatype3():
	line = sched_get_line().strip('\n')
	key, value = line.split(": ")
	if (key == "datatype3"):
		with open(value, "r") as f:
			content = f.read()
		return content
	else:
		return None

def parse_datatype4():
	line = sched_get_line().strip('\n')
	key, value = line.split(": ")
	if (key == "datatype4"):
		with open(value, "r") as f:
			content = f.read()
		return content
	else:
		return None

def parse_datatype5():
	line = sched_get_line().strip('\n')
	key, value = line.split(": ")
	if (key == "datatype5"):
		with open(value, "r") as f:
			content = f.read()
		return content
	else:
		return None



while True:
	# parse date and compare whether or not execute it
	if (parse_date() == 0):
		continue

	# get values to send to
	print(">1 {value}".format(value=parse_datatype1()))
	print(">2 {value}".format(value=parse_datatype2()))
	print(">3 {value}".format(value=parse_datatype3()))
	print(">4 {value}".format(value=parse_datatype4()))
	print(">5 {value}".format(value=parse_datatype5()))
	print()
	sched_get_line() # skip newline between tasks
