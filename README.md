# Learning Progress Tracker
This program keeps track of the registered users, their learning progress, and metrics. It also provides detailed information about each user or any category of users and the overall statistics for the entire learning platform.

## Features
1. Add students: Register new students with their names and email addresses.
2. List students: Display a list of all registered students by their unique IDs.
3. Add points: Update the learning progress by adding points for each student in different courses.
4. Find student: Search for a student by their ID to view their progress and details.
5. Show statistics: Display various statistics about the courses, such as popularity and difficulty.
6. Notify students: Send notifications to students who have completed courses.

## Usage
To run the Learning Progress Tracker, execute the progress_tracker.py in a Python environment (the program was written in Python 3.10). When you start the program, you can enter commands as instructed.

## Example
```
Learning Progress Tracker
> add students
Enter student credentials or 'back' to return:
> John Doe johnd@email.net
The student has been added.
> Jane
Incorrect credentials.
> Jane Spark jspark@yahoo.com
The student has been added.
> back
Total 2 students have been added.
> list
Students:
6b86b273ff
d4735e3a26
> find
Enter an id or 'back' to return:
> 6b86b273ff
6b86b273ff points: Python=0; DSA=0; Databases=0; Flask=0.
> add points
Enter an id and points or 'back' to return:
> 1000 5 6 7 8
No student is found for id=1000.
> 6b86b273ff 8 7 7 5
Points updated.
> 6b86b273ff 13 6 9 7
Points updated.
> 6b86b273ff 6 521 55 0
Points updated.
> d4735e3a26 8 0 8 6
Points updated.
> d4735e3a26 7 0 0 0
Points updated.
> d4735e3a26 9 0 0 5
Points updated.
> back
> statistics
Type the name of a course to see details or 'back' to quit:
Most popular: Python, Databases, Flask
Least popular: DSA
Highest activity: Python
Lowest activity: DSA
Easiest course: DSA
Hardest course: Flask
> python
Python
id           points     completed
6b86b273ff   27         4.5%
d4735e3a26   24         4.0%
> dsa
DSA
id           points     completed
6b86b273ff   534        100.0%
> databases
Databases
id           points     completed
6b86b273ff   71         14.8%
d4735e3a26   8          1.7%
> flask
Flask
id           points     completed
6b86b273ff   12         2.2%
d4735e3a26   11         2.0%
> java
Unknown course.
> back
> notify
To: johnd@email.net
Re: Your Learning Progress
Hello, John Doe! You have accomplished our DSA course!
Total 1 students have been notified.
> notify
Total 0 students have been notified.
> exit
Bye!
```
