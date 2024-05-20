from task import LearningProgressTracker
from task import Statistics
from task import Notification
import pytest


class TestCredentialsValidation:
    def test_name_validation(self):
        sut = LearningProgressTracker()
        valid_names = ["John", "Jean-Claude O'Connor",
                       "O'Neill", "Robert Jemison Van de Graaff",
                       "Ed Eden", "na'me s-u",
                       "n'a me su aa-b'b", "nA me"]
        invalid_names = ["Stanisław", "J.", "", "N",
                         "O''Neill", "-Jean-Claude", "O'Neill-", "námé surname",
                         "name námé", "na--me surname", "'name surname"]

        for name in valid_names:
            assert sut.validate_name(name), f"Expected '{name}' to be a valid name"

        for name in invalid_names:
            assert not sut.validate_name(name), f"Expected '{name}' to be an invalid name"

    def test_email_validation(self):
        sut = LearningProgressTracker()
        valid_emails = ["anny.md@mail.edu", "jcda123@google.net", "125367at@zzz90.z9",
                        "u15da125@a1s2f4f7.a1c2c5s4", "1@1.1", "a1@a1.a1", "ii@ii.ii"]
        invalid_emails = ["emailemail.xyz", "email@emailxyz", "email@e@mail.xyz"]

        for email in valid_emails:
            assert sut.validate_email(email), f"Expected '{email}' to be a valid email"

        for email in invalid_emails:
            assert not sut.validate_email(email), f"Expected '{email}' to be an invalid email"

    def test_if_email_is_unique_for_already_taken_email(self):
        sut = LearningProgressTracker()
        sut.add_students("John Doe johnd@yahoo.com")
        sut.add_students("Jane Spark jspark@gmail.com")

        assert not sut.is_email_unique("jspark@gmail.com"), f"Expected the email to be already taken"

    def test_if_email_is_unique_for_not_previously_used_email(self):
        sut = LearningProgressTracker()
        sut.add_students("John Doe johnd@yahoo.com")
        sut.add_students("Jane Spark jspark@gmail.com")

        assert sut.is_email_unique("foo@gmail.com"), f"Expected the email to be unique"


class TestPointsOperations:
    def test_points_validation(self):
        sut = LearningProgressTracker()
        valid_points = ["1 5 5 5 5", "1000 25 5 3 74", "9999999 99999999 9999999 9999999 9999999",
                        "0 0 0 0 0", "0 0 0 0 1", "d4735e3a26 4 11 0 7", "id 1 2 3 4"]
        invalid_points = ["", "-1 1 1 1", "1 1 2 A", "1 1 1", "-1 -1 -1 -1", "1010 -12 5 6 8", "2.5 2.5 2.4 1.8"]

        for points in valid_points:
            assert sut.validate_points(points), f"Expected '{points}' to be valid points"

        for points in invalid_points:
            assert not sut.validate_points(points), f"Expected '{points}' to be invalid points"

    def test_parsing_points_results_in_string_id_and_int_points_list(self):
        sut = LearningProgressTracker()
        student_id, points_to_add = sut.parse_points("1000 25 5 3 74")

        assert student_id == "1000"
        assert points_to_add == [25, 5, 3, 74]

    def test_points_are_added_to_selected_student(self):
        sut = LearningProgressTracker()

        sut.add_students("John Smith jsmith@hotmail.com")
        sut.add_students("Robert Jemison Van de Graaff robertvdgraaff@mit.edu")

        sut.add_points("6b86b273ff 0 0 0 0")
        sut.add_points("d4735e3a26 4 11 0 1")
        sut.add_points("6b86b273ff 0 0 0 5")

        student1 = sut.students[0]
        student2 = sut.students[1]

        assert student1["course_points"] == {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 5}
        assert student2["course_points"] == {'Python': 4, 'DSA': 11, 'Databases': 0, 'Flask': 1}

    def test_points_are_printed_for_existing_student(self, capsys):
        sut = LearningProgressTracker()

        sut.add_students("John Smith jsmith@hotmail.com")
        sut.add_students("Robert Jemison Van de Graaff robertvdgraaff@mit.edu")

        sut.add_points("d4735e3a26 4 11 0 1")
        sut.print_student_points("d4735e3a26")

        captured = capsys.readouterr()
        all_outputs = captured.out.strip().split('\n')
        last_output = all_outputs[-1]

        assert last_output == "d4735e3a26 points: Python=4; DSA=11; Databases=0; Flask=1.", f"Printed points do not match the expected result"

    def test_correct_message_is_printed_when_student_is_not_found(self, capsys):
        sut = LearningProgressTracker()

        sut.print_student_points("6b86b273ff")
        captured = capsys.readouterr()

        assert captured.out.strip() == "No student is found for id=6b86b273ff.", f"The message when the student is not found does not match the expected message"


