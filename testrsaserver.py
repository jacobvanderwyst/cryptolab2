import os
import sys
import numpy
import socket

def readFile(file):
    content=[]
    try:
        filec=open(file, 'rt', encoding='utf-8')
        while(True):
            #print("loop")
            char=filec.read(1)#reads by char
            #print("read")
            #print(char, end="")
            if not char:
                filec.close()
                break
            content.append(char)
    except Exception as e:
        print(f"Error in reading file: \n{e}")
    filec.close()
    #print(content)#1
    return content
def convertInt(string):
    intstr=[]
    for i in string:
        intstr.append(ord(i))
        #print(str(ord(i)), end=" ")
    #print("")
    return intstr
def encrypt(intstr, e, n):
    #print(intstr)
    fw=open("e.txt", "a", encoding="utf-8")
    for c in intstr:
        if c !="\t":
            #print(type(c))
            fw.write(chr(pow(ord(c),e,n)))
            #print(type(chr(pow(ord(c),e,n))))
    fw.close()
def decrypt(intstr, d, n):
    fw=open("sd.txt", "w", encoding="utf-8")
    for c in intstr:
        if c !="\t":
            #print(c)
            #print(chr(pow(c, d,n)))
            fw.write(chr(pow(c, d,n)))
    fw.close()
def clean():
    #clean the files before run
    os.system("del e.txt")
    os.system("del d.txt")
    os.system("del sbpublic.txt")
    os.system("fsutil file createnew e.txt 1000")
    os.system("fsutil file createnew d.txt 1000")
    os.system("fsutil file createnew sbpublic.txt 0")
def getKeys(key):
    #key files changed for part b
    k=open(key, "r").readlines()
    #n, e
    print(k[0]+" "+k[1])
    return k[0], k[1]
def getFile():
    return input("filepath to encrypt\n")   
def readbybyte(n, file):
    content=readFile(file)
    runningtotal=0
    numstmp=[]
    numArray=numpy.array([])
    i=0
    arrnum=1
    '''for j in content:
        print(j, end=" ")
    print(" ")'''
    while i<len(content):
        runningtotal += ord(content[i])
        #print("run "+str(ord(content[i]))+" "+str(runningtotal)+" "+str(n)+" "+str(maxb))
        if(content[i]!="hash"):
            if(runningtotal>int(n)):
                numArray=numpy.append(numArray,numstmp)
                #print(numArray)
                numArray=numpy.append(numArray,int(arrnum))
                #print(numArray)
                runningtotal=0
                numstmp=[]
                numstmp.append(content[i])
                arrnum+=1
            else:
                numstmp.append(content[i])
            i+=1
            if(i>=len(content)):
                numArray=numpy.append(numArray,numstmp)
                numArray=numpy.append(numArray,int(arrnum))
            #print(numArray, end=" ") #2
        #print(" ")
        #print(numArray) #3
        else:
            numstmp.append(content[i+1])
            numArray=numpy.append(numArray, numstmp)
            print(numArray)
            break
    return numArray
def bnum(arr):
    #print(arr)
    tpe=0
    maxvals=0
    valn=1
    for i in arr: #build formatted empty 2d array
        #print(f"{i}"+str(type(i)))
        try:
            int(i)
        except ValueError:
            pass
        else:
            tpe+=1
            valn=0
        if(valn>maxvals):
            maxvals=valn
        valn+=1
    '''#print(f"max {maxvals} tpe {tpe}")
    narr=[[0]*maxvals]*tpe
    a=0
    b=0
    #print(narr)
    i=0
    while(i<len(arr) and b<maxvals): #append values into formatted 2d array
        try:
            int(arr[i])
        except ValueError:
            print(f"narr[{a}][{b}]=arr[{i}] {arr[i]}")
            print(narr)
            l=arr[i]
            narr[a][b]=str(l)
            print(narr)
            b+=1
        else:
            a+=1
            b=0
        i+=1
        #print(f"a{a} b{b}")
        #print(f"a{a} b{b} {narr[a][b]}")
        print("")'''
    return tpe
def getblock(newarr):
    #print(newarr)
    i=0
    tarr=[]
    while i<len(newarr):
        try:
            int(newarr[i])
        except ValueError:
            if(newarr[i] != "\t"):
                tarr.append(newarr[i])
                newarr[i]="\t" 
        except IndexError:
            print(f"IndexError {i}")
            break
        else:
            tarr.append(newarr[i-1])
            newarr[i]="\t"
            break
        i+=1
        
        '''except IndexError:
            print("Err index")
            break'''
    #print(tarr)
    return tarr
def server():
    clean()
    #file to store client public key
    clipubk=open("sbpublic.txt",'wb')    
    #set up socket to send and recieve on
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 4000))
        s.listen()
        print("server started")
        
        conn, addr=s.accept()
        print("waiting for client...")

        with conn:
            print(f"Connection from {addr}")
            
            #recieve client public key
            file_size=int(conn.recv(28).decode("utf-8")) #containes file size
            pkeyrecv=conn.recv(file_size) #contains public key
            clipubk.write(pkeyrecv) #write to client public key
            clipubk.close()
            
            
            print("\n!----------------------------------------------------------------!\nEncryption and Decryption for B option")
            #get keys
            n, e=getKeys("sbpublic.txt")
            #print(f"n {n} e {e}")
            #build formatted 2d array
            file=getFile()
            arr=readbybyte(n, file)
            blocknum=bnum(arr)

            #create hash and add it to array
            text="".join(arr)
            hashv=hash(text)

            #encrypt contents and hash
            i=0
            tarr=[]
            while(i<blocknum):
                tarr=getblock(arr)
                encrypt(tarr, int(e), int(n))
                i+=1
            i=0
            arhash=[]
            while(i<len(str(hashv))):
                arhash.append(str(hashv)[i])
                i+=1
            encrypt(arhash, int(e), int(n))
            print(f"hash= {hashv}")
            
            #send encrypted file size
            ecpfilesnd=open("e.txt", "rb")
            efilesize=sys.getsizeof(ecpfilesnd)
            print(sys.getsizeof(bytes(str(efilesize), encoding="utf-8")))
            conn.send(bytes(str(efilesize), encoding="utf-8"))
            
            #send encrypted file
            ssend=ecpfilesnd.read(efilesize)
            conn.send(ssend)
            ecpfilesnd.close()
        conn.close()
server()


#print encrypted
re=open("e.txt", "r", encoding="utf-8")
for i in re.readlines():
    print(i, end="")
re.close()
'''#decrypt
n=3337
d=7
dstr=convertInt(readFile("e.txt"))
decrypt(dstr,int(d),int(n))
rd=open("sd.txt", "r", encoding="utf-8")
for i in rd.readlines():
    print(i, end="")
print(f"\n\nN={n}D={d}")
rd.close()
'''