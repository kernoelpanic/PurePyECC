#!/usr/bin/env python
import unittest 
import sys

sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import ecdh as ecdh
import ecexception as ex

class TestECDH(unittest.TestCase):

    def setUp(self):
        self.alice = ecdh.ECDH("K-283")
        self.bob = ecdh.ECDH("K-283") 

    def test_handshake__pos(self):
        da = self.alice.create_priv_key()
        Qa = self.alice.create_pub_key()
        #print "da: %s" % hex(da)
        #print "Qa: \nx=%s\ny=%s " % (hex(Qa[0]),hex(Qa[1]))

        db = self.bob.create_priv_key()
        Qb = self.bob.create_pub_key()
        #print "db: %s" % hex(db)
        #print "Qb: \nx=%s\ny=%s " % (hex(Qb[0]),hex(Qb[1]))

        seca = self.alice.create_secret_key(Qb)
        secb = self.bob.create_secret_key(Qa)
        #print hex(seca[0])
        #print hex(secb[0])
        self.assertTrue(seca[0] == secb[0])

    def test_keypair_creation__pos(self):
	#self.failUnlessEqual(ar._bitLen(0b1), 1)
        d = self.alice.create_priv_key()
        self.assertTrue(1L < d < self.alice.get_base_order()-1L)
        self.assertTrue(d == self.alice.get_priv_key())

        Q = self.alice.create_pub_key()
        self.assertTrue(1 == self.alice.validate_pub_key(Q))
    
    def test_public_key_validation__neg(self):
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(ValueError, self.alice.validate_pub_key, ("asdf",0.0))
        
        Q = self.alice.create_pub_key()
        Qt = (Q[0], Q[1] << 10)
        self.failUnlessRaises(ex.InvalidECPublicKey, self.alice.validate_pub_key, Qt)
        Qt = (Q[0], 0x3f7c12d07bf1313daf82f03c742bdfa62670d4e82004e9bd1ea332ec29793a3d59ea133L)
        self.failUnlessRaises(ex.InvalidECPublicKey, self.alice.validate_pub_key, Qt)
        Qt = (0,0)
        self.failUnlessRaises(ex.InvalidECPublicKey, self.alice.validate_pub_key, Qt)
        

if __name__ == "__main__": 
    unittest.main()
