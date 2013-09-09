#!/usr/bin/env python
import unittest 
import sys

sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import arithmetic0 as ar

class TestFieldArithmetic0(unittest.TestCase):

    def test_gf2m_add__pos(self):
        """ Positive tests for gf2m_add(a,b) 

        Sage test calculations::
            sage: F.<t> = GF(2)[]
            sage: a = x^3 + x^2 + 1    # a = 0b1101
            sage: b = x^2 + x          # b = 0b110
            sage: a+b
            x^3 + x + 1
            sage: b+a
            x^3 + x + 1
        """
	self.failUnlessEqual(ar.gf2m_add(0b1101,0b110), 0b1011)
	self.failUnlessEqual(ar.gf2m_add(0b110,0b1101), 0b1011)

    def test_gf2m_add__neg(self):
        """ Negative tests for gf2m_add(a, b) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(TypeError, ar.gf2m_add, 0.0, 0b110)
        self.failUnlessRaises(TypeError, ar.gf2m_add, "asdf", 0b110)
         
	self.failUnlessEqual(ar.gf2m_add(-0b110,0b1101), 0b1011)
	self.failUnlessEqual(ar.gf2m_add(0b110,-0b1101), 0b1011)
	self.failUnlessEqual(ar.gf2m_add(0b110,-0b1101), 0b1011)

    def test_gf2m_sub__pos(self):
        """ Positive tests for gf2m_sub(a, b)

        Sage test calculations::
            sage: F.<t> = GF(2)[]
            sage: a = x^3 + x^2 + 1    # a = 0b1101
            sage: b = x^2 + x          # b = 0b110
            sage: a-b
            x^3 + x + 1
            sage: b-a
            x^3 + x + 1
        """
	self.failUnlessEqual(ar.gf2m_sub(0b1101,0b110), 0b1011)
	self.failUnlessEqual(ar.gf2m_sub(0b110,0b1101), 0b1011)

    def test_gf2m_sub__neg(self):
        """ Negative tests for gf2m_sub(a,b) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(TypeError, ar.gf2m_sub, 0.0, 0b110)
        self.failUnlessRaises(TypeError, ar.gf2m_sub, "asdf", 0b110)
         
	self.failUnlessEqual(ar.gf2m_sub(-0b110,0b1101), 0b1011)
	self.failUnlessEqual(ar.gf2m_sub(0b110,-0b1101), 0b1011)
	self.failUnlessEqual(ar.gf2m_sub(0b110,-0b1101), 0b1011)

    def test_gf2m_mod__pos(self):
        """ Positive tests gf2m_mod(a, f)
        
        Sage test calculations::
            sage: F.<x> = GF(2)[]
            sage: a  = x^5 + x^3 + x^2 + x      # a = 0b101110
            sage: f = x^4 + x +1                # f = 0b10011
            sage: c.mod(f)
            x^3                                 #  == 0b1000
            sage: a = x^4 + x^3 + x^2 + x + 1   # a = 0b11111
            sage: a.mod(f)
            x^3 + x^2
            sage: a = x^13 + x^12 + x^11 + x^10 + x^9 + x^8 + x^6 + x^5 + x^4 + x^3 + x^2 + x   
            # a = 0b11111101111110
            sage: f = x^8 + x^4 + x^3 + x + 1   # f = 0b100011011
            sage: a.mod(fx)
            1
            sage: f = x^4 + x +1                # f = 0b10011
            sage: a  = x^3 + x                  # a = 0b1010
            sage: a.mod(fx)
            x^3 + x
            ---
            sage: f = x^4 + x + 1
            sage: a = x^0   # a == 1
            sage: a.mod(f)
            1
            sage: a = x^0 + 1 # a == 1 + 1 == 0
            sage: a.mod(f)
            0
        """
	self.failUnlessEqual(ar.gf2m_mod(0b101110,0b10011), 0b1000)
	self.failUnlessEqual(ar.gf2m_mod(0b11111,0b10011), 0b1100)
	self.failUnlessEqual(ar.gf2m_mod(0b11111101111110,0b100011011), 0b1)
	self.failUnlessEqual(ar.gf2m_mod(0b1010,0b10011), 0b1010)
	
        self.failUnlessEqual(ar.gf2m_mod(0b0,0b10011), 0b0)
	self.failUnlessEqual(ar.gf2m_mod(0b1,0b10011), 0b1)

    def test_gf2m_mod__neg(self):
        """ Negative tests for gf2m_mod(a,f) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(AttributeError, ar.gf2m_mod, 0.0, 0b110)
        self.failUnlessRaises(TypeError, ar.gf2m_mod, "asdf", 0b110)
 
	self.failUnlessEqual(ar.gf2m_mod(-0b101110,0b10011), 0b1000)
	self.failUnlessEqual(ar.gf2m_mod(0b101110,-0b10011), 0b1000)
	self.failUnlessEqual(ar.gf2m_mod(-0b101110,-0b10011), 0b1000)

    def test_gf2m_mul__pos(self):
        """ Positive tests for gf2m_mul(a,b)

        Sage test calculations::
            sage: F.<t> = GF(2)[]
            sage: a = x^3 + x^2 + 1    # a = 0b1101
            sage: b = x^2 + x          # b = 0b110
            sage: a*b
            x^5 + x^3 + x^2 + x
            sage: b*a
            x^5 + x^3 + x^2 + x
            sage: (x^6 + x^4 + x + 1)*(x^7 + x^6 + x^3 + x)
    x^13 + x^12 + x^11 + x^10 + x^9 + x^8 + x^6 + x^5 + x^4 + x^3 + x^2 + x
            # a = 0x53
            # b = 0xCA
            ---
            sage: b = x^2 + x
            sage: a = x^0
            sage: a
            1
            sage: a*b
            x^2 + x
            sage: a = x^0 + 1 
            sage: a
            0
            sage: a*b
            0
        """
	self.failUnlessEqual(ar.gf2m_mul(0b1101,0b110), 0b101110)
	self.failUnlessEqual(ar.gf2m_mul(0b110,0b1101), 0b101110)
	
        self.failUnlessEqual(ar.gf2m_mul(0x53,0xCA), 0b11111101111110)
        self.failUnlessEqual(ar.gf2m_mul(0xCA,0x53), 0b11111101111110)
        
	self.failUnlessEqual(ar.gf2m_mul(0b1,0b110), 0b110)
    	self.failUnlessEqual(ar.gf2m_mul(0b0,0b110), 0b0)
    
    def test_gf2m_mul__neg(self):
        """ Negative tests for gf2m_mul(a,b) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(AttributeError, ar.gf2m_mul, 0.0, 0b110)
        self.failUnlessRaises(TypeError, ar.gf2m_mul, "asdf", 0b110)
        
	self.failUnlessEqual(ar.gf2m_mul(-0b1101,0b110), 0b101110)
	self.failUnlessEqual(ar.gf2m_mul(0b1101,-0b110), 0b101110)
	self.failUnlessEqual(ar.gf2m_mul(-0b1101,0b110), 0b101110)

    def test_gf2m_modmul__pos(self):
        """ Positive tests for gf2m_modmul(a, b, f)

        Sage test calculations::
            sage: F.<x> = GF(2)[]
            sage: FF.<y> = GF(2**4, name='y', modulus=x^4 + x + 1 )
            # f = 0b10011
            sage: a = y^3 + y^2 + 1         # a = 0b1101
            sage: b = y^2 + y               # b = 0b110
            sage: a*b
            y^3                             #  == 0b100
            sage: K.<y> = GF(2**8, name='y', modulus=x^8 + x^4 + x^3 + x + 1 )
            # f = 0b100011011
            sage: a = y^6 + y^4 + y + 1     # a = 0b1010011
            sage: b = y^7 + y^6 + y^3 + y   # b = 0b11001010
            sage: a*b
            1   
        """ 
	self.failUnlessEqual(ar.gf2m_modmul(0b1101,0b110,0b10011), 0b1000)
	self.failUnlessEqual(ar.gf2m_modmul(0b110, 0b1101,0b10011), 0b1000)
    
	self.failUnlessEqual(ar.gf2m_modmul(0b1010011, 0b11001010, 0b100011011), 0b1)
	self.failUnlessEqual(ar.gf2m_modmul(0b11001010, 0b1010011, 0b100011011), 0b1)

    def test_gf2m_modmul__neg(self):
        """ Negative tests for gf2m_modmul(a,b) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(AttributeError, ar.gf2m_modmul, 0.0, 0b110, 0b10011)
        self.failUnlessRaises(TypeError, ar.gf2m_modmul, "asdf", 0b110, 0b10011)

	self.failUnlessEqual(ar.gf2m_modmul(-0b1101,0b110,0b10011), 0b1000)
	self.failUnlessEqual(ar.gf2m_modmul(0b1101,-0b110,0b10011), 0b1000)
	self.failUnlessEqual(ar.gf2m_modmul(-0b1101,-0b110,0b10011), 0b1000)
   
    def test_gf2m_modmulinv__pos(self):
        """ Positive tests for gf2m_modmulinv(a,f)

        Sage test calculations::
            sage: F.<y> = GF(2)[]
            sage: a = y^6 + y^4 + y + 1         # a = 0b1010011
            sage: b = y^7 + y^6 + y^3 + y       # b = 0b11001010
            sage: p = y^8 + y^4 + y^3 + y + 1   # f = 0b100011011
            sage: ai = a.inverse_mod(p); ai
            y^7 + y^6 + y^3 + y
            sage: inverse_mod(a,p)
            y^7 + y^6 + y^3 + y
            sage: b == ai
            True
        """ 
	self.failUnlessEqual(ar.gf2m_modmulinv(0b1010011,0b100011011),0b11001010)

    def test_gf2m_modmulinv__neg(self):
        """ Negative tests for gf2m_modmulinv(a,f) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(AttributeError, ar.gf2m_modmulinv, 0.0, 0b10011)
        self.failUnlessRaises(TypeError, ar.gf2m_modmulinv, "asdf", 0b10011)

	self.failUnlessEqual(ar.gf2m_modmulinv(-0b1010011,0b100011011),0b11001010)
	self.failUnlessEqual(ar.gf2m_modmulinv(0b1010011,-0b100011011),0b11001010)
	self.failUnlessEqual(ar.gf2m_modmulinv(-0b1010011,-0b100011011),0b11001010)
    
    def test_gf2m_div__pos(self):
        """ Positive tests for gf2m_div(a, b, f) 

        Sage test calculations::
            sage: F.<x> = GF(2)[]
            sage: a = x^3 + x^2 + 1         # a = 0b1101
            sage: b = x^2 + x               # b = 0b110
            sage: p = x^4 + x + 1           # f = 0b10011
            sage: bi = b.inverse_mod(p); bi
            x^2 + x + 1
            sage: tmp = a * bi; tmp
            x^5 + x + 1
            sage: tmp.mod(p)
            x^2 + 1
            -------
            sage: FF.<y> = GF(2**4, name='y', modulus=x^4 + x + 1 )
            sage: a = y^3 + y^2 + 1
            sage: b = y^2 + y
            sage: a/b
            y^2 + 1
        """
        self.failUnlessEqual(ar.gf2m_div(0b1101, 0b110, 0b10011),0b101)
       
    def test_gf2m_div__neg(self):
        """ Negative tests for gf2m_div(a,b,f) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(AttributeError, ar.gf2m_div, 0.0, 0b110, 0b10011)
        self.failUnlessRaises(TypeError, ar.gf2m_div, "asdf", 0b110, 0b10011)
 
        self.failUnlessEqual(ar.gf2m_div(-0b1101, 0b110, 0b10011),0b101)
        self.failUnlessEqual(ar.gf2m_div(0b1101, -0b110, 0b10011),0b101)
        self.failUnlessEqual(ar.gf2m_div(0b1101, 0b110, -0b10011),0b101)
        self.failUnlessEqual(ar.gf2m_div(-0b1101, -0b110, -0b10011),0b101)

if __name__ == "__main__": 
    unittest.main()
