print("Learning progress tracker")

while True:
    user_command = input().lower()
    if user_command == "exit":
        print("Bye!")
        break
    elif user_command.strip() == "":
        print("No input")
    else:
        print("Unknown command")
