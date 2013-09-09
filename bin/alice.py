#!/usr/bin/env python
# :set tabstop=8 expandtab shiftwidth=4 softtabstop=4
# filetype indent plugin on
""" ECDH test client ALICE """
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
from purepyecc import ecdh

#---NIST curves---
def k283():
    global DH
    DH=ecdh.ECDH("K-283")

def b283(): #stub
    global DH
    DH=ecdh.ECDH("B-283")

curves = { 
       "K-283" : k283,
       "B-283" : b283, #stub
        None : k283              
        }

def recvdecrypt(foo):
    while True:
        data = s.recv(1024)
        if data:
            if options.verbose:
                print "\n<<<[%s][Encrypted]: %s" % (ip,data)
            decoded = DecodeAES(cipher, data)
            print "<<<[%s][Decrypted]: %s" % (ip,decoded)

#---parse args---
parser = OptionParser("alice.py [Options] ip port") 
parser.add_option("-c", "--curve", dest="curve", 
                  help="Used NIST curve, currently only 'K-283' supported") 
parser.add_option("-v", "--verbose", action="store_true", 
                  dest="verbose", default=False, 
                  help="Output increase")

(options, args) = parser.parse_args() 
if len(args) != 2: 
    parser.error("IP and port needed!")
ip = args[0]
port = args[1]

usedcurve = options.curve
if usedcurve in curves: 
    curves[usedcurve]() 
else: 
    parser.error("%s is no supported NIST curve" % usedcurve)

if options.verbose: 
    print "Using NIST curve %s, on ip %s:%s" % (DH.get_curve_name(), ip, port) 

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

#---connect---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((ip, int(port)))

try: 
    #---ECDH handshake---
    print "[%s] Init ECDH handshake ..." % (ip)
    DH.create_priv_key()
    DH.create_pub_key()
    msg = "[ecdh|curve|" + DH.get_curve_name() +"]\n"
    msg += "[ecdh|Qx|" + hex(DH.get_pub_key()[0]) + "]\n"
    msg += "[ecdh|Qy|" + hex(DH.get_pub_key()[1]) + "]\n" 
    s.sendall(msg) # -->

    s.setblocking(1)    
    data = s.recv(1024) # <-- 
   
    if (re.search(r"\[ecdh",data)):
        if options.verbose:
            print "Received Bobs public key:\n%s" % (data) 
        mx = re.search(r"\[ecdh\|Qx\|(.*)L\]",data)
        Qbx = long(mx.group(1),16)
        my = re.search(r"\[ecdh\|Qy\|(.*)L\]",data)
        Qby = long(my.group(1),16)
        Qb = (Qbx,Qby)
        sec = DH.create_secret_key(Qb)
        if options.verbose:
            print "Calculated ECDH secret key:\n%s" % hex(sec[0])
    else:
        s.sendall("[ecdh| handshake error!]")

    #---Secure chat---
    if (DH.get_secret_key() !=0):
        key = hex(DH.get_secret_key()[0])[2:18]
        ctr = Counter.new(128)
        cipher = AES.new(key,MODE_CTR,counter = ctr)
        #cipher = AES.new(key)
        
        thread.start_new_thread(recvdecrypt,("foo",))            
        print "Send messages to Bob:"
        while True: 
            #---send & encrypt---
            emsg = raw_input("") 
            encoded = EncodeAES(cipher, emsg)
            if options.verbose:
                print ">>>[%s][Sent encrypted msg]: %s" % (ip,encoded)
            s.sendall(encoded)
            
finally:
    print "\n\n[%s] Closeing connection..." % (ip) 
    s.close()

