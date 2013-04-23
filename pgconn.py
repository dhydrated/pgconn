#!/usr/bin/python


from optparse import OptionParser
import os
import glob
import time
import gzip
import datetime


class ArgumentParser:
	"""Commandline arguments"""

	options = ""
	args = ""

	def parse(self):
		self.parser = OptionParser()

		home = os.path.expanduser('~')

		self.parser.add_option("-p", "--path", dest="path", metavar="path", default=home+"/.pgpass",
                  help="Path to .pgpass. Default will be ~/.pgpass")

		self.parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="print out messages")

		(self.options, self.args) = self.parser.parse_args()

	def isValid(self):
		return True

	def getPath(self):
		return self.options.path

	def isVerbose(self):
		return self.options.verbose

	def printUsage(self):
		self.parser.print_help()

class Logger:
	"""Script logger"""

	def __init__(self, arguments):
		self.arguments = arguments
		self.verbose = self.arguments.isVerbose()

	def debug(self, msg):
		if self.verbose :
			self._print_(msg)

	def info(self, msg):
		self._print_(msg)
			
	def _print_(self,msg):
		print str(datetime.datetime.today())+" : "+str(msg)

		
class PgInfo:
	"""pg connection details"""
	delimiter=":"

	def __init__(self, logger, rawInfo):
		self.logger = logger
		self.rawInfo = rawInfo

	def parse(self):
		data = self.rawInfo.replace('\n','').split(self.delimiter)
		self.logger.debug(data)
		self.host = data[0]
		self.port = data[1]
		self.dbname = data[2]
		self.username = data[3]
		self.password = data[4]

	def getName(self):
		return self.host+self.delimiter+self.port+self.delimiter+self.dbname+self.delimiter+self.username

	def getExecuteCommand(self):
		return "psql -h "+ self.host +" " + self.dbname + " -U " + self.username

class PgPassParser:
	""".pgpass parser"""
	databases = []

	def __init__(self, logger, arguments):
		self.logger = logger
		self.filePath = arguments.getPath()

	def parse(self):
		fileObject = file(self.filePath, 'r')																		
		for line in fileObject:
			pgInfo = PgInfo(self.logger, line)
			pgInfo.parse()
			self.databases.insert(0, pgInfo)

	def getDatabases(self):
		return self.databases

class MenuBuilder:
	"""Menu builder"""
	menu=""
	selection=None

	def __init__(self, logger, items):
		self.logger = logger
		self.items = items

	def display(self):
		index = 1
		self.menu = "Please select a connection:\n"
		for item in self.items:
			self.menu += str(index) + ") " + item.getName() + "\n"
			index+=1

		self.menu += "Your selection: "
		self.selection = raw_input(self.menu)

	def getSelection(self):
		return self.selection

class ItemExecutor:
	"""Item Executor"""
		
	def __init__(self, logger, items, selection):
		self.logger = logger
		self.selection = selection
		self.items = items

	def execute(self):
		self.logger.debug(self.getItem().getExecuteCommand())
		os.system(self.getItem().getExecuteCommand())

	def getItem(self):
		return self.items[int(self.selection)-1]


def main():
	arguments = ArgumentParser()
	arguments.parse()

	logger = Logger(arguments)

	if arguments.isValid():
		parser = PgPassParser(logger, arguments)
		parser.parse()

		menu = MenuBuilder(logger, parser.getDatabases())
		menu.display()

		executor = ItemExecutor(logger, parser.getDatabases(), menu.getSelection())
		executor.execute()
		
	else:
		arguments.printUsage()


if __name__ == "__main__":
	main()


	
