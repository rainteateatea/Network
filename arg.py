import socket
import argparse
import sys
from urllib.parse import urlparse


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s=''

parser = argparse.ArgumentParser(add_help=False)
group = parser.add_mutually_exclusive_group()
parser.add_argument("operation",help="get|post")
#parser.add_argument("post",help="executes a HTTP POST request and prints the response")
#parser.add_argument("help",help="prints this screen")
parser.add_argument("URL",help="determines the targetd HTTP server")
parser.add_argument("-v",help="Prints the detail of the response such as protocol,status, and headers",action="store_true")
parser.add_argument("-h",help="Associates headers to HTTP Request with the format'key:value'",action="append",default=[])
group.add_argument("-d",help="Associates an inline data to the body HTTP POST request",default='')
group.add_argument("-f",help="Associates the content of a file to the body HTTP POST",default='')
parser.add_argument("-o",help="filename Write the body of the response to the spcified file instead of the console",default='')
parser.add_argument("-help",action='help',default=argparse.SUPPRESS,help='prints this screen')

args=parser.parse_args()
if args.operation=='get' and args.URL:
    url = args.URL
    o = urlparse(url)
    for array in args.h:
        array+='\r\n'
        s+=str(array)

    try:
        conn.connect((o.netloc,80))
        line = 'GET /get?'+o.query+' HTTP/1.1\r\nHost:'+o.netloc+'\r\n'+s+'\r\n'
        request = line.encode("utf-8")
        conn.sendall(request)
        response = conn.recv(1024)
        result12 = response.decode("utf-8")
        result1,result2 = result12.split("\r\n\r\n",1)
        if args.v == False and args.o=='':
            print(result2)
        elif args.v ==True and args.o=='':
            print(result12)
        elif args.v == False and args.o!='':
            file_abs="E:\\"+args.o
            f=open(file_abs,"w")
            f.write(result2)
            f.close()
        elif args.v ==True and args.o!='':
            file_abs="E:\\"+args.o
            f=open(file_abs,"w")
            f.write(result12)
            f.close()
    finally:
        conn.close()

elif args.operation == 'post' and args.URL and args.d !='':
    
    url = args.URL
    o=urlparse(url)
    for array in args.h:
        array+='\r\n'
        s+=str(array)
    l = str(len(args.d))
    
    try:
        conn.connect((o.netloc,80))
        line = 'POST /post HTTP/1.1\r\nHost:'+o.netloc+'\r\nContent-Length:'+l+'\r\n'+s+'\r\n'+args.d

        request = line.encode("utf-8")
        conn.sendall(request)
        response = conn.recv(4096)
        result12 = response.decode("utf-8")
        result1,result2 = result12.split("\r\n\r\n",1)
        if args.v == False and args.o=='':
            print(result2)
        elif args.v ==True and args.o=='':
            print(result12)
        elif args.v == False and args.o!='':
            file_abs="E:\\"+args.o
            f=open(file_abs,"w")
            f.write(result2)
            f.close()
        elif args.v ==True and args.o!='':
            file_abs="E:\\"+args.o
            f=open(file_abs,"w")
            f.write(result12)
            f.close()
        
    finally:
        conn.close()

elif args.operation == 'post' and args.URL and args.f !='':
    url = args.URL
    o=urlparse(url)
    for array in args.h:
        array+='\r\n'
        s+=str(array)
    f=open(args.f)
    file=f.readline()
    a = len(file)-1
    l = str(a)

    try:
        conn.connect((o.netloc,80))
        line = 'POST /post HTTP/1.1\r\nHost:'+o.netloc+'\r\nContent-Length:'+l+'\r\n'+s+'\r\n'+file

        request = line.encode("utf-8")
        conn.sendall(request)
        response = conn.recv(4096)
        result12 = response.decode("utf-8")
        result1,result2 = result12.split("\r\n\r\n",1)
        if args.v == False and args.o=='':
            print(result2)
        elif args.v ==True and args.o=='':
            print(result12)
        elif args.v == False and args.o!='':
            file_abs="E:\\"+args.o
            f=open(file_abs,"w")
            f.write(result2)
            f.close()
        elif args.v ==True and args.o!='':
            file_abs="E:\\"+args.o
            f=open(file_abs,"w")
            f.write(result12)
            f.close()
        
    finally:
        conn.close()

elif args.operation=='httpc'and args.URL=='help':
    print("httpc is a curl-like application but supports HTTP protocol only")
    print("Usage:")
    print("     httpc command [arguments]")
    print("The commands are:")
    print("    get   executes a HTTP GET request and prints the response.")
    print("    post  executes a HTTP POST request and prints the response.")
    print("    help  prints this screen.")
    print(" ")
    print("Use "'"httpc help [commend]"'"for more information about a command.")
elif args.operation=='help' and args.URL=='get':
    print("usage: httpc get [-v]  [-h key:value] URL. [-o filename]")
    print(" ")
    print("Get executes a HTTP GET request for a given URL.")
    print(" ")
    print("  -v       Prints the detail of the response such as protocol,status, and headers.")
    print("  -o       Write the body of the response to the spcified file instead of the console")
    print("  -h  key:value  Associates headers to HTTP Request with the format 'key:value'.")
elif args.operation=='help' and args.URL=='post':
    print("usage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL [-o filename]")
    print(" ")
    print("Post exexutes a HTTP POST request fot a given URL with inline data or from file.")
    print(" ")
    print("  -v             Prints the detail of the reponse such as protocol,status, and headers.")
    print("  -h  key:value  Associates headers to HTTP Request with the format 'key:value'.")
    print("  -d string      Associates an inline data to the boby HTTP POST request.")
    print("  -o       Write the body of the response to the spcified file instead of the console")
    print("  -f file        Associates the content of a file to the body HTTP POST request.")
    print("Either [-d] or [-f] can be used but not both")
        
    
        
    
#else:
 #   print("error")
 #       "{""Assignment"":1}"
        
