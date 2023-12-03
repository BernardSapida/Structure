import re
import validate

def is_support_between_member():
    """
    Prompts the user to determine whether support exists within the line segment of a member.

    Returns:
        bool or None: True if support exists, False if it doesn't, None if the user cancels.
    """
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
    """
    Prompts the user to choose a support type for plotting.

    Returns:
        str: A string representing the chosen support type.
            Possible values are '1' for Roller, '2' for Pin, '3' for Fixed, and '4' for Back.
    """
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
    """
    Prompts the user to choose a release type for plotting.

    Returns:
        str: A string representing the chosen release type.
             Possible values are '1' for Hinge, '2' for Roller, and '3' for Back.
    """
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
    """
    Prompts the user to choose an option related to plotting for a beam.

    Returns:
        str: A string representing the chosen option.
            Possible values are '1' for Plot member, '2' for Plot support,
            '3' for Plot release, and '4' for Show graph.
    """
    pattern = re.compile(r'^(1|2|3|4)$')

    while True:
        print("\n=========================================================\n")
        print("Choose an option bellow:")
        print("[1] Plot member")
        print("[2] Plot support")
        print("[3] Plot release")
        print("[4] Show graph")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def trusses_options():
    """
    Prompts the user to choose an option related to plotting for trusses.

    Returns:
        str: A string representing the chosen option.
             Possible values are '1' for Plot member, '2' for Plot support,
             '3' for Plot joint, and '4' for Show graph.
    """
    pattern = re.compile(r'^(1|2|3|4)$')

    while True:
        print("\n=========================================================\n")
        print("Choose an option bellow:")
        print("[1] Plot member")
        print("[2] Plot support")
        print("[3] Plot joint")
        print("[4] Show graph")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def structure_to_solve():
    """
    Prompts the user to choose a structure type to solve.

    Returns:
        str: A string representing the chosen structure type.
             Possible values are '1' for Beams & Frames and '2' for Trusses.
    """
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
    """
    Prompts the user to choose a fixed alignment.

    Returns:
        str: A string representing the chosen fixed alignment.
             'vertical' for Vertical alignment and 'horizontal' for Horizontal alignment.
    """
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
    """
    Prompts the user to input coordinates in the format "x y" for a specified point.

    Args:
        name (str): The name or identifier of the point.

    Returns:
        list or None: A list [x, y] representing the coordinates if valid.
            Returns None if the user chooses to cancel.
    """
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
    """
    Prompts the user to input coordinates in the format "x1 y1, x2 y2" for a specified point.

    Args:
        name (str): The name or identifier of the point.

    Returns:
        list or None: A list [[x1, y1], [x2, y2]] representing the coordinates if valid.
            Returns None if the user chooses to cancel.
    """
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
    """
    Prompts the user to choose a pin face for a structural element.

    Returns:
        str: A string representing the chosen pin face.
            Possible values are 'up', 'down', 'left', and 'right'.
    """
    pattern = re.compile(r'^(1|2|3|4)$')

    while True:
        print("\n=========================================================\n")
        print("Choose pin face:")
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
    """
    Prompts the user to choose a hinge type for a structural element.

    Returns:
        str: A string representing the chosen hinge type.
            Possible values are '1' for Hinge between 1 member,
            '2' for Hinge between 2 members, and '3' for Back.
    """
    pattern = re.compile(r'^(1|2|3)$')

    while True:
        print("\n=========================================================\n")
        print("Choose a support type to plot bellow:")
        print("[1] Hinge between 1 member")
        print("[2] Hinge between 2 members")
        print("[3] Back")
        user_input = input('Choice: ')

        if pattern.match(user_input):
            return user_input
        else:
            print("Invalid input! Please try again.")

def roller_type():
    """
    Prompts the user to choose a roller type for a structural element.

    Returns:
        str: A string representing the chosen roller type.
            Possible values are '1' for Roller vertical,
            '2' for Roller horizontal, and '3' for Back.
    """
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
    """
    Prompts the user to choose the placement position for a horizontal end-connected roller.

    Returns:
        str or None: A string representing the chosen roller placement position.
            Possible values are '1' for Top, '2' for Bottom, and None if the user cancels.
    """
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Roller placement position:")
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
    """
    Prompts the user to choose the placement position for a vertical end-connected roller.

    Returns:
        str or None: A string representing the chosen roller placement position.
            Possible values are '1' for Left, '2' for Right, and None if the user cancels.
    """
    pattern = re.compile(r'^(1|2)$')

    while True:
        print("\n=========================================================\n")
        print("Type \"cancel\" to cancel.")
        print("Roller placement position:")
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
    """
    Prompts the user to choose where to connect a structural member.

    Returns:
        str: A string representing the chosen placement option.
            Possible values are '1' for Member, '2' for Support, and '3' for Back.
    """
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