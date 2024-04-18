import re


class LearningProgressTracker:
    def __init__(self):
        self.student_id = 0
        self.students = []

    def add_students(self, credentials):
        if self.validate_student_credentials(credentials):
            self.student_id += 1
            self.students.append({"id": self.student_id,
                                  "credentials": credentials,
                                  "subjects": {"Python": 0,
                                               "DSA": 0,
                                               "Databases": 0,
                                               "Flask": 0}})
            print("The student has been added.")

    def list_students(self):
        if not self.students:
            print("No students found.")
        else:
            print("Students:")
            for student in self.students:
                print(student["id"])

    def add_points(self, points):
        if not self.validate_points(points):
            print("Incorrect points format.")
            return

        data = self.convert_points_string_into_int_array(points)
        student_id = data[0]
        points_to_add = data[1:]

        for student in self.students:
            if student["id"] == student_id:
                subjects = student["subjects"]
                for subject, pts in zip(["Python", "DSA", "Databases", "Flask"], points_to_add):
                    subjects[subject] += pts
                print("Points updated.")
                return

        print(f"No student is found for id={student_id}.")

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
        name_pattern = r'^[a-z](?!.*[-\']{2})[a-z\' -]*[a-z]$'
        return re.match(name_pattern, name, re.IGNORECASE)

    @staticmethod
    def validate_email(email):
        # Should contain name, the @ symbol, and domain
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(email_pattern, email)

    def is_email_unique(self, email):
        for student in self.students:
            credentials = student["credentials"]
            student_email = credentials.split()[-1]
            if student_email == email:
                return False

        return True

    @staticmethod
    def validate_points(points):
        points_pattern = r'^\d+( \d+){4}$'
        return re.match(points_pattern, points)

    @staticmethod
    def convert_points_string_into_int_array(points):
        modified_points = [int(x) for x in points.split()]
        return modified_points


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
        print(f"Total {len(self.tracker.students)} students have been added.")

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

    def add_points_command(self):
        print("Enter an id and points or 'back' to return:")
        while True:
            points = input()
            if points == "back":
                break
            else:
                self.tracker.add_points(points)

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
            elif user_command == "add points":
                self.add_points_command()
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
