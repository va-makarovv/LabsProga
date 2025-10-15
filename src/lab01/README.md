# Лабораторная работа 1
## №1
```python
name = str(input("Имя: "))
age = int(input("Возраст: ")) + 1

print("Привет, " + name + "! Через год тебе будет " + str(age))
```
![](/images/lab01/n1.png)

## №2
```python
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
```

![](/images/lab01/n2.png)

## №3
```python
price = float(input("Price: "))
discount = float(input("Discount: "))
vat = float(input("Vat: "))
base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
print("База после скидки:", f"{base:.2f}","₽")
print("НДС:",f"{vat_amount:.2f}","₽")
print("Итого к оплате:",f"{total:.2f}","₽")
```

![](/images/lab01/n3.png)

## №4
```python
min = int(input("Минуты: "))
hours = min//60
minutes = min%60
print(f"{hours:02d}:{minutes:02d}")
```

![](/images/lab01/n4.png)

## №5
```python
full_name = input("ФИО: ")
words = full_name.strip().split()
cleanwords = " ".join(words)
initials = ''.join(word[0].upper() for word in words) + '.'

print("Инициалы:",initials)
print("Длина (символов):", len(cleanwords))
```

![](/images/lab01/n5.png)
