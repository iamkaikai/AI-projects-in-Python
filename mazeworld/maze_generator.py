import random

class maze_generator:
    def __init__(self, width, height, edge):
        self.w = width      # int
        self.h = height     # int
        self.e = edge       # boolean
        self.result = []    # list of str
        
    def generator(self):
        for h in range(self.h):
            row = '' 
            for w in range(self.w):
                if self.e and (h in [0, self.h - 1] or w in [0, self.w - 1]):
                    element = 1  # Make the border as wall if edge is True
                    row += '#'
                else:
                    element = random.randint(0, 10)
                    row += '#' if element > 8 else '.'
            self.result.append(row)
        
        return '\n'.join(self.result)

if __name__ == "__main__":
    m = maze_generator(40, 40, True)
    maze = m.generator()
    print(maze)
