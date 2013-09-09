#!/usr/bin/env python
""" Functions for basic ECC arithmetic.

- Basic binary arithmetic.
- Field arithmetic with polynomials in GF(2)/GF(2^m).
- EC arithmetic on ECs in GF(2^m).
"""
__version__ = "0.1.0"
__author__ = "Aljosha Judmayer"
__licence__ = """ GPL """

import re # needed for poly_to_num()

#----------------------------------------------
# Functions for EC arithmetic on ECs in GF(2^m) 
#----------------------------------------------

def ecgf2m_add_point(x1, y1, x2, y2, f, a=0b0):
    """ Add a point to another (x1,y1)+(x2,y2)=(x3,y3)
    
    let J + K = L where L = (x3, y3), then the equations 
    to add two points with different x coodrinates x1 != x2::
        s = (y2 + y1) / (x2 + x1)
        x3 = s^2 + s + x1 + x2 + a
        y3 = s*(x1 + x3) + x3 + y1 = s*(x2 + x3) + x3 + y2
    @param x1,y1: point one as two binary polynomials
    @type x1: int or long
    @type y1: int or long
    @param x2,y2: Point two as two binary polynomials
    @type x2: int or long
    @type y2: int or long
    @param f: irreducable polynome f(x), used for modular reduction
    @type f: int or long
    @param a: Coefficient 'a' of curve, default is a=0. In a Koblitz curve 'a' is either 0 or 1 and 'b' is always zero, b=0. 
    @type a: int or long
    @return: (x3,y3), sum of two points as new point represented as tuple 
    """
    if (((not type(x1) is int) and (not type(x1) is long)) or
    	((not type(y1) is int) and (not type(y1) is long)) or
    	((not type(x2) is int) and (not type(x2) is long)) or
    	((not type(y2) is int) and (not type(y2) is long)) or
	((not type(f) is int) and (not type(f) is long)) or
	((not type(a) is int) and (not type(a) is long))):
	raise ValueError("No valid int or long input!")
    
    if (x1 == x2):
        if (y1 != y2):
            return (0,0) # point at infinity
        else:
            return ecgf2m_dbl_point(x1, y1, f, a)
    s = gf2m_div(gf2m_add(y2,y1),gf2m_add(x2,x1),f)
    x3 = gf2m_add(gf2m_add(gf2m_add(gf2m_add(gf2m_modmul(s,s,f),s),x1),x2),a)
    y3 = gf2m_add(gf2m_add(gf2m_modmul(s,gf2m_add(x1,x3),f),x3),y1)
    return (x3, y3) 


def ecgf2m_dbl_point(x, y, f, a=0b0):
    """ Add point to itself aka. double point. (x,y)*2=(x3,y3)

    Let 2J = L where L = (x3, y3). The the equations to double 
    the point J = (x, y) are as follows::
        s = x + (y / x)
        x3 = s^2 + s + a = x^2 + b / x^2
        y3 = x^2 + s*x3 + x3
    @param x,y: point to double as two binary polynomials
    @type x: int or long
    @type y: int or long
    @param f: irreducable polynome f(x), used for modular reduction
    @type f: int or long
    @param a: Coefficient 'a' of curve, default is a=0. In a Koblitz curve 'a' is either 0 or 1 and 'b' is always zero, b=0.
    @type a: int or long
    @return: (x3,y3), doubled point as tuple
    """
    if (((not type(x) is int) and (not type(x) is long)) or
    	((not type(y) is int) and (not type(y) is long)) or
	((not type(f) is int) and (not type(f) is long)) or
	((not type(a) is int) and (not type(a) is long))):
	raise ValueError("No valid int or long input!")

    if (x == 0):
        return (0,0) # point at infinity
    else:
        s = gf2m_add(x,gf2m_div(y,x,f))
        x3 = gf2m_add(gf2m_add(gf2m_modmul(s,s,f),s),a) 
        y3 = gf2m_add(gf2m_add(gf2m_modmul(x,x,f),gf2m_modmul(s,x3,f)),x3)
        return (x3,y3)

