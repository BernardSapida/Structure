import matplotlib.pyplot as plt
import re
import math
import validate
import query

class Structure:
    def __init__(self):
        # A dictionary to store information about occupied coordinates.
        self.occupied_coords = {}

        # A dictionary to store information about plotted members.
        self.plotted_members = {}

        # A dictionary to store information about members' nodes.
        self.members_node = {}

        # A dictionary to store information about plotted joints.
        self.plotted_joints = {}
        
        # A dictionary to store information about isolated support.
        self.isolated_support = {}

        # A list to store x-coordinates of members.
        self.members_x_coords = []

        # A list to store y-coordinates of members.
        self.members_y_coords = []

        # A list to store coordinates of rollers.
        self.roller_coords = []

        # A list to store coordinates of pins.
        self.pin_coords = []

        # A list to store coordinates of fixed supports.
        self.fixed_coords = []

        # A list to store coordinates of ec hinges.
        self.ec_hinge_coords = []

        # A list to store coordinates of ec rollers.
        self.ec_roller_coords = []

        #  A list to store coordinates of joints.
        self.joints_coords = []

        # An integer representing the degree of indeterminacy of the structure.
        self.degree_of_indeterminacy = 0

        # An integer representing the number of members in the structure.
        self.members = 0

        # An integer representing the number of reactions in the structure.
        self.reactions = 0

        # An integer representing the number of ec in the structure.
        self.ec = 0

        # An integer representing the number of joints in the structure.
        self.joints = 0

        # A string to store the result of degree of indeterminacy.
        self.result = ""

        # A string to store the type of structure to solve.
        self.structure_to_solve = ''

    def plot_all(self):
        """
        Plots the entire structure, including members, supports, joints, and ec.

        If the structure to solve is a 'beam', it computes and plots the degree of indeterminacy for beams.
        Otherwise, it computes and plots the degree of indeterminacy for trusses.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function generates a Matplotlib plot showing the structure, members, supports, joints,
        and ec. It utilizes helper functions such as plot_members, plot_rollers,
        plot_pins, plot_fixed, plot_joints, plot_ec_hinge, and plot_ec_roller to visualize the elements.

        The X-axis and Y-axis labels are set, and the plot title reflects the result of the degree of
        indeterminacy or defaults to 'Structure of Beams, Frames, & Trusses' if no result is available.

        Note:
        To continue the program, the user should close the generated plot window.
        """
        if self.structure_to_solve == 'beam':
            self.compute_beam_di()
        else:
            self.compute_trusses_di()

        fig, ax = plt.subplots()

        plt.scatter(0, 10, color='white')
        plt.scatter(0, -10, color='white')

        self.plot_members()
        self.plot_rollers()
        self.plot_pins()
        self.plot_fixed()
        self.plot_joints()
        self.plot_ec_hinge()
        self.plot_ec_roller()

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title(self.result if self.result else 'Structure of Beams, Frames, & Trusses')

        print("Close the window to continue...")
        plt.show()

    def plot_members(self):
        """
        Plots the members of the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the x and y coordinates of members stored in the
        Structure class attributes members_x_coords and members_y_coords. It then plots each
        member using Matplotlib, with a specified color (#000000) and linewidth (2).

        Note:
        This function is typically called as part of the plot_all method to visualize the
        members of the structure.
        """
        for i in range(len(self.members_x_coords)):
            plt.plot(self.members_x_coords[i], self.members_y_coords[i], color='#000000', linewidth=2)

    def plot_rollers(self):
        """
        Plots the roller supports in the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the roller coordinates stored in the Structure class attribute
        roller_coords. For each set of coordinates, it plots a green circular marker (representing a roller)
        on the Matplotlib plot with a size of 200.

        Note:
        This function is typically called as part of the plot_all method to visualize the roller supports
        in the structure.
        """
        for coords in self.roller_coords:
            [x, y] = coords
            plt.scatter(x, y, 200, marker='o', color='g')
        
    def plot_pins(self):
        """
        Plots the pin supports in the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the pin coordinates stored in the Structure class attribute pin_coords.
        For each set of coordinates and face direction, it plots a green triangular marker (representing a pin)
        on the Matplotlib plot with a size of 200. The face direction determines the orientation of the marker.

        Note:
        - Pin faces: 'up', 'down', 'right', 'left'
        - This function is typically called as part of the plot_all method to visualize the pin supports in the structure.
        """
        for coords in self.pin_coords:
            [x, y, face] = coords

            if face == 'up':
                plt.scatter(x, y, 200, marker='^', color='g')
            elif face == 'down':
                plt.scatter(x, y, 200, marker='v', color='g')
            elif face == 'right':
                plt.scatter(x, y, 200, marker='>', color='g')
            elif face == 'left':
                plt.scatter(x, y, 200, marker='<', color='g')
        
    def plot_fixed(self):
        """
        Plots the fixed supports in the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the fixed support coordinates stored in the Structure class attribute
        fixed_coords. For each set of coordinates and alignment, it plots a green marker (representing a fixed support)
        on the Matplotlib plot with a size of 1500. The alignment determines whether the marker is vertical or horizontal.

        Note:
        - Alignment options: 'vertical', 'horizontal'
        - This function is typically called as part of the plot_all method to visualize the fixed supports in the structure.
        """
        for coords in self.fixed_coords:
            [x, y, alignment] = coords

            if alignment == 'vertical':
                plt.scatter(x, y, 1500, marker='|', color='g')
            elif alignment == 'horizontal':
                plt.scatter(x, y, 1500, marker='_', color='g')
    
    def plot_joints(self):
        """
        Plots the joints in the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the joint coordinates stored in the Structure class attribute joints_coords.
        For each set of coordinates, it plots a red circular marker (representing a joint) on the Matplotlib plot
        with a size of 50.

        Note:
        - This function is typically called as part of the plot_all method to visualize the joints in the structure.
        """
        for coords in self.joints_coords:
            [x, y] = coords
            plt.scatter(x, y, 50, marker='o', color='r')
            
    def plot_ec_hinge(self):
        """
        Plots the ec hinges in the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the ec hinge coordinates stored in the Structure class
        attribute ec_hinge_coords. For each set of coordinates, it plots two circular markers (representing
        an ec hinge) on the Matplotlib plot. The first marker is blue with a size of 200, and the
        second marker is yellow with a size of 40.

        Note:
        - This function is typically called as part of the plot_all method to visualize the ec hinges
        in the structure.
        """
        for coords in self.ec_hinge_coords:
            [x, y] = coords
            plt.scatter(x, y, 200, marker='o', color='blue')
            plt.scatter(x, y, 40, marker='o', color='yellow')

    def plot_ec_roller(self):
        """
        Plots the ec rollers in the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        This function iterates through the ec roller coordinates stored in the Structure class
        attribute ec_roller_coords. For each set of coordinates, it plots a circular marker (representing
        an ec roller) on the Matplotlib plot with a size of 200 and a blue color.

        Note:
        - This function is typically called as part of the plot_all method to visualize the ec rollers
        in the structure.
        """
        for coords in self.ec_roller_coords:
            [x, y] = coords
            plt.scatter(x, y, 200, marker='o', color='blue')

    def member(self):
        """
        Adds a member to the structure based on user-provided coordinates.

        This method enters a loop and prompts the user to input coordinates for a member using the
        `query.two_point_coords` function. The user can provide two points, and the coordinates are
        checked for occupancy. If the coordinates are occupied, the user is prompted to choose different
        coordinates. If the coordinates are not occupied, the member is added to the structure using
        the `add_member` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used to interactively add members to the structure during the
        construction phase.
        """
        while True:
            coords = query.two_point_coords("Member")

            if not coords:
                break

            [[x1, y1], [x2, y2]] = coords
            key = f"{x1} {y1} {x2} {y2}"
            is_occupied = self.is_occupied_coords(key)

            if is_occupied:
                print("Coordinate is occupied. Please try another coordinate.")
            else:
                self.add_member(coords[0], coords[1])
                break

    def roller(self):
        """
        Adds a roller support to the structure based on user-provided coordinates.

        This method enters a loop and prompts the user to specify whether the roller support is located
        between members using the `query.is_support_between_member` function. If the user cancels the operation,
        the loop is terminated. If the roller support is between members, the method checks if the specified
        coordinates are within the coordinates of an existing member. If not, the user is prompted to try again.
        The user is then prompted to input coordinates for the roller support using the `query.one_point_coords`
        function. If the coordinates are occupied or if they do not meet the specified conditions, the user is
        prompted to choose different coordinates. If the coordinates are valid, the roller support is added to
        the structure using the `add_support` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used to interactively add roller supports to the structure during the
        construction phase.
        """
        while True:
            is_support_between_member = query.is_support_between_member()
            
            if is_support_between_member == None:
                break
            elif is_support_between_member:
               member_coords = self.exists_member_coords()

            coords = query.one_point_coords("Roller")

            if not coords:
                break

            if is_support_between_member:
                # Validate if coords is within member coordinates
                member_start_coords = member_coords[0]
                member_end_coords = member_coords[1]
                support_coords = " ".join([str(coord) for coord in coords])
                start_coords = " ".join([str(coord) for coord in member_start_coords])
                end_coords = " ".join([str(coord) for coord in member_end_coords])
                is_coords_between = validate.is_coords_between(member_coords[0], member_coords[1], coords)

                if not is_coords_between:
                    print("Roller coordinate is not located between the member line segment! Please try again.")
                    continue

                if not (" ".join(start_coords) == " ".join(support_coords) or " ".join(end_coords) == " ".join(support_coords)):
                    self.reactions += 1  

            key = " ".join([str(coord) for coord in coords])
            is_occupied = self.is_occupied_coords(key)

            if is_occupied:
                print("Coordinate is occupied. Please try another coordinate.")
            else:
                self.add_support(coords, "Roller", key)
                break

    def pin(self):
        """
        Adds a pin support to the structure based on user-provided coordinates.

        This method enters a loop and prompts the user to specify whether the pin support is located
        between members using the `query.is_support_between_member` function. If the user cancels the operation,
        the loop is terminated. If the pin support is between members, the method checks if the specified
        coordinates are within the coordinates of an existing member. If not, the user is prompted to try again.
        The user is then prompted to input coordinates for the pin support using the `query.one_point_coords`
        function. If the coordinates are occupied or if they do not meet the specified conditions, the user is
        prompted to choose different coordinates. If the coordinates are valid, the method prompts the user to
        specify the face direction of the pin support using the `query.pin_face` function. The pin support is
        then added to the structure using the `add_support` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used to interactively add pin supports to the structure during the
        construction phase.
        """
        while True:
            is_support_between_member = query.is_support_between_member()

            if is_support_between_member:
               member_coords = self.exists_member_coords()

            coords = query.one_point_coords("Pin")

            if not coords:
                break

            if is_support_between_member:
                # Validate if coords is within member coordinates
                member_start_coords = member_coords[0]
                member_end_coords = member_coords[1]
                support_coords = " ".join([str(coord) for coord in coords])
                start_coords = " ".join([str(coord) for coord in member_start_coords])
                end_coords = " ".join([str(coord) for coord in member_end_coords])
                is_coords_between = validate.is_coords_between(member_start_coords, member_end_coords, coords)

                if not is_coords_between:
                    print("Roller coordinate is not located between the member line segment! Please try again.")
                    continue
                
                if not (" ".join(start_coords) == " ".join(support_coords) or " ".join(end_coords) == " ".join(support_coords)):
                    self.reactions += 2  

            key = " ".join([str(coord) for coord in coords])
            is_occupied = self.is_occupied_coords(key)

            if is_occupied:
                print("Coordinate is occupied. Please try another coordinate.")
                continue
            
            face = query.pin_face()
            coords.append(face)
            self.add_support(coords, "Pin", key)
            break

    def fixed(self):
        """
        Adds a fixed support to the structure based on user-provided coordinates.

        This method enters a loop and prompts the user to input coordinates for the fixed support
        using the `query.one_point_coords` function. If the user cancels the operation, the loop is
        terminated. The coordinates are then checked for occupancy. If the coordinates are occupied, the
        user is prompted to choose different coordinates. If the coordinates are valid, the method prompts
        the user to specify the alignment of the fixed support (either 'vertical' or 'horizontal') using
        the `query.fixed_alignment` function. The fixed support is then added to the structure using the
        `add_support` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used to interactively add fixed supports to the structure during the
        construction phase.
        """
        while True:
            coords = query.one_point_coords("Fixed")

            if not coords:
                break

            key = " ".join([str(coord) for coord in coords])
            is_occupied = self.is_occupied_coords(key)

            if is_occupied:
                print("Coordinate is occupied. Please try another coordinate.")
            else:
                alignment = query.fixed_alignment()
                coords.append(alignment)
                self.add_support(coords, "Fixed", key)
                break

    def ec_hinge(self):
        """
        Adds an ec hinge to the structure based on user-selected hinge type.

        This method checks if there are occupied coordinates in the structure. If not, it informs the user
        that a hinge cannot be added without a support and returns `None`. If there are occupied coordinates,
        the method prompts the user to select a hinge type using the `query.hinge_type` function. If the user
        cancels the operation or selects the '3' option, the method returns `None`. If the user selects the
        '1' option, it calls the `hinge_one_member` method. Otherwise, it calls the `hinge_two_member` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used to interactively add ec hinges to the structure during the
        construction phase.
        """
        if len(self.occupied_coords.values()) == 0:
            print("Cannot add a hinge! Please add a support first.")
            return None

        hinge_type = query.hinge_type()
        
        if hinge_type == '3':
            return None

        if hinge_type == '1':
            self.hinge_one_member()
        else:
            self.hinge_two_member()
            
    def hinge_one_member(self):
        """
        Adds an ec hinge connected to one member in the structure.

        This method guides the user through the process of adding an ec hinge to one member.
        The user is prompted to select the starting coordinate of the member to which the hinge will be connected.
        The hinge coordinate is then specified by the user. The method checks if the hinge coordinate is between
        the selected member's coordinates and if it is unoccupied. If the conditions are met, the hinge support
        is added to the structure. The user is then prompted to specify the end coordinate of the member.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used as part of the process to add ec hinges to the structure
        during the construction phase.
        """
        while True:
            print("\n=========================================================\n")
            print("Note:")
            print("• Plot: Hinge -> Member")
            print("• Hinge must be connected to the member.")
            print("• Hinge coordinate will be the starting coordinate of member.")
            
            member_coords = self.exists_member_coords("Member coordinate where you'll connect the hinge")
            if not member_coords:
                return None

            while True:
                hinge_coords = query.one_point_coords("Hinge")
                if not hinge_coords:
                    return None

                valid_hinge_coords = validate.is_coords_between(member_coords[0], member_coords[1], hinge_coords)
                hinge_key = " ".join([str(coord) for coord in hinge_coords])
                is_occupied = self.is_occupied_coords(hinge_key)

                if valid_hinge_coords and not is_occupied:
                    self.add_support(hinge_coords, "EC Hinge", hinge_key)
                    break

            while True:
                member_end_coords = query.one_point_coords("End member")
                if not member_end_coords:
                    self.remove_ec_hinge(hinge_key)
                    return None

                member_end_key = f"{hinge_coords[0]} {hinge_coords[1]} {member_end_coords[0]} {member_end_coords[1]}"
                is_occupied = self.is_occupied_coords(member_end_key)

                if is_occupied:
                    print("Coordinate is occupied. Please try another coordinate.")
                else:
                    self.add_member(hinge_coords, member_end_coords)
                    return None

    def hinge_two_member(self):
        """
        Adds an ec hinge connected to two members in the structure.

        This method guides the user through the process of adding an ec hinge between two members.
        The user is prompted to select the placement option for the first member and input the coordinates.
        The start coordinate of the first member should be connected to an existing member/support, and the
        end coordinate will be the coordinate of the hinge. The end coordinate of the first member will be the
        start coordinate of the second member. The user is then prompted to input the coordinates for the
        end of the second member. If the user cancels the operation, the added members and hinge are removed.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used as part of the process to add ec hinges between two members
        in the structure during the construction phase.
        """
        while True:
            print("\n=========================================================\n")
            print("Note:")
            print("• Plot: First member -> Hinge -> Last Member")
            print("• The start coordinate of the first member should be connected to member/support.")
            print("• The end coordinate of the first member will be the coordinate of hinge.")
            print("• The end coordinate of the first member will be the start coordinate of the second member.")
            
            while True:
                option = query.member_placement()

                first_member_coords = query.two_point_coords("First member")
                if not first_member_coords:
                    return None
                
                [[x1, y1], [x2, y2]] = first_member_coords

                if option == '3':
                    return None
                elif option == '1':
                    member_coords = self.exists_member_coords("Member coordinate where you'll connect the first member")
                    
                    if not member_coords:
                        return None
                else:
                    is_occupied = self.is_occupied_coords(f"{x1} {y1}")

                    if not is_occupied:
                        print("Invalid input! Please try again.")
                        continue

                first_member_key = f"{x1} {y1} {x2} {y2}"
                hinge_key = f"{x2} {y2}"
                is_occupied = self.is_occupied_coords(first_member_key)

                if is_occupied:
                    print("Coordinate is occupied. Please try another coordinate.")
                else:
                    self.add_member(first_member_coords[0], first_member_coords[1])
                    self.add_support(first_member_coords[1], "EC Hinge", hinge_key)
                    break

            while True:
                end_member_coords = query.one_point_coords("End second member")
                if not end_member_coords:
                    self.remove_member(first_member_key)
                    self.remove_ec_hinge(hinge_key)
                    return None
                self.add_member(first_member_coords[1], end_member_coords)
                return None
            
    def ec_roller(self):
        """
        Adds an ec roller to the structure based on user-selected roller type.

        This method checks if there are occupied coordinates in the structure. If not, it informs the user
        that a roller cannot be added without a support and returns `None`. If there are occupied coordinates,
        the method prompts the user to select a roller type using the `query.roller_type` function. If the user
        cancels the operation or selects the '3' option, the method returns `None`. If the user selects the
        '1' option, it calls the `roller_vertical` method. Otherwise, it calls the `roller_horizontal` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used to interactively add ec rollers to the structure during the
        construction phase.
        """
        if len(self.occupied_coords.values()) == 0:
            print("Cannot add a roller! Please add a support first.")
            return None

        option = query.roller_type()

        if option == '3':
            return None

        if option == '1':
            self.roller_vertical()
        else:
            self.roller_horizontal()

    def roller_vertical(self):
        """
        Adds a vertical ec roller to the structure between two members.

        This method guides the user through the process of adding a vertical ec roller between two
        members. The user is prompted to input coordinates for the first member. The method checks if the first
        member is vertical (i.e., if the x-coordinates of its two points are equal). If not, the user is prompted
        to try again. Once a valid first member is specified, it is added to the structure. The user is then prompted
        to select the placement option for the roller (to the left or right of the first member's end). The roller
        support is added to the structure accordingly. Finally, the user is prompted to input the coordinates for the
        end of the last member, and if the operation is canceled, the added members and roller are removed.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used as part of the process to add vertical ec rollers between two
        members in the structure during the construction phase.
        """
        while True:
            print("\n=========================================================\n")
            print("Note:")
            print("• Plot: First member -> Roller -> Last Member")
            print("• The roller is placed to the left or right of the end of the first member")
            print("• The start coordinate of last member may at the left or right of the roller")
            
            first_member_coords = query.two_point_coords("First member")
            if not first_member_coords:
                return None

            [[x1, y1], [x2, y2]] = first_member_coords

            if not (x1 == x2):
                print("The member is not vertical! X coordinates of two points are not equal.")
                continue

            first_member_key = f"{x1} {y1} {x2} {y2}"
            is_occupied_by_member = self.is_occupied_coords(first_member_key)

            if is_occupied_by_member :
                print("Coordinate is occupied. Please try another coordinate.")
                continue
                
            self.add_member(first_member_coords[0], first_member_coords[1])
            
            roller_placement_option = query.vertical_ec_roller_placement()
            
            if not roller_placement_option:
                self.remove_member(first_member_key)
                return None
            elif roller_placement_option == '1':
                x2 -= 1
            else:
                x2 += 1

            roller_key = f"{x2} {y2}"
            is_occupied_support = self.is_occupied_coords(roller_key)

            if is_occupied_support:
                print("Coordinate is occupied. Please try another coordinate.")
                continue

            self.add_support([x2, y2], "EC Roller", roller_key)

            if roller_placement_option == '1':
                x2 -= 1
            else:
                x2 += 1

            print(f"The starting coordinate of last member is [{x2}, {y2}]")

            last_member_end_coords = query.one_point_coords("Last member end")

            if not last_member_end_coords:
                self.remove_member(first_member_key)
                self.remove_ec_roller(roller_key)
                return None
            elif not (last_member_end_coords[0] == x2):
                print("The last member is not vertical! X coordinates of two points are not equal.")
                continue
            
            self.add_member([x2, y2], last_member_end_coords)
            break
                
    def roller_horizontal(self):
        """
        Adds a horizontal ec roller to the structure between two members.

        This method guides the user through the process of adding a horizontal ec roller between two
        members. The user is prompted to input coordinates for the first member. The method checks if the first
        member is horizontal (i.e., if the y-coordinates of its two points are equal). If not, the user is prompted
        to try again. Once a valid first member is specified, it is added to the structure. The user is then prompted
        to select the placement option for the roller (to the top or bottom of the first member's end). The roller
        support is added to the structure accordingly. Finally, the user is prompted to input the coordinates for the
        end of the last member, and if the operation is canceled, the added members and roller are removed.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - This method is typically used as part of the process to add horizontal ec rollers between two
        members in the structure during the construction phase.
        """
        while True:
            print("\n=========================================================\n")
            print("Note:")
            print("• Plot: First member -> Roller -> Last Member")
            print("• The roller is placed to the top or bottom of the end of the first member")
            print("• The start coordinate of last member may at the top or bottom of the roller")
            
            first_member_coords = query.two_point_coords("First member")
            if not first_member_coords:
                return None

            [[x1, y1], [x2, y2]] = first_member_coords

            if not (y1 == y2):
                print("The member is not horizontal! Y coordinates of two points are not equal.")
                continue

            first_member_key = f"{x1} {y1} {x2} {y2}"
            is_occupied_by_member = self.is_occupied_coords(first_member_key)

            if is_occupied_by_member :
                print("Coordinate is occupied. Please try another coordinate.")
                continue
                
            self.add_member(first_member_coords[0], first_member_coords[1])
            
            roller_placement_option = query.horizontal_ec_roller_placement()
            
            if not roller_placement_option:
                self.remove_member(first_member_key)
                return None
            elif roller_placement_option == '1':
                y2 += 1
            else:
                y2 -= 1

            roller_key = f"{x2} {y2}"
            is_occupied_support = self.is_occupied_coords(roller_key)

            if is_occupied_support:
                print("Coordinate is occupied. Please try another coordinate.")
                continue

            self.add_support([x2, y2], "EC Roller", roller_key)

            if roller_placement_option == '1':
                y2 += 1
            else:
                y2 -= 1

            print(f"The starting coordinate of last member is [{x2}, {y2}]")

            last_member_end_coords = query.one_point_coords("Last member end")

            if not last_member_end_coords:
                self.remove_member(first_member_key)
                self.remove_ec_roller(roller_key)
                return None
            elif not (last_member_end_coords[1] == y2):
                print("The last member is not horizontal! Y coordinates of two points are not equal.")
                continue
            
            self.add_member([x2, y2], last_member_end_coords)
            break

    def is_occupied_coords(self, key):
        """
        Checks if the specified coordinates are occupied in the structure.

        This method takes a key representing coordinates and checks if the corresponding position is occupied
        in the structure. The key is typically generated based on the coordinates of a point or a range of points
        in the structure.

        Parameters:
        - self: The instance of the Structure class.
        - key (str): A string key representing the coordinates to check.

        Returns:
        - bool: True if the coordinates are occupied, False otherwise.

        Note:
        - The method utilizes the `occupied_coords` dictionary in the Structure class to store information about
        occupied coordinates in the structure.
        """
        return self.occupied_coords.get(key)

    def exists_member_coords(self, name = "Member"):
        """
        Checks if the specified member coordinates exist and are occupied in the structure.

        This method prompts the user to input coordinates for a member (defaultly named "Member") and checks if
        the specified member coordinates exist in the structure. If the coordinates are found and occupied,
        the method returns the coordinates. If the operation is canceled or the coordinates are not occupied,
        the method returns `None`.

        Parameters:
        - self: The instance of the Structure class.
        - name (str, optional): The name or identifier for the member. Defaults to "Member".

        Returns:
        - list or None: The member coordinates if found and occupied, None otherwise.

        Note:
        - The method relies on the `query.two_point_coords` function to interactively collect coordinates from the user.
        - The method uses the `is_occupied_coords` method to check if the specified member coordinates are occupied.
        """
        while True:
            coords = query.two_point_coords(name)

            if not coords:
                return None

            [[x1, y1], [x2, y2]] = coords
            key = f"{x1} {y1} {x2} {y2}"
            is_occupied = self.is_occupied_coords(key)

            if is_occupied:
                return coords
            else:
                print("Member coordinates are not found! Please try another coordinate.")

    def add_support(self, coords, name, key):
        """
        Adds a support to the structure and updates relevant information.

        This method adds a support to the structure, updates the `occupied_coords` dictionary to mark the specified
        coordinates as occupied, and updates information related to the type of support added. The method handles
        different types of supports such as rollers, pins, fixed supports, ec hinges, ec rollers,
        and joints. Additionally, it updates the plot of the entire structure.

        Parameters:
        - self: The instance of the Structure class.
        - coords (list): A list containing the coordinates of the support.
        - name (str): The type or name of the support (e.g., "Roller", "Pin", "Fixed", "EC Hinge", "EC Roller", "Joint").
        - key (str): A string key representing the coordinates of the support.

        Returns:
        - None

        Note:
        - The method updates various attributes and lists in the Structure class to reflect the changes in the structure.
        - It utilizes the `plot_all` method to update the plot of the entire structure after adding the support.
        """
        self.occupied_coords[key] = True

        if name == "Roller":
            self.roller_coords.append(coords)

            if self.members_node.get(key):
                self.reactions += 1
            else:
                self.isolated_support[key] = "Roller"

        elif name == "Pin":
            self.pin_coords.append(coords)

            if self.members_node.get(key):
                self.reactions += 2
            else:
                self.isolated_support[key] = "Pin"

        elif name == "Fixed":
            self.fixed_coords.append(coords)

            if self.members_node.get(key):
                self.reactions += 3
            else:
                self.isolated_support[key] = "Fixed"

        elif name == "EC Hinge":
            self.ec_hinge_coords.append(coords)
            self.ec += 1
        elif name == "EC Roller":
            self.ec_roller_coords.append(coords)
            self.ec += 2
        elif name == "joint":
            self.joints_coords.append(coords)
            self.joints += 1

        self.plot_all()

    def add_joint(self, coords):
        """
        Adds a joint to the structure and updates relevant information.

        This method adds a joint to the structure, updates the `joints_coords` list, and increments the count
        of joints in the structure. Additionally, it updates the plot of the entire structure.

        Parameters:
        - self: The instance of the Structure class.
        - coords (list): A list containing the coordinates of the joint.

        Returns:
        - None

        Note:
        - The method is typically used to add joints to the structure during the construction phase.
        - It utilizes the `plot_all` method to update the plot of the entire structure after adding the joint.
        """
        self.joints_coords.append(coords)
        self.joints += 1
        self.plot_all()

    def remove_isolated_support(self, coords):
        """
        Removes an isolated support from the structure and updates relevant information.

        This method removes an isolated support from the structure based on the specified coordinates, and
        updates relevant information, such as the type of support and the reactions in the structure.

        Parameters:
        - self: The instance of the Structure class.
        - coords (list): A list containing the coordinates of the isolated support.

        Returns:
        - None

        Note:
        - The method checks if an isolated support exists at the specified coordinates and removes it.
        - The reactions in the structure are updated based on the type of support removed (Roller, Pin, or Fixed).
        """
        [x, y] = coords

        if self.isolated_support.get(f"{x} {y}"):
            support_type = self.isolated_support.pop(f"{x} {y}")

            if support_type == "Roller":
                self.reactions += 1
            elif support_type == "Pin":
                self.reactions += 2
            elif support_type == "Fixed":
                self.reactions += 3

    def add_member(self, start_coords, end_coords):
        """
        Adds a member to the structure and updates relevant information.

        This method adds a member to the structure based on the specified start and end coordinates,
        updates the `members_node` dictionary to reflect the connections of nodes, removes isolated supports
        at the start and end coordinates, updates the `occupied_coords` dictionary to mark the member as occupied,
        increments the count of members, and updates lists containing x and y coordinates of members. Additionally,
        it updates the plot of the entire structure.

        Parameters:
        - self: The instance of the Structure class.
        - start_coords (list): A list containing the coordinates of the starting point of the member.
        - end_coords (list): A list containing the coordinates of the ending point of the member.

        Returns:
        - None

        Note:
        - The method updates various attributes and lists in the Structure class to reflect the changes in the structure.
        - It utilizes the `plot_all` method to update the plot of the entire structure after adding the member.
        """
        [x1, y1] = start_coords
        [x2, y2] = end_coords
        
        if not self.members_node.get(f"{x1} {y1}"):
            self.members_node[f"{x1} {y1}"] = 1
        else:
            self.members_node[f"{x1} {y1}"] += 1

        if not self.members_node.get(f"{x2} {y2}"):
            self.members_node[f"{x2} {y2}"] = 1
        else:
            self.members_node[f"{x2} {y2}"] += 1

        self.remove_isolated_support(start_coords)
        self.remove_isolated_support(end_coords)

        key = f"{x1} {y1} {x2} {y2}"
        self.occupied_coords[key] = True

        reversed_key = f"{x2} {y2} {x1} {y1}"
        self.occupied_coords[reversed_key] = True

        self.members += 1

        self.members_x_coords.append([x1, x2])
        self.members_y_coords.append([y1, y2])
        self.plot_all()

    def can_plot_joint(self, coords):
        """
        Checks if a joint can be plotted at the specified coordinates.

        This method verifies whether a joint can be plotted at the specified coordinates based on the following conditions:
        - The coordinates must correspond to a node with at least two connected members.
        - The joint must not have been plotted previously at the same coordinates.

        Parameters:
        - self: The instance of the Structure class.
        - coords (list): A list containing the coordinates of the joint.

        Returns:
        - bool: True if a joint can be plotted; False otherwise.

        Note:
        - The method checks the conditions to determine if a joint can be successfully plotted at the specified coordinates.
        """
        [x, y] = coords

        if self.members_node.get(f"{x} {y}") == None or self.members_node.get(f"{x} {y}") < 2 or self.plotted_joints.get(f"{x} {y}"):
            return False
        
        self.plotted_joints[f"{x} {y}"] = True
        return True

    def remove_member(self, key):
        """
        Removes a member from the structure and updates relevant information.

        This method removes a member from the structure based on the specified key, which represents the
        coordinates of the member. It updates the lists containing x and y coordinates of members, removes
        entries related to the member from the `occupied_coords` dictionary, and decrements the count of members.

        Parameters:
        - self: The instance of the Structure class.
        - key (str): A string representing the key associated with the member's coordinates.

        Returns:
        - None

        Note:
        - The method updates various attributes and lists in the Structure class to reflect the changes in the structure.
        """
        [x1, y1, x2, y2] = key.split(" ")

        self.members_x_coords.pop()
        self.members_y_coords.pop()

        self.occupied_coords.pop(f"{x1} {y1} {x2} {y2}")
        self.occupied_coords.pop(f"{x2} {y2} {x1} {y1}")

        self.members -= 1

    def remove_ec_hinge(self, key):
        """
        Removes an ec hinge from the structure and updates relevant information.

        This method removes an ec hinge from the structure based on the specified key, which represents the
        coordinates of the hinge. It updates the `occupied_coords` dictionary to remove the entry related to the hinge,
        removes the hinge coordinates from the `ec_hinge_coords` list, and decrements the count of ec hinges (ec).

        Parameters:
        - self: The instance of the Structure class.
        - key (str): A string representing the key associated with the hinge's coordinates.

        Returns:
        - None

        Note:
        - The method updates various attributes and lists in the Structure class to reflect the changes in the structure.
        """
        self.occupied_coords.pop(key)
        self.ec_hinge_coords.pop()
        self.ec -= 1

    def remove_ec_roller(self, key):
        """
        Removes an ec roller from the structure and updates relevant information.

        This method removes an ec roller from the structure based on the specified key, which represents the
        coordinates of the roller. It updates the `occupied_coords` dictionary to remove the entry related to the roller,
        removes the roller coordinates from the `ec_roller_coords` list, and decrements the count of ec rollers (ec).

        Parameters:
        - self: The instance of the Structure class.
        - key (str): A string representing the key associated with the roller's coordinates.

        Returns:
        - None

        Note:
        - The method updates various attributes and lists in the Structure class to reflect the changes in the structure.
        """
        self.occupied_coords.pop(key)
        self.ec_roller_coords.pop()
        self.ec -= 1

    def support(self):
        """
        Adds a support to the structure based on the user's choice.

        This method prompts the user to choose a type of support (roller, pin, fixed) and calls the corresponding
        method to add that type of support to the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method interacts with the user through the `query.support_type()` method to determine the type of support to add.
        - It then calls the appropriate support method (roller, pin, fixed) based on the user's choice.
        """
        support_type = query.support_type()

        if support_type == "4":
            return None

        if support_type == "1":
            self.roller()
        elif support_type == "2":
            self.pin()
        elif support_type == "3":
            self.fixed()

    def joint(self):
        """
        Adds a joint to the structure at the specified coordinates.

        This method prompts the user to input coordinates for a joint and checks if a joint can be plotted at those coordinates.
        If conditions are met, it calls the `add_joint` method to add the joint to the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method interacts with the user through the `query.one_point_coords("Joint")` method to get joint coordinates.
        - It checks if a joint can be plotted at the specified coordinates using the `can_plot_joint` method.
        - If conditions are met, it calls the `add_joint` method to add the joint to the structure.
        """
        while True:
            coords = query.one_point_coords("Joint")

            if not coords:
                return None

            if self.can_plot_joint(coords):
                self.add_joint(coords)
                break
            else:
                print("Cannot apply joint in this coordinate! Please try again.")
                continue

    def release(self):
        """
        Adds a release (ec hinge or ec roller) to the structure based on the user's choice.

        This method checks if there are existing supports in the structure. If so, it prompts the user to choose the type
        of release (ec hinge or ec roller) and calls the corresponding method to add that type of release.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method interacts with the user through the `query.release_type()` method to determine the type of release to add.
        - It then calls the appropriate release method (ec hinge or ec roller) based on the user's choice.
        """
        if len(self.occupied_coords.values()) == 0:
            print("Cannot add a release! Please add a support first.")
            return None

        support_type = query.release_type()

        if support_type == "3":
            return None

        if support_type == "1":
            self.ec_hinge()
        elif support_type == "2":
            self.ec_roller()

    def beams(self):
        """
        Manages the addition of beams, supports, releases, and displays the current structure.

        This method presents a menu to the user for interacting with the structure. The user can choose to:
        1. Add a beam member using the `member` method.
        2. Add a support using the `support` method.
        3. Add a release (ec hinge or ec roller) using the `release` method.
        4. Display the current structure using the `plot_all` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method interacts with the user through various `query` methods to gather input for different options.
        - It calls specific methods based on the user's chosen option to modify the structure accordingly.
        """
        while True:
            option = query.beam_options()

            if option == '1':
                self.member()
            elif option == '2':
                self.support()
            elif option == '3':
                self.release()
            elif option == '4':
                self.plot_all()             

    def trusses(self):
        """
        Manages the addition of truss members, supports, joints, and displays the current structure.

        This method presents a menu to the user for interacting with the truss structure. The user can choose to:
        1. Add a truss member using the `member` method.
        2. Add a support using the `support` method.
        3. Add a joint using the `joint` method.
        4. Display the current truss structure using the `plot_all` method.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method interacts with the user through various `query` methods to gather input for different options.
        - It calls specific methods based on the user's chosen option to modify the truss structure accordingly.
        """
        while True:
            option = query.trusses_options()

            if option == '1':
                self.member()
            elif option == '2':
                self.support()
            elif option == '3':
                self.joint()
            elif option == '4':
                self.plot_all()   

    def compute_beam_di(self):
        """
        Computes the degree of indeterminacy for a beam structure and updates the result accordingly.

        This method calculates the degree of indeterminacy (DI) for a beam structure based on the number of reactions,
        ec supports, and joints in the structure. It then updates the result string to reflect the type of structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method updates the `degree_of_indeterminacy` attribute in the structure instance.
        - It also updates the `result` attribute with a string indicating the type of structure (externally determinate,
        externally indeterminate, or unstable).
        - The result is printed for externally determinate structures.
        """
        self.degree_of_indeterminacy = self.reactions - (3 + self.ec)
        
        if self.degree_of_indeterminacy < 0:
            self.result = "Statistically Unstable Externally"
        elif self.degree_of_indeterminacy == 0:
            self.result = "Statistically Determinate Externally"
            print(self.result)
        else:
            self.result = f"Statically Indeterminate Externally\nDI = {self.degree_of_indeterminacy}"

    def compute_trusses_di(self):
        """
        Computes the degree of indeterminacy for a truss structure and updates the result accordingly.

        This method calculates the degree of indeterminacy (DI) for a truss structure based on the number of members,
        reactions, and joints in the structure. It then updates the result string to reflect the type of structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method updates the `degree_of_indeterminacy` attribute in the structure instance.
        - It also updates the `result` attribute with a string indicating the type of structure (externally determinate,
        externally indeterminate, or unstable).
        """
        self.degree_of_indeterminacy = (self.members + self.reactions) - 2 * self.joints
        
        if self.degree_of_indeterminacy < 0:
            self.result = "Statistically Unstable Externally"
        elif self.degree_of_indeterminacy == 0:
            self.result = "Statistically Determinate Externally"
        else:
            self.result = f"Statically Indeterminate Externally\nDI = {self.degree_of_indeterminacy}"

    def start(self):
        """
        Initiates the process of defining and analyzing a structural system.

        This method prompts the user to choose between solving a beam or truss structure and then calls the
        corresponding method ('beams' or 'trusses') to allow the user to interactively define and analyze the structure.

        Parameters:
        - self: The instance of the Structure class.

        Returns:
        - None

        Note:
        - The method interacts with the user through the `query.structure_to_solve` method to determine the type of
        structure the user wants to solve.
        - Depending on the user's choice, it calls either the 'beams' or 'trusses' method to proceed with the definition
        and analysis of the structural system.
        """
        option = query.structure_to_solve()

        if option == '1':
            self.structure_to_solve = 'beam'
            self.beams()
        elif option == '2':
            self.structure_to_solve = 'trusses'
            self.trusses()

# Structure class instantiation
structure = Structure()

# Start plotting the structure
structure.start()