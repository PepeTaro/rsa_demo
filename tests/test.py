import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../rsa')))
import number_theory
import rsa

def is_two_lists_equal(list1,list2):
    if(len(list1) != len(list2)): return False

    for e1,e2 in zip(list1,list2):
        if(e1 != e2): return False

    return True

def rsa_test():
    [(n,e),(d,p,q)] = rsa.generate_keys1024()
    #print("n",n)
    
    #num = 314159265358979123456789031415926535897912345678903141592653589791234567890
    num = random.getrandbits(1000)
    print("original:",num,"\n")
    
    ciphertext = rsa.encrypt(num,n,e)
    print("cipher:",ciphertext,"\n")
    
    plaintext = rsa.decrypt(ciphertext,d,n)
    print("plain:",plaintext,"\n")

    print("Success?:",(num == plaintext))
    assert(num == plaintext)

def main():
    rsa_test()
    
if __name__=='__main__':
    main()
