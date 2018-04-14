import unittest
import tweettest
import subprocess
import time
import os


class Test2(unittest.TestCase):
	def test_mp4(self):
			count = 0
			subprocess.call("python tweettest.py",shell = True)
			for file in os.listdir('.'):
				if file.endswith('mp4'):
					count = count + 1


	
if __name__ == '__main__': 
		unittest.main() 