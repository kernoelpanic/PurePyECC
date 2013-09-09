#!/usr/bin/env python
# :set tabstop=8 expandtab shiftwidth=4 softtabstop=4
# filetype indent plugin on
""" Custom exceptions for elliptic curve validation

Some definitions of custom exceptions for the elliptic
curve validation process
"""
class InvalidECPublicKey(Exception): 
    def __init__(self, q, msg=""): 
        self.Q = q 
 
    def __str__(self): 
        return "Invalid elliptic curve public key"

class InvalidECDomainParameter(Exception): 
    def __init__(self, p, msg=""): 
        self.P = p 
 
    def __str__(self): 
        return "Invalid elliptic curve domain parameter"
