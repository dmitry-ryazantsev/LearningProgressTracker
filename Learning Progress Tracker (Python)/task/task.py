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

    def add_students(self, credentials):
        parsed_credentials = self.parse_credentials(credentials)
        if parsed_credentials is None:
            print("Incorrect credentials.")
            return

        first_name, last_name, email = parsed_credentials
        if self.validate_student_credentials(first_name, last_name, email):
            self.student_id += 1
            hashed_id = self.hash_student_id(self.student_id)
            self.students.append({"id": hashed_id,
                                  "first_name": first_name.title(),
                                  "last_name": last_name.title(),
                                  "email": email,
                                  "course_points": {course: 0 for course in self.courses},
                                  "course_submissions": {course: 0 for course in self.courses}})
            print("The student has been added.")

    @staticmethod
    def hash_student_id(student_id):
        hashed_id = hashlib.sha256(str(student_id).encode()).hexdigest()
        shortened_hashed_id = hashed_id[:10]
        return shortened_hashed_id

    @staticmethod
    def parse_credentials(credentials):
        parts = credentials.split()
        if len(parts) < 3:  # Not enough parts to validate
            return None

        first_name = parts[0]
        last_name = ' '.join(parts[1:-1])
        email = parts[-1]
        return first_name, last_name, email

    def validate_student_credentials(self, first_name, last_name, email):
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
            student_email = student["email"]
            if student_email == email:
                return False

        return True

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

    def print_student_points(self, student_id):
        student = self.find_student_by_id(student_id)
        if student is None:
            return

        course_points = student["course_points"]
        print(f"{student_id} points: Python={course_points['Python']}; DSA={course_points['DSA']}; Databases={course_points['Databases']}; Flask={course_points['Flask']}.")

    def find_student_by_id(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                return student

        print(f"No student is found for id={student_id}.")
        return None


class Statistics:
    def __init__(self, courses, course_completion_requirements):
        self.courses = courses
        self.course_completion_requirements = course_completion_requirements
        self.statistics = {
            "MP": "n/a",  # Most Popular
            "LP": "n/a",  # Least Popular
            "HA": "n/a",  # Highest Activity
            "LA": "n/a",  # Lowest Activity
            "EC": "n/a",  # Easiest Course
            "HC": "n/a"  # Hardest Course
        }

    def calculate_course_statistics(self, students):
        course_enrollment = {course: 0 for course in self.courses}
        course_submissions = {course: 0 for course in self.courses}
        course_points = {course: 0 for course in self.courses}
        average_course_points = {course: 0.0 for course in self.courses}

        for student in students:
            for course, points in student["course_points"].items():
                if points > 0:
                    course_enrollment[course] += 1
                    course_points[course] += points

            for course, submissions in student["course_submissions"].items():
                course_submissions[course] += submissions

        for course in self.courses:
            if course_submissions[course] > 0:
                average_course_points[course] = course_points[course] / course_submissions[course]

        # Update statistics only if there's data in at least one course
        zero_counter = 0
        for course in course_enrollment:
            if course_enrollment[course] == 0:
                zero_counter += 1
        if zero_counter != len(self.courses):
            # Find most and least popular courses based on student enrollment
            self.update_course_statistics(course_enrollment, "MP", "LP")
            # Find highest and lowest activity courses based on submissions
            self.update_course_statistics(course_submissions, "HA", "LA")
            # Find easiest and hardest courses based on average course points
            self.update_course_statistics(average_course_points, "EC", "HC")

    def update_course_statistics(self, dictionary, high_stat, low_stat):
        max_value = max(dictionary.values())
        min_value = min(dictionary.values())
        high_stat_course_list = [course for course, value in dictionary.items() if value == max_value]
        self.statistics[high_stat] = ", ".join(high_stat_course_list)

        # If max and min values are equal, then all courses are max and min stays n/a as set by default
        if max_value != min_value:
            low_stat_course_list = [course for course, value in dictionary.items() if value == min_value]
            self.statistics[low_stat] = ", ".join(low_stat_course_list)

    def get_statistics(self):
        return self.statistics

    def show_course_top_learners(self, course, students):
        course = course.upper() if course == "dsa" else course.capitalize()

        print(course)
        print("{:<12} {:<10} {:9}".format("id", "points", "completed"))

        student_course_info = []
        for student in students:
            course_points = student["course_points"][course]
            if course_points > 0:
                student_course_info.append({"id": student["id"],
                                            "points": course_points,
                                            "course_completion": self.calculate_course_completion(course, course_points)})

        # Sort by points in descending order
        # and by ID in ascending order for the same number of points
        student_course_info.sort(key=lambda d: d["id"])
        student_course_info.sort(key=lambda d: d["points"], reverse=True)

        for student in student_course_info:
            print("{:<12} {:<10} {:3}%".format(student["id"], student["points"], student["course_completion"]))

    def calculate_course_completion(self, course, points):
        completion_percentage = round(points / self.course_completion_requirements[course] * 100, 1)

        if completion_percentage > 100.0:
            completion_percentage = 100.0

        return completion_percentage


class Notification:
    def __init__(self, courses, course_completion_requirements):
        self.courses = courses
        self.course_completion_requirements = course_completion_requirements
        self.notified_students = {course: [] for course in self.courses}

    def notify_students(self, students):
        students_to_notify = set()

        for student in students:
            email = student['email']
            full_name = f"{student['first_name']} {student['last_name']}"

            for course, points in student["course_points"].items():
                if (points >= self.course_completion_requirements[course]
                        and student["id"] not in self.notified_students[course]):
                    self.send_notification(email, full_name, course)
                    # Track how many unique students are being notified in the current method call
                    students_to_notify.add(student["id"])
                    # Track which students should not be notified again for the same course in the future
                    self.notified_students[course].append(student["id"])

        print(f"Total {len(students_to_notify)} students have been notified.")

    @staticmethod
    def send_notification(email, full_name, course):
        print(f"To: {email}\n"
              f"Re: Your Learning Progress\n"
              f"Hello, {full_name}! You have accomplished our {course} course!")


class UserMenu:
    def __init__(self, tracker):
        self.tracker = tracker
        self.statistics = Statistics(tracker.courses, tracker.course_completion_requirements)
        self.notifications = Notification(tracker.courses, tracker.course_completion_requirements)

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
            self.statistics.calculate_course_statistics(self.tracker.students)

        stats = self.statistics.get_statistics()
        print(f"Most popular: {stats['MP']}\n"
              f"Least popular: {stats['LP']}\n"
              f"Highest activity: {stats['HA']}\n"
              f"Lowest activity: {stats['LA']}\n"
              f"Easiest course: {stats['EC']}\n"
              f"Hardest course: {stats['HC']}")

        while True:
            course = input().lower().strip()
            if course == "back":
                break
            if course in [course.lower() for course in self.statistics.courses]:
                self.statistics.show_course_top_learners(course, self.tracker.students)
            else:
                print("Unknown course.")

    def notify_command(self):
        self.notifications.notify_students(self.tracker.students)

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
            elif user_command == "notify":
                self.notify_command()
            elif user_command == "back":
                print("Enter 'exit' to exit the program.")
            elif user_command.strip() == "":
                print("No input")
            else:
                print("Unknown command.")


def main():
    try:
        tracker = LearningProgressTracker()
        menu = UserMenu(tracker)
        menu.display_menu()
    except KeyboardInterrupt:
        print("Execution interrupted. Exiting program.")


if __name__ == "__main__":
    main()
