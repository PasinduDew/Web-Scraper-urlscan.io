temp = {1, 2, 3, 4, 5, 6, 7, 8}

print(temp)

y = list(temp)
print(len(temp))
x = y[2:]
s = set(x)

print(s)
print(len(s))


from datetime import datetime

now = datetime.now()
dateStr = now.strftime("%Y%m%d")
dateStr_1 = now.strftime("%Y%b%d")

print(dateStr)
print(dateStr_1)




