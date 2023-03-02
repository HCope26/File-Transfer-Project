import hashlib

# This is udpserver.py file
import socket
from function import *

# create a UDP socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Get local machine address
ip = "192.168.1.12"                          

# Set port number for this server
port = 13000                                          

# Bind to the port
serversocket.bind((ip, port))

print("Waiting to receive message on port " + str(port) + '\n')

while True:
    data, addr = serversocket.recvfrom(1024)
    print("received: " + data.decode())  #receive
    cmd = data.decode() #receive
    
    if cmd == "PUT_csv":
        with open("Server_Directory\lab10_test_data.csv","wb+") as fo:
            while True:
                data, addr = serversocket.recvfrom(1024)
                fo.write(data)
                if not data:
                    #eof
                    break
        fo.close()

        file = open("Server_Directory\lab10_test_data.csv","rb")
        file_data = file.read()
        hex_dig = hashlib.sha384(file_data).hexdigest()
        file.close()
        
        print("File Stored")
        
        hexdig, addr = serversocket.recvfrom(1024)
        og_hexdig = hexdig.decode()
        print("Original hash vlaue:")
        print(og_hexdig)
        print(" ")
        
        print("New File Hash Value:")
        print(hex_dig)
        print(" ")
        
        if og_hexdig == hex_dig:
            print("File hash match... Transfer successfull")
            print("")
            
        else:
            print("File hash mismatch...")
            print("")
            
            


    if cmd == "GET_csv":
        file = open("lab10_test_data.csv","rb")
        file_data = file.read()
        hex_dig = hashlib.sha384(file_data).hexdigest()
        file.close()
        with open("lab10_test_data.csv","rb")as fo:
            while True:
                b = fo.read(1)
                if not b:
                    #eof
                    serversocket.sendto(b, addr)      
                    break
                serversocket.sendto(b, addr)
        fo.close()
        serversocket.sendto(hex_dig.encode(), addr)
        print("File uploaded")
        print("")


    if cmd == "PUT_pdf":
        with open("Server_Directory\ESET689_415_Syllabus_Fall22.pdf","wb+") as fo:
            while True:
                data, addr = serversocket.recvfrom(1024)
                fo.write(data)
                if not data:
                    #eof
                    break
        fo.close()
        print("File Stored")

        file = open("Server_Directory\ESET689_415_Syllabus_Fall22.pdf","rb")
        Transf_File = file.read()
        hex_dig = hashlib.sha384(Transf_File).hexdigest()
        file.close()
        
        hexdig, addr = serversocket.recvfrom(1024)
        og_hexdig = hexdig.decode()
        print("Original hash vlaue:")
        print(og_hexdig)
        print(" ")
        
        print("New File Hash Value:")
        print(hex_dig)
        print(" ")
        
        if og_hexdig == hex_dig:
            print("File hash match... Transfer successfull")
            print("")
            
        else:
            print("File hash mismatch...")
            print("")
            

    if cmd == "GET_pdf":
        file = open("ESET689_415_Syllabus_Fall22.pdf","rb")
        file_data = file.read()
        hex_dig = hashlib.sha384(file_data).hexdigest()
        file.close()
        
        with open("ESET689_415_Syllabus_Fall22.pdf","rb")as fo:
            while True:
                b = fo.read(1)
                if not b:
                    #eof
                    serversocket.sendto(b, addr)      
                    break
                serversocket.sendto(b, addr)
        fo.close()        
        serversocket.sendto(hex_dig.encode(), addr)
        print("File uploaded")
        print("")
        

    if cmd == "EXIT":
        # Close connection
        print("Connection closed")
        serversocket.close()
        break
    

  
