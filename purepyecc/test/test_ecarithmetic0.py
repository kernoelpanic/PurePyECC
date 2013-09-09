#!/usr/bin/env python
import unittest 
import sys

sys.path.append("../") # to run it from test/
sys.path.append("./")  # to run it from ../
import arithmetic0 as ar

class TestEcArithmetic0(unittest.TestCase):

    def test_add_point__pos(self):
        """ Positive test for ecgf2m_add_point(x1, y1, x2, y2, f, a=0b0) 

        Sage test calculations::
            sage: F.<x> = GF(2)[]
            sage: KK.<y> = GF(2**4, name='y', modulus=x^4 + x + 1 )
            sage: E = EllipticCurve(KK, [1,0,0,0,1])
            sage: p1 = E.point((y^3, y^3 + y^2 + y + 1, 1))
            sage: p2 = E.point((y^2 + y + 1, y^2 + y + 1, 1))
            sage: p1+p2
            (y^3 + y^2 : y^2 + y : 1)
            sage: p1*2
            (y^2 + y : y^2 + y : 1)
            sage: p1+p1
            (y^2 + y : y^2 + y : 1)
            sage: p1+p1 == p1*2
            True
            sage: p2*2
            (1 : 1 : 1)
            sage: p2+p2
            (1 : 1 : 1)
            #-----------------------
            # Test point at infinity
            #-----------------------
            sage: p2 = E.point((y^3, y^2 + y + 1, 1))
            sage: p1+p2
            (0 : 1 : 0)
            sage: p3 = p1+p2
            sage: p3.xy()
            ---------------------------------------------------------------------------
            ZeroDivisionError
        """
	result = ar.ecgf2m_add_point(0b1000,0b1111,0b111,0b111,0b10011)
        self.assertEqual(result, (0b1100, 0b110))
	result = ar.ecgf2m_add_point(0b111,0b111,0b1000,0b1111,0b10011)
        self.assertEqual(result, (0b1100, 0b110))
	result = ar.ecgf2m_add_point(0b1000,0b1111,0b1000,0b111,0b10011)
        self.assertEqual(result, (0b0, 0b0)) #point at infinity
        

    def test_add_point__neg(self):
        """ Negative test for ecgf2m_add_point(x1, y1, x2, y2, f, a=0b0) """
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(ValueError, ar.ecgf2m_add_point, 0.0, 0b1111,0b111,0b111,0b10011)
        self.failUnlessRaises(ValueError, ar.ecgf2m_add_point, 0b1000, "asdf" ,0b111,0b111,0b10011)
	
        result = ar.ecgf2m_add_point(-0b111,0b111,0b1000,0b1111,0b10011)
        self.assertEqual(result, (0b1100, 0b110))
        result = ar.ecgf2m_add_point(0b111,0b111,-0b1000,0b1111,0b10011)
        self.assertEqual(result, (0b1100, 0b110))
        result = ar.ecgf2m_add_point(0b111,-0b111,0b1000,0b1111,0b10011)
        self.assertEqual(result, (0b1100, 0b110))
        result = ar.ecgf2m_add_point(0b111,0b111,0b1000,-0b1111,0b10011)
        self.assertEqual(result, (0b1100, 0b110))
        result = ar.ecgf2m_add_point(-0b111,-0b111,-0b1000,-0b1111,-0b10011)
        self.assertEqual(result, (0b1100, 0b110))

    def test_dbl_point__pos(self):
        """ Positive tests for ecgf2m_dbl_point(x, y, f, a=0b0) 

        Sage test calculations::
            sage: F.<x> = GF(2)[]
            sage: KK.<y> = GF(2**4, name='y', modulus=x^4 + x + 1 )
            sage: E = EllipticCurve(KK, [1,0,0,0,1])
            sage: p1 = E.point((y^3, y^3 + y^2 + y + 1, 1))
            sage: p2 = E.point((y^2 + y + 1, y^2 + y + 1, 1))
            sage: p1+p2
            (y^3 + y^2 : y^2 + y : 1)
            sage: p1*2
            (y^2 + y : y^2 + y : 1)
            sage: p1+p1
            (y^2 + y : y^2 + y : 1)
            sage: p1+p1 == p1*2
            True
            sage: p2*2
            (1 : 1 : 1)
            sage: p2+p2
            (1 : 1 : 1) 
        """
        result = ar.ecgf2m_dbl_point(0b1000,0b1111,0b10011)
        self.assertEqual(result, (0b110, 0b110))

    def test_dbl_point__neg(self):
        """ Negative tests for ecgf2m_dbl_point(x,y,f,a=0b0) """ 
        # Not meant to be called with other values than int or long
        self.failUnlessRaises(ValueError, ar.ecgf2m_dbl_point, 0.0, 0b1111, 0b10011)
        self.failUnlessRaises(ValueError, ar.ecgf2m_dbl_point, 0b1000, "asdf" ,0b10011)
 
        result = ar.ecgf2m_dbl_point(-0b1000,0b1111,0b10011)
        self.assertEqual(result, (0b110, 0b110))
        result = ar.ecgf2m_dbl_point(0b1000,-0b1111,0b10011)
        self.assertEqual(result, (0b110, 0b110))
        result = ar.ecgf2m_dbl_point(0b1000,0b1111,-0b10011)
        self.assertEqual(result, (0b110, 0b110))
        result = ar.ecgf2m_dbl_point(-0b1000,-0b1111,-0b10011)
        self.assertEqual(result, (0b110, 0b110))

    def test_dbl_add_point_xxl__pos(self):
        """ Positive tests for add and dbl points on elliptice curve K-283 

        Sagte test calculations::
            sage: F.<t> = GF(2)[]
            sage: KK.<p> = GF(2**283, name='p', modulus=t^283 + t^12 + t^7 + t^5 + 1 )
            sage: E = EllipticCurve(KK, [1,0,0,0,1])
            sage: E.order()
            15541351137805832567355695254588151253139246935172245297183499990119263318817690415492
            sage: E.abelian_group()
            Additive abelian group isomorphic to Z/15541351137805832567355695254588151253139246935172245297183499990119263318817690415492 embedded in Abelian group of points on Elliptic Curve defined by y^2 + x*y = x^3 + 1 over Finite Field in p of size 2^283
            sage: x1=t^282+t^280+t^273+t^272+t^269+t^264+t^261+t^260+t^259+t^258+t^257+t^256+t^254+t^253+t^252+t^251+t^247+t^246+t^243+t^241+t^238+t^234+t^231+t^227+t^221+t^220+t^219+t^218+t^217+t^216+t^212+t^211+t^209+t^205+t^204+t^203+t^201+t^200+t^199+t^192+t^190+t^189+t^185+t^183+t^182+t^181+t^180+t^176+t^175+t^171+t^167+t^166+t^165+t^162+t^160+t^158+t^156+t^153+t^152+t^151+t^150+t^147+t^146+t^144+t^141+t^138+t^137+t^134+t^132+t^131+t^130+t^129+t^128+t^125+t^121+t^120+t^119+t^118+t^112+t^110+t^108+t^106+t^105+t^102+t^101+t^100+t^99+t^97+t^92+t^90+t^89+t^87+t^82+t^81+t^80+t^78+t^77+t^75+t^72+t^68+t^65+t^64+t^63+t^61+t^60+t^55+t^54+t^49+t^47+t^45+t^43+t^42+t^37+t^34+t^30+t^28+t^27+t^22+t^19+t^16+t^13+t^11+t^5+t^4+t^2+t^1
            sage: y1=t^280+t^279+t^278+t^275+t^274+t^271+t^270+t^268+t^267+t^265+t^261+t^260+t^259+t^251+t^250+t^249+t^248+t^244+t^243+t^242+t^239+t^236+t^235+t^234+t^233+t^229+t^228+t^224+t^223+t^219+t^218+t^216+t^215+t^212+t^207+t^206+t^205+t^204+t^203+t^200+t^198+t^196+t^195+t^194+t^192+t^186+t^185+t^184+t^183+t^182+t^181+t^178+t^176+t^174+t^169+t^166+t^165+t^163+t^162+t^161+t^160+t^159+t^158+t^157+t^155+t^150+t^149+t^148+t^147+t^146+t^145+t^142+t^138+t^136+t^135+t^134+t^127+t^126+t^125+t^123+t^116+t^115+t^110+t^106+t^105+t^103+t^100+t^99+t^95+t^94+t^93+t^90+t^86+t^84+t^83+t^80+t^78+t^77+t^73+t^69+t^68+t^66+t^65+t^62+t^59+t^58+t^57+t^53+t^52+t^50+t^44+t^40+t^38+t^37+t^32+t^30+t^29+t^28+t^26+t^25+t^24+t^23+t^22+t^20+t^19+t^18+t^16+t^13+t^9+t^6+t^4+t^3+1  
            sage: p1 = E.point((x1, y1, 1))
            sage: p1.order()
            3885337784451458141838923813647037813284811733793061324295874997529815829704422603873
            sage: r = p1*1
            sage: r.xy() #observe that it is the same point as entered
            sage: r2 = p1*2
            sage: r2.xy()
            (p^281 + p^280 + p^275 + p^273 + p^271 + p^270 + p^269 + p^267 + p^264 + p^262 + p^261 + p^259 + p^256 + p^255 + p^253 + p^252 + p^251 + p^248 + p^246 + p^245 + p^244 + p^243 + p^240 + p^237 + p^235 + p^234 + p^232 + p^230 + p^226 + p^223 + p^221 + p^220 + p^219 + p^218 + p^217 + p^216 + p^215 + p^214 + p^212 + p^211 + p^209 + p^207 + p^206 + p^205 + p^199 + p^194 + p^193 + p^191 + p^190 + p^188 + p^187 + p^186 + p^182 + p^181 + p^179 + p^178 + p^177 + p^176 + p^175 + p^173 + p^168 + p^161 + p^160 + p^159 + p^156 + p^155 + p^154 + p^153 + p^150 + p^148 + p^145 + p^143 + p^141 + p^138 + p^134 + p^132 + p^131 + p^128 + p^127 + p^125 + p^122 + p^120 + p^118 + p^114 + p^112 + p^111 + p^110 + p^109 + p^106 + p^105 + p^104 + p^103 + p^99 + p^97 + p^96 + p^94 + p^92 + p^90 + p^89 + p^88 + p^87 + p^85 + p^80 + p^79 + p^78 + p^75 + p^72 + p^71 + p^70 + p^68 + p^66 + p^65 + p^64 + p^62 + p^59 + p^56 + p^55 + p^54 + p^48 + p^47 + p^46 + p^44 + p^43 + p^42 + p^38 + p^37 + p^35 + p^34 + p^33 + p^32 + p^31 + p^29 + p^27 + p^26 + p^25 + p^23 + p^21 + p^19 + p^18 + p^17 + p^16 + p^15 + p^7 + p^6 + p^3 + p^2 + p + 1,
     p^282 + p^280 + p^279 + p^276 + p^275 + p^274 + p^272 + p^270 + p^269 + p^268 + p^265 + p^262 + p^261 + p^259 + p^257 + p^255 + p^253 + p^248 + p^247 + p^245 + p^244 + p^242 + p^241 + p^240 + p^235 + p^234 + p^230 + p^228 + p^227 + p^226 + p^225 + p^223 + p^220 + p^219 + p^218 + p^217 + p^216 + p^215 + p^214 + p^213 + p^212 + p^211 + p^209 + p^206 + p^202 + p^201 + p^199 + p^198 + p^196 + p^194 + p^193 + p^191 + p^189 + p^184 + p^183 + p^182 + p^181 + p^180 + p^179 + p^176 + p^172 + p^169 + p^167 + p^165 + p^164 + p^161 + p^160 + p^156 + p^154 + p^151 + p^143 + p^141 + p^140 + p^139 + p^138 + p^133 + p^132 + p^131 + p^130 + p^128 + p^127 + p^123 + p^122 + p^121 + p^115 + p^114 + p^111 + p^109 + p^107 + p^105 + p^104 + p^100 + p^98 + p^97 + p^94 + p^93 + p^90 + p^89 + p^86 + p^83 + p^80 + p^78 + p^77 + p^76 + p^75 + p^74 + p^73 + p^72 + p^68 + p^66 + p^65 + p^63 + p^61 + p^60 + p^59 + p^56 + p^54 + p^53 + p^52 + p^45 + p^42 + p^40 + p^38 + p^37 + p^34 + p^29 + p^26 + p^25 + p^24 + p^23 + p^21 + p^20 + p^17 + p^15 + p^14 + p^13 + p^12 + p^11 + p^10 + p)
            #-----------
            # x = 0x30ae969b9792d44bfdae086dc6fa1039e52a459a545e78b57a1c9d749c1dc6faeaf80cfL
            # y = 0x059D726AA1B70C5E9FFA46D6A1F912B31480BC3D8E0CAB1666497F16B970256427B2FC02
        """
        x=0x503213f78ca44883f1a3b8162f188e553cd265f23c1567a16876913b0c2ac2458492836
        y=0x1ccda380f1c9e318d90f95d07e5426fe87e45c0e8184698e45962364e34116177dd2259
        f=0b10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000010100001
        result = ar.ecgf2m_dbl_point(x,y,f,0b0)
        self.assertEqual(result, (0x030AE969B9792D44BFDAE086DC6FA1039E52A459A545E78B57A1C9D749C1DC6FAEAF80CF, 0x059D726AA1B70C5E9FFA46D6A1F912B31480BC3D8E0CAB1666497F16B970256427B2FC02))        

if __name__ == "__main__": 
    unittest.main()
