import sys

from crossword import Variable, Crossword


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            values_to_remove = set()
            for value in self.domains[var]:
                if len(value) is not var.length:
                    values_to_remove.add(value)
            for value in values_to_remove:
                self.domains[var].remove(value)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is not None:
            values_to_remove = set()
            x_index = self.crossword.overlaps[x, y][0]
            y_index = self.crossword.overlaps[x, y][1]
            for x_value in self.domains[x]:
                correspondes = False
                for y_value in self.domains[y]:
                    if x_value[x_index] == y_value[y_index]:
                        correspondes = True
                        break
                if correspondes == False:
                    values_to_remove.add(x_value)
            if len(values_to_remove) > 0:
                for value in values_to_remove:
                    self.domains[x].remove(value)
                return True
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Get a queue of arcs
        if arcs:
            queue = arcs
        else:
            queue = []
            for var1 in self.crossword.variables:
                for var2 in self.crossword.variables:
                    if var1 is not var2 and self.crossword.overlaps[var1, var2] is not None:
                        queue.append((var1, var2))

        # For each arc enforce arc consistency
        while len(queue) > 0:
            arc = queue.pop(0)
            if self.revise(arc[0], arc[1]) == True:
                # If there are no values in arc[0]'s domain that is consistent, then the problem is impossible
                if len(self.domains[arc[0]]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(arc[0]):
                    if neighbor is not arc[1]:
                        queue.append((neighbor, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        used_values = set()
        for var in assignment:
            # Every value is the correct length
            if len(assignment[var]) is not var.length:
                return False
            # There are no conflicts between neighboring variables
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    var_index = self.crossword.overlaps[var, neighbor][0]
                    neighbor_index = self.crossword.overlaps[var, neighbor][1]
                    if assignment[var][var_index] is not assignment[neighbor][neighbor_index]:
                        return False
            # All values are distinct
            if assignment[var] in used_values:
                return False
            used_values.add(var)
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Create a list of tuples that contain values and the number of values they rule out for neighboring variables, then sort it according to n
        n_list = []
        for value in self.domains[var]:
            n = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    for neighborValue in self.domains[neighbor]:
                        var_index = self.crossword.overlaps[var, neighbor][0]
                        neighbor_index = self.crossword.overlaps[var, neighbor][1]
                        if value[var_index] is not neighborValue[neighbor_index]:
                            n += 1
            n_list.append((value, n))
        n_list = sorted(n_list, key=lambda x: x[1])

        # Take the first elements in the tuples to create a values list
        value_list = []
        for value in n_list:
            value_list.append(value[0])
        return value_list
            
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = []
        for var in self.crossword.variables:
            if var not in assignment:
                domain_count = len(self.domains[var])
                arc_count = len(self.crossword.neighbors(var))
                unassigned_vars.append((var, domain_count, arc_count))
        unassigned_vars = sorted(unassigned_vars, key=lambda x: x[2], reverse=True)
        unassigned_vars = sorted(unassigned_vars, key=lambda x: x[1], reverse=True)
        return unassigned_vars[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None
        
        ''' (With Inference)
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            old_domains = self.domains.copy()
            if self.consistent(assignment):
                arcs = []
                for neighbor in self.crossword.neighbors(var):
                    if neighbor not in assignment:
                        arcs.append((neighbor, var))
                inferences_made = self.ac3()
                if inferences_made == False:
                    continue
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
            self.domains = old_domains
        return None
        '''


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