def ecgf2m_sub_point(x1, y1, x2, y2, f, a=0b0):
    """ Subtraction of two points (x1,y1)-(x2,y2)=(x3,y3)

    Let J - K = J + (-K) where -K = (xk,xk + yk):: 
        (x1,y1) - (x2,y2) = (x1,y1) + (-(x2,y2))
        (x1,y1) - (x2,y2) = (x1,y1) + (x2,x2 + y2))
    @param x1,y1: Point one as two binary polynomials
    @type x1: int or long
    @type y1: int or long
    @param x2,y2: Point two as two binary polynomials
    @type x2: int or long
    @type y2: int or long
    @param f: irreducable polynome f(x), used for modular reduction
    @type f: int or long
    @param a: Coefficient 'a' of curve, default is a=0. In a Koblitz curve 'a' is either 0 or 1 and 'b' is always zero, b=0.
    @type a: int or long
    @return: (x3,y3), subtracted point as tuple 
    """
    if (((not type(x1) is int) and (not type(x1) is long)) or
        ((not type(y1) is int) and (not type(y1) is long)) or
        ((not type(x2) is int) and (not type(x2) is long)) or
        ((not type(y2) is int) and (not type(y2) is long)) or
        ((not type(f) is int) and (not type(f) is long)) or
        ((not type(a) is int) and (not type(a) is long))):
        raise ValueError("No valid int or long input!")

    return ecgf2m_add_point(x1,y1,x2,gf2m_add(x2,y2),f,a)

#---------------------------------------
# Function for field arithmetic with 
# polynomials in GF(2)/GF(2^m) 
#---------------------------------------

def gf2m_add(a, b):
    """ Element addition: (a+b)
    
    Addition and substraction are the same in GF(2^m). 
    The operation is a simple XOR of the absolute values. 
    @param a,b: binary polynomials
    @type a: int or long
    @type b: int or long
    @return: sum as binary polynomial in GF(2)
    """
    return abs(a) ^ abs(b)

def gf2m_sub(a, b):
    """ Element substraction: (a-b)
    
    Addition and substraction are the same in GF(2^m).
    The operation is a simple XOR of the absolute values. 
    @param a,b: binary polynomials
    @type a: int or long
    @type b: int or long
    @return: difference as binary polynomial in GF(2)
    """
    return abs(a) ^ abs(b)

def gf2m_mul(a, b):
    """ Element multiplication: (a*b)
    
    Multiplication of two elements, 
    without reduction by irreducable polynom.
    @param a,b: binary polynomials
    @type a: int or long
    @type b: int or long
    @return: c, product as binary polynomial
    """
    a, b = abs(a),abs(b)
    n, i, c = _bitlen(a), 0, 0b0
    for i in range(n):
        if (_bittest(a,0)):
            c = c ^ b
        a = a >> 1    
        b = b << 1 
        #print "DBG: i=%d a=%s\tb=%s\tc=%s" % (i,bin(a),bin(b),bin(c))
    return c

def gf2m_modmul(a, b, f):
    """ Element multiplication: (a*b) mod f
    
    Including reduction by irreducable polynom f.
    @param a,b: binary polynomials
    @type a: int or long
    @type b: int or long
    @param f: irreducable polynome f(x), used for modular reduction
    @type f: int or long
    @return: product as reduced binary polynomial    
    """
    return gf2m_mod(gf2m_mul(a,b),f)

def gf2m_div(a, b, f):
    """ Element division: a/b mod f(x) == a*b^-1 mod f(x)
    
    @param a,b: divident and divisor as binary polynomials
    @type a: int or long
    @type b: int or long
    @param f: irreducable modular reduction polynomial as binary polynomail 
    @type f: int or long
    @return: c, quotient as binary polynomial
    """
    c = gf2m_modmul(a,gf2m_modmulinv(b,f),f)
    return c

def gf2m_mod(a, f):
    """ Element modular reduction: a(x) modulo f(x)
    
    A binary polynomial a(x) getrs reduced to a degree lower than that
    of f(x). An irreducable binary polynomial f is used for modular reduction.
    @param a:   binary polyonomial
    @type a: int or long
    @param f:   irreducable binary polynomial f(x)
    @type f: int or long
    @return: c, reduced binary polynomail 
    """
    c = abs(a)
    f = abs(f)
    while (_bitlen(c) >= _bitlen(f)):
        x= f << _bitlen(c)-_bitlen(f)
        c=c ^ x
    return c

