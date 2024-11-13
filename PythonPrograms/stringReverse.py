def isPalindrome(s,left, right, count):
    if s[left] != s[right]:return False
    if count == len(s)-1:return True
    return isPalindrome(s, left+1, right-1, count+1)

s = input("Enter any string : ")
print(isPalindrome(s=s,left=0, right=len(s)-1, count=0))