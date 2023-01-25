def gcd(v1, v2):
    while v2 !=0:
        v1, v2=v2, v1%v2
    return v1
def coprime(v1,v2):
    return gcd(v1, v2)==1
def getpqe():
    pqe=input("Enter p, q, and e delimited by a space\n")
    if(pqe ==""):
        fnum=input("Filenumber 1,2,3\n")
        p,q,e=getdata(fnum)
    else:
        p, q, e=pqe.split()
    return int(p),int(q),int(e)
def getdata(fnum):
    f1=open("d1.txt", "r")
    f2=open("d2.txt", "r")
    f3=open("d3.txt", "r")
    
    if fnum=='1':
        return f1.readlines()
    elif fnum=='2':
        return f2.readlines()
    elif fnum=='3':
        return f3.readlines()
    else:
        print("invalid value")
        
i=0
while(i<3):
    #get values
    p, q, e=getpqe()
    phin=(p-1)*(q-1) #get phi_n

    cprime=coprime(e, phin) #check primes
    print(f"!---------------------!\n{e} and ({p}-1)*({q}-1) is {cprime}")
    i+=1
