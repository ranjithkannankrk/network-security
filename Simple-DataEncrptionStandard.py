import time

#---------------------------------------------------------------
#1. Code for SDES starts here

def perm8(listname, arr):
        result = []
        for i in arr:
                result.append(listname[i])
        return result

def exor(L,R):
	result = []
	j = len(L)-1
	for i in range(0, len(L)):
		result.append(int(L[j])^int(R[j]))
		j = j - 1
	return result[::-1]
	
def keyAlgo(K,n):
        for i in range(0,n):
                K1 = K[0:5]
                K2 = K[5:10]
                K1.insert(4,K1.pop(0))
                K2.insert(4,K2.pop(0))
                K = K1 + K2
                
        result_K = perm8(K,[5,2,6,3,7,4,9,8])
        return result_K
		 
def cipher(R,K):
        m = perm8( R,[3,0,1,2,1,2,3,0])
        eResult = exor(m,K)
        B_1 = eResult[0:4]
        B_2 = eResult[4:8]
        S_1 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
        s_2 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
        temp_s1r = int(str(B_1[0])+str(B_1[3]),2)
        temp_s1c = int(str(B_1[1])+str(B_1[2]),2)
        S1 = S_1[temp_s1r][temp_s1c]
        temp_s2r = int(str(B_2[0])+str(B_2[3]),2)
        temp_s2c = int(str(B_2[1])+str(B_2[2]),2)
        S2 = s_2[temp_s2r][temp_s2c]
        S1 = list(format(S1,"#02b")[2:])
        S2 = list(format(S2,"#02b")[2:])
        if len(S1) == 1:
                S1.insert(0,0)
        if len(S2) == 1:
                S2.insert(0,0)
        P_temp = S1 + S2
        P = perm8(P_temp,[1,3,2,0])
        return P

def s_des(L,R,K):
        operate = cipher(R,K)
        L = exor(L,operate)
        return L, R

def encipher(ip,key1,key2):
        ip = perm8(ip,[1,5,2,0,3,7,4,6])
        L = ip[0:4]
        R = ip[4:8]
        R,L = s_des(L,R,key1)
        R,L = s_des(L,R,key2)
        result = R + L
        output = perm8(result,[3,0,2,4,6,1,7,5])
        return output
# 1. Code for SDES ends here
#---------------------------------------------------------------

def bruteForce(keys1,plain,cipher):
        keyset = []
        for i in keys1:
                K1 = i[0]
                K2 = i[1]
                K1 = perm8(K1,[2,4,1,6,3,9,0,8,7,5])
                K2 = perm8(K2,[2,4,1,6,3,9,0,8,7,5])
                key1_c = keyAlgo(K1,1)
                key2_c = keyAlgo(K1,3)
                output_cipher = encipher(plain,key1_c,key2_c)
                key1_c = keyAlgo(K2,1)
                key2_c = keyAlgo(K2,3)
                output_cipher2 = encipher(output_cipher,key1_c,key2_c)
                if cipher == output_cipher2:
                        keyset.append(i)
        return keyset


perumutation = [2,4,1,6,3,9,0,8,7,5]

#---------------------------------------------------------------
# code to collect all the keys
# Starts here
a = '0000000000'
b = '0000000001'

allKeys = []
allKeys.append([0,0,0,0,0,0,0,0,0,0])

for i in range(1,2**10):
        c = list(bin(int(a,2)+int(b,2))[2:])
        if len(c) < 10:
                for j in range(0,10 - len(c)):
                        c.insert(j,"0")
        a = "".join(c)
        m = list(a)
        res = []
        for k in m:
                res.append(int(k))
        allKeys.append(res)

allKeys.append(res)
# Ends here
#---------------------------------------------------------------

#---------------------------------------------------------------
# 3. code to find the keys using meet in the middle attack
# Starts here
timeStart = time.time()

input_c = [0,1,1,0,1,0,1,1]
inputList_d = [1,1,0,0,1,0,0,0]
allCipher = []
for key1 in allKeys:
        keyset = perm8(key1,perumutation)
        key1_c = keyAlgo(keyset,1)
        key2_c = keyAlgo(keyset,3)
        output = encipher(input_c,key1_c,key2_c)
        allCipher.append(output)

ks = []
count = 0
allDecipher = []
for key2 in allKeys:
        keyset = perm8(key2,perumutation)
        key1_c = keyAlgo(keyset,1)
        key2_c = keyAlgo(keyset,3)
        output = encipher(inputList_d,key2_c,key1_c)
        allDecipher.append(output)

count = 0
for m,i in enumerate(allCipher):
        for n,j in enumerate (allDecipher):
                if i == j:
                        ks.append([allKeys[m],allKeys[n]])
                        
