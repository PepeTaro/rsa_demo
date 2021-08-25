import sys
import os
import random
import binascii
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../rsa')))
import number_theory
import rsa

def utf8_to_int(utf8_form):
    bin_form = utf8_form.encode("utf-8")
    hex_form = binascii.hexlify(bin_form)
    int_form = int(hex_form,16)
    return int_form

def int_to_utf8(int_form):
    hex_form   = hex(int_form)
    hex_form   = hex_form[2:] #先頭にある"0x"の部分を取り除く
    ascii_form = hex_form.encode("ascii")
    bin_form   = binascii.unhexlify(ascii_form)
    utf8_form  = bin_form.decode("utf-8")
    return utf8_form

def rsa_test():
    #[(n,e),(d,p,q)] = rsa.generate_keys1024()
    [(n,e),(d,p,q)] = rsa.generate_keys(20)
    print("keys:",[(n,e),(d,p,q)])
    
    #num = 314159265358979123456789031415926535897912345678903141592653589791234567890
    num = random.getrandbits(100)
    print("original:",num,"\n")

    print("spllited:",rsa.split_plaintext(num,n),"\n")
    
    ciphertext = rsa.encrypt(num,n,e)
    print("cipher:",ciphertext,"\n")
    
    plaintext = rsa.decrypt(ciphertext,d,n)
    print("plain:",plaintext,"\n")

    print("Success?:",(num == plaintext))
    assert(num == plaintext)

def utf8_test():
    [(n,e),(d,p,q)] = rsa.generate_keys1024()
    plaintext = "Hello,World!\nこんにちは,世界!"
    print("original:",plaintext,"\n")
    
    plaintext_in_int = utf8_to_int(plaintext)
    
    ciphertext = rsa.encrypt(plaintext_in_int,n,e)
    print("cipher:",ciphertext,"\n")
    
    encrypted = rsa.decrypt(ciphertext,d,n)
    print("encrypted:",int_to_utf8(encrypted),"\n")
    
def main():
    utf8_test()
    rsa_test()
    
if __name__=='__main__':
    main()
