#!/usr/bin/env python
import unittest 
import sys

sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import arithmetic0 as ar

class TestTemplate(unittest.TestCase):

    def test_pos(self):
        #self.failUnlessEqual(ar._bitLen(0b1), 1)
        #self.assertEqual(Q, (0,0), "msg")
        return 0
    
    def test_neg(self):
        # Not meant to be called with other values than int or long
        #self.failUnlessRaises(ValueError, ar._testBit, 0.0, 1)
        #self.failUnlessRaises(TypeError, ar._testBit, 0b101, 1.0)
        return 0

if __name__ == "__main__": 
    unittest.main()
