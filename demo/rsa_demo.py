from rsa_file import encrypt_file,decrypt_file

def main():
    """
    encrypt_file("./data/pepe_wee.jpg","./data/encrypt_pepe_wee.jpg","./data/pub_keys","./data/priv_keys")
    decrypt_file("./data/encrypt_pepe_wee.jpg","./data/decrypt_pepe_wee.jpg","./data/priv_keys")
    """

    encrypt_file("./data/text.txt","./data/encrypt_text.txt","./data/pub_keys","./data/priv_keys")
    decrypt_file("./data/encrypt_text.txt","./data/decrypt_text.txt","./data/priv_keys")

if __name__=='__main__':
    main()
