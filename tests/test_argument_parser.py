from pgconn.argument_parser import ArgumentParser
from nose.tools import *
import os


class TestArgumentParser():

	arguments = None

	def setUp(self):
		self.arguments = ArgumentParser()
		self.arguments.parse()

	def tearDown(self):
		self.arguments = None

	def test_argument_parser_after_parsed(self):		

		actual = self.arguments.getPath()
		expected = os.path.expanduser('~') + '/.pgpass'

		eq_(actual, expected, msg="%s is not equal %s" % (actual, expected))
