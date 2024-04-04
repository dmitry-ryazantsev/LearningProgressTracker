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
                self.add_students()
            elif user_command == "back":
                print("Enter 'exit' to exit the program.")
            elif user_command.strip() == "":
                print("No input")
            else:
                print("Unknown command.")

    @staticmethod
    def greet():
        print("Learning Progress Tracker")

    @staticmethod
    def exit_program():
        print("Bye!")

    def add_students(self):
        print("Enter student credentials or 'back' to return:")
        while True:
            user_command = input().lower()
            if user_command == "back":
                self.back()
                return
            else:
                if self.validate_student_credentials(user_command):
                    self.students_number += 1
                    self.students_list.append(user_command)
                    print("The student has been added.")

    def back(self):
        print(f"Total {self.students_number} students have been added.")

    def validate_student_credentials(self, credentials):
        parts = credentials.split()
        if len(parts) < 3:  # Not enough parts to validate
            print("Incorrect credentials.")
            return False

        email = parts[-1]
        name = parts[:-1]
        first_name = name[0]
        last_name = ' '.join(name[1:]) if len(name) > 1 else ''

        invalid_credentials = False

        if not self.validate_name(first_name):
            print("Incorrect first name.")
            invalid_credentials = True

        if not self.validate_name(last_name):
            print("Incorrect last name.")
            invalid_credentials = True

        if not self.validate_email(email):
            print("Incorrect email.")
            invalid_credentials = True

        return not invalid_credentials

    @staticmethod
    def validate_name(name):
        # Requirements:
        # - Only ASCII characters, hyphens and apostrophes
        # - Hyphens and apostrophes cannot be the first or the last characters
        # - Hyphens and apostrophes cannot be adjacent to each other
        # - Must be at least two characters long
        pattern = r'^[a-z](?!.*[-\']{2})[a-z\' -]*[a-z]$'
        return bool(re.match(pattern, name, re.IGNORECASE))

    @staticmethod
    def validate_email(email):
        # Should contain name, the @ symbol, and domain
        pattern = r'^\S+@\S+\.\S+$'
        return bool(re.match(pattern, email))


program = LearningProgressTracker()
program.main()
