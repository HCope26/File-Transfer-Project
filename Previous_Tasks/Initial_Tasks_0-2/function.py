def encryptCaesar(plaintext, n):
    your_ciphertext = ""

    for letter in plaintext:
        #obtaining ascii value of letter
        value = ord(letter)
        #increase ascii value by n
        value = (value + n) % 128
        #concatenating new encrypted letters
        your_ciphertext = your_ciphertext + chr(value)
    return  your_ciphertext 


def decryptCaesar(plaintext, n):
    your_ciphertext = ""
    for letter in plaintext:
        #obtaining ascii value of letter
        value = ord(letter)
        #decrease ascii value by n
        value = (value - n) % 128
        #concatenating new encrypted letters
        your_ciphertext = your_ciphertext + chr(value)
    return  your_ciphertext 

def polyEncrypt(plaintext, key):
    your_ciphertext = ""
    i = 0
    for letter in plaintext:
        ascii_value = (ord(letter) + ord(key[i])) % 128
        i = (i + 1) % len(key)
        your_ciphertext = your_ciphertext + chr(ascii_value)

    return your_ciphertext

def polyDecrypt(plaintext, key):
    your_ciphertext = ""
    i = 0
    for letter in plaintext:
        ascii_value = (ord(letter) - ord(key[i])) % 128
        i = (i + 1) % len(key)
        your_ciphertext = your_ciphertext + chr(ascii_value)

    return your_ciphertext

    
