import re
import validate

def is_support_between_member():
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Does support within the line segment of member:")
        print("[1] Yes")
        print("[2] No")
        user_input = input('Choice: ')

        if user_input == "cancel":
            return None
            
        if pattern.match(user_input):
            if user_input == '1':
                return True
            else:
                return False
        else:
            print("Invalid input! Please try again.")

def support_type():
    pattern = re.compile(r'^(1|2|3|4)$')

    while True:
        print("\n=========================================================\n")
        print("Choose a support type to plot bellow:")
        print("[1] Roller")
        print("[2] Pin")
        print("[3] Fixed")
        print("[4] Back")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def release_type():
    pattern = re.compile(r'^(1|2|3)$')

    while True:
        print("\n=========================================================\n")
        print("Choose a release type to plot bellow:")
        print("[1] Hinge")
        print("[2] Roller")
        print("[3] Back")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def beam_options():
        pattern = re.compile(r'^(1|2|3|4|5)$')

        while True:
            print("\n=========================================================\n")
            print("Choose an option bellow:")
            print("[1] Plot member")
            print("[2] Plot support")
            print("[3] Plot release")
            print("[4] Show graph")
            print("[5] Compute degree of indeterminacy")
            user_input = input('Choice: ')

            if pattern.match(user_input):
                return user_input
            else:
                print("Invalid input! Please try again.")

def trusses_options():
        pattern = re.compile(r'^(1|2|3|4|5)$')

        while True:
            print("\n=========================================================\n")
            print("Choose an option bellow:")
            print("[1] Plot member")
            print("[2] Plot support")
            print("[3] Plot joint")
            print("[4] Show graph")
            print("[5] Compute degree of indeterminacy")
            user_input = input('Choice: ')

            if pattern.match(user_input):
                return user_input
            else:
                print("Invalid input! Please try again.")

def structure_to_solve():
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Choose structure to solve:")
        print("[1] Beams & Frames")
        print("[2] Trusses")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def fixed_alignment():
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Choose fixed alignment:")
        print("[1] Vertical")
        print("[2] Horizontal")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            if user_input == '1':
                return 'vertical'
            else:
                return 'horizontal'
        else:
            print("Invalid input! Please try again.")

def one_point_coords(name):
    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Input format: x y")
        user_input = input(f"{name} coordinate: ")

        if user_input == "cancel":
            return None

        valid_coordinate = validate.one_point_input_coordinate(user_input)

        if valid_coordinate:
            return valid_coordinate
        else:
            print("Invalid coordinate! Please try again")

def two_point_coords(name):
    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Input format: x y, x y")
        user_input = input(f"{name} coordinate: ")

        if user_input == "cancel":
            return None

        valid_coordinate = validate.two_point_input_coordinates(user_input)

        if valid_coordinate:
            return valid_coordinate
        else:
            print("Invalid coordinate! Please try again")

def pin_face():
    pattern = re.compile(r'^(1|2|3|4)$')

    while True:
        print("\n=========================================================\n")
        print("Choose structure to solve:")
        print("[1] Up")
        print("[2] Down")
        print("[3] Left")
        print("[4] Right")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            if user_input == "1":
                return "up"
            elif user_input == "2":
                return "down"
            elif user_input == "3":
                return "left"
            else:
                return "right"
        else:
            print("Invalid input! Please try again.")

def hinge_type():
    pattern = re.compile(r'^(1|2|3)$')

    while True:
        print("\n=========================================================\n")
        print("Choose a support type to plot bellow:")
        print("[1] Hinge with 1 member")
        print("[2] Hinge with 2 members")
        print("[3] Back")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def roller_type():
    pattern = re.compile(r'^(1|2|3)$')

    while True:
        print("\n=========================================================\n")
        print("Choose a support type to plot bellow:")
        print("[1] Roller vertical")
        print("[2] Roller horizontal")
        print("[3] Back")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def horizontal_ec_roller_placement():
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Roller left vertical member position:")
        print("[1] Top")
        print("[2] Bottom")
        user_input = input('Choice: ')

        if user_input == 'cancel':
            return None

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def vertical_ec_roller_placement():
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Roller left vertical member position:")
        print("[1] Left")
        print("[2] Right")
        user_input = input('Choice: ')

        if user_input == 'cancel':
            return None

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def member_placement():
    pattern = re.compile(r'^(1|2|3)$')

    while True:
        print("\n=========================================================\n")
        print("Choose where to connect member:")
        print("[1] Member")
        print("[2] Support")
        print("[3] Back")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")