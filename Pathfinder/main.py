import sys


class Node:
    def __init__(self, state, action, parent):
        self.action = action
        self.state = state
        self.parent = parent


class Stack:
    def __init__(self):
        self.frontier = []
        self.processed = []

    def add_node(self, node):
        if self.search(node=node):
            self.frontier.append(node)

    def add_explored(self, node):
        self.processed.append(node.state)

    def search(self, node):
        for pnode in self.processed:
            if pnode == node.state:
                return False
        return True

    def remove_node(self):
        if len(self.frontier) == 0:
            raise Exception("empty frontier")
        else:
            return self.frontier.pop()


class Queue(Stack):
    def remove_node(self):
        return self.frontier.pop(0)


def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


class NotepadMaze:
    def __init__(self, filename):

        self.num_explored = 0
        self.explored = None

        # Read file and set height and width of maze
        contents = open(filename).read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbours(self, state):
        # unpacked tuple
        row, column = state
        coordinates = [("left", (row, column - 1)), ("up", (row + 1, column)), ("down", (row - 1, column)),
                       ("right", (row, column + 1))]

        ans = []
        for action, (x, y) in coordinates:
            if x in range(self.height) and y in range(self.width) and not self.walls[x][y]:
                ans.append((action, (x, y)))

        return ans

    def solve(self):
        # set do while with frontier as function

        frontier = Stack()
        # frontier = Queue()

        frontier.add_node(node=Node(state=self.start, parent=None, action=None))
        frontier.add_explored(node=Node(state=self.start, parent=None, action=None))
        k = 0

        while True:

            if not frontier.frontier:
                break

            k += 1
            # print(k)
            # print(frontier.frontier)
            node = frontier.remove_node()

            if self.goal == node.state:
                actions = []
                states = []
                self.explored = frontier.processed
                self.num_explored = len(self.explored)
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)

            for action, state in self.neighbours(state=node.state):
                if frontier.frontier:
                    for fnode in frontier.frontier:
                        if state != fnode.state:
                            child = Node(state=state, action=action, parent=node)
                            frontier.add_node(child)
                            frontier.add_explored(node=child)
                else:
                    child = Node(state=state, action=action, parent=node)
                    frontier.add_node(child)
                    frontier.add_explored(node=child)

            # if frontier is empty, no soln
            # Remove node from frontier
            # If current state/ removed node is goal, end loop
            # get next state/nodes

    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

m = NotepadMaze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze.png", show_explored=True)
m.output_image("maze.png", show_solution=True)
