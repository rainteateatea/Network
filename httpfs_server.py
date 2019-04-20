import socket
import threading
import argparse
import os
import mimetypes
from email.utils import formatdate
from datetime import datetime
from time import mktime



def getDate():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return formatdate(
        timeval     = stamp,
        localtime   = False,
        usegmt      = True
    )

def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Echo server is listening at', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()

def handle_client(conn, addr):
    print("New client from", addr)
    try:
        data = conn.recv(1024)
        print("Receiving request: \n" +data.decode("utf-8"))
        try:
            response = analysis(data.decode("utf-8"))
        except Exception as e:
            code = e.args[0]
            reason = 'oh Something wrong!'
            response = "HTTP/1.1 " +str(code) +" " +reason +"\r\n\r\nError " +str(code) +" (" +reason +") \n"
            response = response.encode("utf-8")
        finally:
            print("\nSending response: \n" +response.decode("utf-8"))
            conn.sendall(response)
    finally:
        conn.close()

def analysis(line):
    src = line.split(" ",2)
    if src[0]=='GET' and src[1]=='/':
        p = os.listdir(dirname)
        content = " ".join(p)
        file = content+'\r\n'
        data = file.encode("utf-8")
    elif src[0]=='GET' and len(src[1])>1:
        file = src[1].strip('/')
        if os.path.isfile(dirname+file)==True:
            path = dirname+file
            f= open(path,'r')
            line = f.read()
            s= file.split(".")
            suffix= '.'+s[1]
            if suffix=='.txt':
                disposition='Content-Disposition: inline\r\n'
            else :
                disposition='Content-Disposition: attachment\r\n'
            #print(mimetypes.types_map[suffix])
            data = ('HTTP/1.1 200 OK\r\nDate:'+getDate()+'\r\n'+disposition+'Content-Type: '+mimetypes.types_map[suffix]+'\r\n'+'Connection: close'+'\r\n\r\n'+line+'\r\n').encode("utf-8")
        else:
            print(dirname+file)
            line ='404 the file not found\r\n'
            data = line.encode("utf-8")
    elif src[0]=='POST':
        filename = src[1].strip('/')
        path = dirname+filename
        if os.path.isfile(path)==True:
            result = 'your file has been overwrite.\r\n'
            data = result.encode("utf-8")
        else:
            result = 'your file has been created.\r\n'
            data = result.encode("utf-8")
        content = src[2].split("\r\n\r\n")

        f = open(path,"w")
        f.write(content[1])
        f.close()
    else:
        print("here")
        result = '400 Bad Request. \r\n'
        data = result.encode("utf-8")
    return data

# Usage python echoserver.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("-v",help= "Prints debuffing messages.",action="store_true")
parser.add_argument("-p","--port",help="Specifies the port number that the server will listen and serve at.",type=int,default=8080)
parser.add_argument("-d","--path-to-dir",help="specifies the directory that the server will use to read/write requested files",default='/Users/DanQiao/Downloads/python/')
args = parser.parse_args()
dirname = args.path_to_dir
run_server('', args.port)
