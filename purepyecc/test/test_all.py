#!/usr/bin/env python

import unittest
import sys

sys.path.append("./purepyecc") # to run it from package root
sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import test_bitarithmetic0 as t1
import test_fieldarithmetic0 as t2
import test_ecarithmetic0 as t3
import test_ec as t4
import test_ecdh as t5

suite = unittest.TestSuite()

casesT1 = unittest.TestLoader().loadTestsFromTestCase(t1.TestBitArithmetic0)
casesT2 = unittest.TestLoader().loadTestsFromTestCase(t2.TestFieldArithmetic0)
casesT3 = unittest.TestLoader().loadTestsFromTestCase(t3.TestEcArithmetic0)
casesT4 = unittest.TestLoader().loadTestsFromTestCase(t4.TestEC)
casesT5 = unittest.TestLoader().loadTestsFromTestCase(t5.TestECDH)

suite.addTests(casesT1)
suite.addTests(casesT2)
suite.addTests(casesT3)
suite.addTests(casesT4)
suite.addTests(casesT5)

unittest.TextTestRunner(verbosity=2).run(suite)
