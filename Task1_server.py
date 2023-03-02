import hashlib
from knapsack_crypt import*
from inv_mod_knapsack import*
import pickle

# This is udpserver.py file
import socket
from function import *

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "192.168.1.12"

# Set port number for this server
port = 13001                                          

# Bind to the port
serversocket.bind((ip, port))

#servers key info
n = 249
m = 419
s_priv = [2,3,6,13,27,52,105,210] #private key
s_pub = pub_key(n, m, s_priv)
#inv_mod_n = getInvMod(n,m)

print("Server's public key will be sent to client: ", s_pub)

print("Waiting to receive message on port " + str(port) + '\n')

#receive key from client
data, addr = serversocket.recvfrom(1024)
#print(addr)
clientPublicKey_bin = data
#print("Client's key received: " , clientPublicKey_bin)
c_pub = pickle.loads(clientPublicKey_bin)
print("Client's public key list:", c_pub)

#send server's public key to client
serverPublicKey_bin = pickle.dumps(s_pub)
#print("\n Will send server's public key ", serverPublicKey_bin)
serversocket.sendto(serverPublicKey_bin, addr)
print("Sent server's public key ")

while True:
    #receive upload/download file command from client
    data, addr = serversocket.recvfrom(1024)
    print("received: " + data.decode())  #receive
    cmd = data.decode() #receive

    #Server downloads CSV file from client
    if cmd == "PUT_csv":
        x = 0
        print("Downloading CSV file from client...")
        
        #Creating and writng to new file in Server Directory
        with open(r"Server_Directory\test_data.csv","wb+") as fo:
            while True:
                #receive each encrypted byte from client
                data, addr = serversocket.recvfrom(1024)
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
                    #decrypting byte with server private key
                    b = knapsack_decrypt(int(b_knap),n,m,s_priv)
                    #encode decrypted value to write byte object to new file
                    b_enc = b.encode()
                    fo.write(b_enc)

        #closing and reopening file to obtain hash value
        #This allows the hash value to be grabbed from the new file with no issues
        fo.close()
        
        fo = open(r"Server_directory\test_data.csv","rb")
        Transf_File = fo.read()
        hash_object = hashlib.sha384(Transf_File)
        hex_dig_new = hash_object.hexdigest()
        fo.close()

        print("File Stored")
        #Grabs the hash value sent from client
        #This is the last piece of data sent from client 
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
            
            

    #Server Uploads CSV file to client
    if cmd == "GET_csv":
        print("Uploading CSV file to client...")
        
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
                #sending every byte of file to server
                #first three bytes utf-8 encoding
                b = fo.read(1)
                x += 1
                if x<= 3:
                    serversocket.sendto(b, addr)
                    
                else:
                    #encrypting each byte with client public key
                    b_knap = knapsack_encrypt(b, n, m, s_priv, c_pub)
                    
                    if not b:
                        #eof
                        #Sends very last encrypted byte of file and breaks while loop
                        #encode to turn encrypted value into byte object
                        serversocket.sendto(str(b_knap).encode(), addr)      
                        break
                    
                    #send encrypted byte to client
                    serversocket.sendto(str(b_knap).encode(), addr)
                    
        print("File uploaded")
        fo.close()

        #sending obtained hash value of this file to client for verification
        serversocket.sendto(hex_dig.encode(), addr)
        print("")


    #Server downloads PDF file from client
    if cmd == "PUT_pdf":
        x = 0
        print("Downloading PDF file from client...")
        
        #Creating and writng to new file in Server Directory
        with open(r"Server_Directory\ESET415_Syllabus_Fall22.pdf","wb+") as fo:
            while True:
                #receive each encrypted byte from client
                data, addr = serversocket.recvfrom(1024)
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
                    b = knapsack_decrypt(int(b_knap),n,m,s_priv)
                    #encode decrypted value to write byte object to new file
                    b_enc = b.encode()
                    fo.write(b_enc)

        #closing and reopening file to obtain hash value
        #This allows the hash value to be grabbed from the new file with no issues
        fo.close()

        #receiving orginal hash value
        data, addr = serversocket.recvfrom(1024)
        
        fo = open(r"Server_directory\ESET415_Syllabus_Fall22.pdf","rb")
        Transf_File = fo.read()
        hash_object = hashlib.sha384(Transf_File)
        hex_dig_new = hash_object.hexdigest()
        fo.close()

        print("File Stored")
        #Grabs the hash value sent from client
        #This is the last piece of data sent from client 
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
            

    #Server Uploads PDF file to client
    if cmd == "GET_pdf":
        print("Uploading PDF file to client...")
        
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
                    serversocket.sendto(b,addr)
                    break
                
                #checking for encoded byte, encryption messes these up
                elif clean[3] == 'x':
                    serversocket.sendto(b, addr)
                    
                else:
                    #encrypting each byte with server public key
                    b_knap = knapsack_encrypt(b, n, m, s_priv, c_pub)
                    if not b:
                        #eof
                        #Sends very last encrypted byte of file and breaks while loop
                        #encode to turn encrypted value into byte object
                        serversocket.sendto(str(b_knap).encode(), addr)      
                        break
                    
                #send encrypted byte to client
                serversocket.sendto(str(b_knap).encode(), addr)
                
        print("File uploaded")
        fo.close()

        #sending obtained hash value of this file to client for verification
        serversocket.sendto(hex_dig.encode(), addr)
        print("")
        

    if cmd == "EXIT":
        # Close connection
        print("Connection closed")
        serversocket.close()
        break
    

  