class TestStatistics:
    def test_calculating_statistics_with_data_available(self):
        sut = LearningProgressTracker()
        statistics = Statistics(sut.courses, sut.course_completion_requirements)

        sut.add_students("John Doe johnd@email.net")
        sut.add_students("Jane Spark jspark@yahoo.com")

        sut.add_points("6b86b273ff 8 7 7 5")
        sut.add_points("6b86b273ff 7 6 9 7")
        sut.add_points("6b86b273ff 6 5 5 0")
        sut.add_points("d4735e3a26 8 0 8 6")
        sut.add_points("d4735e3a26 7 0 0 0")
        sut.add_points("d4735e3a26 9 0 0 5")

        statistics.calculate_course_statistics(sut.students)

        assert statistics.get_statistics() == {
            "MP": "Python, Databases, Flask",
            "LP": "DSA",
            "HA": "Python",
            "LA": "DSA",
            "EC": "Python",
            "HC": "Flask"
        }, "Course statistics do not match the expected result"

    def test_calculating_statistics_with_no_data_available(self):
        sut = LearningProgressTracker()
        statistics = Statistics(sut.courses, sut.course_completion_requirements)

        assert statistics.get_statistics() == {
            "MP": "n/a",
            "LP": "n/a",
            "HA": "n/a",
            "LA": "n/a",
            "EC": "n/a",
            "HC": "n/a"
        }, "No statistics should be available when there are no students"

    def test_top_learners_course_info_is_shown_in_correct_format(self, capsys):
        sut = LearningProgressTracker()
        statistics = Statistics(sut.courses, sut.course_completion_requirements)

        sut.add_students("John Smith jsmith@hotmail.com")
        sut.add_students("Robert Jemison Van de Graaff robertvdgraaff@mit.edu")

        sut.add_points("d4735e3a26 656 11 0 1")
        sut.add_points("6b86b273ff 3 7 0 5")

        course = "python"

        statistics.show_course_top_learners(course, sut.students)

        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')
        course_info_lines = output_lines[4:]

        assert course_info_lines[0] == "Python", "Expected course name in the header"
        assert course_info_lines[1] == "id           points     completed", "Expected a line with 'id', 'points', 'completed'"
        assert course_info_lines[
                   2] == "d4735e3a26   656        100.0%", "Incorrect data or print format"
        assert course_info_lines[
                   3] == "6b86b273ff   3          0.5%", "Incorrect data or print format"

    def test_should_show_only_course_name_and_column_headers_when_top_learners_data_is_blank(self, capsys):
        sut = LearningProgressTracker()
        statistics = Statistics(sut.courses, sut.course_completion_requirements)

        course = "dsa"
        statistics.show_course_top_learners(course, sut.students)

        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')

        assert output_lines[0] == "DSA", "Expected course name in the header"
        assert output_lines[1] == "id           points     completed", "Expected a line with 'id', 'points', 'completed'"


class TestNotification:
    def test_notify_student_who_completed_multiple_courses(self, capsys):
        sut = LearningProgressTracker()
        notification = Notification(sut.courses, sut.course_completion_requirements)

        sut.add_students("John Doe johnd@email.net")
        sut.add_students("Jane Spark jspark@yahoo.com")

        sut.add_points("6b86b273ff 600 400 0 12")
        sut.add_points("d4735e3a26 4 11 0 1")

        notification.notify_students(sut.students)

        captured = capsys.readouterr()
        last_output = captured.out.strip().split('\n')[-1]

        assert last_output == "Total 1 students have been notified.", "The number of students is different from the expected result"
        assert notification.notified_students == {'Python': ['6b86b273ff'],
                                                  'DSA': ['6b86b273ff'],
                                                  'Databases': [],
                                                  'Flask': []}, "Notified students data does not match the expected result"

    def test_notify_students_who_completed_the_same_course(self, capsys):
        sut = LearningProgressTracker()
        notification = Notification(sut.courses, sut.course_completion_requirements)

        sut.add_students("John Doe johnd@email.net")
        sut.add_students("Jane Spark jspark@yahoo.com")

        sut.add_points("6b86b273ff 7 230 6 558")
        sut.add_points("d4735e3a26 0 121 56 554")

        notification.notify_students(sut.students)

        captured = capsys.readouterr()
        last_output = captured.out.strip().split('\n')[-1]

        assert last_output == "Total 2 students have been notified.", "The number of students is different from the expected result"
        assert notification.notified_students == {'Python': [],
                                                  'DSA': [],
                                                  'Databases': [],
                                                  'Flask': ['6b86b273ff', 'd4735e3a26']}, "Notified students data does not match the expected result"

    def test_notification_about_completed_course_is_sent_only_once(self, capsys):
        sut = LearningProgressTracker()
        notification = Notification(sut.courses, sut.course_completion_requirements)

        sut.add_students("John Doe johnd@email.net")
        sut.add_points("6b86b273ff 5 7 480 12")
        notification.notify_students(sut.students)
        notification.notify_students(sut.students)

        captured = capsys.readouterr()
        last_output = captured.out.strip().split('\n')[-1]

        assert last_output == "Total 0 students have been notified.", "The number of students is different from the expected result"
        assert notification.notified_students == {'Python': [],
                                                  'DSA': [],
                                                  'Databases': ['6b86b273ff'],
                                                  'Flask': []}, "Notified students data does not match the expected result"

    def test_notification_format_is_correct(self, capsys):
        sut = LearningProgressTracker()
        notification = Notification(sut.courses, sut.course_completion_requirements)

        sut.add_students("jean-claude o'connor JCDA123@GOOGLE.NET")
        sut.add_points("6b86b273ff 5 7 480 12")
        notification.notify_students(sut.students)

        captured = capsys.readouterr()
        notification_email = captured.out.strip().split('\n')[-4:-1]

        assert notification_email == ['To: jcda123@google.net',
                                      'Re: Your Learning Progress',
                                      "Hello, Jean-Claude O'Connor! You have accomplished our Databases course!"], "The email format does not match the expected format"


def test_should_only_add_students_that_match_credential_requirements():
    sut = LearningProgressTracker()

    sut.add_students("John Smith jsmith@hotmail.com")
    sut.add_students("-name surname email@email.xyz")
    sut.add_students("Stanisław Oğuz 1@1.1")
    sut.add_students("Robert Jemison Van de Graaff robertvdgraaff@mit.edu")
    sut.add_students("陳 港 生")
    sut.add_students("")
    sut.add_students(" ")

    assert len(sut.students) == 2, "Number of students is different from expected result"
