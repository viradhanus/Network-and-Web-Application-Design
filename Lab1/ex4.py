from dataclasses import dataclass
from typing import List, Dict
from dataclasses import asdict
import json
from json import dumps

@dataclass

class Student:

    """A student's course registration details"""

    given_name: str

    surname: str

    registered_courses: List[str]

#------------1st method--------------------------------------------

def load_course_registrations(filename: str) -> List[Student]:

    """ Returns a list of Student objects read from filename"""

    student_obj = list()

    with open(filename) as f:

        for line in f:
            line = line.strip() #removes \n character from right
            stu_details = line.split(',')   #split the csv

            fname = stu_details[0]
            lname = stu_details[1]
            course_list = stu_details[2:len(stu_details)]

            student_obj.append(Student(fname,lname,course_list))    #append to the student object list

    return student_obj

# Read the file into a list of Student objects using the above definition.
stu_list = load_course_registrations('stu_details.txt')

# c. Use `map` function to apply asdict() to a list of Student objects.
stu_data =  map(asdict, stu_list)

converted_list = list(stu_data)
print(converted_list)

# d. write the output to a file named student_registrations.json.
with open('student_registrations.json','w') as write_file: 
    json.dump(converted_list , write_file)


"""
------------2nd method--------------------------------------------

s1 = Student("Saman","Silva",["CO324","CO321","CO325"]) #student obj s1
s2 = Student("Viraj","Perera",["CO334","CO321","CO329"]) #student obj s2
s3 = Student("Ashan","Thilakarathna",["CO334","CO325","CO329"]) #student obj s3

dumps(asdict(s1))   #serialize student obj s1
dumps(asdict(s2))   #serialize student obj s2
dumps(asdict(s3))   #serialize student obj s3

Students = []   #list to hold student objects

Students.append(s1) #append s1 to Students list
Students.append(s2) #append s2 to Students list

# c. Use `map` function to apply asdict() to a list of Student objects.
result = map(asdict, Students) 

converted_list = list(result)
print(converted_list)

# d. write the output to a file named student_registrations.json.
with open('student_registrations.json','w') as write_file: 
    json.dump(converted_list , write_file)

"""


