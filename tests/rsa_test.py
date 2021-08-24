import sys
import os
import random
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../rsa')))
from rsa import *

class TestRSA(unittest.TestCase):        
    def test_encrypt_and_decrypt(self):
        integers = "123456789"
        
        [encrypted_integers_in_list,
         pub_key1,
         pub_key2,
         priv_key1,
         priv_key2] = encrypt(integers,2,100)
        
        print([encrypted_integers_in_list,
               pub_key1,
               pub_key2,
               priv_key1,
               priv_key2])
        
        decrypt_integers = decrypt(encrypted_integers_in_list,
                                   pub_key1,
                                   pub_key2,
                                   priv_key1,
                                   priv_key2)
                
        print(decrypt_integers)
        self.assertAlmostEqual(decrypt_integers,integers)
        
        """
        integers = "12345678905534789593201481458222"*100
        
        [encrypted_integers_in_list,
         pub_key1,
         pub_key2,
         priv_key1,
         priv_key2] = encrypt(integers,100,100)
        
        print([encrypted_integers_in_list,
               pub_key1,
               pub_key2,
               priv_key1,
               priv_key2])
        
        decrypt_integers = decrypt(encrypted_integers_in_list,
                                   pub_key1,
                                   pub_key2,
                                   priv_key1,
                                   priv_key2)
                
        print(decrypt_integers)
        self.assertAlmostEqual(decrypt_integers,integers)
        """
        """
        for _ in range(100):
            digit = random.getrandbits(10)
            integers_in_str = str(random.getrandbits(digit))
            [encrypted_integers_in_list,
             pub_key1,
             pub_key2,
             priv_key1,
             priv_key2] = encrypt(integers_in_str,10,100)
        
            decrypted_integers = decrypt(encrypted_integers_in_list,
                                       pub_key1,
                                       pub_key2,
                                       priv_key1,
                                       priv_key2)
            
            self.assertAlmostEqual(decrypted_integers,integers_in_str)
        """
        
def main():
    unittest.main()

if __name__=='__main__':
    main()
