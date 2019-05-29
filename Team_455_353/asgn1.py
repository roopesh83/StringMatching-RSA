#!/usr/bin/env python
# coding: utf-8

'''
Problem:
 a) Implement Rabin-Karp string matcher for Text search with alphabet {a-z, A-Z, 0-9}
 b) Implement RSA-Encryption with 32-bit Primes for encoding consisting of a
 19-digit number , composed from 16-digit Credit card number + 3-digit CVV.
Data :
 a) Any Text File with atleast Size n = 100,000 character from the specified alphabet
 b) Use any 19 digit number !!!
Interface Support
 a) >>> RK -t TxtFile -o OutPutFile
 b) >>> RSA -i inputFile -o OutPutFile
Demo:
 a) Your program should take a Pattern ( may be up to 1000Char long) entered from the
 keyboard and write out the VALID Shifts to the specified output file. You should be able to
 confirm your result either with Naive String Matcher or a Python Lib function
 b) Your Program Should take the input file consisting of 19-digit numbers and produce an
 encrypted number file
 You should be able to confirm your Encryption with Decryption to produce the Input file
 ( This means you should produce the Public and Private Keys First and store them !!)
Report:
 – Should contain your design and implementation details
 – Timings for various size Patterns and Timings for Encryption and Decryption
Last para of your report should contain your observations on the Learning Outcomes of this project.
'''


import time
from Crypto.Util import number



d = 256
start_time = 0
stop_time = 0
silent = False

def search(P, T, q):   #pattern, text and prime number
    global start_time
    global stop_time
    M = len(P) 
    N = len(T) 
    i = 0
    j = 0
    p = 0  
    t = 0 
    h = 1
    listValidShifts = []


    #for i in range(M-1): 
        #h = (h * d)% q   #(d^m-1)%q
    start_time = time.time()
    for i in range(M): 
        p = (d * p + ord(P[i]))% q   #ascii equivalent of characters
        t = (d * t + ord(T[i]))% q 
        if(i < M-1):
            h = (h * d)% q

    for i in range(N-M + 1): 
        if p == t:   #could be spurious hit, so check for matching
            for j in range(M): 
                if T[i + j] != P[j]: 
                    break
            j+= 1
            if j == M:
                listValidShifts.append(i)
                if not silent:
                    print("Pattern P found at index " + str(i)) 

        if i < N-M: 
            t = (d*(t-ord(T[i])*h) + ord(T[i + M]))% q
            #to handle negative values of t
            if t < 0: 
                t = t + q
    stop_time = time.time()
    return listValidShifts


# In[26]:


def readText(fileName = 'C:\\Users\\dell\\Documents\\Assignments 2nd semester\\AA\\sample.txt'): #keyword arg with default value
    '''returns text read from file'''
    while True:
        try:
            with open(fileName) as file:
                text = file.read()
                file.close()
                break
        except FileNotFoundError:
            print('File {} not found'.format(fileName))
            fileName = input('re-enter the filename :-')
    return text

def writeText(pattern, listValidShifts, fileName = 'C:\\Users\\dell\\Documents\\Assignments 2nd semester\\AA\\validShifts.txt'):
    print('Number of valid shifts for pattern {} '.format(len(listValidShifts)))
    with open(fileName, 'w') as file:
        file.write('Valid shifts for pattern \'{}\'\n'.format(pattern))
        for i in listValidShifts:
            file.write('{}\t'.format(i))
        file.close()
    print('list of valid shifts written to \'{}\'\n'.format(fileName))




def naiveStringMatcher(text, pattern, outputFileName):
    global start_time
    global stop_time
    start_time = time.time()
    
    listOfValidShifts = []
    
    n = len(text)
    m = len(pattern)
    for i in range(n - m):
        if(text[i: i + m] == pattern):
            listOfValidShifts.append(i)
    
    listOfValidShifts_str = str(listOfValidShifts)
    listOfValidShifts_str = listOfValidShifts_str.strip('[')
    listOfValidShifts_str = listOfValidShifts_str.strip(']')
    if not silent:
        print('list of valid shifts is {}\n'.format(listOfValidShifts_str))
    writeText(pattern = pattern, listValidShifts = listOfValidShifts, fileName=outputFileName)
    stop_time = time.time()
    print('time taken for naive string matching is {} second'.format(stop_time - start_time))       



