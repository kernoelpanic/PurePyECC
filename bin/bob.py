#!/usr/bin/env python
# :set tabstop=8 expandtab shiftwidth=4 softtabstop=4
# filetype indent plugin on
""" ECDH test client BOB """
import socket 
import thread
import base64
import os
import sys
import re
from optparse import OptionParser

sys.path.append("../pycrypto-2.6/lib2")
sys.path.append("../../pycrypto-2.6/lib2")
from Crypto.Cipher import AES
from Crypto.Util import Counter

sys.path.append("./")
sys.path.append("../")
#import ecdh as ecdh
from purepyecc import ecdh

def recvdecrypt(bar):   
    while True:
        data = con.recv(1024)
        if data:
            if options.verbose:
                print "\n<<<[%s][Encrypted]: %s" % (addr[0], data)
            decoded = DecodeAES(cipher, data)
            print "<<<[%s][Decrypted]: %s" % (addr[0], decoded)

#---parse args---
parser = OptionParser("bob.py [option] port")
parser.add_option("-v", "--verbose", action="store_true",
                  dest="verbose", default=False,
                  help="Output increase")

(options, args) = parser.parse_args()
if len(args) != 1:
    parser.error("Port needed!")
port = args[0]

#---AES--- 
#from: http://www.codekoala.com/blog/2009/aes-encryption-python-using-pycrypto/
#---------
MODE_CTR = 6
# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 16
# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'
# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

#---network---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(("", int(port))) 
s.listen(1)

try: 
    con, addr = s.accept()
    print "[%s] Client connected" % addr[0]
    data = con.recv(1024) # <--
    
    #---ECDH handshake---
    if (re.search(r"\[ecdh",data)):
        print "[%s] Init ECDH handshake ..." % addr[0]
        if options.verbose:             
            print "Received Alice public key:\n%s" % (data)     
        mc = re.search(r"\[ecdh\|curve\|(.*)\]",data)
        curvename = mc.group(1)
        mx = re.search(r"\[ecdh\|Qx\|(.*)L\]",data)
        Qax = long(mx.group(1),16)
        my = re.search(r"\[ecdh\|Qy\|(.*)L\]",data)
        Qay = long(my.group(1),16)
        Qa = (Qax,Qay)
        
        global DH
        DH = ecdh.ECDH(curvename)
        DH.create_priv_key()
        Qb = DH.create_pub_key()
        
        msg = "[ecdh|Qx|" + hex(Qb[0]) + "]\n"
        msg += "[ecdh|Qy|" + hex(Qb[1]) + "]\n"
        con.sendall(msg) #-->  
        
        sec = DH.create_secret_key(Qa)
        if options.verbose:
            print "Calculated ECDH secret key:\n%s" % hex(sec[0])
    else:        
        con.sendall("[ecdh| handshake error!]")
    
    #---Secure chat---
    if (DH.get_secret_key() != 0):
        key = hex(DH.get_secret_key()[0])[2:18]
        ctr = Counter.new(128)
        cipher = AES.new(key,MODE_CTR,counter=ctr)
        #cipher = AES.new(key)
        
        thread.start_new_thread(recvdecrypt,("foo",))
        print "Send messages to Alice:"
        while True:
            #---send & encrypt---
            emsg = raw_input("")
            encoded = EncodeAES(cipher, emsg)
            if options.verbose:
                print ">>>[%s][Sent encrypted msg]: %s" % (addr[0],encoded)
            con.sendall(encoded) 

finally: 
    print "\n\n[%s] Closeing connection..." % addr[0] 
    con.close()
    s.close()
