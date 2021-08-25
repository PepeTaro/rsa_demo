import sys
import os
import random
import binascii
import base64
import pickle
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

def image_to_int(binary_form):
    encoded_string= base64.b64encode(binary_form)
    utf8_form = encoded_string.decode('utf-8')
    int_form = utf8_to_int(utf8_form)

    return int_form

def int_to_image(int_form):
    utf8_form = int_to_utf8(int_form)
    decoded_string = utf8_form.encode("utf-8")
    binary_form = base64.b64decode(decoded_string)

    return binary_form

def read_file(filename):
    with open(filename, "rb") as f:
        binary_form = f.read()        
    return binary_form

def write_file(filename,data):
    with open(filename, "wb") as f:
        f.write(data)        

def encrypt(plaintext,n,e):
    assert(isinstance(plaintext,int))    
    encrypted_text = rsa.encrypt(plaintext,n,e)
    return encrypted_text

def decrypt(ciphertext,d,p,q):    
    decrypted_text = rsa.decrypt(ciphertext,d,n)
    return decrypted_text

def write_python_data(filename,data):
    with open(filename, 'wb') as f:
        pickle.dump(data,f)

def read_python_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def save_public_keys(filename,public_keys):
    write_python_data(filename,public_keys)

def save_private_keys(filename,private_keys):
    write_python_data(filename,private_keys)

def save_ciphertext(filename,ciphertext):
    write_python_data(filename,ciphertext)

def load_public_keys(filename):
    return read_python_data(filename)

def load_private_keys(filename):
    return read_python_data(filename)

def load_ciphertext(filename):
    return read_python_data(filename)

def encrypt_file(enc_filename,save_filename,pub_key_filename,priv_key_filename):
    [(n,e),(d,p,q)] = rsa.generate_keys1024()    
    text = read_file(enc_filename)
    int_form = image_to_int(text)        
    encrypted_text = encrypt(int_form,n,e)

    save_public_keys(pub_key_filename,(n,e))
    save_private_keys(priv_key_filename,(d,p,q))
    save_ciphertext(save_filename,encrypted_text)
    
def decrypt_file(load_filename,save_filename,pub_key_filename,priv_key_filename):
    (d,p,q) = load_private_keys(priv_key_filename)
    encrypted_text  = load_ciphertext(load_filename)
    int_form = rsa.decrypt(encrypted_text,d,p,q)    
    binary_form = int_to_image(int_form)
    write_file(save_filename,binary_form)
    
def main():
    """
    encrypt_file("./data/pepe_wee.jpg","./data/encrypt_pepe_wee.jpg","./data/pub_keys","./data/priv_keys")
    decrypt_file("./data/encrypt_pepe_wee.jpg","./data/decrypt_pepe_wee.jpg","./data/pub_keys","./data/priv_keys")
    """
    
    encrypt_file("./data/text.txt","./data/encrypt_text.txt","./data/pub_keys","./data/priv_keys")
    decrypt_file("./data/encrypt_text.txt","./data/decrypt_text.txt","./data/pub_keys","./data/priv_keys")
    
if __name__=='__main__':
    main()
