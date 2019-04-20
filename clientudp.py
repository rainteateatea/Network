import argparse
import ipaddress
import socket
from urllib.parse import urlparse
from packet import Packet

#url = args.URL
#o = urlparse(url)
filesplit=[]
postfile=[]
postfilename = ''
def message():
   # print('111')
    url = args.URL
    o = urlparse(url)
    host,port = o.netloc.split(':')
    if args.operation =='get' and args.URL:
        run_get(args.routerhost,args.routerport,host,port,0,1,'SYN')
    elif args.operation =='post' and args.URL :
        print(port)
        run_post(args.routerhost,args.routerport,host,port,0,1,'SYN')
        
            
            
       
    
   # run_client(args.routerhost, args.routerport, host, port)



def run_get(router_addr,router_port,server_addr,server_port,p_t,s_n,msg):
#    url = args.URL
 #   o = urlparse(url)
  #  host,port = o.netloc.split(':')
    #filesplit=[]
    geturl = args.URL
    geto = urlparse(geturl)
    line = 'GET '+geto.path
    
    peer_ip= ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    timeout = 5
    
  #  conn.bind(('',5000))
    
    try:
    #    conn.bind(('',5000))
    #第一次握手
        p = Packet(packet_type=p_t,
                   seq_num=s_n,
                   peer_ip_addr=peer_ip,
                   peer_port = server_port,
                   payload = msg.encode("utf-8"))
        conn.sendto(p.to_bytes(), (router_addr,router_port))
        print('Send "{}" to router'.format(msg))

        conn.settimeout(timeout)
        print('Waiting for a response')
        response,sender = conn.recvfrom(1024)
        p = Packet.from_bytes(response)
     #   print('Payload: ' + p.payload.decode("utf-8"))
        
       # if p.payload.decode("utf-8")=='ACK':
        if p.packet_type == 0:

            #GET第二次握手
            print('Packet: ', p)
            print(p.packet_type)
            print('Payload: ' + p.payload.decode("utf-8"))
            
            return run_get(router_addr,router_port,server_addr,server_port,1,0,line)
        else:
            if p.packet_type==1:
                
                print('Packet: ', p)
                print(p.packet_type)
                print('Payload: ' + p.payload.decode("utf-8"))
            elif p.packet_type==2:
                print(p.seq_num)
                seq = p.seq_num+1
                filesplit.append(p.payload)
             #   print(filesplit)
                
               # print('Payload: ' + p.payload.decode("utf-8"))
                run_get(router_addr,router_port,server_addr,server_port,1,seq,line)
            elif p.packet_type==3:
                print('Payload: ' + p.payload.decode("utf-8"))
           
            if len(filesplit)>0 :
                a = geto.path.strip('/')
                s= a.split('.')
                suffix = '.'+ s[1]
                with open("E:\\download\\"+a,'wb') as f2:
                    for index in range(len(filesplit)):
                        n=f2.write(filesplit[index])
            else:
                print("finish")
                
          

    except socket.timeout:
        print('No response after {}s'.format(timeout)+'  send request again')
        print(msg+'111')
        print(s_n)
        run_get(router_addr,router_port,server_addr,server_port,p_t,s_n,msg)
    #    elif a =='GET /':
     #       run_get(router_addr,router_port,server_addr,server_port,2,s_n,a)
               
    finally:
        conn.close()
def run_post(router_addr,router_port,server_addr,server_port,p_t,s_n,msg):
    peer_ip = ipaddress.ip_address(socket.gethostbyname(server_addr))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = 5
    
    posturl = args.URL
    posto = urlparse(posturl)
   #post -D 
    if args.d!='':
        line = 'POST '+posto.path+'\r\n\r\n'+args.d
       
        try:
            
            p = Packet(packet_type = p_t,
                     seq_num = s_n,
                     peer_ip_addr = peer_ip,
                     peer_port = server_port,
                     payload = msg.encode("utf-8"))
            conn.sendto(p.to_bytes(),(router_addr,router_port))
            print('Send "{}" to router'.format(msg))
            conn.settimeout(timeout)
            print('Waiting for a response')
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
            print('Router: ', sender)
            print('Packet: ', p)
            print(p.packet_type)
            print('Payload: ' + p.payload.decode("utf-8"))
            if p.packet_type==0:
                #POST第二次握手
                return run_post(router_addr,router_port,server_addr,server_port,1,0,line)
            elif p.packet_type==1:
                print('Packet: ', p)
                print(p.packet_type)
                print('Payload: ' + p.payload.decode("utf-8"))
        
                
                
        except socket.timeout :
            print('No response after {}s'.format(timeout)+'  send request again')
            run_post(router_addr,router_port,server_addr,server_port,p_t,s_n,msg)
        finally:
            conn.close()
        
        
        
