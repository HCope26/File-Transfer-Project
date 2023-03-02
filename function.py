from inv_mod_knapsack import*


def formatChar(myChar):
    decode = myChar.decode('utf-8')
    ascii_val = ord(decode)
    hex_val = hex(ascii_val)
    myBin = "{0:08b}".format(int(hex_val,16))
    myList = list(myBin)
    binList = []
    for i in myList:
        binList.append(int(i))

    return binList

def pdf_knap_encrypt(plaintext,n,m,private_key, public_key):
   # print("KNAPSACK ENCRYPTION \n")
    scale = 16
    ciphertext = 0
    inv_mod = getInvMod(n,m)
    
    for letter in plaintext:
        #ASCII Value
        #decimal_value = ord(letter)
        #ASCII to hex
        hex_value = hex(decimal_value)
        #Hex to binary
        bin_value = "{0:08b}".format(int(hex_value,scale))
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
            
        ciphertext = ciphertext + present

    #print("Ciphertext:", ciphertext,"\n")
    return(ciphertext)

def pdf_knap_decrypt(ciphertext,n,m,private_key):
    #print("KNAPSACK DECRYPTION \n")
    scale = 16
    plaintext = ""
    #obtaining inverse n with custom function
    inv_n = getInvMod(n,m)
    
    ctext = []
    ctext.append(ciphertext)

    for value in ctext:
        plaintext_binval = ""
        #calculate ptext value to get binary values of plaintext
        Ptext = (inv_n * value) % m
        n = len(private_key) - 1
        while n >= 0:
            if Ptext < private_key[n]:
                plaintext_binval = "0" + plaintext_binval

            elif Ptext >= private_key[n]:
                Ptext = Ptext - private_key[n]
                plaintext_binval = "1" + plaintext_binval
            n -= 1
        #binary to hex
        plaintext_hexval = hex(int(plaintext_binval, 2))
        #hex to ASCII decimal value
        plaintext_ascii = int(plaintext_hexval,16)
        #ASCII to character
        plaintext = plaintext + chr(plaintext_ascii)
    #print("Plaintext:",plaintext,"\n")
    return(plaintext)


        
###########################################################
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

    
