full_name = input("ФИО: ")
words = full_name.strip().split()
cleanwords = " ".join(words)
initials = '.'.join(word[0].upper() for word in words) + '.'

print("Инициалы:",initials)
print("Длина (символов):", len(cleanwords))