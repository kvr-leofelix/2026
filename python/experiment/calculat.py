try:
    a=int(input("enter the first number"))
    b=int(input("enter the second number"))
    print("choose among these",
          "1:add\n",
          "2:sub\n",
          "3:mul\n",
          "4:div\n")
    cal=input().strip().lower()
    if cal=="add":
        ans=a+b
    elif cal=="sub":
        ans=a-b
    elif cal=="div":
        if b==0:
            print("error can't divide by 0")
            ans =None
        else:
            ans=a/b
    else:
        print("invalid operator")
        ans=None







except ValueError:
    print("invalid error")