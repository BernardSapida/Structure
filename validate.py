import math
import re

def two_point_input_coordinates(user_input):
    '''
    Validates and parses a user input string representing two sets of coordinates.

    Sample input:
    Input format: x1 y1, x2 y2

    Parameters:
    user_input (str): The user input string to validate and parse.

    Returns:
    list or False: A list containing two lists, each representing the x and y coordinates of a point.
        Returns False if the input does not match the expected format.
    '''
    pattern = re.compile(r'^-?\d+(\.\d+)?\s-?\d+(\.\d+)?,\s-?\d+(\.\d+)?\s-?\d+(\.\d+)?$')

    if not pattern.match(user_input):
        return False

    # ['x y'], ['x y']
    [start_coordinate, end_coordinate] = user_input.split(', ')
    [x1, y1] = start_coordinate.split(' ')
    [x2, y2] = end_coordinate.split(' ')

    return [
        [
            float(x1), 
            float(y1)
        ], 
        [
            float(x2), 
            float(y2)
        ]
    ]

def one_point_input_coordinate(user_input):
    '''
    Validates and parses a user input string representing a single set of coordinates.

    Sample input:
    Input format: x y

    Parameters:
    user_input (str): The user input string to validate and parse.

    Returns:
    list or False: A list containing the x and y coordinates of a point.
        Returns False if the input does not match the expected format.
    '''

    # valid format: 0.00, 0.00
    pattern = re.compile(r'^-?\d+(\.\d+)?\s-?\d+(\.\d+)?$') 

    if not pattern.match(user_input):
        return False

    # ['x', 'y'] string coords
    [x, y] = user_input.split(' ') 

    # [x, y] float coords
    return [float(x), float(y)] 

def is_coords_between(s, e, c):
    # s = start, e = end, c = center
    # Calculate squared distances formula
    d_sc_squared = math.sqrt((c[0] - s[0])**2 + (c[1] - s[1])**2)
    d_ce_squared = math.sqrt((e[0] - c[0])**2 + (e[1] - c[1])**2)
    d_se_squared = math.sqrt((e[0] - s[0])**2 + (e[1] - s[1])**2)

    # Check if c is between s and e
    return d_sc_squared + d_ce_squared == d_se_squared