import matplotlib.pyplot as plt
import re
import math
import validate
import query

class Structure:
    def __init__(self):
        self.occupied_coords = {}
        self.plotted_members = {}
        self.plotted_joints = {}
        self.members_node = {}
        self.isolated_support = {}

        self.members_x_coords = []
        self.members_y_coords = []
        self.roller_coords = []
        self.pin_coords = []
        self.fixed_coords = []
        self.ec_hinge_coords = []
        self.ec_roller_coords = []
        self.joints_coords = []

        # Formula's variables
        self.degree_of_indeterminacy = 0
        self.members = 0
        self.reactions = 0
        self.ec = 0
        self.joints = 0
        self.result = ""

        # Supports = Number of releases
        self.roller_count = 0
        self.pin_count = 0
        self.fixed_count = 0

        # EC = Number of releases
        self.ec_hinge_count = 0
        self.ec_roller_count = 0

        # Trusses
        self.pin_connection_count = 0

        self.structure_to_solve = ''

    def plot_all(self):
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
        for i in range(len(self.members_x_coords)):
            plt.plot(self.members_x_coords[i], self.members_y_coords[i], color='#000000', linewidth=2)

    def plot_rollers(self):
        for coords in self.roller_coords:
            [x, y] = coords
            plt.scatter(x, y, 200, marker='o', color='g')
        
    def plot_pins(self):
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
        for coords in self.fixed_coords:
            [x, y, alignment] = coords

            if alignment == 'vertical':
                plt.scatter(x, y, 1500, marker='|', color='g')
            elif alignment == 'horizontal':
                plt.scatter(x, y, 1500, marker='_', color='g')
    
    def plot_joints(self):
        for coords in self.joints_coords:
            [x, y] = coords
            plt.scatter(x, y, 50, marker='o', color='r')
            
    def plot_ec_hinge(self):
        for coords in self.ec_hinge_coords:
            [x, y] = coords
            plt.scatter(x, y, 200, marker='o', color='blue')
            plt.scatter(x, y, 40, marker='o', color='yellow')

    def plot_ec_roller(self):
        for coords in self.ec_roller_coords:
            [x, y] = coords
            plt.scatter(x, y, 200, marker='o', color='blue')

    def member(self):
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
        return self.occupied_coords.get(key)

    def exists_member_coords(self, name = "Member"):
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
        self.joints_coords.append(coords)
        self.joints += 1
        self.plot_all()

    def remove_isolated_support(self, coords):
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
        [x, y] = coords

        if self.members_node.get(f"{x} {y}") == None or self.members_node.get(f"{x} {y}") < 2 or self.plotted_joints.get(f"{x} {y}"):
            return False
        
        self.plotted_joints[f"{x} {y}"] = True
        return True

    def remove_member(self, key):
        [x1, y1, x2, y2] = key.split(" ")

        self.members_x_coords.pop()
        self.members_y_coords.pop()

        self.occupied_coords.pop(f"{x1} {y1} {x2} {y2}")
        self.occupied_coords.pop(f"{x2} {y2} {x1} {y1}")

        self.members -= 1

    def remove_ec_hinge(self, key):
        self.occupied_coords.pop(key)
        self.ec_hinge_coords.pop()
        self.ec -= 1

    def remove_ec_roller(self, key):
        self.occupied_coords.pop(key)
        self.ec_roller_coords.pop()
        self.ec -= 1

    def support(self):
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
        self.degree_of_indeterminacy = self.reactions - (3 + self.ec)
        
        if self.degree_of_indeterminacy < 0:
            self.result = "Statistically Unstable Externally"
        elif self.degree_of_indeterminacy == 0:
            self.result = "Statistically Determinate Externally"
            print(self.result)
        else:
            self.result = f"Statically Indeterminate Externally\nDI = {self.degree_of_indeterminacy}"

    def compute_trusses_di(self):
        self.degree_of_indeterminacy = (self.members + self.reactions) - 2 * self.joints
        
        if self.degree_of_indeterminacy < 0:
            self.result = "Statistically Unstable Externally"
        elif self.degree_of_indeterminacy == 0:
            self.result = "Statistically Determinate Externally"
        else:
            self.result = f"Statically Indeterminate Externally\nDI = {self.degree_of_indeterminacy}"

    def start(self):
        option = query.structure_to_solve()

        if option == '1':
            self.structure_to_solve = 'beam'
            self.beams()
        elif option == '2':
            self.structure_to_solve = 'trusses'
            self.trusses()

structure = Structure()
structure.start()