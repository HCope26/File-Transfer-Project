
plaintext = "Hi"
scale = 16
ciphertext = []

seq = [2,7,11,21,42,89,180,354]
public_key = []
n = 588
m = 881
for num in seq:
    knap_norm = (num * n) % m
    public_key.append(knap_norm)
    
print("Public Key:")
print(public_key,"\n")
    
for letter in plaintext:
    #ASCII Value
    decimal_value = ord(letter)
    #ASCII to hex
    hex_value = hex(decimal_value)
    #Hex to binary
    bin_value = "{0:08b}".format(int(hex_value,scale))
    print(letter)
    print(decimal_value)
    print(hex_value)
    print(bin_value,"\n")
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

print("Ciphertext:")   
print(ciphertext,"\n")
        
        
    
        
    
