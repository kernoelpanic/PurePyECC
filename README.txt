=========
PurePyECC
=========

PurePyECC should help you to learn the basics of ECC arithmetic over binary curves. Therefore, it was written in pure python and has no external dependencies other than python 2.7.

The implementation should help people to understand the basics of elliptic
curve cryptography over binary curves by providing a simple example. So this
code is for learning purposes only. The implementation is not optimized for performance or security! 

At the moment only the NIST K-283 curve is supported. 

Test cases
==========
Test cases for several different operations can be found in ``./purepyecc/test``.
To run all test cases type ``python ./purepyecc/test/test_all.py``.

Documentation
=============
Epydoc generated HTML documentation can be found in ``./docs/toc.html``. The
*sage* input for the test case generation can be found in the comments of the
related test cases unter ``./purepyecc/test/test_*``.

ECC Arithmetic
==============
* The basic ECC Arithmetic is performed in *arithmetic0.py* and is pure python.

* The structure of a curve is defined in *ec.py*.

ECDH 
====
    
The package also containes an ECDH implementation. 
ECDH over K-283 can be used in other python applications as follows::

    #!/usr/bin/env python

    from PurePyECC import ecdh

    DH=ecdh.ECDH("K-283")
    DH.create_priv_key()
    DH.create_pub_key()
    
    curve = DH.get_curve_name() # "K-283"
    Qax = hex(DH.get_pub_key()[0]) # Alice public key x coordinate
    Qay = hex(DH.get_pub_key()[1]) # Alice public key y coordinate

    # --> send public key from Alice
    # <-- get public key from Bob
    Qb = (Qbx, Qby)
    sec = DH.create_secret_key(Qb)
    print "Calculated ECDH secret key:\n%s" % hex(sec[0])        

Author
======
The programm was written by aljosha judmayer (kernoelpanic [at] 3-volution.net)
