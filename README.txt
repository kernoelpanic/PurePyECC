=========
PurePyECC
=========

PurePyECC provides basic ECC arithmetic over binary curves written in pure python.
The implementation should help people to understand the basics of 
elliptic curve cryptography over binary curves by providing a simple example. 
The implementation is not optimized for performance or a high level of security! 

At the moment only the NIST K-283 curve is supported. It also containes an
ECDH implementation as well as an example client-server chat that uses ECDH
for key negotiation. 

The scripts in ``./bin/alice.py`` and ``./bin/bob.py`` contain the client-server
example where ``./bin/bob.py`` is the server. This example uses pycrypto-2.6 for
AES encryption using the negotiated ECDH secret as key. 

1. Run ``./bin/bob.py -v 5533`` whit a port to listen as parameter. 
   Optionally be verbose by using "-v".

2. Run ``./bin/alice.py -v $IPofBob 5533`` where $IPofBob is the IP-address
   on which Bob listens at port 5533, in a test scenario this will be
   ``localhost``. 
   Optionally be verbose by using "-v".
    
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

Documentation
=============
Epydoc generated HTML documentation can be found in ``./docs/toc.html``. The
*sage* input for the test case generation can be found in the comments of the
related test cases unter ``./purepyecc/test/test_*``.

ECC Arithmetic
==============
* The basic ECC Arithmetic is performed in *arithmetic0.py* and is pure python.

* The structure of a curve is defined in *ec.py*.

Author
======
The programm was written by aljosha judmayer (dev [at] 3-volution.net)
