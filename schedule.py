#!/usr/bin/python3


# https://github.com/python273/vk_api/tree/master/examples
# vk_api manual. use it whenever you have questions.


import os
import sys
import time
from datetime import datetime
import numpy
import hashlib
import vkcomm


UID_VIRM  = 559680030
UID_NIKKI = 652380543
VERBOSE_MODE = 0


def vprint(msg):
	global VERBOSE_MODE
	if (VERBOSE_MODE == 1):
		print(msg)


# 0     1
# index state
class SchedDB:
	def __init__(self, pathname):
		self.pathname = pathname
		self.db = numpy.empty((0, 2), int)
		self.idx = 0


	def init(self):
		pass

	# mark task with index `idx' as performed
	def mark(self):
		self.db[self.idx][1] = 0
		self.idx += 1

	# append task into db
	def append(self):
		item = numpy.array([[self.idx, 1]])
		self.db = numpy.append(self.db, item, axis=0)
		self.idx += 1

	def isfree(self):
		if self.db[self.idx][1] == 1:
			return 1
		return 0

	def show(self):
		print("> db show: ", self.db)

	def reset(self):
		self.idx = 0

	def load(self):
		if os.path.exists(self.pathname) == 1:
			self.db = numpy.loadtxt(self.pathname, dtype=int, delimiter=',')

	def save(self):
		numpy.savetxt(self.pathname, self.db, delimiter=',')