def getPrime32():
    return number.getPrime(32)


p = getPrime32()    #53
q = getPrime32()  #59
n = p * q


# In[45]:


phi = (p - 1)*(q - 1)


# In[38]:


# Extended Euclidean Algorithm 



def extended_gcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)


def mulinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = extended_gcd(a, b)
    if g == 1:
        return x % b

a = 35
b = 15



for i in range(3, n, 2):
    gcd = extended_gcd(i, phi)[0]
    if( (gcd == 1) and (i % 2 != 0) ):
        e = i
        break


# In[44]:


#print('e is {}'.format(e))
# e*d -eq (1 mod phi(n)) i.e. d is multiplicative modular inverse of e wrt. phi(n)

# In[60]:


d = mulinv(e, phi)


# pow(2121212102121212101, e, n)

# pow(pow(89, e, n), d, n)

# In[86]:


def encrypt(m):
    return pow(m, e, n)
def decrypt(c):
    return pow(c, d, n)


# encrypt(89)

# decrypt(1394)

# In[94]:


def creditCardNumber_str(listOfAscii):
    '''returns string from a sequence of ascii chars'''
    str1 = ''
    for x in listOfAscii:
        str1 += chr(x)
    return str1


# In[83]:


def ascii_list(str1):
    return [ord(x) for x in str1]


# ascii_list('a')

# lst

# creditCardNumber_str(lst)

# In[177]:


def encryptCreditCard(credit_card_string):
    listOfAscii = ascii_list(credit_card_string)
#     print(listOfAscii)
    listOfEncryptedAscii = [encrypt(x) for x in listOfAscii]
#     print(listOfEncryptedAscii)
    return listOfEncryptedAscii


# In[98]:


# credit_card_string = '2121212102121212101'
# cipherText = encryptCreditCard(credit_card_string)


# In[160]:


def decryptCreditCard(encryptedCreditCard):
    listOfDecryptedAscii = [decrypt(x) for x in encryptedCreditCard]
#     print(creditCardNumber_str(listOfDecryptedAscii))
    return (creditCardNumber_str(listOfDecryptedAscii))


# In[102]:


# decryptCreditCard(cipherText)


# In[105]:





# In[174]:


def writeCipherTextToFile(firstLine, cipherText, filename = 'outputFile.txt'):
    '''accepts cipher text chars as list and writes them to file'''
    with open(filename, 'a+') as file:
        str1 = str(cipherText)
        str1 = str1.replace('[', '')
        str1 = str1.replace(']', '')
        str1 = str1.replace(',', '')
        if firstLine:
            file.write(str1)
        else:
            file.write('\n' + str1)
        file.close()
    


# In[ ]:


# def write


# In[123]:


# writeCipherTextToFile(cipherText)


# In[110]:


# str1


# In[126]:


import numpy as np


# In[143]:


def generateRandomCreditCard():
    a = ''
    while len(a) < 19:
        a += str(np.random.randint(0, 123456789))
    a = a[0:19]
    return a
    # print(a)
    # print(len(a))


# In[ ]:





# # to generate 1000 random credit card numbers in inputFile.txt

# In[167]:


def generateRandomCreditCardNumbers(n, fileName = 'inputFile.txt'):
    '''accepts n, and generates n random credit card numbers'''
    with open(fileName, 'w') as file:
        for i in range(n):
            file.write(generateRandomCreditCard())
            if (i < n - 1):
                file.write('\n')
                
        file.close()
    print('Random numbers generated')
        


# In[163]:


# generateRandomCreditCardNumbers(50)


# # to generate ciphertext and store them in outputfile.txt

# In[175]:


def rsa_encryption(inputFilename = 'inputFile.txt', outputFilename = 'outputFile.txt'):
    global start_time
    global stop_time
    try:
        with open(outputFilename, 'w') as file1: # clearing the file contents
            file1.close()
    except FileNotFoundError:
        print('File {} not found '.format(inputFilename))
        inputFilename = input('Please re-enter the input filename:- ')
    
    firstLine = True
    
    while True:
        try:
            with open(inputFilename, 'r') as file:
                line = file.readline()
                line = line.strip('\n')
                start_time = time.time()
                while(line):                      
                    writeCipherTextToFile(firstLine, encryptCreditCard(line), outputFilename)
                    firstLine = False
                    line = file.readline()
                    line = line.strip('\n')
                stop_time = time.time()
                file.close()
                print('cipher text written to {}'.format(outputFilename))
                break
        except FileNotFoundError:
            print('File {} not found '.format(inputFilename))
            inputFilename = input('Please re-enter the input filename:- ')
            


