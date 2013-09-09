#!/usr/bin/env python
# :set tabstop=8 expandtab shiftwidth=4 softtabstop=4
# :set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<
# :set list
# :set nolist
# filetype indent plugin on
""" ECDH pub/priv key calculation from NIST curves.

ECDH key exchange implementation for some NIST curves.
"""
import re
import random # random.SystemRandom() uses os.urandom() whic is secure for crypto
import arithmetic0 as ar
import ec as ec
import ecexception as ex

class ECDH(object):
    def __init__(self,curve):
        if (re.search(r"[kK]-*283",curve)):
            self._curve_name = "K-283"
            self._curve_m = 283
            self._curve_r = 3885337784451458141838923813647037813284811733793061324295874997529815829704422603873L
            self._curve_gx = 0x503213f78ca44883f1a3b8162f188e553cd265f23c1567a16876913b0c2ac2458492836L
            self._curve_gy = 0x1ccda380f1c9e318d90f95d07e5426fe87e45c0e8184698e45962364e34116177dd2259L
            self._curve_fx = 0x800000000000000000000000000000000000000000000000000000000000000000010a1L
            self._curve_T = 6
            self._curve_a = 0
            self._Qa = 0
            self._d = 0
            self._Qb = 0
            self._secret = 0 

            self._curve = ec.KoblitzEC(self._curve_m,
                                       self._curve_a, 
                                       self._curve_r, 
                                       self._curve_gx, 
                                       self._curve_gy, 
                                       self._curve_fx, 
                                       self._curve_T)

        elif (re.search(r"[bB]-*283",curve)):
            self._curve_name = "B-283"
            #TODO

    def create_priv_key(self):
        self._d = random.SystemRandom().randint(1L, self._curve_r-1L)
        return self._d

    def get_priv_key(self):
        return self._d

    def _set_priv_key(self, d):
        self._d = d
        return self._d

    def create_pub_key(self):
        self._Qa = self._curve.affine_point_mul(self._d, self._curve_gx, self._curve_gy)
        return self._Qa

    def get_pub_key(self):
        return self._Qa

    def _set_pub_key(self, Qa):
        self._Qa = Qa
        return self._Qa
    
    def get_keypair(self):
        return (self._d, self._Qa)

    def get_base_order(self):
        return self._curve_r

    def get_curve_name(self):
        return self._curve_name

    def validate_pub_key(self, Q):
        # check: type
        if (((not type(Q[0]) is int) and (not type(Q[0]) is long)) or
            ((not type(Q[1]) is int) and (not type(Q[1]) is long))): 
            raise ValueError
        # check: point-at-infintiy
        if (Q[0] == 0 and Q[1] == 0): 
            raise ex.InvalidECPublicKey(Q,"Point at infinity")
        # check: degree <= m-1 
        if ((ar._binpolydeg(Q[0]) >= self._curve_m) or 
            (ar._binpolydeg(Q[1]) >= self._curve_m)):
            raise ex.InvalidECPublicKey(Q,"Degree error")
        # check: point on curve
        if (self._curve.check_point_on_curve(Q) == 0):
            raise ex.InvalidECPublicKey(Q,"Point not on curve")
        return 1

    def create_secret_key(self, Qb):
        try:
            self.validate_pub_key(Qb)
        except ex.InvalidECPublicKey, e:
            print "Validation error: %s of public key: %s" % (e.msg,e.Q)

        self._secret = self._curve.affine_point_mul(self._d, Qb[0], Qb[1])
        return self._secret

    def get_secret_key(self):
        return self._secret

