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
    fw=open("de.txt", "a", encoding="utf-8")
    for c in intstr:
        if c !="\t":
            #print(type(c))
            fw.write(chr(pow(ord(c),e,n)))
            #print(type(chr(pow(ord(c),e,n))))
    fw.close()
def decrypt(intstr, d, n):
    fw=open("dd.txt", "w", encoding="utf-8")
    for c in intstr:
        if c !="\t":
            #print(c)
            #print(chr(pow(c, d,n)))
            fw.write(chr(pow(c, d,n)))
    fw.close()
def clean():
    #clean the files before run
    os.system("del de.txt")
    os.system("del dd.txt")
    os.system("fsutil file createnew de.txt 1000")
    os.system("fsutil file createnew dd.txt 1000")
def getKeys(public, private):
    #key files changed for part b
    k=open(public, "r").readlines()
    a=open(private, "r").readlines()
    #n, e, d
    print(k[0]+" "+k[1]+" "+a[1])
    return k[0], k[1], a[1]
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
#encrypt file to send
clean()

print("!----------------------------------------------------------------!\nEncryption and Decryption with test values for D option")
file=getFile()
print("\nEncrypted Text")
#collect keys
p=137
q=131
n, e, d=getKeys("testpublic.txt", "testprivate.txt")

#build formatted 2d array
arr=readbybyte(n, file)
blocknum=bnum(arr)

i=0
b=0
flag=True
#print("blocking")
while(i<blocknum):
    tarr=getblock(arr)
    encrypt(tarr, int(e), int(n))
    i+=1

#print encrypted
re=open("e.txt", "r", encoding="utf-8")
for i in re.readlines():
    print(i, end="")
print("\n\nDecrypted Text")

#decrypt
dstr=convertInt(readFile("de.txt"))
decrypt(dstr,int(d),int(n))
rd=open("dd.txt", "r", encoding="utf-8")
for i in rd.readlines():
    print(i, end="")
print(f"\n\nE={e}\nN={n}D={d}\nP={p}\nQ={q}")

re.close()
rd.close()