import unittest
import tweettest
import subprocess
import time
import os


class Testmini1(unittest.TestCase):

	def test_time(self):
		start = time.time()
		subprocess.call("python tweettest.py",shell = True)
		stop = time.time()
		time1 = stop - start
		self.assertLess(time1,10)
	


	
if __name__ == '__main__': 
		unittest.main() 