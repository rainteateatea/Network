import argparse
import socket
import threading
import os
import mimetypes
from email.utils import formatdate
from datetime import datetime
from time import mktime


from packet import Packet

filesplit=[b'']*1024*1024
filename=''
name='1'

def getDate():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return formatdate(
        timeval     = stamp,
        localtime   = False,
        usegmt      = True
    )
def run_server(port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('Echo server is listening at',port)
        while True:
            data, sender = conn.recvfrom(1024)
            threading.Thread(target=handle_client, args=(conn, data, sender)).start()
          #  handle_client(conn, data, sender)
    finally:
        conn.close()
        
def handle_client(conn,data,sender):
    global name
    try:
        p = Packet.from_bytes(data)
        print("Router: ", sender)
        print("Packet: ", p)
    #    print("Payload: ", p.payload.decode("utf-8"))
        
        #if p.payload.decode("utf-8")=='SYN'or p.payload.decode("utf-8")=='NAK':
        if p.packet_type == 0:   
            p.packet_type =0
            p.seq_num = 1
            msg ="ACK"
            p.payload=msg.encode("utf-8")
            conn.sendto(p.to_bytes(), sender)
        elif p.packet_type==1:
            receive = p.payload.decode("utf-8")
            src = receive.split(" ")
         #   print(src[0])
            if src[0]=='GET' and src[1]=='/':
                folder = os.listdir(dirname)
                content = " ".join(folder)
                p.packet_type = 1
                p.seq_num = 0
                p.payload = content.encode("utf-8")
                conn.sendto(p.to_bytes(), sender)
            elif src[0]=='GET'and len(src[1])>1:
                file = src[1].strip('/')
                if os.path.isfile(dirname+file)==True :
                    o=[]

                    path = dirname+file
                    with open(path,'rb') as f1:
                        while True:
                            buf = f1.read(1013)
                            if buf:
                               o.append(buf)
                            else:
                                break
                  #  p.packet_type = 2
                    if p.seq_num<len(o):
                        p.packet_type = 2
                        #p.payload = (o[p.seq_num]).encode("utf-8")
                        p.payload = o[p.seq_num]
                     #   print(len(o))
                        conn.sendto(p.to_bytes(),sender)
                    else:
                        p.packet_type=3
                        msg = "finish"
                        p.payload =msg.encode("utf-8")
                        
                        conn.sendto(p.to_bytes(),sender)
                else:
                    p.packet_type =1
                    p.seq_num =0
                    p.payload = ("404 the file not found").encode("utf-8")
                    conn.sendto(p.to_bytes(),sender)
            elif src[0]=='POST':
                if '\r\n\r\n' in src[1]:
                    file,content = src[1].split('\r\n\r\n')
                    filename = file.strip('/')
                    
                    f=open(dirname+filename,"w")
                    f.write(content)
                    f.close()
                    p.packet_type = 1
                    p.seq_num = 0
                    p.payload = ("finish").encode("utf-8")
                    conn.sendto(p.to_bytes(), sender)
                else:
                #    global name
                    name = src[1].strip('/')
                    p.packet_type=4
                    p.payload = ("start").encode("utf-8")
                    conn.sendto(p.to_bytes(),sender)
                    
                    print(name)
##########
        elif p.packet_type==4 :
            filesplit[p.seq_num] = p.payload
           # filesplit.append(p.payload)
            p.seq_num=p.seq_num+1
            p.payload = ("ACK").encode("utf-8")
            conn.sendto(p.to_bytes(),sender)
                    

                  
        if filesplit!=[]:
            
            print(name)
            with open(dirname+name,'wb') as f2:
                for index in range(len(filesplit)):
                    n= f2.write(filesplit[index])
        #del filesplit[:]
           ###清空数组
            
            
                    
    except Exception as e:
        print("Error: ", e)
        
            
    





parser = argparse.ArgumentParser()
parser.add_argument("-v",help= "Prints debuffing messages.",action="store_true")
parser.add_argument("-p","--port",help="Specifies the port number that the server will listen and serve at.",type=int,default=8007)
parser.add_argument("-d","--path-to-dir",help="specifies the directory that the server will use to read/write requested files",default='E:\\directory\\')
args = parser.parse_args()
dirname = args.path_to_dir
print(args.port)
run_server(args.port)
