import socket
import requests
import select
import threading
import queue
import random
import os
import customtkinter
import customtkinter as CTk
import customtkinter as ctk



def noprint(*args):
    pass

print=noprint

authdata=["UserNaN","QuotaNaN"]
counter=random.randint(1,20000)  
packetssofar=1;
prev=0;



tabsarray=[]
tabref={}

def authsucc():
    for i in tabsarray:
        i.showframe();

def gettabframe(name):
    return tabsarray[tabref[name]].frame1


def gui():
    loginwindow=None
    def loginpage():
        nonlocal loginwindow;
        loginwindow=ctk.CTkToplevel(window);
        loginwindow.geometry("300x200")
        loginwindow.title("Login")
        loginwindow.attributes("-topmost",True)
        authsucc()
        
        CTk.CTkLabel(loginwindow,text="Username: ").grid(row=0,column=0,padx=5)
        CTk.CTkLabel(loginwindow,text="Password: ").grid(row=1,column=0,padx=5)
        CTk.CTkEntry(loginwindow,placeholder_text="Enter Username",width=200).grid(pady=10,row=0,column=2)
        CTk.CTkEntry(loginwindow,placeholder_text="Enter Password",width=200).grid(pady=10,row=1,column=2)
        CTk.CTkButton(loginwindow,text="Login").grid(row=4,column=2)
        CTk.CTkLabel(loginwindow,text="No account? Sign Up Now !").grid(row=3,column=2)
        


    def login(tab):
        frame=CTk.CTkFrame(tab);
        CTk.CTkLabel(frame,text="Please Login To Use",font=("Arial",20)).pack(pady=20);
        CTk.CTkButton(frame,text="Continue to Login",command=loginpage).pack()
        return frame;



    
    window=customtkinter.CTk()
    
    CTk.set_appearance_mode("system")
    customtkinter.set_default_color_theme("green")
    
    window.title("CloudVPN+")
    window.resizable(False,False)
    window.geometry("1000x600")
    tabset=CTk.CTkTabview(window,width=950,height=550)
    tabset.pack()

    class createtabs:
        def __init__(self,name):
            self.tab=tabset.add(name)
            self.frame1=CTk.CTkFrame(self.tab)
            self.login=login(self.tab)
            self.login.pack();
            tabref[name]=len(tabsarray)
            tabsarray.append(self);
        def showframe(self):
            self.login.pack_forget()
            self.frame1.pack(fill='both',expand=True)
            

    createtabs("Usage Details")
    createtabs("History")
    createtabs("Blocked Sites")
    createtabs("Servers")
    createtabs("Logs")

    
    
    
    #Usage Tab
    usagevar=CTk.StringVar();
    username=CTk.StringVar();
    remdata=CTk.StringVar();
    datausedtoday=CTk.StringVar();
    speed=CTk.StringVar()
    highestspeed=CTk.StringVar();
    quota=CTk.StringVar();
    def update():
            global prev;
            remdata.set(f"Reamaining Data: NaN")
            quota.set(f"Quota: {authdata[1]}")
            username.set(f"Username: {authdata[0]}")
            speed.set(f"Speed: {round(round(packetssofar/(1000*1000),2)-round(prev/(1000*1000),2),2):.2f}Mbps")
            prev=packetssofar;
            usagevar.set(f"Data Used: {round(packetssofar/(1000*1000*1000),2):.2f}Gb")
            window.after(1000,update)
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=username,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=0+5,column=0,sticky='ew',pady=20)
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=speed,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=1+5,column=0,sticky='ew')
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=usagevar,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=2+5,column=0,sticky='ew')
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=remdata,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=4+5,column=0,sticky='ew')
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=quota,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=3+5,column=0,sticky='ew')
    update()
    #End Usage Tab

    #authsucc()


    window.mainloop()

threading.Thread(target=gui).start();






os.system("cls");
dns={}
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
sock.bind(("0.0.0.0",8080));
sock.listen(5);


servsocklist=[("127.0.0.1",8081)]




socketstorage={}
def sendtoserverqueue(c,addr,datapackets):
    global counter;
    counter+=1;
    magnum=counter; 
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
        #print(f"Querying {host}") 
        #query=requests.get("https://one.one.one.one/dns-query?name="+host,headers={"accept":"application/dns-json"})
        #ip=query.json()["Answer"][len(query.json()["Answer"])-1]["data"];
        ip=socket.gethostbyname(host);
        dns[host]=ip;
    socketstorage[magnum]=c;
    #relsock.setblocking(False)
    datapackets.put(b"jiolinkXoXoXoXsourjyakrishna"+f"{ip} {port} {magnum}".encode()+b"VooXoBsourjyaraushan"+firstbindat.split(b"\r\n\r\n")[1])
    
    while True:
        sel,_,_=select.select([c],[],[])
        if(c in sel):
            try:
                print("queing for ",host);
                data=c.recv(4096000)
                global packetssofar
                packetssofar+=len(data)
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
def receivefromserverandsendtoclient(clts):
    secondbuff=b''
    clts.setblocking(True)
    print("------")
    checkandbreak=1
    while True:
        
        try:
            rdatpsf=clts.recv(10000)
            receiveddat=secondbuff+rdatpsf
            global packetssofar
            packetssofar+=len(rdatpsf)
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
                socketstorage[int(payloadheader[2])].sendall(payloaddata)
            except:
                print("Connection closed from browser: ",payloadheader)
            #print(payloaddata.decode())
dpq=[]
for inx,servs in enumerate(servsocklist):
    clts=socket.socket()
    clts.connect(servs)
    datapackets=queue.Queue();
    dpq.append(datapackets);
    threading.Thread(target=receivefromserverandsendtoclient,args=(clts,)).start()
    threading.Thread(target=senddatatoserver,args=(datapackets,clts)).start();

#threading.Thread(target=receivefromserverandsendtoclient).start()
while True:
    cl,addr1=sock.accept()
    threading.Thread(target=sendtoserverqueue,args=(cl,addr1,dpq[random.randint(1,20000)%len(dpq)])).start()


