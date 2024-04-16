import re


class LearningProgressTracker:
    def __init__(self):
        self.students_number = 0
        self.students = {}

    def add_students(self, credentials):
        if self.validate_student_credentials(credentials):
            self.students_number += 1
            student_id = self.students_number

            self.students[student_id] = credentials
            print("The student has been added.")

    def list_students(self):
        if self.students == {}:
            print("No students found.")
        else:
            print("Students:")
            for student in self.students.keys():
                print(student)

    def validate_student_credentials(self, credentials):
        parts = credentials.split()
        if len(parts) < 3:  # Not enough parts to validate
            print("Incorrect credentials.")
            return False

        first_name = parts[0]
        last_name = ' '.join(parts[1:-1])
        email = parts[-1]

        if not self.validate_name(first_name):
            print("Incorrect first name.")
            return False

        if not self.validate_name(last_name):
            print("Incorrect last name.")
            return False

        if not self.validate_email(email):
            print("Incorrect email.")
            return False

        if not self.is_email_unique(email):
            print("This email is already taken.")
            return False

        return True

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
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return bool(re.match(pattern, email))

    def is_email_unique(self, email):
        for credentials in self.students.values():
            student_email = credentials.split()[-1]
            if student_email == email:
                return False
        return True


class UserMenu:
    def __init__(self, tracker):
        self.tracker = tracker

    @staticmethod
    def greet_user():
        print("Learning Progress Tracker")

    @staticmethod
    def exit_command():
        print("Bye!")

    def back_command(self):
        print(f"Total {self.tracker.students_number} students have been added.")

    def add_students_command(self):
        print("Enter student credentials or 'back' to return:")
        while True:
            credentials = input().lower().strip()
            if credentials == "back":
                self.back_command()
                break
            else:
                self.tracker.add_students(credentials)

    def list_students_command(self):
        self.tracker.list_students()

    def display_menu(self):
        self.greet_user()
        while True:
            user_command = input().lower().strip()
            if user_command == "exit":
                self.exit_command()
                break
            elif user_command == "add students":
                self.add_students_command()
            elif user_command == "list":
                self.list_students_command()
            elif user_command == "back":
                print("Enter 'exit' to exit the program.")
            elif user_command.strip() == "":
                print("No input")
            else:
                print("Unknown command.")


def main():
    tracker = LearningProgressTracker()
    menu = UserMenu(tracker)
    menu.display_menu()


if __name__ == "__main__":
    main()
