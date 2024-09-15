# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   Sohail Nassiri,09/09/2024,Created Script
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "enrollments.json"  # Set the json file name

# Define the Data Variables
students: list = []  # Table of student data
menu_choice: str = ''  # Hold the choice made by the user


class Person:
    """
    A class representing person data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.

    ChangeLog:
        - Sohail Nassiri, 09.09.2024: Created the class.
    """

    # Constructor with private attributes for the first_name and last_name data
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    #  Property getter and setter for first name using the same code as in the Student class
    @property  # Decorator for the getter or accessor
    def first_name(self):
        return self.__first_name.title()  # Formatting code

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha() or value == "":  # Is character or empty string
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    # Property getter and setter for last name using the same code as in the Student class
    @property
    def last_name(self):
        return self.__last_name.title()  # Formatting code

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha() or value == "":  # Is character or empty string
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    #  Override the default __str__() method's behavior and return a coma-separated string of data
    def __str__(self):
        return f'{self.first_name},{self.last_name}'


#  Student class which will inherit code from the person class
class Student(Person):
    """
    A class representing student data.

    Properties:
        first_name (str): The student's first name.
        last_name (str): The student's last name.
        course_name (str): The course name that the student is registered for.

    ChangeLog: (Who, When, What)
    Sohail Nassiri,09.09.2024,Created Class, added properties, private attributes, moved first_name and last_name into a
    parent class
    """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        #  Passing the parameter data to the Person "super" class
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    #  Assignment to the course_name property using the course_name parameter
    @property
    def course_name(self):
        return self.__course_name

    #  Getter and setter for course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    #  Overriding the __str__() method to return the student data
    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'


# Processing --------------------------------------- #
class FileProcessor:
    """
        A collection of processing layer functions that work with json files

    ChangeLog: (Who, When, What)
    Sohail Nassiri,09.09.2024,Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file into a list of dictionary rows

        Note:
        - Data sent to the student_data parameter will be overwritten.

        ChangeLog: (Who, When, What)
        Sohail Nassiri,09.09.2024,Created function

        :param file_name: string with the name of the file we are reading
        :param student_data: list of dictionary rows we are adding data to
        :return: list of dictionary rows filled with data
        """

        try:
            file = open(file_name, "r")
            list_of_dictionary_data = json.load(file)
            for student in list_of_dictionary_data:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_data.append(student_object)

            file.close()
        except FileNotFoundError as e:  # Raises exception if file is not found
            # Sending error messages to a function in IO
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:  # Raises any other general exception that is not specifically called out
            IO.output_error_messages("There was a non-specific error when reading the file!", e)
        finally:
            if file:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file from a list of dictionary rows

        ChangeLog: (Who, When, What)
        Sohail Nassiri,09.09.2024,Created function

        :param file_name: string with the name of the file we are writing to
        :param student_data: list of dictionary rows we have in our data
        :return: None
        """
        try:
            list_of_dictionary_data: list = []
            for student in student_data:
                student_json: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name,
                       "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)
            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file)
            file.close()
            IO.output_student_courses(student_data=student_data)  # Sending output to a function in IO
        except FileNotFoundError as e:  # Raises exception if file is not found
            # Sending error messages to a function in IO
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:  # Raises any other general exception that is not specifically called out
            IO.output_error_messages("There was a non-specific error when reading the file!", e)
        finally:
            if file:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    Sohail Nassiri,09.09.2024,Created Class, Added menu input/output functions, displaying of data, and custom error
    messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the custom error messages to the user

          Note: Allows to customize error messages in one place and affect all error handling

        ChangeLog: (Who, When, What)
        Sohail Nassiri,09.09.2024,Created function and toggling technical message off if no exception object is passed

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays a menu of option to the user

        :return: None
        """
        print()  # Adding extra space to make it look cleaner
        print(menu)
        print()  # Adding extra space to make it look cleaner

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the current data to the user

        :return: None
        """
        print("-" * 50)
        for student in student_data:  # Iterates through each row of table
            print(
                f"Student {student.first_name} {student.last_name} is enrolled in {student.course_name}")
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets data from the user and adds it to a list of dictionary rows

        :param student_data: list of dictionary rows containing our current data
        :return: list of dictionary rows filled with a new row of data
        """

        try:
            student = Student()
            student.first_name = input("Enter the student's first name: ")
            student.last_name = input("Enter the student's last name: ")
            student.course_name = input("Please enter the name of the course: ")
            student_data.append(student)
            print(
                f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")  # Displays
            #  input registration
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")
