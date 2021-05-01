from dataclasses import dataclass

from typing import List, Dict


@dataclass

class Student:

    """A student's course registration details"""

    given_name: str

    surname: str

    registered_courses: List[str]


def load_course_registrations(filename: str) -> List[Student]:

    """ Returns a list of Student objects read from filename"""

    student_obj = {}    # define Student object dictionary

    with open(filename) as f:

        for line in f:
            line = line.strip() #removes \n character from right
            stu_details = line.split(',')   #split the csv

            fname = stu_details[0]
            lname = stu_details[1]
            course_list = stu_details[2:len(stu_details)]

            # Store Student objects in a dictionary using a tuple (surname, given_name) as the key
            student_obj[(fname,lname)] = Student(fname,lname,course_list)   

    return student_obj

# Read the file into a list of Student objects using the above definition.
student_obj_dict = load_course_registrations('stu_details.txt')
print(student_obj_dict)