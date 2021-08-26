import sys
import os
from . import number_theory

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

    (p,q) = generate_prime_pair(bit_length,e)# 素数のペアを生成        
    n = p*q # modulusを計算
    phi_n = (p-1)*(q-1) # nのオイラー関数を計算
    d = get_secret_exponent(e,phi_n)# secret exponentを計算
        
    return [(n,e),(d,p,q)] #[公開鍵,秘密鍵]を返す

def get_secret_exponent(e,phi_n):
    """
    secret exponentを計算してその結果を返す。
    """
    euclidean_solution = number_theory.euclidean(e,phi_n)
    if(euclidean_solution[0] != 1):#secrent exponentの条件を満たさない場合
        print("[!]Error(generate_keys):eとphi_nが互いに素でない")
        exit(-1)

    d = euclidean_solution[1] # secret exponentを取り出す
    assert(1 < d < phi_n) #secrent exponentの条件を確認

    return d

def generate_prime_pair(bit_length,e):
    """
    p*qのビット長がbit_lengthとほぼ等しくなるような,素数のペア(p,q)を生成し返す。
    (注意) 素数生成にはMiller-Rabin素数判定法を使用しているため,必ず素数を返すとは限らない(ただし,合成数を返す確率は(デフォルト動作において)限りなく0に近い確率)
    """

    assert(bit_length >= 10) #10ビット長以上でないと素数がうまく生成されない(例えば bit_length == 6だと,常にp==qとなる)
    
    while(True):
        while(True):
            p = number_theory.generate_n_bits_prime(bit_length//2)
            if((p-1)%e != 1):break
        while(True):
            q = number_theory.generate_n_bits_prime(bit_length - bit_length//2)
            if((q-1)%e != 1):break

        if (p == q): continue   
        elif(p < q):# p > q　となるように調整
            (p,q) = swap(p,q)
            break
    
    return (p,q)

def split_plaintext(plaintext,n):
    """
    引数plaintext(整数)を,modulusである引数nに応じて分割し,その結果を整数のリストとして返す。

    整数plaintextを,各"ブロック"がn未満となるように分割
    例) split_plaintext(123456789,100) => [12,34,56,78,9]
    """

    assert(n >= 10) # nが10未満の場合,分割できない
    
    splitted_plaintext = []    
    # ブロックに分割しやすくするために,strに変換
    plaintext_str = str(plaintext)
    size = len(plaintext_str)
    
    position = 0
    while(position < size):
        offset = 1

        # ブロックの先頭が0の場合即座に分割(例: 0103 => [0,103])
        # (0が先頭にあると,整数に変換したときに情報が失われるため)
        if(int(plaintext_str[position:position+offset]) == 0):
            m = int(plaintext_str[position:position+offset])
            splitted_plaintext.append(m)
            position = position + offset
        else:
            while((position+offset) <= size and int(plaintext_str[position:position+offset]) < n):
                offset += 1
                
            m = int(plaintext_str[position:position+offset-1])
            assert(0 <= m < n)
            
            splitted_plaintext.append(m)
            position = position + offset - 1
              
    return splitted_plaintext

def encrypt(plaintext,n,e):
    """
    引数plaintext(整数)を引数n(modulus)に応じて,リストに分割し各々の元を暗号化し,その結果であるリストを返す。
    """

    splitted_plaintext = split_plaintext(plaintext,n)#整数をリストに分割
    ciphertext = []
    for m in splitted_plaintext:
        c = number_theory.exp_mod(m,e,n)#各元を暗号化
        ciphertext.append(c)

    return ciphertext

def decrypt(ciphertext,d,p,q):
    """
    引数ciphertext(整数のリスト)の各元を,秘密鍵であるd,p,qに応じて,リストの各元を
    復号化し,最後に各元を連結しその結果である整数を返す。
    """

    n = p*q
    plaintext = []
    for c in ciphertext:
        m = number_theory.exp_mod(c,d,n)#各元を復号化
        plaintext.append(m)
    
    return int("".join(map(str,plaintext)))

def swap(p,q):
    return (q,p)
