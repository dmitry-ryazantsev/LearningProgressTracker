import re


class LearningProgressTracker:
    def __init__(self):
        self.students_number = 0
        self.students_list = []

    def main(self):
        self.greet()
        while True:
            user_command = input().lower()
            if user_command == "exit":
                self.exit_program()
                break
            elif user_command == "add students":
                self.add_students_loop()
            elif user_command == "back":
                self.back()
            else:
                print("Incorrect command.")

    @staticmethod
    def greet():
        print("Learning Progress Tracker")

    @staticmethod
    def exit_program():
        print("Bye!")

    def add_students_loop(self):
        print("Enter student credentials or 'back' to return:")
        while True:
            user_command = input().lower()
            if user_command == "exit":
                self.exit_program()
                return
            elif user_command == "back":
                self.back()
                return
            else:
                if self.validate_student_credentials(user_command):
                    self.students_number += 1
                    self.students_list.append(user_command)
                    print("The student has been added.")

    def back(self):
        if self.students_number > 0:
            print(f"Total {self.students_number} students have been added.")
        else:
            print("Enter 'exit' to exit the program.")

    def validate_student_credentials(self, credentials):
        parts = credentials.split()
        if len(parts) != 3:
            print("Incorrect credentials.")
            return False

        first_name, last_name, email = parts

        invalid_credentials = False

        if not self.validate_name(first_name):
            print("Incorrect first name.")
            invalid_credentials = True

        if not self.validate_last_name(last_name):
            print("Incorrect last name.")
            invalid_credentials = True

        if not self.validate_email(email):
            print("Incorrect email.")
            invalid_credentials = True

        return not invalid_credentials

    @staticmethod
    def validate_name(first_name):
        return True

    @staticmethod
    def validate_last_name(last_name):
        return True

    @staticmethod
    def validate_email(email):
        pattern = r'^\S+@\S+\.\S+$'
        return bool(re.match(pattern, email))


program = LearningProgressTracker()
program.main()
