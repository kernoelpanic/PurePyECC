#!/usr/bin/env python
import unittest 
import sys

sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import arithmetic0 as ar

class TestBitArithmetic0(unittest.TestCase):

    def test_bitlen_pos(self):
	self.failUnlessEqual(ar._bitlen(0b1), 1)
	self.failUnlessEqual(ar._bitlen(0b0), 0) #this might be confusing

        self.failUnlessEqual(ar._bitlen(0b1111), 4) 
	self.failUnlessEqual(ar._bitlen(0b1000), 4)
	self.failUnlessEqual(ar._bitlen(8),4)
	self.failUnlessEqual(ar._bitlen(8L),4)

	self.failUnlessEqual(ar._bitlen(0b10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000010100001),284)
        self.failUnlessEqual(ar._bitlen(15541351137805832567355695254588151253139254712417116170014499277911234281641667989665L),284)

    def test_bitlen_neg(self): 
        # Not meant to be called with other values than int or long
	self.failUnlessRaises(AttributeError, ar._bitlen, 0.0) 
	
	self.assertEqual(ar._bitlen(-1),1)
	self.assertEqual(ar._bitlen(-0b1),1)
	self.assertEqual(ar._bitlen(-0),0)
	self.assertEqual(ar._bitlen(-0b0),0)
	
	self.failUnlessEqual(ar._bitlen(-8),4)
	self.failUnlessEqual(ar._bitlen(-8L),4)

    def test_binpolydeg_pos(self):
        self.failUnlessEqual(ar._binpolydeg(0b1),0) # 1 
        self.failUnlessEqual(ar._binpolydeg(0b11),1) # x + 1
        self.failUnlessEqual(ar._binpolydeg(0b10),1) # x
        
        self.failUnlessEqual(ar._binpolydeg(0b101),2) # x^2 + 1
        self.failUnlessEqual(ar._binpolydeg(0b1000000),6) # x^6

        self.failUnlessEqual(ar._binpolydeg(0b10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000010100001),283)
        self.failUnlessEqual(ar._binpolydeg(15541351137805832567355695254588151253139254712417116170014499277911234281641667989665L),283)

    def test_binpolydeg_neg(self):
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(AttributeError, ar._binpolydeg, 0.0)

        self.failUnlessEqual(ar._binpolydeg(0b0),0)

        self.failUnlessEqual(ar._binpolydeg(-0b1),0) # ignores signed
        self.failUnlessEqual(ar._binpolydeg(-0b0),0) 
        self.failUnlessEqual(ar._binpolydeg(-0b101),2)

    def test_bittest_pos(self):
        self.failUnlessEqual(ar._bittest(0b1,0),1)
        self.failUnlessEqual(ar._bittest(0b0,0),0)
        self.failUnlessEqual(ar._bittest(0b111,1),1)
        self.failUnlessEqual(ar._bittest(0b101,1),0)

        self.failUnlessEqual(ar._bittest(0b1000,3),1)
        self.failUnlessEqual(ar._bittest(0b1000,2),0)
        self.failUnlessEqual(ar._bittest(8,3),1)
        self.failUnlessEqual(ar._bittest(8,2),0)
        self.failUnlessEqual(ar._bittest(8L,3),1)
        self.failUnlessEqual(ar._bittest(8L,2),0)
        
        self.failUnlessEqual(ar._bittest(0b10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000010100001,283),1)
        self.failUnlessEqual(ar._bittest(15541351137805832567355695254588151253139254712417116170014499277911234281641667989665L,283),1)
    
    def test_bittest_neg(self):
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(TypeError, ar._bittest, 0.0, 1)
        self.failUnlessRaises(TypeError, ar._bittest, 0b101, 1.0)

        # overflow of offset
        self.failUnlessEqual(ar._bittest(0b00000,2),0)
        self.failUnlessEqual(ar._bittest(0b0,2),0)
        self.failUnlessEqual(ar._bittest(0b0,283),0)
        self.failUnlessEqual(ar._bittest(0b1,3),0)
        self.failUnlessEqual(ar._bittest(0b10000,8),0)

        # negativ offset
        self.failUnlessEqual(ar._bittest(0b101,-1),0)
        self.failUnlessEqual(ar._bittest(0b101,-2),1)
        self.failUnlessEqual(ar._bittest(0b101,-0),1)

        # negativ value
        self.failUnlessEqual(ar._bittest(-0b1111,2),1)
        self.failUnlessEqual(ar._bittest(-0b1011,2),0)

if __name__ == "__main__": 
    unittest.main()
