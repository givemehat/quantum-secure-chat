def encrypt(message: str, key: str) -> str:
   
    if not key:
        raise ValueError("Encryption key must not be empty.")

    encrypted = [
        chr(ord(ch) ^ int(key[i % len(key)]))
        for i, ch in enumerate(message)
    ]
    return ''.join(encrypted)


def decrypt(ciphertext: str, key: str) -> str:
    
    if not key:
        raise ValueError("Decryption key must not be empty.")

    decrypted = [
        chr(ord(ch) ^ int(key[i % len(key)]))
        for i, ch in enumerate(ciphertext)
    ]
    return ''.join(decrypted)
