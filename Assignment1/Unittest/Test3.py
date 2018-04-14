import unittest
import tweettest
import subprocess
import time
import os


class Testmini1(unittest.TestCase):
	
	def test_label(self):
		find = 0
		subprocess.call("python tweettest.py",shell = True)
		for file in os.listdir('./photo'):
			if file.endswith('txt'):
				find = find+ 1


		self.assertEqual(find,1)

	
if __name__ == '__main__': 
		unittest.main() 