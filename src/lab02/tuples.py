rec1 = ("Иванов Иван Иванович", "BIVT-25", 4.6)
rec2 = ("Петров Пётр", "IKBO-12", 5.0)
rec3 = ("Петров Пётр Петрович", "IKBO-12", 5.0)
rec4 = (" сидорова анна сергеевна ", "ABB-01", 3.999)
rec5 = ("", "ABB-01", 3.999)


def fio(rec):
    part = rec[0].split()
    if not part:
        raise ValueError("FIO is empty")
    init = "".join(l[0].upper() for l in part[1:])
    surn = part[0][0].upper() + part[0][1:]
    return f"{surn} {'.'.join(init)}."


def gpa(rec):
    gp = rec[2]
    if not gp:
        raise ValueError("GPA is empty")
    else:
        return round(rec[2], 2)


def formatRec(rec):
    if len(rec) != 3:
        raise ValueError("Wrong data")
    else:
        name = fio(rec)
        gr = rec[1]
        if not gr:
            raise ValueError("Group is empty")
        gp = gpa(rec)
        print(f"{name}, гр. {gr}, GPA: {gp}")


formatRec(rec1)
formatRec(rec2)
formatRec(rec3)
formatRec(rec4)
formatRec(rec5)
