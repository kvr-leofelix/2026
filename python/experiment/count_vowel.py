a=input("enter the word to check")
vowel="aeiou"
count=0
for i in a:
    if i in vowel:
        count+=1
print(count)

# ------------
b=input("enter the word")
print(sum(ch in "aeiou" for ch in b))