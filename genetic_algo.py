'''
ma hoa mat khau
'''
import random
import string
alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP"\
"QRSTUVWXYZ 1234567890, .-;:_!\"#%&/()=?@${[]}" # Các ký tự hợp lệ

pas = "le@rn a1g0ri7ths f ewou oei@@@@qwur ueqwoiru jnqmw,enr qm,wr v1th 3xp3rt5"
len1 = len(pas)
random.seed()
def dis(a, pas):
    res = 0
    for i in range(len1):
        res = res + (pas[i]==a[i])
    return res
def cmp(a):
    return dis(a,pas)

# tao quan the ban dau
sz = 1000 # kich thuoc quan the
gen = []
for i in range(sz):
    gen.append(''.join(random.choices(alpha,k=len1)))
time = 0
while True:
    gen.sort(reverse=True,key=cmp)
    time = time + 1
    sz = len(gen) # kich thuoc quan the 
    if(gen[0]==pas):
        break
    #print(sz)
    szn = 20
    print(dis(gen[0],pas)/len1*100)
    ngen = []
    for i in range(szn):
        for j in range(szn):
            if(j==i):
                continue
            ngen.append(gen[i][:(len1//2)] + gen[j][(len1//2):])
    #print(ngen[0])
    for i in range(len(ngen)):
        strk = list(ngen[i])
        #print(type(strk))
        for j in range(len1):
            rd = random.random()
            if(rd<0.05):
                strk[j] = random.choice(alpha)
        ngen.append(''.join(strk))
    for i in range(sz-len(ngen)):
        strk = list(gen[i+szn])
        #print(type(strk))
        for j in range(len1):
            rd = random.random()
            if(rd<0.15):
                strk[j] = random.choice(alpha)
        ngen.append(''.join(strk))
    gen = ngen
print(time)