from ex1 import student_list

sorted_student_list = sorted(student_list, key = lambda s: s.surname + s.given_name)
print("Sorted student list by surname and given name :")
print("")
print(sorted_student_list)
print("\n")

# How would you sort students by the number of courses that they are registered for?
sorted_student_list_course = sorted(student_list, key = lambda s: len(s.registered_courses))
print("Sorted student list by number of courses that they are registered :")
print("")
print(sorted_student_list_course)