PT = [[1,0,0,1,0,1,1,0],[0,0,1,0,1,0,1,1],[1,0,1,0,1,0,1,0],[0,0,0,1,1,1,0,0]]
CT = [[0,0,0,0,0,1,1,1],[0,0,0,1,0,0,1,0],[1,0,0,1,1,0,1,1],[1,0,1,0,0,0,0,0]]


for m,i in enumerate(PT):
        ks = bruteForce(ks,i,CT[m])



timeEnd = time.time()
totalTime = timeEnd - timeStart


K1 = ""
for i in ks[0][0]:
        K1 = K1 + str(i)
K2 = ""
for j in ks[0][1]:
        K2 = K2 + str(j)
        
print("2. The keys found using MTIM attack are ",K1," and ",K2)
print("2. The keys in hex format are 0x2E9 and 0x1DA")
print("3. Total time taken for MITM attack",totalTime)

#3. Ends here
#---------------------------------------------------------------

#---------------------------------------------------------------
# 4. code to find the keys using brute force
# 4. Starts here
timeStart = time.time()

input_c = [0,1,1,0,1,0,1,1]
inputList_d = [1,1,0,0,1,0,0,0]
keys = []
for ki1 in allKeys:
        keyset_c = perm8(ki1,perumutation)
        key1_c = keyAlgo(keyset_c,1)
        key2_c = keyAlgo(keyset_c,3)
        output_cipher = encipher(input_c,key1_c,key2_c)
        for ki2 in allKeys:
                keyset_c = perm8(ki2,perumutation)
                key1_c = keyAlgo(keyset_c,1)
                key2_c = keyAlgo(keyset_c,3)
                output_cipher2 = encipher(output_cipher,key1_c,key2_c)
                if output_cipher2 == inputList_d:
                        keys.append([ki1,ki2])

PT = [[1,0,0,1,0,1,1,0],[0,0,1,0,1,0,1,1],[1,0,1,0,1,0,1,0],[0,0,0,1,1,1,0,0]]
CT = [[0,0,0,0,0,1,1,1],[0,0,0,1,0,0,1,0],[1,0,0,1,1,0,1,1],[1,0,1,0,0,0,0,0]]

for m,i in enumerate(PT):
        keys = bruteForce(keys,i,CT[m])

timeEnd = time.time()
totalTime = timeEnd - timeStart

K1 = ""
for i in keys[0][0]:
        K1 = K1 + str(i)
K2 = ""
for j in keys[0][1]:
        K2 = K2 + str(j)

print("4. total time taken for brute force",totalTime)
print("4. The keys found using MTIM attack are ",K1," and ",K2)
print("4. The keys in hex format are 0x2E9 and 0x1DA")

# 4. Ends here
#---------------------------------------------------------------
        
#---------------------------------------------------------------
# 5. Code to deciper the text using the CBC mode
# 5. Starts here

ip_cbc = '1101000001100110100110011100001101010010001110000111010100001011111101101110101111010001101100110011111100101000111010100001001100101101110100101100101100100011011101010000101101110010011010111100000110000001111110101100010100110001010110100110101001000000'
ip_cbc = list(ip_cbc)
input_cbc = []
ip = []
for i, j in enumerate(ip_cbc):
        ip.append(int(j))
        if len(ip) == 8:
                input_cbc.append(ip)
                ip = []
                
K1 = keys[0][0]
K2 = keys[0][1]
K1 = perm8(K1,perumutation)
K2 = perm8(K2,perumutation)
key1 = keyAlgo(K1,1)
key2 = keyAlgo(K1,3)
key3 = keyAlgo(K2,1)
key4 = keyAlgo(K2,3)

pt_cbc = []
IV = [1,0,0,1,1,1,0,0]
for i in input_cbc:
        output = encipher(i,key4,key3)
        output3 = encipher(output,key2,key1)
        pt = exor(IV,output3)
        pt_cbc.append(pt)
        IV = i

binary_format = ""
for i in pt_cbc:
        for j in i:
                binary_format = binary_format + str(j)
                

print("5. the deciphered text in binary format is ", binary_format)
print("5. the deciphered text in hex format is 0x436F6E67726174756C6174696F6E73206F6E20796F7572207375636365737321")

# 5. Ends Here
#---------------------------------------------------------------


#---------------------------------------------------------------
# 6. Starts here
print("6. List of weak keys are as follows")
print(" (i) 0000000000 (ii) 1111111111 (iii) 0101010101 (iv) 1010101010 ")
print(" weak keys in hex format")
print(" (i) 0x00 (ii) 0x3FF (iii) 0x155 (iv) 0x2AA ")
# 6. Ends here
#---------------------------------------------------------------




