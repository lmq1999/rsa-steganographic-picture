import random
import os,sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re

from random import randrange, getrandbits


def int_to_bin(rgb):
    r, g, b = rgb
    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b))

def bin_to_int(rgb):

    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))

#RSA
# STEP 1: Generate Two Large Prime Numbers (p,q) randomly

print("Generating custom RSA key:.....")

def power(a,d,n):
    ans=1
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
            if x==1:cover_image  = Image.open("stegano.jpg")
# cover_image_pixels = cover_image.load()
# cover_row,cover_col=cover_image.size





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
    p = getrandbits(length)
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
print("φ(n):",eulerTotient)



#Step 3: Find E such that GCD(E,eulerTotient)=1 satisfies this condition:  1<E<eulerTotient

def GCD(a,b):
    if a==0:
        return b
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


print("Public key (e:",E,"n:",N,")")
print("Private key (d:",D,"n:",N,")")
print("============================")

####################################################################################################################################
encrypt_img  = Image.open("test.jpeg")
encrypt_img_pixels = encrypt_img.load()
# print("Picture infomation:")
# print("Size:"+str(encrypt_img.size)+" Format:"+encrypt_img.format)


encrypt_row,encrypt_col=encrypt_img.size
enc = [[0 for x in range(encrypt_row)] for y in range(encrypt_col)]


#Step 5: Encryption
print("Encrypting picture with RSA public key (e:",E,"n:",N,")...")
for i in range(encrypt_row):
  for j in range(encrypt_col):
    red,green,blue = encrypt_img_pixels[i,j]
    C1=power(red,E,N)
    C2=power(green,E,N)
    C3=power(blue,E,N)
    enc[i][j]=[C1,C2,C3]
    C1=C1%256
    C2=C2%256
    C3=C3%256
    encrypt_img_pixels[i,j]=(C1,C2,C3)

encrypt_img.save("./rsa_encrypt_output.png")
print("RSA_encrypted picture complete, save at ./rsa_encrypt_output.png")
print("============================")
####################################################################################################################################
#Step B: Embedding image

cover_image  = Image.open("stegano.jpg")
cover_image_pixels = cover_image.load()
cover_row,cover_col=cover_image.size

di,dj=0,0

def embebding(di,dj,count,red_b,green_b,blue_b):
    d_red,d_green,d_blue = int_to_bin(cover_image_pixels[di,dj])
    d_red = d_red[0:6]+red_b[count]
    d_green = d_green[0:6]+green_b[count]
    d_blue = d_blue[0:6]+blue_b[count]
    rgb=(d_red, d_green, d_blue)
    d_red, d_green, d_blue = bin_to_int(rgb)
    cover_image_pixels[di,dj]=(d_red, d_green, d_blue)
    return di, dj

print("Embemding encrypted picture to cover picture...")
for ei in range(encrypt_row):
  for ej in range(encrypt_col):
    e_red,e_green,e_blue = int_to_bin(encrypt_img_pixels[ei,ej])
    red_b = re.findall('..',e_red)
    green_b = re.findall('..',e_green)
    blue_b = re.findall('..',e_blue)
    for count in range(4):
        di,dj=embebding(di,dj,count,red_b,green_b,blue_b)
        dj+=1
        if (dj == cover_col):
            dj=0
            di+=1
cover_image.save("./embed_cover.png")
print("Finish embemd encrypted picture to cover picture...")
print("============================")
####################################################################################################################################
#Step B: De-embedding image

embeded_image=Image.open("embed_cover.png")
embeded_image_pixels = embeded_image.load()
embeded_image_row,embeded_image_col=embeded_image.size

dei,dej=0,0
def de_embebed(dei,dej):
    dej_red,dej_green,dej_blue = int_to_bin(embeded_image_pixels[dei,dej])
    dej_red = dej_red[6:8]
    dej_green = dej_green[6:8]
    dej_blue = dej_blue[6:8]
    return dei, dej, dej_red, dej_green, dej_blue

new_image = Image.new(encrypt_img.mode, encrypt_img.size)
pixels_new = new_image.load()
new_image_row,new_image_col=new_image.size

for ni in range(new_image_row):
    for nj in range(new_image_col):
        dei_red,dei_green,dei_blue="","",""
        for count in range(4):
            dei,dej,dei_red_b,dei_green_b,dei_blue_b=de_embebed(dei,dej)
            dei_red+=dei_red_b
            dei_green+=dei_green_b
            dei_blue+=dei_blue_b
            dej+=1
            if (dej == embeded_image_col):
                dej=0
                dei+=1
        rgb=(dei_red,dei_green,dei_blue)
        dei_red,dei_green,dei_blue = bin_to_int(rgb)
        pixels_new[ni,nj]=(dei_red,dei_green,dei_blue)

new_image.save("./de_embebed.png")



####################################################################################################################################
#Step 6: Decryption
decrypted_image=Image.open("de_embebed.png")
decrypted_image_pixels = decrypted_image.load()
decrypted_image_row,decrypted_image_col=decrypted_image.size

print("Decrypting picture with RSA private key (d:",D,"n:",N,")...")
for i in range(decrypted_image_row):
  for j in range(decrypted_image_col):
    red,green,blue =enc[i][j]
    M1=power(red,D,N)
    M2=power(green,D,N)
    M3=power(blue,D,N)
    decrypted_image_pixels[i,j]=(M1,M2,M3)

decrypted_image.save("./rsa_decrypt_output.png")
print("RSA_decrypted picture complete, save at ./rsa_decrypt_output.png")
