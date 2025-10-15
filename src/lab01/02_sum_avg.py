a = input("a: ")
b = input("b: ")
if a.count(",")==1:
    a = a.replace(",",".")
if b.count(",")==1:
    b = b.replace(",",".")
a1 = float(a)
b1 = float(b)
summ = a1+b1
avg = summ/2
print("sum =",f"{summ:.2f};","avg =",f"{avg:.2f}")