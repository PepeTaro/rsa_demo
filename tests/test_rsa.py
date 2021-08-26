import sys
import os
import random
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from rsa.rsa import *

def is_two_lists_equal(list1,list2):
    if(len(list1) != len(list2)): return False

    for e1,e2 in zip(list1,list2):
        if(e1 != e2): return False

    return True

class TestRSA(unittest.TestCase):
    
    def test_split_plaintext(self):
        expectation = [12,34,56,78,9]
        self.assertTrue(is_two_lists_equal(split_plaintext(123456789,100),expectation))

        expectation = [1,2,3,4,5,6,7,8,9]
        self.assertTrue(is_two_lists_equal(split_plaintext(123456789,10),expectation))

        expectation = [2,0,1]
        self.assertTrue(is_two_lists_equal(split_plaintext(201,10),expectation))

        expectation = [123]
        self.assertTrue(is_two_lists_equal(split_plaintext(123,124),expectation))

    def test_encrypt_decrypt(self):        
        [(n,e),(d,p,q)] = generate_keys(10)        
        plaintext = random.getrandbits(100)
        encrypted_text = encrypt(plaintext,n,e)
        decrypted_text = decrypt(encrypted_text,d,p,q)
        self.assertTrue(plaintext == decrypted_text)

        
        [(n,e),(d,p,q)] = generate_keys(11)        
        plaintext = random.getrandbits(100)
        encrypted_text = encrypt(plaintext,n,e)
        decrypted_text = decrypt(encrypted_text,d,p,q)
        self.assertTrue(plaintext == decrypted_text)

    def test_encrypt_decrypt1024(self):
        [(n,e),(d,p,q)] = generate_keys1024()
        
        plaintext = random.getrandbits(1000)
        encrypted_text = encrypt(plaintext,n,e)
        decrypted_text = decrypt(encrypted_text,d,p,q)
        self.assertTrue(plaintext == decrypted_text)

    # 2048,3072,4096ビット鍵のテストは,鍵生成時間が長いため割愛。
    """
    def test_encrypt_decrypt2048(self):
        [(n,e),(d,p,q)] = generate_keys2048()
        
        plaintext = random.getrandbits(1000)
        encrypted_text = encrypt(plaintext,n,e)
        decrypted_text = decrypt(encrypted_text,d,p,q)
        self.assertTrue(plaintext == decrypted_text)
    
    def test_encrypt_decrypt3072(self):
        [(n,e),(d,p,q)] = generate_keys3072()
        
        plaintext = random.getrandbits(1000)
        encrypted_text = encrypt(plaintext,n,e)
        decrypted_text = decrypt(encrypted_text,d,p,q)
        self.assertTrue(plaintext == decrypted_text)

    def test_encrypt_decrypt4096(self):
        [(n,e),(d,p,q)] = generate_keys4096()
        
        plaintext = random.getrandbits(1000)
        encrypted_text = encrypt(plaintext,n,e)
        decrypted_text = decrypt(encrypted_text,d,p,q)
        self.assertTrue(plaintext == decrypted_text)
    """
    
def main():
    unittest.main()

if __name__=='__main__':
    main()
