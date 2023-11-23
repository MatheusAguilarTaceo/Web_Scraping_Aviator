A = [90 , 10, 10, 10, 50, 60,70]
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