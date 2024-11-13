def TableSwitch(A, B, n, m):
    Ai = 0
    Bi = 0
    switch = 0
    prevA = -1
    prevB = -1
    
    while Ai < n and Bi < m:
        if A[Ai] < B[Bi]:
            if prevA != Ai:
                switch += 1
            Ai += 1
            prevA = Ai
        elif B[Bi] < A[Ai]:
            if prevB != Bi:
                switch += 1
            Bi += 1
            prevB = Bi
    
   
    
    return switch

n = int(input("Enter the size of A: "))
m = int(input("Enter the size of B: "))
a_arr = list(map(int, input("Enter A (with spaces): ").split()))
b_arr = list(map(int, input("Enter B (with spaces): ").split()))

if a_arr[0] < b_arr[0]:
    res = TableSwitch(a_arr, b_arr, n, m)
else:
    res = TableSwitch(b_arr, a_arr, m, n)

print("Number of Switches:", res)
