import random
import json
import sys
import math

from rsa_keys import RsaKeys
import number_theory
from number_theory import is_integer,is_positive_integer,is_non_negative_integer

def generate_priv_pub_keys(digit_of_primes,num_tries=100):
    """
    digit_of_primes桁の素数である秘密鍵、公開鍵を生成して鍵を格納したクラスを返す。
    """
    assert(digit_of_primes >= 2)
    
    p = number_theory.generate_n_digit_prime(digit_of_primes,num_tries) # 素数生成　秘密鍵
    q = number_theory.generate_n_digit_prime(digit_of_primes,num_tries) # 素数生成　秘密鍵
    m = p*q #　公開鍵
    phi_m = p*q - p - q + 1 # オイラー関数の値 euler_phi(m)
    # kの値は,この値がいいらしい(https://crypto.stackexchange.com/questions/5572/in-rsa-encryption-does-the-value-of-e-need-to-be-random)
    k = 65537 # gcd(k,phi_m)=1でなくてはいけない(公開鍵)
    
    while(number_theory.euclidean(k,phi_m)[0] != 1): # kとphi_mが互いに素になるまで、繰り返す
        p = number_theory.generate_prime(digits_of_primes,num_tries) # 素数生成　秘密鍵
        q = number_theory.generate_prime(digits_of_primes,num_tries) # 素数生成　秘密鍵
        m = p*q #　公開鍵
        phi_m = p*q - p - q + 1 # オイラー関数の値 euler_phi(m)

    return RsaKeys(k=k,m=m,p=p,q=q)

def encrypt_integers_in_list(splitted_integers_in_list,rsa_keys):
    """
    リストsplitted_integers_in_listに格納されている各整数を独立に暗号化。
    暗号化した結果をrsa_keysクラスに保存。

    Args
    ---------
    splitted_integers:整数を格納したリスト
    rsa_keys:公開鍵などを格納したクラス    
    """

    k = rsa_keys.get_pub_key1()
    m = rsa_keys.get_pub_key2()
    
    encrypted_integers_in_list = []
    for integer_in_str in splitted_integers_in_list: # 各元を取り出して暗号化し,ecrypted_integersに格納。
        integer = int(integer_in_str)
        b = number_theory.exp_mod(integer,k,m)
        encrypted_integers_in_list.append(b)

    rsa_keys.add_encrypted_integers_in_list(encrypted_integers_in_list)

def decrypt_integers_in_list(rsa_keys,has_priv_keys=False):
    """
    rsa_keys内に格納されているencrypted_integers_in_listを独立に復号化。
    結果をrsa_keysクラスに保存。
    
    has_priv_keysがFalseならば、総当りで復号化を試す（時間がかかる）
    has_priv_keysがTrueならば、秘密鍵を使って復号化（高速）

    Args
    ----------
    rsa_keys:公開鍵などを格納したクラス
    has_priv_keys:秘密鍵を持っているか否かを示す引数
    """

    k = rsa_keys.get_pub_key1()
    m = rsa_keys.get_pub_key2()
    p = rsa_keys.get_priv_key1()
    q = rsa_keys.get_priv_key2()
    encrypted_integers_in_list = rsa_keys.get_encrypted_integers_in_list()# 暗号化された整数が格納されたリスト
    decrypted_integers_in_list = []
    
    for encrypted_integer in encrypted_integers_in_list:
        if(has_priv_keys):#秘密鍵を持っている場合                        
            phi_m = p*q - p - q + 1
            root = number_theory.root_mod(k,encrypted_integer,m,phi_m)            
        else:#秘密鍵を持っていない場合
            root = number_theory.root_mod(k,encrypted_integer,m)
            
        decrypted_integers_in_list.append(str(root))

    rsa_keys.add_decrypted_integers_in_list(decrypted_integers_in_list)

def encrypt(integer_in_str,digit_of_primes=10,num_tries=100):
    """
    integer_in_strを暗号化。
    Args
    ----------
    integer_in_str:整数を表す文字列
    digits_of_primes:正整数
    num_tries:正整数

    Returns
    --------
    暗号化した整数を格納したリスト,1つ目の公開鍵,2つ目の公開鍵,1つ目の秘密鍵,2つ目の秘密鍵。
    """

    assert(isinstance(integer_in_str,str))
        
    (splitted_integers_in_list,rsa_keys) = pre_process_integers(integer_in_str,digit_of_primes,num_tries)#扱いやすいようにプリプロセス
    encrypt_integers_in_list(splitted_integers_in_list,rsa_keys)#暗号化
    
    if(is_encrypting_success(splitted_integers_in_list,rsa_keys)):#暗号化に成功?
        #print("[*] 暗号化に成功")
        return [rsa_keys.get_encrypted_integers_in_list(),
                rsa_keys.get_pub_key1(),
                rsa_keys.get_pub_key2(),
                rsa_keys.get_priv_key1(),
                rsa_keys.get_priv_key2()]

    else:
        #print("[!] 暗号化に失敗")
        raise ValueError('[!]暗号化に失敗しました。')
    
