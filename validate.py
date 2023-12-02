import math

def two_point_input_coordinates(user_input):
    '''
        Sample input
        Input format: x y, x y

        Where x and y are integer
    '''
    try:
        member_coordinate = user_input.split(', ') # ['x y'], ['x y']
        start_coordinate = member_coordinate[0].split(' ') # ['x', 'y']
        end_coordinate = member_coordinate[1].split(' ') # ['x', 'y']

        # Check if there are exactly two coordinates
        if len(member_coordinate) != 2 or len(start_coordinate) != 2 or len(end_coordinate) != 2 or start_coordinate == end_coordinate:
            return False

        return [
            [
                float(start_coordinate[0]), 
                float(start_coordinate[1])
            ], 
            [
                float(end_coordinate[0]), 
                float(end_coordinate[1])
            ]
        ]
    except ValueError:
        return False

def one_point_input_coordinate(user_input):
    '''
        Sample input
        Input format: x y

        Where x and y are integer
    '''
    try:
        coordinate = user_input.split(' ') # [x, y]

        # Check if there are exactly two coordinates
        if len(coordinate) != 2:
            return False

        return [float(coordinate[0]), float(coordinate[1])]
    except ValueError:
        return False
    

def is_coords_between(s, e, c):
    # s = start, e = end, c = center
    # Calculate squared distances formula
    d_sc_squared = math.sqrt((c[0] - s[0])**2 + (c[1] - s[1])**2)
    d_ce_squared = math.sqrt((e[0] - c[0])**2 + (e[1] - c[1])**2)
    d_se_squared = math.sqrt((e[0] - s[0])**2 + (e[1] - s[1])**2)

    # Check if c is between s and e
    return d_sc_squared + d_ce_squared == d_se_squared