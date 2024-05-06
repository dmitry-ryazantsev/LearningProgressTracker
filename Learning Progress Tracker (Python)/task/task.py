import hashlib
import re


class LearningProgressTracker:
    def __init__(self):
        self.student_id = 0
        self.students = []
        self.courses = ["Python", "DSA", "Databases", "Flask"]
        self.course_completion_requirements = {
            "Python": 600,
            "DSA": 400,
            "Databases": 480,
            "Flask": 550
        }
        self.statistics = {
            "MP": "n/a",
            "LP": "n/a",
            "HA": "n/a",
            "LA": "n/a",
            "EC": "n/a",
            "HC": "n/a"
        }

    def add_students(self, credentials):
        if self.validate_student_credentials(credentials):
            self.student_id += 1
            hashed_id = self.hash_student_id(self.student_id)
            self.students.append({"id": hashed_id,
                                  "credentials": credentials,
                                  "course_points": {course: 0 for course in self.courses},
                                  "course_submissions": {course: 0 for course in self.courses}})
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

        student_id, points_to_add = self.parse_points(points)
        student = self.find_student_by_id(student_id)
        if student is None:
            return

        course_points = student["course_points"]
        submissions = student["course_submissions"]
        for course, pts in zip(self.courses, points_to_add):
            if pts > 0:
                course_points[course] += pts
                submissions[course] += 1
        print("Points updated.")

    def print_student_points(self, student_id):
        student = self.find_student_by_id(student_id)
        if student is None:
            return

        course_points = student["course_points"]
        print(f"{student_id} points: Python={course_points['Python']}; DSA={course_points['DSA']}; Databases={course_points['Databases']}; Flask={course_points['Flask']}.")

    @staticmethod
    def hash_student_id(student_id):
        hashed_id = hashlib.sha256(str(student_id).encode()).hexdigest()
        shortened_hashed_id = hashed_id[:10]
        return shortened_hashed_id

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                return student

        print(f"No student is found for id={student_id}.")
        return None

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
        points_pattern = r'^\w+( \d+){4}$'
        return re.match(points_pattern, points)

    @staticmethod
    def parse_points(points):
        data = points.split()
        student_id = data[0]
        points_to_add = [int(x) for x in data[1:]]
        return student_id, points_to_add

    def calculate_course_statistics(self):
        course_enrollment = {course: 0 for course in self.courses}
        course_submissions = {course: 0 for course in self.courses}
        course_points = {course: 0 for course in self.courses}
        average_course_points = {course: 0.0 for course in self.courses}

        for student in self.students:
            for course, points in student["course_points"].items():
                if points > 0:
                    course_enrollment[course] += 1
                    course_points[course] += points

            for course, submissions in student["course_submissions"].items():
                course_submissions[course] += submissions

        # skip updating statistics if enrollment in all courses is zero
        zero_counter = 0
        for course in course_enrollment:
            if course_enrollment[course] == 0:
                zero_counter += 1
        if zero_counter == len(self.courses):
            return

        # determine most and least popular courses
        max_enrollment = max(course_enrollment.values())
        min_enrollment = min(course_enrollment.values())
        most_popular_courses = [course for course, count in course_enrollment.items() if count == max_enrollment]
        self.statistics["MP"] = ", ".join(most_popular_courses)
        if max_enrollment != min_enrollment:
            least_popular_courses = [course for course, count in course_enrollment.items() if count == min_enrollment]
            self.statistics["LP"] = ", ".join(least_popular_courses)

        # determine highest and lowest activity courses
        max_submissions = max(course_submissions.values())
        min_submissions = min(course_submissions.values())
        most_submitted_courses = [course for course, count in course_submissions.items() if count == max_submissions]
        self.statistics["HA"] = ", ".join(most_submitted_courses)
        if max_submissions != min_submissions:
            least_submitted_courses = [course for course, count in course_submissions.items() if
                                       count == min_submissions]
            self.statistics["LA"] = ", ".join(least_submitted_courses)

        # determine easiest and hardest courses
        for course in self.courses:
            if course_submissions[course] > 0:
                average_course_points[course] = course_points[course] / course_submissions[course]

        max_average_grade = max(average_course_points.values())
        min_average_grade = min(average_course_points.values())
        easiest_courses = [course for course, points in average_course_points.items() if points == max_average_grade]
        self.statistics["EC"] = ", ".join(easiest_courses)
        if max_average_grade != min_average_grade:
            hardest_courses = [course for course, points in average_course_points.items() if points == min_average_grade]
            self.statistics["HC"] = ", ".join(hardest_courses)

    def show_course_top_learners(self, course):
        course = course.upper() if course == "dsa" else course.capitalize()

        print(course)
        print("{:<12} {:<10} {:<10}".format("id", "points", "completed"))

        student_course_info = []
        for student in self.students:
            course_points = student["course_points"][course]
            if course_points > 0:
                student_course_info.append({"id": student["id"],
                                            "points": course_points,
                                            "course_completion": self.calculate_course_completion(course, course_points)})

        # Sort by points in descending order
        # and by ID in ascending order for the same number of points
        student_course_info.sort(key=lambda x: x["id"])
        student_course_info.sort(key=lambda x: x["points"], reverse=True)

        for student in student_course_info:
            print("{:<12} {:<10} {:<10}".format(student["id"], student["points"], f"{student['course_completion']}%"))

    def calculate_course_completion(self, course, points):
        completion_percentage = round(points / self.course_completion_requirements[course] * 100, 1)

        if completion_percentage > 100.0:
            completion_percentage = 100.0

        return completion_percentage


class UserMenu:
    def __init__(self, tracker):
        self.tracker = tracker

    @staticmethod
    def greet_user():
        print("Learning Progress Tracker")

    @staticmethod
    def exit_command():
        print("Bye!")

    def add_students_command(self):
        print("Enter student credentials or 'back' to return:")
        while True:
            credentials = input().lower().strip()
            if credentials == "back":
                print(f"Total {len(self.tracker.students)} students have been added.")
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

    def find_student_command(self):
        print("Enter an id or 'back' to return:")
        while True:
            student_id = input()
            if student_id == "back":
                break
            else:
                self.tracker.print_student_points(student_id)

    def statistics_command(self):
        print("Type the name of a course to see details or 'back' to quit:")

        if self.tracker.students:
            self.tracker.calculate_course_statistics()

        print(f"Most popular: {self.tracker.statistics['MP']}\n"
              f"Least popular: {self.tracker.statistics['LP']}\n"
              f"Highest activity: {self.tracker.statistics['HA']}\n"
              f"Lowest activity: {self.tracker.statistics['LA']}\n"
              f"Easiest course: {self.tracker.statistics['EC']}\n"
              f"Hardest course: {self.tracker.statistics['HC']}")

        while True:
            course = input().lower().strip()
            if course == "back":
                break
            if course in [course.lower() for course in self.tracker.courses]:
                self.tracker.show_course_top_learners(course)
            else:
                print("Unknown course.")

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
            elif user_command == "find":
                self.find_student_command()
            elif user_command == "statistics":
                self.statistics_command()
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
