from knapsack_crypt import*

cpriv = [2,7,11,21,42,89,180,354]
cpub = [295,592,301,14,28,353,120,236]

spriv = [2,3,6,13,27,52,105,210]
spub = [79,328,237,304,19,378,167]

plaintext = "Hello"
n = 249
m = 419

encryption = knapsack_encrypt(plaintext, 588, 881, spriv)

decryption = knapsack_decrypt(encryption,588,881,spriv)

print("Encryption ciphertext:",encryption)
print("Decryption plaintext:",decryption)