def decrypt(encrypted_integers_in_list,pub_key1,pub_key2,priv_key1,priv_key2):
    if(priv_key1 != None and priv_key2 != None):
        has_priv_keys = True
    else:
        has_priv_keys = False
        
    rsa_keys = RsaKeys(pub_key1,pub_key2,priv_key1,priv_key2,encrypted_integers_in_list)
    
    if(has_priv_keys == False):
        decrypt_integers_in_list(rsa_keys,False)#復号化
    else:
        decrypt_integers_in_list(rsa_keys,True)#復号化
        
    return post_process_integers(rsa_keys.get_decrypted_integers_in_list())

def pre_process_integers(integer_in_str,digit_of_primes,num_tries):
    """
    文字列表示の整数integer_in_strをRSAの仕様と合致するようにプリプロセス。
    """
    encryption_is_success = False
    
    while(not encryption_is_success):#暗号化が成功するまで繰り返す
        rsa_keys = generate_priv_pub_keys(digit_of_primes,num_tries)# 公開鍵、秘密鍵を生成
        m = rsa_keys.get_pub_key2()# 公開鍵のひとつを取り出す
        splitted_integers_in_list = split_integer_in_str_to_blocks(integer_in_str,get_length_of_integer_in_str(m)-1)#適切なブロックに分解
        encryption_is_success = is_split_valid(splitted_integers_in_list,m) #分割した各メッセージaがmと互いに素か否かチェック

    return (splitted_integers_in_list,rsa_keys)

def post_process_integers(decrypted_integers_in_list):
    """
    復号化直後は、リストの状態なので連結して元の状態に戻す。
    """
    return ''.join(decrypted_integers_in_list)#連結

def is_encrypting_success(splitted_integers_in_list,rsa_keys):
    """
    暗号化されたモノが復号化可能化否かをチェック。
    """
    decrypt_integers_in_list(rsa_keys,True)#復号化
    if(compare_lists(splitted_integers_in_list,rsa_keys.get_decrypted_integers_in_list())):#復号化可能か否かチェaック
        return True
    else:
        return False

def is_split_valid(splitted_integer_in_list,m):
    """
    扱いやすい整数のリストが出来上がったあとに、RSAの仕様(リストの各整数は,mと互い素でないと復号化できない)
    を満たすかどうかをチェック。
    満たすならばTrue,そうでないならFalseを返す

    Parameters
    ----------
    splitted_integer:list
    m:正整数

    Returns
    --------
    :bool
    """
    
    for integer_in_str in splitted_integer_in_list:
        integer = int(integer_in_str)
        if(integer == 0): return False
        if(number_theory.euclidean(integer,m)[0] != 1):
            return False
        
    return True
    

def compare_lists(list1,list2):
    """
    list1とlist2の各元(順序も含め)を比較する

    Parameters
    ----------
    list1:list
    list2:list
    Returns
    ---------
    :bool
    ２つのリストの各元が等しいならTrue、そうでないならFalseを返す
    """
    if(len(list1) != len(list2)): # list1とlist2の長さを比較
        return False
    for a,b in zip(list1,list2):
        if(a != b):
            return False
    return True


def get_one_block_from_beginning(string,block_size):
    """
    stringのインデックス0からblock_size-1までの文字列を返す。
    """
    if(len(string) < block_size):
        return string[0:]
    else:
        return string[0:block_size]

def split_integer_in_str_to_blocks(integer_in_str,block_size):
    """
    文字列表示の整数integer_in_strを、大きさblock_sizeのブロックに分割して、各々をリストに格納して返す。
    """
    assert(block_size >= 1)

    blocks = []
    for i in range(math.ceil(get_length_of_integer_in_str(integer_in_str)/block_size)):
        block = get_one_block_from_beginning(integer_in_str[i*block_size:],block_size)        
        blocks.append(block)
    return blocks

def check_splitted_integers_valid(splitted_integers,m):
    """
    分割した整数splitted_integersの妥当性をチェック。
    block_sizeが大きい場合失敗する可能性あり。
    """
    for integer in splitted_integers:
        if(int(integer) > m):
            print("[!] 分割された整数が適切でない。")
            return False        
    return True

def get_length_of_integer_in_str(integer_in_str):
    return len(str(integer_in_str))


