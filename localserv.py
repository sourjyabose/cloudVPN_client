import socket
import requests
import select
import threading
import queue
import random
import multiprocessing
if __name__=='__main__':
    
    dns={}
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    sock.bind(("0.0.0.0",8080));
    sock.listen(5);


    servsocklist=[("127.0.0.1",8081)]



socketstorage={}
def sendtoserverqueue(c,addr,datapackets):
    magnum=random.randint(1,20000)
        
    firstbindat=c.recv(1024)
    c.setblocking(False)
    decoded=firstbindat.split(b"\r\n\r\n")[0].decode();
    
    arrd=decoded.split();
    host,port=arrd[1].split(":");
    
    #if(host.find("youtube")==-1):
        #print("Packet rejected for",host)
     #   c.close()
      #  return
    c.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n");
    try:
        ip=dns[host];
        
    except: 
        query=requests.get("https://one.one.one.one/dns-query?name="+host,headers={"accept":"application/dns-json"})
        ip=query.json()["Answer"][len(query.json()["Answer"])-1]["data"];
        
        dns[host]=ip;
    socketstorage[magnum]=c;
    ipccoms.put(socketstorage);
    #relsock.setblocking(False)
    datapackets.put(b"jiolinkXoXoXoXsourjyakrishna"+f"{ip} {port} {magnum}".encode()+b"VooXoBsourjyaraushan"+firstbindat.split(b"\r\n\r\n")[1])
    
    while True:
        sel,_,_=select.select([c],[],[])
        if(c in sel):
            try:
                print("queing for ",host);
                data=c.recv(4096000)
                if (data != b''):
                    datapackets.put(b"jiolinkXoXoXoXsourjyakrishna"+f"{ip} {port} {magnum}".encode()+b"VooXoBsourjyaraushan"+data)
                else:
                    break;
            except Exception as e:
                print(e);
                c.close()
                #relsock.close()
                break;

def senddatatoserver(datapackets,sockserv):
    #dpl=len(datapackets)
    #ind=0;
    while True:
        #if(ind!=len(datapackets)):
        procbuf=datapackets.get();
        sockserv.sendall(procbuf);
            #dpl=len(datapackets)
            #ind+=1;
def receivefromserverandsendtoclient(clts,ipcoms):
    secondbuff=b''
    clts.setblocking(True)
    print("------")
    checkandbreak=1
    while True:
        
        try:
            
            receiveddat=secondbuff+clts.recv(1000000000)
            print("Returning recv len: ",len(receiveddat))
            
            if(checkandbreak!=1):
                print("ERROR: NO DATA")
                #break;
            checkandbreak=0;                
        except :
            print("Closing Socket")
            break;
        print("================")
        buf=receiveddat.split(b"jiolinkXoXoXoXsourjyakrishna")
        print("BUF LEN:",len(buf))
        secondbuff=b'jiolinkXoXoXoXsourjyakrishna'+buf[len(buf)-1]
        buf[len(buf)-1]=b''
        for dpack in buf:
            if(dpack==b''):
                #print("Execution halt prelouge")
                continue;
            
            payloadheader,payloaddata=dpack.split(b"VooXoBsourjyaraushan")
            
            payloadheader=payloadheader.decode()
            print(payloadheader)
            checkandbreak=1;
            payloadheader=payloadheader.split()
            try:
                ipcoms.get()[int(payloadheader[2])].sendall(payloaddata)
            except:
                print("Connection closed from browser: ",payloadheader)
            #print(payloaddata.decode())
print(__name__);
if __name__=='__main__':
    dpq=[]
    ipccoms=multiprocessing.Queue();
    for inx,servs in enumerate(servsocklist):
        clts=socket.socket()
        clts.connect(servs)
        datapackets=multiprocessing.Queue();
        dpq.append(datapackets);
        multiprocessing.Process(target=receivefromserverandsendtoclient,args=(clts,ipccoms)).start()
        multiprocessing.Process(target=senddatatoserver,args=(datapackets,clts)).start();

    #threading.Thread(target=receivefromserverandsendtoclient).start()
    while True:
        cl,addr1=sock.accept()
        threading.Thread(target=sendtoserverqueue,args=(cl,addr1,dpq[random.randint(1,20000)%len(dpq)])).start()


