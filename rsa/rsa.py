import sys
import os
import number_theory

def generate_keys1024():
    return generate_keys(1024)

def generate_keys2048():
    return generate_keys(2048)

def generate_keys3072():
    return generate_keys(3072)

def generate_keys4096():
    return generate_keys(4096)

def generate_keys(bit_length):
    """
    RSAの公開鍵と秘密鍵のペアを返す。
    引数bit_length(bitの長さであることに注意)は,modulusの長さを指定している。
    """
    e = 65537 # public exponent
    
    p = number_theory.generate_n_bits_prime(bit_length//2)
    q = number_theory.generate_n_bits_prime(bit_length - bit_length//2)
        
    n = p*q # modulusを計算
    phi_n = p*q - p - q + 1 # nのオイラー関数を計算
    
    euclidean_solution = number_theory.euclidean(e,phi_n)
    if(euclidean_solution[0] != 1):#secrent exponentの条件を満たさない場合
        print("[!]Error(generate_keys):eとphi_nが互いに素でない")
        exit(-1)

    d = euclidean_solution[1] # secret exponentを取り出す
    assert(1 < d < phi_n) #secrent exponentの条件を確認
    
    return [(n,e),(d,p,q)] #[公開鍵,秘密鍵]を返す

def split_plaintext(plaintext,n):
    """
    引数plaintext(整数)を,modulusである引数nに応じて分割し,分割して結果をリストとして返す
    """
    
    splitted_plaintext = []
    
    # ブロックに分割しやすくするために,strに変換
    plaintext_str = str(plaintext)
    size = len(plaintext_str)

    """
    # TODO:アルゴリズムを変える
    split_size = len(str(n)) - 1
    assert(split_size > 1)    
    position = 0    
    while(position < size):        
        m = int(plaintext_str[position:position+split_size])
        assert(1 < m < n)
        splitted_plaintext.append(m)
        position += split_size
    """
    
    position = 0
    while(position < size):
        offset = 1
        while((position+offset) <= size and
              int(plaintext_str[position:position+offset]) < n):
            offset += 1

        m = int(plaintext_str[position:position+offset-1])        
        assert(1 < m < n)
        splitted_plaintext.append(m)
        position = position + offset - 1
              
    return splitted_plaintext

def encrypt(plaintext,n,e):
    """
    引数plaintext(整数)を引数n(modulus)に応じて,リストに分割し各々の元を暗号化し,
    その結果であるリストを返す。
    """

    splitted_plaintext = split_plaintext(plaintext,n)#整数をリストに分割
    ciphertext = []
    for m in splitted_plaintext:
        c = number_theory.exp_mod(m,e,n)#各元を暗号化
        ciphertext.append(c)

    return ciphertext

def decrypt(ciphertext,d,n):
    """
    引数ciphertext(整数のリスト)の各元を,秘密鍵であるd,nに応じて,
    復号化し,その結果をリストを返す。
    """
    
    plaintext = []
    for c in ciphertext:
        m = number_theory.exp_mod(c,d,n)#各元を復号化
        plaintext.append(m)

    return int("".join(map(str,plaintext)))


