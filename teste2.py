A = [0]

B = [90, 20, 40, 90 , 10, 10, 10]
# B = []
# B = [40, 90 , 10, 10, 10, 10, 10, 20 , 30, 40, 50, 60, 70, 80, 90, 100 ]
# B = [40, 90 , 100, 10, 20 , 30, 40, 50, 60, 70, 80, 90, 100 ]

# A = [10, 20 , 30, 40, 50, 60,70]
# B = [80, 10, 20 , 30, 40, 50, 60]


C = []
for i in range(len(A)):
    for j in range(len(B)):
        if(A[i] == B[j]):
            try:    
                if(A[i+1] == B[j+1] and A[i+2] == B[j+2]):
                    break
            except:
                break    
        C.append(B[j])
    else:
        continue
    break

print(C)
A = [90, 20, 40, 90 , 10, 10, 10]
B = [90, 55 , 90, 20, 40, 90 , 10]

C =[]
for i in range(len(A)):
    for j in range(len(B)):
        if(A[i] == B[j]):
            try:    
                if(A[i+1] == B[j+1] and A[i+2] == B[j+2]):
                    break
            except:
                break    
        C.append(B[j])
    else:
        continue
    break

print(C)

import datetime
import pytz
day = datetime.datetime.now().strftime('%Y-%m-%d')
print(day)
hour = '17:59:30'
date = f'{day} {hour}'
print(date)
date =  datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').astimezone()
print(date)
date = date.astimezone(pytz.timezone('UTC'))
print(date)
date = f"'{date.strftime('%Y-%m-%d %H:%M:%S')}'"
print(date)


previous = ['10']
next = [10]

if(previous[0] == next[0]):
    print('SIM')
else:
    print('Não')    


STR = '2022-11-23'
STR = f" '{STR}' "
FRASE = f"HOJE {STR}"

print(FRASE)

STR = 'UTC_TIMESTAMP'

FRASE = f"HOJE {STR}"
print(FRASE)