def gf2m_modmulinv(a, f):
    """ Element Inversion a(x) => a^-1 mod f(x)

    Calculates the modular multiplicative inverse of a(x) mod f(x). 
    Ueses an adapted version of the exdendet euclidiean algorithem. 
    The outline for the adapted algorithem was taken from Katsuki Kobayashi et al.
    'An Algorithem for Inversion in $GF(2^m)$ Suitable for Implementation 
    Using a Polynomial Multiply Instruction on GF(2)'.
    The same algorithem can also be found in Hankerson et al. 
    'Software Implementation of Elliptic Curve Cryptography 
    over Binary Fields', 24.01.2000
    @param a: binary polynomial
    @type a: int or long
    @return: ux, modular multiplicative as binary polynomail
    """
    sx, rx, vx, ux = abs(f), abs(a), 0, 1
    #print "DBG: rx=%s\tsx=%s\tux=%s\tvx=%s" % (bin(rx),bin(sx),bin(ux),bin(vx))
    while (_binpolydeg(rx) != 0):
        delta = _binpolydeg(sx)-_binpolydeg(rx)
        if (delta < 0):
            temp = sx
            sx = rx
            rx = temp
            temp = vx
            vx = ux
            ux = temp
        sx = gf2m_sub(sx,gf2m_mul(1 << abs(delta),rx)) 
        vx = gf2m_sub(vx,gf2m_mul(1 << abs(delta),ux))
        #print "DBG: rx=%s\tsx=%s\tux=%s\tvx=%s\tdelta=%s" % (bin(rx),bin(sx),bin(ux),bin(vx),bin(delta))
    return ux

#-------------------------------
# Functions for binary aritmetic
#-------------------------------

def _bittest(n, offset):
    """ Test bit at offset of numeric value 
    
    If bit at offset is 1, 1 is returned. 
    This means that 2**offset is numeric & mask. 
    No check of offset length is done!
    @param n: numeric value
    @type n: int or long
    @param offset: position of bit in n to test, starts with 0
    @type offset: int or long
    @return: 1 or 0 
    """
    mask = 1 << abs(offset)
    if (abs(n) & mask) != 0:
        return 1
    return 0

def _bitset(n, offset):
    mask = 1 << abs(offset)
    return(abs(n) | mask)

def _bitlencount(n):
    """ Bit length of value and count of bits set to 1
  
    DEPRICATED
    Since python 2.7 value.bit_length() should be used instead.
    This function does not work for negative values!
    @param n:  positive numeric value
    @type n: int or long
    @return: tuple of 'length' and 'count' valu
    """
    length = 0
    count = 0
    while (n):
        count += (n & 1)
        length += 1
        n >>= 1
    return(length, count)

def _bitlen(n):
    """ Bit length of value
    
    Since python 2.7 this is very easy
    @param n: numeric value
    @type n: int or long
    @return: length, number of bits used to represent n, as numeric value
    """
    return n.bit_length()

def _binpolydeg(n):
    """ Degree of polynomial n: deg(n)

    Interprets input value as binary polynomial and returns its degree
    @param n: numeric value
    @type n: int or long
    @return: Degree as numeric value
    """
    length = _bitlen(n)
    if (length > 1): 
        return (length-1)
    return 0

#-------------------------------------
# Helper functions for test out-/input
#-------------------------------------

def num_to_poly(n,var="x"):
    """ Helper function to print numeric value as a polynomial
    
    @param n: numeric value
    @type n: int or long
    @return: poly, list of polynomail representation
    """
    if (n==0):
        return 0
    var=var+"^"
    poly=[]
    i = 0
    length = _bitlen(n)
    for i in range(length):
        if (_bittest(n,0)):
            if (i == 0):
                poly.append("1")
            else:
                poly.append(str(i))
                poly.append(var)
            poly.append("+")
        n = n >> 1
    poly.pop() 
    poly.reverse()
        
    polystr=''
    for k in poly: 
        polystr=polystr+str(k)

    return polystr

def poly_to_num(polystr,var="x"):
    binpoly = 0b0
    match = re.findall(var + "\^(\d*)",polystr)
    if (re.search("[^\^]\s*(" + var + ")",polystr)):
        match.append("1")
    if (re.search("\+\s*(1)",polystr)): # TODO: case 1 + at beginning
        match.append("0")
    match.reverse()
    if (len(match) == 0):
        return 0
    for i in match:
        #binpoly = _bitset(binpoly,int(i)) # alternative function
        mask = 1 << abs(int(i))
        binpoly = (binpoly | mask)
    return binpoly
