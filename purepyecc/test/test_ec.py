#!/usr/bin/env python
import unittest 
import sys

sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import arithmetic0 as ar
import ec as ec

class TestEC(unittest.TestCase):

    def test_EC_affine_point_mul_on_kc_small_k_pos(self):
        gx=0x503213f78ca44883f1a3b8162f188e553cd265f23c1567a16876913b0c2ac2458492836L
        gy=0x1ccda380f1c9e318d90f95d07e5426fe87e45c0e8184698e45962364e34116177dd2259L
        f=0x800000000000000000000000000000000000000000000000000000000000000000010a1L
        r=0x1ffffffffffffffffffffffffffffffffffe9ae2ed07577265dff7f94451e061e163c61L
        kc = ec.KoblitzEC(283, 0b0,r, gx, gy, f, 6)
        
        k = 1
        x = 0x0503213F78CA44883F1A3B8162F188E553CD265F23C1567A16876913B0C2AC2458492836L
        y = 0x01CCDA380F1C9E318D90F95D07E5426FE87E45C0E8184698E45962364E34116177DD2259L
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "1 Incorrect point/scalar multiplication Q=k*G") 

        k = 2
        x = 0x030AE969B9792D44BFDAE086DC6FA1039E52A459A545E78B57A1C9D749C1DC6FAEAF80CFL
        y = 0x059D726AA1B70C5E9FFA46D6A1F912B31480BC3D8E0CAB1666497F16B970256427B2FC02L
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "2 Incorrect point/scalar multiplication Q=k*G") 
       
        k = 3
        x = 0x015DCCC30A8B1F5146412D51FEC337741090321408AAC521391AD36C5912E280124FE3B5L
        y = 0x053FC9BED137312952AD97F6A98C4C7AC1B421635FBAFE28898E9213D979D5B4D279F192L
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "3 Incorrect point/scalar multiplication Q=k*G") 
        
        k = 4
        x = 0x03949AFAEDDDE457A6B7F17129776A4EA5C5C671594A553C5F1DFC1C2C6C5D36CC6F7B91L
        y = 0x0286EE1883F14F990BD23310F6212E0CB2578DE1DC43C6B52729D57A5FE072317C1AFB8EL
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "4 Incorrect point/scalar multiplication Q=k*G") 
        
        k = 112233445566778899
        x = 0x02A97071496676C2FF9F345FA007C678FC9D86B423C8AB17AD9A1374936847AFE60611F4L
        y = 0x0034DA6E836869547366E006FDDACBB27ABD7DD5C8EFA4F17CFDCF92C033DAF9D2812FCBL
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "5 Incorrect point/scalar multiplication Q=k*G") 

    def test_EC_affine_point_mul_on_kc_xxl_k_pos(self):
        gx=0x503213f78ca44883f1a3b8162f188e553cd265f23c1567a16876913b0c2ac2458492836L
        gy=0x1ccda380f1c9e318d90f95d07e5426fe87e45c0e8184698e45962364e34116177dd2259L
        f=0x800000000000000000000000000000000000000000000000000000000000000000010a1L
        r=0x1ffffffffffffffffffffffffffffffffffe9ae2ed07577265dff7f94451e061e163c61L
        kc = ec.KoblitzEC(283, 0b0,r, gx, gy, f, 6)

        k = 3885337784451458141838923813647037813284811733793061324295874997529815829704422603872
        x = 0x0503213F78CA44883F1A3B8162F188E553CD265F23C1567A16876913B0C2AC2458492836L
        y = 0x04CFFB0777D6DAB9B28AC2DC6514CA8ABBB3639FCBD910E2F2DE0B25FEF6BD452F940A6FL
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "1 Incorrect point/scalar multiplication Q=k*G") 
        
        k = 3885337784451458141838923813647037813284811733793061324295874997529815829704422603871
        x = 0x030AE969B9792D44BFDAE086DC6FA1039E52A459A545E78B57A1C9D749C1DC6FAEAF80CFL
        y = 0x06979B0318CE211A2020A6507D96B3B08AD218642B494C9D31E8B6C1F0B1F90B891D7CCDL
        Q = kc.affine_point_mul(k, gx, gy)
        self.assertEqual(Q, (x,y), "2 Incorrect point/scalar multiplication Q=k*G") 

    def test_EC_affine_point_mul_on_kc_neg(self):
        # Not meant to be called with other values than int or long
        #self.failUnlessRaises(TypeError, ar._testBit, 0.0, 1)
        #self.failUnlessRaises(TypeError, ar._testBit, 0b101, 1.0)
        pass

if __name__ == "__main__": 
    unittest.main()
