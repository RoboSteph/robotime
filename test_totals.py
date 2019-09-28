#Trying out python unittest
#Stephanie Simpler
#9-28-2019

import unittest

class TestEventTotals(unittest.TestCase):

	def set_up(self):
		#self.widget = Widget('The widget')
		print("This method will be run for every test.")

	def test_totals(self):
		#self.assertTrue(output)
		print("Test")

	def test_error(self):
		with self.assertRaises(TypeError):
			s = "say"
			s.split(2)

	def tear_down(self):
		#self.widget.dispose()
		print("This method runs after the test method")

if __name__ == '__main__':
	unittest.main()