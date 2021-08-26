# 簡易RSAアルゴリズムデモ
簡易RSAアルゴリズムデモ	

# 特徴
* スクラッチからRSA公開鍵暗号系をPython3を使用して実装
* 最適化が完全にされていないため鍵生成,暗号化,復号化が既存のライブラリと比較して,著しく遅い
* デモのため,セキュリティは極めて脆弱
* デモのため,ユニットテストが完全ではない
* ハイブリット暗号ではない(つまり,任意の長さの平文は適度な大きさに分割し,各々を暗号化)

### RSAアルゴリズムを使用したファイル暗号化デモ(/demo/rsa_demo.py)
```python
from rsa_file import encrypt_file,decrypt_file

def main():
    
    # text.txtを暗号化し,その結果をencrypt_text.txtに格納
    # 公開鍵と秘密鍵はそれぞれpub_keys,priv_keysに格納
    encrypt_file("./data/text.txt","./data/encrypt_text.txt","./data/pub_keys","./data/priv_keys")

    # priv_keysに格納されている秘密鍵を使用して,encrypt_text.txtを復号化し,その結果をdecrypt_text.txtに格納
    decrypt_file("./data/encrypt_text.txt","./data/decrypt_text.txt","./data/priv_keys")

if __name__=='__main__':
    main()

### 一般的な例

```python
from rsa.rsa import *

# 公開鍵の一部であるn(RSA modulus)が少なくとも1024ビット長となるように,公開鍵と秘密鍵のペアを生成
# (n,e),(d,p,q)がそれぞれ公開鍵,秘密鍵に対応
[(n,e),(d,p,q)] = generate_keys1024()

plaintext = random.getrandbits(1000) # 1000ビット長の適当な乱数を生成(この整数を暗号化する)

encrypted_text = encrypt(plaintext,n,e) # 暗号化
decrypted_text = decrypt(encrypted_text,d,p,q) # 復号化
```

### テスト
``` bash
> cd ./tests
> python3 -m unittest
```
