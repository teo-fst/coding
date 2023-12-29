import itertools 
students = ["John", "Alex", "Jo"]
books = ["Math", "Science"]
studentsId = [1,2,3]

for s,b,i in zip(students, books, studentsId): 
    print(s, b, i)