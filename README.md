# RSA公開鍵暗号系デモ
簡易RSA公開鍵暗号系デモ

##特徴
*スクラッチからRSA公開鍵暗号系をPython3を使用して実装
*最適化が完全にされていないため鍵生成,暗号化,復号化が既存のライブラリと比較して,著しく遅い
*デモのため,セキュリティは極めて脆弱
*ハイブリット暗号ではない(つまり,任意の長さを平文は適度な大きさに分割し,各々を暗号化)

```python

encrypt_file("./data/text.txt","./data/encrypt_text.txt","./data/pub_keys","./data/priv_keys")
decrypt_file("./data/encrypt_text.txt","./data/decrypt_text.txt","./data/pub_keys","./data/priv_keys")
    
```