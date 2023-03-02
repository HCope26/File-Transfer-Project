import hashlib
from knapsack_crypt import*
from inv_mod_knapsack import*
import pickle

# This is udpclient.py file

#Import socket programming module
import socket
from function import*

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set destination port
port = 13001

# Include the server Address 
serverAddr = ('192.168.1.12', port)

#clients key info
n = 588 #multiplier
m = 881 # modulus m
c_priv = [2,7,11,21,42,89,180,354] #private key
c_pub = pub_key(n, m, c_priv) #public key

#inv_mod_n = getInvMod(n,m)

#send public key to server
clientPublicKey_bin = pickle.dumps(c_pub)
print("Clients public key will be sent to server: ", c_pub, "\n")
s.sendto(clientPublicKey_bin, serverAddr)
print("Sent client's public key\n")


#wait for the server's public key 
msg, addr = s.recvfrom(1024)
#print(addr)
serverPublicKey_bin = msg
#print("Server's public key received: ", serverPublicKey_bin)
s_pub = pickle.loads(serverPublicKey_bin)
print("Server's public key list:", s_pub)



while True:
    # Send message (input from the keyboard). The string needs to be converted to bytes.
    # To send more than one message, please create a loop
    #Choice of command to upload or download file to/from server
    print("Enter one command: PUT_csv, PUT_pdf, GET_csv, GET_pdf, EXIT")
    cmd = input("->")
    s.sendto(cmd.encode(), serverAddr)

    #putFile()
    #Client uploads CSV to Server
    if cmd == "PUT_csv":
        print("Uploading CSV file to server...")
        
        #Open file to get hash value before encryption
        file = open("test_data.csv","rb")
        file_data = file.read()
        hash_object = hashlib.sha384(file_data)
        hex_dig = hash_object.hexdigest()
        file.close()
        #file closed to enable byte by byte reading
        
        x = 0
        
        #open read and send file
        #reading file one byte at a time
        with open("test_data.csv","rb")as fo:
            while True:
                ### SKIP FIRST 3 BYTES (utf-8 encoding)###
                #sending every byte of file to server
                b = fo.read(1)
                x += 1
                if x <= 3:
                    s.sendto(b, serverAddr)
                    
                else:
                    #encrypting each byte with server public key
                    b_knap = knapsack_encrypt(b, n, m, c_priv, s_pub)
                    
                    if not b:
                        #eof
                        #Sends very last encrypted byte of file and breaks while loop
                        #encode to turn encrypted value into byte object
                        s.sendto(str(b_knap).encode(), serverAddr)      
                        break
                    
                    #send encrypted byte to server
                    s.sendto(str(b_knap).encode(), serverAddr)

        print("File uploaded")
        fo.close()
        
        #sending obtained hash value of this file to server for verification
        s.sendto(hex_dig.encode(), serverAddr)
        print(" ")
        

    #getFile()
    #client downloads CSV from Server
    if cmd == "GET_csv":
        x = 0
        print("Downloading CSV file from server...")
        
        #Creating and writng to new file in Client Directory
        with open(r"Client_Directory\test_data.csv","wb+") as fo:
            while True:
                #receive each encrypted byte from client
                data, addr = s.recvfrom(1024)
                x += 1
                if x <= 3:
                    fo.write(data)
                    
                else:
                    #checks that data received is byte sized
                    #loop breaks if data is larger than a byte
                    #data larger would be the hash value being sent from the og client file
                    if len(data) > 9:
                        #eof
                        break
                    
                    #decode encrypted byte for decryption
                    b_knap = data.decode()
                    #decrypting byte with client private key
                    b = knapsack_decrypt(int(b_knap),n,m,c_priv)
                    #encode decrypted value to write byte object to new file
                    b_enc = b.encode()
                    fo.write(b.encode())
                    
        #closing and reopening file to obtain hash value
        #This allows the hash value to be grabbed from the new file with no issues                
        fo.close()
        print(b)
        
        fo = open(r"Client_directory\test_data.csv","rb")
        Transf_File = fo.read()
        hash_object = hashlib.sha384(Transf_File)
        hex_dig_new = hash_object.hexdigest()
        fo.close()
        
        print("File Stored")
        
        #Grabs the hash value sent from server
        #data here is the last piece of data sent from server 
        og_hexdig = data.decode()
        print("Original hash value:")
        print(og_hexdig)
        print(" ")
        
        print("New File Hash Value:")
        print(hex_dig_new)
        print(" ")

        #comparing original hex value with hash value obtained from newly written file
        if og_hexdig == hex_dig_new:
            print("File hash match... Transfer successfull")
            print("")
            
        else:
            print("File hash mismatch...")
            print("")
            

    #putFile()
    #Client uploads PDF to Server
    if cmd == "PUT_pdf":
        print("Uploading PDF file to server...")
        
        #Open file to get hash value before encryption
        file = open("ESET415_Syllabus_Fall22.pdf","rb")
        file_data = file.read()
        hash_object = hashlib.sha384(file_data)
        hex_dig = hash_object.hexdigest()
        file.close()
        #file closed to enable byte by byte reading
        
        x = 0
        
        #open read and send file
        #reading file one byte at a time
        with open("ESET415_Syllabus_Fall22.pdf","rb")as fo:
            while True:
                #sending every byte of file to server
                b = fo.read(1)
                clean = str(b)
                x += 1
                #last byte of file
                #I tried and tried to avoid this, but i could not get it to work any other way
                if x == 502891:
                    s.sendto(b,serverAddr)
                    break
                
                #checking for encoded byte, encryption messes these up
                elif clean[3] == 'x':
                    s.sendto(b, serverAddr)
                    
                else:
                    #encrypting each byte with server public key
                    b_knap = knapsack_encrypt(b, n, m, c_priv, s_pub)
                    if not b:
                        #eof
                        #Sends very last encrypted byte of file and breaks while loop
                        #encode to turn encrypted value into byte object
                        s.sendto(str(b_knap).encode(), serverAddr)      
                        break
                    
                    #send encrypted byte to server
                    s.sendto(str(b_knap).encode(), serverAddr)

        print("File uploaded")
        fo.close()
        
        #sending obtained hash value of this file to server for verification
        s.sendto(hex_dig.encode(), serverAddr)
        print(" ")

        
    #getFile()
    #client downloads PDF from Server
    if cmd == "GET_pdf":
        print("Downloading PDF file from server...")
        x = 0
        #Creating and writng to new file in Client Directory
        with open(r"Client_Directory\ESET415_Syllabus_Fall22.pdf","wb+") as fo:
            while True:
                #receive each encrypted byte from client
                data, addr = s.recvfrom(1024)
                clean = str(data)
                x += 1
                #last byte of file
                if x == 502891:
                    fo.write(data)
                    break
                    
                elif clean[3] == 'x':
                    fo.write(data)

                else:
                    #checks that data received is byte sized
                    #loop breaks if data is larger than a byte
                    #data larger would be the hash value being sent from the og client file
                    if len(data) > 9:
                        #eof
                        break
                    
                    #decode encrypted byte for decryption
                    b_knap = data.decode()
                    #decrypting byte with server private key
                    b = knapsack_decrypt(int(b_knap),n,m,c_priv)
                    #encode decrypted value to write byte object to new file
                    b_enc = b.encode()
                    fo.write(b_enc)
                    
        #closing and reopening file to obtain hash value
        #This allows the hash value to be grabbed from the new file with no issues                
        fo.close()
        
        fo = open(r"Client_directory\ESET415_Syllabus_Fall22.pdf","rb")
        Transf_File = fo.read()
        hash_object = hashlib.sha384(Transf_File)
        hex_dig_new = hash_object.hexdigest()
        fo.close()
        
        print("File Stored")
        #Grabs the hash value sent from server
        #This is the last piece of data sent from server 
        og_hexdig = data.decode()
        print("Original hash value:")
        print(og_hexdig)
        print(" ")
        
        print("New File Hash Value:")
        print(hex_dig_new)
        print(" ")

        #comparing original hex value with hash value obtained from newly written file
        if og_hexdig == hex_dig_new:
            print("File hash match... Transfer successfull")
            print("")
            
        else:
            print("File hash mismatch...")
            print("")
            
        
#Stop Program
    if cmd == "EXIT":
        # Close connection
        print("Connection closed")
        s.close()
        break



    