# # to read encrypted characters from outputfile.txt and decrypt them, and store the decrypted characters to outputFileConfirm.txt

# In[172]:


def rsa_decryption(inputFilename = 'outputFile.txt', outputFilename = 'outputFileConfirm.txt'):    
    '''here outputFilename consists of ciphertext
    outputFilename corresponds to a file same as plaintext file
    '''   
    global start_time
    global stop_time
    while True:    
        try:
            with open(inputFilename, 'r') as file:
                start_time = time.time()
                line = file.readline()
                line = line.strip('\n')
                with open(outputFilename, 'w') as file1:
                    while(line):
        #                print(line)
                        creditcard_encrypted_chars = line.split(' ')
                        creditcard_encrypted_chars = [int(x) for x in creditcard_encrypted_chars]
    #                   print(decryptCreditCard(creditcard_encrypted_chars))
                        file1.write(decryptCreditCard(creditcard_encrypted_chars) + '\n')
                        line = file.readline()
                        line = line.strip('\n')
                    file1.close()
                file.close()
                print('decrypted msg stored in {}'.format(outputFilename))
                stop_time = time.time()
                break
        except FileNotFoundError:
            print('File {} not found'.format(inputFilename))
            inputFilename = input('Please re-enter the input filename:- ')
    
    


# In[179]:
            
def timeTaken():
    print('time taken is {} second'.format(stop_time - start_time))
           
            

print('Usage: RK/RSAe/RSAd/gen/naive_sm -i/-c <inputfilename/n> -o <outputfilename>')
cmd = ''
cmd = input('>>')
while cmd != 'exit':
    cmd = cmd.split(' ')
    #print(len(cmd))
    if cmd[0] == 'exit':
        break
    elif len(cmd) != 5:
        if cmd[0] == 'silent':
            print('silent is {}, changed to {}'.format(silent, not silent))
            silent = not silent
        elif cmd[0] == 'params':
            print('Prime numbers are (p, q) = ({}, {}), n is {}, phi is {}, e is {}, d is {}'.format(p, q, n, phi, e, d))
        else:
            print('Usage: RK/RSAe/RSAd/gen -i/-c <inputfilename/n> -o <outputfilename>')
            print('invalid input')
    else:
        if(cmd[0] in ['RK', 'RSAe', 'RSAd', 'gen', 'naive_sm']):
            if(cmd[0] == 'RK'):
                if(cmd[1] in ['-t', '-i']):
                    if(cmd[3] == '-o'):
                        textFile = readText(cmd[2])
                        P = input('Enter the pattern:- ')
                        q = 101 # A prime number 
                        writeText(pattern = P, listValidShifts = search(P = P, T = textFile, q = 101), fileName=cmd[4])
                        timeTaken()
                    else:
                        print('-o missing')
                else:
                    print('Expected args -t/-i')
            elif cmd[0] == 'RSAe':
                if(cmd[1] in ['-i']):
                    if(cmd[3] == '-o'):
                        rsa_encryption(inputFilename = cmd[2], outputFilename=cmd[4])
                        timeTaken()
                    else:
                        print('-o missing')
                else:
                    print('Expected args -t/-i')
            elif cmd[0] == 'RSAd':
                if(cmd[1] in ['-i']):
                    if(cmd[3] == '-o'):
                        rsa_decryption(inputFilename = cmd[2], outputFilename=cmd[4])
                        timeTaken()
                    else:
                        print('-o missing')
                else:
                    print('Expected args -t/-i')
            elif cmd[0] == 'gen':
                if(cmd[1] in ['-c']):
                    if(cmd[3] == '-o'):
                        generateRandomCreditCardNumbers(n = int(cmd[2]), fileName=cmd[4])
                    else:
                        print('-o missing')
                else:
                    print('Expected args -t/-i')
            elif (cmd[0] == 'naive_sm' ):
                naiveStringMatcher(readText(cmd[2]), input('Enter pattern:- '), outputFileName=cmd[4])
                
        else:
            print('Inavlid input :expected RK/RSA')
    cmd = input('>>')
    





