import hashlib

# This is udpclient.py file

#Import socket programming module
import socket
from function import*

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set destination port
port = 13000

# Include the server Address 
serverAddr = ('192.168.1.12', port)


while True:
    # Send message (input from the keyboard). The string needs to be converted to bytes.
    # To send more than one message, please create a loop
    print("Enter one command: PUT_csv, PUT_pdf, GET_csv, GET_pdf, EXIT")
    cmd = input("->")
    s.sendto(cmd.encode(), serverAddr)

    #putFile()
    if cmd == "PUT_csv":
        #hash from og file
        file = open("lab10_test_data.csv","rb")
        file_data = file.read()
        hex_dig = hashlib.sha384(file_data).hexdigest()
        file.close()
        #open read and send file
        #reading file one byte at a time
        with open("lab10_test_data.csv","rb")as fo:
            while True:
                b = fo.read(1)
                if not b:
                     #eof
                    s.sendto(b, serverAddr)      
                    break
                s.sendto(b, serverAddr)
        s.sendto(hex_dig.encode(), serverAddr)
        print("File uploaded")
        fo.close()
        #print("Hash Value:")
        #print(hex_dig) #verify hash received at server matches
        print(" ")

    #getFile()
    if cmd == "GET_csv":
        with open("Client_Directory\lab10_test_data.csv","wb+") as fo:
            while True:
                data, addr = s.recvfrom(1024)
                fo.write(data)
                if not data:
                    #eof
                    break
        fo.close()
        print("File Stored")

        file = open("Client_Directory\lab10_test_data.csv","rb")
        Transf_File = file.read()
        hex_dig = hashlib.sha384(Transf_File).hexdigest()
        file.close()

        hexdig, addr = s.recvfrom(1024)
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
            


    #putFile()
    if cmd == "PUT_pdf":
        file = open("ESET689_415_Syllabus_Fall22.pdf","rb")
        file_data = file.read()
        hex_dig = hashlib.sha384(file_data).hexdigest()
        file.close()
        #open read and send file
        #reading file one byte at a time
        with open("ESET689_415_Syllabus_Fall22.pdf","rb")as fo:
            while True:
                b = fo.read(1)
                if not b:
                     #eof
                    s.sendto(b, serverAddr)      
                    break
                s.sendto(b, serverAddr)
        fo.close()
        s.sendto(hex_dig.encode(), serverAddr)
        print("File uploaded","\n")
        
    #getFile()
    if cmd == "GET_pdf":
        with open("Client_Directory\ESET689_415_Syllabus_Fall22.pdf","wb+") as fo:
            while True:
                data, addr = s.recvfrom(1024)
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

        hexdig, addr = s.recvfrom(1024)
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
            
        
#Stop Program
    if cmd == "EXIT":
        # Close connection
        print("Connection closed")
        s.close()
        break



    
