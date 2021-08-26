import sys
import os
from math import log10,floor
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from rsa.number_theory import *

def get_digit(n):
    return floor(log10(n))+1

def get_bit_length(n):
    return n.bit_length()

class TestNumberTheory(unittest.TestCase):
    
    def test_is_integer(self):
        self.assertAlmostEqual(is_integer(1),True)
        self.assertAlmostEqual(is_integer(0),True)
        self.assertAlmostEqual(is_integer(-1),True)
        self.assertAlmostEqual(is_integer(-1),True)
        self.assertAlmostEqual(is_integer(0.001),False)
        self.assertAlmostEqual(is_integer(0.0),False)
        self.assertAlmostEqual(is_integer(-0.1),False)

    def test_is_positive_integer(self):
        self.assertAlmostEqual(is_positive_integer(1),True)
        self.assertAlmostEqual(is_positive_integer(1000),True)
        self.assertAlmostEqual(is_positive_integer(0.01),False)
        self.assertAlmostEqual(is_positive_integer(0),False)
        self.assertAlmostEqual(is_positive_integer(-0),False)
        self.assertAlmostEqual(is_positive_integer(-0.1),False)
        self.assertAlmostEqual(is_positive_integer(-1),False)

    def test_is_none_positive_integer(self):
        self.assertAlmostEqual(is_non_negative_integer(1),True)
        self.assertAlmostEqual(is_non_negative_integer(1000),True)
        self.assertAlmostEqual(is_non_negative_integer(0),True)
        self.assertAlmostEqual(is_non_negative_integer(-0),True)
        self.assertAlmostEqual(is_non_negative_integer(0.01),False)
        self.assertAlmostEqual(is_non_negative_integer(-0.1),False)
        self.assertAlmostEqual(is_non_negative_integer(-1),False)
                               
    def test_is_divislbe(self):
        self.assertAlmostEqual(is_divisible(4,2),True)        
        self.assertAlmostEqual(is_divisible(0,3),True)
        self.assertAlmostEqual(is_divisible(6,3),True)
        self.assertAlmostEqual(is_divisible(-2,2),True)
        self.assertAlmostEqual(is_divisible(12345,1),True)
        self.assertAlmostEqual(is_divisible(4,3),False)
        self.assertAlmostEqual(is_divisible(1,2),False)
        self.assertAlmostEqual(is_divisible(1,2),False)
        self.assertAlmostEqual(is_divisible(-1,2),False)

    def test_is_prime(self):
        self.assertAlmostEqual(is_prime(2),True)
        self.assertAlmostEqual(is_prime(3),True)
        self.assertAlmostEqual(is_prime(11),True)
        self.assertAlmostEqual(is_prime(1),False)
        self.assertAlmostEqual(is_prime(4),False)
        self.assertAlmostEqual(is_prime(121),False)
        
    def test_factorize(self):
        self.assertAlmostEqual(factorize(2),{2:1})
        self.assertAlmostEqual(factorize(3),{3:1})
        self.assertAlmostEqual(factorize(4),{2:2})
        self.assertAlmostEqual(factorize(121),{11:2})                       
        self.assertAlmostEqual(factorize(126),{2:1,3:2,7:1})
        
    def test_euler_phi(self):
        self.assertAlmostEqual(euler_phi(1),1)
        self.assertAlmostEqual(euler_phi(2),1)
        self.assertAlmostEqual(euler_phi(3),2)
        self.assertAlmostEqual(euler_phi(4),2)
        self.assertAlmostEqual(euler_phi(2401),2058)
        
    def test_euclidean(self):
        self.assertAlmostEqual(euclidean(105,121),(1,68,-59))
        self.assertAlmostEqual(euclidean(12345,67890),(15,11,-2))
        self.assertAlmostEqual(euclidean(1,1),(1,1,0))
        self.assertAlmostEqual(euclidean(2,1),(1,1,-1))
        self.assertAlmostEqual(euclidean(4,2),(2,1,-1))
        self.assertAlmostEqual(euclidean(3,2),(1,1,-1))
        
    def test_exp_mod(self):
        self.assertAlmostEqual(exp_mod(7,327,853),286)
        self.assertAlmostEqual(exp_mod(1234,5678,1),0)
        self.assertAlmostEqual(exp_mod(2,1234,2),0)
        self.assertAlmostEqual(exp_mod(1,1,1),0)
        self.assertAlmostEqual(exp_mod(1,1,12345),1)
        self.assertAlmostEqual(exp_mod(2,3,0),8)
        self.assertAlmostEqual(exp_mod(2,0,2),1)
        
    def test_root_mod(self):
        self.assertAlmostEqual(root_mod(3968039,34781,27040397),22929826)
        self.assertAlmostEqual(root_mod(131,758,1073),905)
        self.assertAlmostEqual(root_mod(329,452,1147),763)
        self.assertAlmostEqual(root_mod(1,1,2),1)
        self.assertAlmostEqual(root_mod(1,1,1),0)
        
    def test_miller_rabin_test(self):
        self.assertAlmostEqual(miller_rabin_test(561,2),True)        
        self.assertAlmostEqual(miller_rabin_test(172947529,17),False)
        self.assertAlmostEqual(miller_rabin_test(172947529,23),True)
        self.assertAlmostEqual(miller_rabin_test(2,1),True)
        self.assertAlmostEqual(miller_rabin_test(3,1),False)
        
    def test_miller_rabin_prime_test(self):
        # 確率的に正しくない答えを返す場合があるが、確率アルゴリズムなのでしょうがない。
        self.assertAlmostEqual(miller_rabin_prime_test(155196355420821961,100),True)
        self.assertAlmostEqual(miller_rabin_prime_test(155196355420821889,100),False)
        self.assertAlmostEqual(miller_rabin_prime_test(285707540662569884530199015485750433489,100),False)
        self.assertAlmostEqual(miller_rabin_prime_test(285707540662569884530199015485751094149,100),True)
        self.assertAlmostEqual(miller_rabin_prime_test(2,1),True)
        self.assertAlmostEqual(miller_rabin_prime_test(3,1),True)
        self.assertAlmostEqual(miller_rabin_prime_test(4,1),False)
        self.assertAlmostEqual(miller_rabin_prime_test(5,1),True)
        
    def test_generate_n_digit_prime(self):
        # 確率的に正しくない答えを返す場合があるが、確率アルゴリズムなのでしょうがない。
        p = generate_n_digit_prime(1)
        self.assertTrue(p in [2,3,5,7] and get_digit(p) == 1)
        
        p = generate_n_digit_prime(2)
        self.assertTrue(p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97] and get_digit(p) == 2)
        
    def test_generate_n_bits_prime(self):
        # 確率的に正しくない答えを返す場合があるが、確率アルゴリズムなのでしょうがない。
        primes = [2,3,5,7,11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        
        p = generate_n_bits_prime(2)
        self.assertTrue(p in primes and get_bit_length(p) >= 2)
        
        p = generate_n_bits_prime(3)
        self.assertTrue(p in primes and get_bit_length(p) >= 3)

        p = generate_n_bits_prime(4)
        self.assertTrue(p in primes and get_bit_length(p) >= 4)

        p = generate_n_bits_prime(5)
        self.assertTrue(p in primes and get_bit_length(p) >= 5)

def main():
    unittest.main()

if __name__=='__main__':
    main()