class Schedule:
	def __init__(self, fname):
		self.fname   = fname
		self.file    = None
		self.curline = None
		self.SCHED_DATA_FUNCS = [
			self.parse_datatype1,
			self.parse_datatype2,
			self.parse_datatype3,
			self.parse_datatype4,
			self.parse_datatype5
			]
		self.db = SchedDB("content/db.csv")


	def open(self):
		try:
			self.file = open(self.fname)
		except:
			print("error: sched: {fname} does not exist".format(fname=self.fname))
			sys.exist(1)

		self.curline = self.file.readline()
		# skip comments in the beggining (if any)
		self.skiplines()

		# init schedule db too
		self.initdb()

	def close(self):
		try:
			close(self.file)
		except:
			print("error: sched: could not close schedule file")


	def rewind(self):
		self.file.seek(0)
		self.curline = self.file.readline()
		self.skiplines()


	# FIXME: cockroach
	# interval should precisely 3600 seconds (one hour)
	# because programm will resend the same messages within
	# same hour
	def run(self, interval=3600):
		RIGHT_NOW = datetime.now().strftime("%Y-%m-%d %Hh")
		print("Local time: {time}".format(time=RIGHT_NOW))
		print("sched: interval =", interval)

		while True:
			self.parse()
			self.rewind()

			time.sleep(interval)
			print()

	def initdb(self):
		# save sha256sum of schedule.txt file
		# if it's same then load db state from it
		fname_shasum = "content/shasum"
		fname_sched  = "content/schedule.txt"
		content_sched= open(fname_sched).read()
		shasum_cur   = hashlib.sha256(content_sched.encode()).hexdigest()

		if (os.path.exists(fname_shasum)):
			shasum_prev = open(fname_shasum).read().strip()
			if shasum_cur == shasum_prev:
				self.db.load()
				vprint("sched: db state is loaded")
				return 0
			else:
				os.remove(fname_shasum)



		while (self.getcurline() != ''):
			if (self.isdate() == 1):
				self.db.append()
			self.nextline()


		# reinit schedule file
		self.rewind()

		# rewind db idx as well
		self.db.reset()

		# save inited db state
		self.db.save()

		# save sha256sum as well
		file_shasum = open(fname_shasum, "w")
		file_shasum.write(shasum_cur)


	def parse(self):
		while (self.getcurline() != ''):

			if (self.parse_date() == 1 and self.db.isfree()):
				self.db.mark()

				# CAUTION: cockroach
				# parse_date() doesn't get next line automatically
				# cuz it breaks top while loop
				self.nextline()

				print("> task is executed")
				while (self.getcurline() != '' and self.getcurline() != '\n' and not self.isdate()):
					for func in self.SCHED_DATA_FUNCS:
						value = func()
						if (value):
							vkcomm.reply(UID_VIRM, value)
							vprint("message: [{value}]".format(value=value))
							break

					# skip multiple newline and comments (if any)
					self.skiplines()

			else:
				print("> task is skipped")
				while (self.getcurline() != '' and self.getcurline() != '\n'):
					self.nextline()

			# go to next schedule task
			self.skiplines()

		# rewind data index for next time
		self.db.reset()

		# save db state into file
		self.db.save()


	def getcurline(self):
		return self.curline

	def showline(self):
		print(self.curline, end='')

	def nextline(self):
		self.curline = self.file.readline()
		return self.curline

	# skip multi newlines and comments
	def skiplines(self):
		while (self.curline and (self.curline == '\n' or self.curline[0] == '#')):
			self.nextline()

	def ispadding(self):
		if (self.curline and (self.curline == '\n' or self.curline[0] == '#')):
			return 1
		else:
			return 0

	def skiptask(self):
		if ("date:" in self.curline):
			while (self.ispadding() == 1):
				self.nextline()
		else:
			print("error: sched: syntax error - cannot skip task")


	# 1 - perform task
	# 0 - skip current task (it's not time yet)
	def parse_date(self):
		RIGHT_NOW = datetime.now().strftime("%Y-%m-%d %Hh")
		out = 1 # ok by default

		line = self.curline.strip()
		if (line == ''):
			return ""

		key, value = line.split(": ")
		if (key == "date"):
			if value == RIGHT_NOW:
				out = 1
			else:
				out = 0
		else:
			print("error: sched: syntax error: date [{date}]".format(date=value))
			out = 0

		return out


	# to know when tasks finished
	def isdate(self):
		if "date: " in self.curline:
			return 1
		return 0


	# read string value
	def parse_datatype1(self):
		vprint(">> parse_datatype1")
		line = self.curline.strip()

		if (line == ""):
			return ""
		key, value = line.split(": ")
		if (key == "datatype1"):
			# update curline if parsing was successful
			self.nextline()
			return value
		else:
			return ""


	# read file
	def parse_datatype2(self):
		vprint(">> parse_datatype2")
		line = self.curline.strip()

		if (line == ""):
			return ""
		key, value = line.split(": ")
		if (key == "datatype2"):
			try:
				with open(value, "r") as f:
					content = f.read()
				# update curline if parsing was successful
				self.nextline()
				return content.strip()
			except:
				print("error: sched: file does not exist - {fname}".format(fname=value))
				# update curline if parsing was successful
				self.nextline()
				return ""

		else:
			return ""

	# read photo
	def parse_datatype3(self):
		vprint(">> parse_datatype3")
		line = self.curline.strip()

		if (line == ""):
			return ""
		key, value = line.split(": ")
		if (key == "datatype3"):
			with open(value, "r") as f:
				content = f.read()
			# update curline if parsing was successful
			self.nextline()
			return content.strip()
		else:
			return ""

	# read video file
	def parse_datatype4(self):
		vprint(">> parse_datatype4")
		line = self.curline.strip()

		if (line == ""):
			return ""
		key, value = line.split(": ")
		if (key == "datatype4"):
			with open(value, "r") as f:
				content = f.read()
			# update curline if parsing was successful
			self.nextline()
			return content.strip()
		else:
			return ""

	# read audio file
	def parse_datatype5(self):
		vprint(">> parse_datatype5")
		line = self.curline.strip()

		if (line == ""):
			return ""
		key, value = line.split(": ")
		if (key == "datatype5"):
			with open(value, "r") as f:
				content = f.read()
			# update curline if parsing was successful
			self.nextline()
			return content.strip()
		else:
			return ""
