def insert_student(name : str, math : int, eng : int):

    print("Name: ", name)

    if type(math) == int and type(eng) == int:
        total = math + eng
        print("Total marks: ", total)
    else:
        print("Wrong data type inserted!!!")

insert_student('Munim', '34', '78')
insert_student('Rahim', 45, 60)