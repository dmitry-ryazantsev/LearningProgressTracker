from task import LearningProgressTracker
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

    def test_whole_credentials_validation(self):
        sut = LearningProgressTracker()
        valid_credentials = ["John Smith jsmith@hotmail.com", "Anny Doolittle anny.md@mail.edu",
                             "Jean-Claude O'Connor jcda123@google.net",
                             "Al Owen u15da125@a1s2f4f7.a1c2c5s4",
                             "Robert Jemison Van de Graaff robertvdgraaff@mit.edu",
                             "Ed Eden a1@a1.a1", "na'me s-u ii@ii.ii",
                             "n'a me su aa-b'b ab@ab.ab", "nA me 1@1.1"]
        invalid_credentials = ["name surname", "", " ",
                               "-name surname email@email.xyz", "name- surname email@email.xyz",
                               "name s email@email.xyz", "name surnam''e email@email.xyz",
                               "name su-'rname email@email.xyz", "name surname- email@email.xyz",
                               "name surname emailemail.xyz", "name surname email@e@mail.xyz"]

        for credentials in valid_credentials:
            assert sut.validate_student_credentials(credentials), f"Expected '{credentials}' to be valid credentials"

        for credentials in invalid_credentials:
            assert not sut.validate_student_credentials(credentials), f"Expected '{credentials}' to be invalid credentials"


def test_adding_students():
    sut = LearningProgressTracker()

    sut.add_students("John Smith jsmith@hotmail.com")
    sut.add_students("Robert Jemison Van de Graaff robertvdgraaff@mit.edu")
    sut.add_students("-name surname email@email.xyz")
    sut.add_students("Stanisław Oğuz 1@1.1")
    sut.add_students("陳 港 生")

    assert sut.students_number == 2, "Number of students is different from expected result"
    assert sut.students_list == ["John Smith jsmith@hotmail.com",
                                 "Robert Jemison Van de Graaff robertvdgraaff@mit.edu"]
