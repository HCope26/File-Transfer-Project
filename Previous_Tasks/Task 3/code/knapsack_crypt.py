from inv_mod_knapsack import*

def knapsack_encrypt(plaintext,n,m,private_key):
    print("KNAPSACK ENCRYPTION \n")
    scale = 16
    ciphertext = []
    public_key = []
    inv_mod = getInvMod(n,m)

    for num in private_key:
        knap_norm = (num * n) % m
        public_key.append(knap_norm)

    print("Plaintext:",plaintext)
    print("Private Key:",private_key)
    print("n:",n)
    print("m:",m)
    print("Inverse mod n:", inv_mod)
    print("Public Key:",public_key,"\n")
    
    for letter in plaintext:
        #ASCII Value
        decimal_value = ord(letter)
        #ASCII to hex
        hex_value = hex(decimal_value)
        #Hex to binary
        bin_value = "{0:08b}".format(int(hex_value,scale))
        #print(letter)
        #print(decimal_value)
        #print(hex_value)
        #print(bin_value,"\n")
        #obtain ciphertext value
        i = 0
        present = 0
        for pos in public_key:
            if i >= len(bin_value):
               break

            if bin_value[i] == "1":
                present = present + pos
                i += 1

            elif bin_value[i] == "0":
                i += 1
            
        ciphertext.append(present)

    print("Ciphertext:", ciphertext,"\n")
    return(ciphertext)


def knapsack_decrypt(ciphertext,n,m,private_key):
    print("KNAPSACK DECRYPTION \n")
    scale = 16
    plaintext = ""
    #obtaining inverse n with custom function
    inv_n = getInvMod(n,m)

    print("Ciphertext:",ciphertext)
    print("Private Key:",private_key)
    print("n:",n)
    print("m:",m,"\n")

    for value in ciphertext:
        plaintext_binval = ""
        #calculate ptext value to get binary values of plaintext
        Ptext = (inv_n * value) % m
        n = len(private_key) - 1
        bin_one = "1"
        bin_zero = "0"
        newval = 0
        while n >= 0:
            if Ptext < private_key[n]:
                plaintext_binval = "0" + plaintext_binval

            elif Ptext >= private_key[n]:
                Ptext = Ptext - private_key[n]
                plaintext_binval = "1" + plaintext_binval
            n -= 1
        #print(plaintext_binval)
        #binary to hex
        plaintext_hexval = hex(int(plaintext_binval, 2))
        #print(plaintext_hexval)
        #hex to ASCII decimal value
        plaintext_ascii = int(plaintext_hexval,16)
        #print(plaintext_ascii)
        #ASCII to character
        plaintext = plaintext + chr(plaintext_ascii)

    print("Plaintext:",plaintext,"\n")
    return(plaintext)
