import rsa

class RsaKeys:
    """
    Rsaの公開鍵,秘密鍵や暗号化,復号化されたデータを保存するクラス
    """
    def __init__(self,k,m,p,q,encrypted_integers_in_list=None,decrypted_integers_in_list=None):
        self.pub_key1 = k
        self.pub_key2 = m
        self.priv_key1 = p
        self.priv_key2 = q

        self.encrypted_integers_in_list = encrypted_integers_in_list
        self.decrypted_integers_in_list = decrypted_integers_in_list
        
    def add_encrypted_integers_in_list(self,encrypted_integers_in_list):
        self.encrypted_integers_in_list = encrypted_integers_in_list

    def add_decrypted_integers_in_list(self,decrypted_integers_in_list):
        self.decrypted_integers_in_list = decrypted_integers_in_list

    def get_encrypted_integers_in_list(self):
        return self.encrypted_integers_in_list

    def get_decrypted_integers_in_list(self):
        return self.decrypted_integers_in_list

    def get_pub_key1(self):
        return self.pub_key1

    def get_pub_key2(self):
        return self.pub_key2

    def get_priv_key1(self):
        return self.priv_key1

    def get_priv_key2(self):
        return self.priv_key2
