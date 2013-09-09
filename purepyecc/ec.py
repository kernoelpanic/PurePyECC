#!/usr/bin/env python
# :set tabstop=8 expandtab shiftwidth=4 softtabstop=4
# filetype indent plugin on
""" Elliptic Curve definitions

Classes that define some elliptic curves found in the 
NIST recommended elliptic curves for federal government use
"""
import arithmetic0 as ar

POLY=1 # polynomial basis
NORM=2 # normal basis

class EllipticCurve(object):
    def __init__(self, a, b, r, gx, gy, fx, h):
        self._a=a
	self._b=b
        self._r=r
	self._gx=gx
        self._gy=gy
        self._fx=fx
        self._h=h

    def __del__(self):
        pass
       
    def projective_point_mul(self, k,x,y,z):
        pass

    def projective_to_affine(x,y):
        pass

    def affine_to_projective(x,y,z):
        pass

class PrimeEC(EllipticCurve):
    """ Elliptic curve over F_p

    According to SEC 1:
    T = (p, a, b, G, n, h)
    """
    #TODO
    pass

class BinaryEC(EllipticCurve):
    """ Elliptic curve over F_{2^m}

    According to SEC 1:
    T = (m, f(x), a, b, G, n, h)
    """
    def __init__(self, m, a, b, r, gx, gy, fx, h, basis=POLY, s=0):
        """ Initi with (m, a, r, gx, gy, fx, h, basis=POLY)

        @param m: Value of finite field F_{2^m}
        @param a: a \in F_{2^m} coefficient specifying the EC E(F_{2^m})
        @param r: Order of G = (gx, gy) on E(F_{2^m})
        @param gx: x coordinate of G = (gx, gy)
        @param gy: y coordinate of G = (gx, gy)
        @param fx: Irreducible binary polynomail of degree m
        @param h: Cofactor h = #(E(F_{2^m})/r)
        @param basis: Normal or polynomial basis basis = {POLY, NORM}
        """ 
        EllipticCurve.__init__(self, a, b, r, gx, gy, fx, h)
        self._m=m
        self._basis=basis

    def check_point_on_curve(self, P):
        """ Checks if point is on curve. 

        y^2 + x*y = x^3 + a*x^2 + b
        """
        x = P[0]
        y = P[1]
        if ((ar._binpolydeg(x) >= self._m) or
            (ar._binpolydeg(y) >= self._m)):
                return 0
        left = ar.gf2m_add(ar.gf2m_modmul(y,y,self._fx),
                           ar.gf2m_modmul(x,y,self._fx))
        right = ar.gf2m_add(ar.gf2m_add(
                ar.gf2m_modmul(ar.gf2m_modmul(x,x,self._fx),x,self._fx),
                ar.gf2m_modmul(self._a,ar.gf2m_modmul(x,x,self._fx),self._fx)),
                self._b)
        if (left == right):
            return 1
        return 0
 
    def affine_point_mul(self, k, x, y):
        Q = (0,0) # point at infinity
        first = True 

        for i in range(0,k.bit_length()):
            Q = ar.ecgf2m_dbl_point(Q[0],Q[1],self._fx,self._a)

            if (ar._bittest(k,(k.bit_length()-1) - i) == 0b1):
                if (first):
                    Q = (x,y)
                    first = False                    
                else:
                    Q = ar.ecgf2m_add_point(Q[0],Q[1],x,y,self._fx,self._a)
            #print "DBG:\ni=%d\nQ[0]=%s\nQ[1]=%s\n" % (i,hex(Q[0]),hex(Q[1]))
        return Q

class KoblitzEC(BinaryEC):
    """ Koblitz curve over F_{2^m}

    b=1
    a={0,1}
    h={2,4}
    """
    def __init__(self, m, a, r, gx, gy, fx, T, basis=POLY):
        """ Initi with (m, a, r, gx, gy, fx, T, basis=POLY)

        @param m: Value of finite field F_{2^m}
        @param a: a \in F_{2^m} coefficient specifying the EC E(F_{2^m})
        @param r: Order of G = (gx, gy) on E(F_{2^m})
        @param gx: x coordinate of G = (gx, gy)
        @param gy: y coordinate of G = (gx, gy)
        @param fx: Irreducible binary polynomail of degree m
        @param T: Normal basis type
        @param basis: Normal or polynomial basis basis = {POLY, NORM}
        """
        if (a == 1): # h = 2
            BinaryEC.__init__(self, m, a, 1, r, gx, gy, fx, 2, basis)
        elif (a == 0): # h = 4
            BinaryEC.__init__(self, m, a, 1, r, gx, gy, fx, 4, basis)
        self._T=T

