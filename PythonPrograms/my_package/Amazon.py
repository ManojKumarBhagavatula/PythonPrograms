def getOutlierValue(arr):
   
    sum_arr = sum(arr) 
    outliers = [] 
    for i in range(len(arr)): 
        rem_sum = sum_arr - arr[i] 
        if arr[i] not in arr[:i] + arr[i+1:] and arr[i] != rem_sum:
            outliers.append(arr[i]) 
    return max(outliers)