# post -F
    elif args.f!='':
        print('111')
        line = 'POST '+posto.path
        global postfilename
        postfilename = 'E://upload/'+args.f
        try:
            p = Packet(packet_type = p_t,
                     seq_num = s_n,
                     peer_ip_addr = peer_ip,
                     peer_port = server_port,
                     payload = msg.encode("utf-8"))
            conn.sendto(p.to_bytes(),(router_addr,router_port))
    #        print('Send "{}" to router'.format(msg))
            conn.settimeout(timeout)
     #       print('Waiting for a response')
            response, sender = conn.recvfrom(1024)
            p = Packet.from_bytes(response)
      #      print('Router: ', sender)
       #     print('Packet: ', p)
        #    print(p.packet_type)
         #   print('Payload: ' + p.payload.decode("utf-8"))
            if p.packet_type==0:
                #POST第二次握手
                return run_post(router_addr,router_port,server_addr,server_port,1,0,line)
####################
            elif p.packet_type==4:
                post_sendfile(p.seq_num)
                
            '''    i =0
                with open(filename,'rb') as f1:
                    f1.seek(1013*p.seq_num,1)
                    print(p.seq_num)
                    buf = f1.read(1013)
                    print(len(buf))
                    if buf:
                        #print("222")
                        print(type(buf))
                        content = bytes.decode(buf)
                        post_sendfile()
                      #  run_post(router_addr,router_port,server_addr,server_port,4,p.seq_num,content)
                    else:
                        print("finish")'''
            
           
                
        except socket.timeout:
            print('No response after {}s'.format(timeout)+'  send request again')
            run_post(router_addr,router_port,server_addr,server_port,p_t,s_n,msg)
        finally:
            conn.close()



            
def post_sendfile(s_n):
    print(s_n)
    peer_ip = ipaddress.ip_address(socket.gethostbyname('localhost'))
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = 5
    with open(postfilename,'rb') as f1:
        f1.seek(1013*s_n)
        buf = f1.read(1013)
        if buf:
            try:
                p = Packet(packet_type=4,
                   seq_num=s_n,
                   peer_ip_addr=peer_ip,
                   peer_port=8007,
                   payload= buf)
                conn.sendto(p.to_bytes(), (args.routerhost, args.routerport))
                conn.settimeout(timeout)
                response, sender = conn.recvfrom(1024)
                p = Packet.from_bytes(response)
                print('Payload: ' + p.payload.decode("utf-8"))
                post_sendfile(p.seq_num)
            except socket.timeout:
                print('No response after {}s'.format(timeout))
                post_sendfile(s_n)
            finally:
                conn.close()
        else:
            print("finish")
            exit()
            




parser = argparse.ArgumentParser(add_help=False)
group = parser.add_mutually_exclusive_group()

parser.add_argument("operation",help="get|post")
parser.add_argument("URL",help="determines the targetd HTTP server")
parser.add_argument("-v",help="Prints the detail of the response such as protocol,status, and headers",action="store_true")
parser.add_argument("-h",help="Associates headers to HTTP Request with the format'key:value'",action="append",default=[])
group.add_argument("-d",help="Associates an inline data to the body HTTP POST request",default='')
group.add_argument("-f",help="Associates the content of a file to the body HTTP POST",default='')
parser.add_argument("-o",help="filename Write the body of the response to the spcified file instead of the console",default='')
parser.add_argument("-help",action='help',default=argparse.SUPPRESS,help='prints this screen')


parser.add_argument("--routerhost", help="router host", default="localhost")
parser.add_argument("--routerport", help="router port", type=int, default=3000)

parser.add_argument("--serverhost", help="server host", default="localhost")
parser.add_argument("--serverport", help="server port", type=int, default=8007)

args = parser.parse_args()

#run_client(args.routerhost, args.routerport)
message()
