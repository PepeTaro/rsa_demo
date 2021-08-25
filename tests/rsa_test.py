import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../rsa')))
from rsa import *

def is_two_lists_equal(list1,list2):
    if(len(list1) != len(list2)): return False

    for e1,e2 in zip(list1,list2):
        if(e1 != e2): return False

    return True

class TestRSA(unittest.TestCase):
    
    def test_split_plaintext(self):
        expectation = [12,34,56,78,9]
        self.assertTrue(is_two_lists_equal(split_plaintext(123456789,100),expectation))

        
def main():
    unittest.main()

if __name__=='__main__':
    main()
