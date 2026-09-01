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
import requests
import os
import hashlib
import pickle
import string
from tkinter import messagebox
from dotenv import load_dotenv
import time

go=0;
validity=1;
firstTimeRun=0;
info={};
load_dotenv()

try:
    info=pickle.load(open(".deviceInfo","rb"))
except Exception as e:
    firstTimeRun=1;
    characters = string.ascii_letters + string.digits
    
    info["deviceId"]=''.join(random.choices(characters, k=16))


url=os.getenv("ccserver")


    

def encodeNonce(email,value):
    nonce=requests.get(url+"/nonce",json={"UEmail":email}).json()["nonce"]
    return hashlib.sha256((value+str(nonce)).encode("utf-8")).hexdigest()


def noprint(*args):
    pass

print=noprint

authdata=["UserNaN",0,0]
counter=random.randint(1,20000)  
packetssofar=1;
prev=0;



tabsarray=[]
tabref={}

def authsucc():
    global go;
    print("Go set")
    go=1;
    for i in tabsarray:
        i.showframe();

def gettabframe(name):
    return tabsarray[tabref[name]].frame1


def gui():
    
    loginwindow=None
    email=0
    passwd=0;
    def loginpage():
        nonlocal loginwindow;
        loginwindow=ctk.CTkToplevel(window);
        loginwindow.geometry("300x200")
        loginwindow.title("Login")
        loginwindow.attributes("-topmost",True)
        #authsucc()
        
        CTk.CTkLabel(loginwindow,text="Username: ").grid(row=0,column=0,padx=5)
        CTk.CTkLabel(loginwindow,text="Password: ").grid(row=1,column=0,padx=5)
        email=CTk.CTkEntry(loginwindow,placeholder_text="Enter Email",width=200)
        email.grid(pady=10,row=0,column=2)
        passwd=CTk.CTkEntry(loginwindow,placeholder_text="Enter Password",width=200)
        passwd.grid(pady=10,row=1,column=2)
        CTk.CTkButton(loginwindow,text="Login",command=lambda: process(email.get(),passwd.get(),loginwindow)).grid(row=4,column=2)
        CTk.CTkLabel(loginwindow,text="No account? Sign Up Now !").grid(row=3,column=2)
        
    def process(email,passwd,loginwindow):
        global url;
        global info;
        try:
            response=requests.get(f"{url}/authenticate/{email}/{encodeNonce(email,passwd)}/{info["deviceId"]}")
        except Exception as e:
            messagebox.showerror("Error","Something went wrong") 
        response=response.json()
        if response["status"]=="success":
            authdata[0]=response["data"]["email"]
            authdata[1]=response["data"]["quota"]
            authdata[2]=response["data"]["bytesusedsofar"]
            authsucc()
            if firstTimeRun==1:
                info["email"]=email;
                info["password"]=passwd;
                pickle.dump(info,open(".deviceInfo","wb"))
                if loginwindow!=None:
                    loginwindow.destroy()
        elif response["status"]=="ADR":
            messagebox.showwarning("Another Device in Use","The account you are trying to log into is logged in on another device");
            if messagebox.askokcancel("Remove Device?","Proceed to log put from another device ?") :
                response=requests.get(f"{url}/changedevice/{email}/{encodeNonce(email,passwd)}/{info["deviceId"]}")
                process(email,passwd,loginwindow)
        elif response["status"]=="AuthFail":
            messagebox.showerror("Authentication Failure","Invalid Email or Password")
        elif response["status"]=="Blocked":
            messagebox.showwarning("Account Deactivated","Your account has been deactivated for violating our policy.\n If you think this is a mistake contact us. Thank You.")
            

        


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
    seconds=0;
    reportprev=0

    def reporting():
        nonlocal reportprev
        
        if go==1:
            requests.get(f"{url}/reporting/dataUsage/{info["email"]}/{encodeNonce(info["email"],info["password"])}/{packetssofar-reportprev}")
            reportprev=packetssofar
        else:
            requests.get(f"{url}/reporting/dataUsage/{info["email"]}/{encodeNonce(info["email"],info["password"])}/8799007739")


    def update():
            nonlocal seconds
            global prev;
            global go;
            if go==1:
                if (packetssofar+authdata[2])>(authdata[1]*1000*1000*1000):
                    messagebox.showinfo("Data Exhausted !","Please Recharge to Continue using it.")
                    #authdata[1]="Quota: Data Exhausted ! Please Recharge to Continue using it. Data Left: 0"
                    go=0;
            seconds+=1;
            if(seconds%30==0):
                reporting();
            remdata.set(f"Reamaining Data: {round(((authdata[1]*1000*1000*1000)-(authdata[2]+packetssofar))/(1000*1000*1000),2):.2f}Gb")
            quota.set(f"Quota: {round(authdata[1],2)} GB")
            username.set(f"Username: {authdata[0]}")
            speed.set(f"Speed: {round(round(packetssofar/(1000*1000),2)-round(prev/(1000*1000),2),2):.2f}Mbps")
            prev=packetssofar;
            usagevar.set(f"Data Used: {round((authdata[2]+packetssofar)/(1000*1000*1000),2):.2f}Gb")
            window.after(1000,update)


    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=username,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=0+5,column=0,sticky='ew',pady=20)
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=speed,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=1+5,column=0,sticky='ew')
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=quota,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=2+5,column=0,sticky='ew')
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=usagevar,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=3+5,column=0,sticky='ew')
    CTk.CTkLabel(gettabframe("Usage Details"),textvariable=remdata,compound="left",justify="left",anchor='w',width=100,font=('Arial',20)).grid(row=4+5,column=0,sticky='ew')
    
    update()
    #End Usage Tab
    if firstTimeRun==0:
        process(info["email"],info["password"],None)
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
        if go==0:
            return None;
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
        if go==0:
            return None;
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
        if go==0:
            return None;
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

while go==0:
    time.sleep(0.001)

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


