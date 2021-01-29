import random
import os,sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from random import randrange, getrandbits

my_img  = Image.open("stegano.jpg")
pixels = my_img.load()
print("Size:"+str(my_img.size)+" Format:"+my_img.format)
plt.imshow(my_img, cmap="gray")

#RSA

# STEP 1: Generate Two Large Prime Numbers (p,q) randomly


def power(a,d,n):
    ans=1;
    while d!=0:
        if d%2==1:
            ans=((ans%n)*(a%n))%n
        a=((a%n)*(a%n))%n
        d>>=1
    return ans


def MillerRabin(N,d):
    a = randrange(2, N - 1)
    x=power(a,d,N)
    if x==1 or x==N-1:
        return True
    else:
        while(d!=N-1):
            x=((x%N)*(x%N))%N
            if x==1:
                return False
            if x==N-1:
                return True
            d<<=1
    return False


def is_prime(N,K):
    if N==3 or N==2:
        return True
    if N<=1 or N%2==0:
        return False
  
  #Find d such that d*(2^r)=X-1
    d=N-1
    while d%2!=0:
        d/=2
    for _ in range(K):
        if not MillerRabin(N,d):
            return False
    return True; 
  



def generate_prime_candidate(length):
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    # Set MSB to 1 to make sure we have a Number of 1024 bits.
    # Set LSB to 1 to make sure we get a Odd Number.
    p |= (1 << length - 1) | 1
    return p



def generatePrimeNumber(length):
  A=4
  while not is_prime(A, 128):
        A = generate_prime_candidate(length)
  return A



length=5
P=generatePrimeNumber(length)
Q=generatePrimeNumber(length)

print("P:",P)
print("Q:",Q)


#Step 2: Calculate N=P*Q and Euler Totient Function = (P-1)*(Q-1)
N=P*Q
eulerTotient=(P-1)*(Q-1)
print("N:",N)
print("φ:",eulerTotient)



#Step 3: Find E such that GCD(E,eulerTotient)=1 satisfies this condition:  1<E<eulerTotient

def GCD(a,b):
    if a==0:
        return b;
    return GCD(b%a,a)


E=generatePrimeNumber(4)
while GCD(E,eulerTotient)!=1:
    E=generatePrimeNumber(4)
print("E:",E)



# Step 4: Find D. 
#Use Extended Euclidean Algorithm: ax+by=1 i.e., eulerTotient(x)+E(y)=GCD(eulerTotient,e)

def gcdExtended(E,eulerTotient):
    a1,a2,b1,b2,d1,d2=1,0,0,1,eulerTotient,E

    while d2!=1:

    # k
        k=(d1//d2)

        #a
        temp=a2
        a2=a1-(a2*k)
        a1=temp

        #b
        temp=b2
        b2=b1-(b2*k)
        b1=temp

        #d
        temp=d2
        d2=d1-(d2*k)
        d1=temp

        D=b2

    if D>eulerTotient:
        D=D%eulerTotient
    elif D<0:
        D=D+eulerTotient

    return D


D=gcdExtended(E,eulerTotient)
print("D:",D)


row,col=my_img.size
enc = [[0 for x in range(3000)] for y in range(3000)]

#Step 5: Encryption
for i in range(row):
  for j in range(col):
    r,g,b = pixels[i,j]
    C1=power(r,E,N)
    C2=power(g,E,N)
    C3=power(b,E,N)
    enc[i][j]=[C1,C2,C3]
    C1=C1%256
    C2=C2%256
    C3=C3%256
    pixels[i,j]=(C1,C2,C3)

my_img.save("./rsa_encrypt_output.png")





#Step 6: Decryption
for i in range(row):
  for j in range(col):
    r,g,b=enc[i][j]
    M1=power(r,D,N)
    M2=power(g,D,N)
    M3=power(b,D,N)
    pixels[i,j]=(M1,M2,M3)

my_img.save("./rsa_decrypt_output.png")
