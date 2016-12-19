import pygame, random
from pygame.locals import *

#Global var
screen_caption = "DFS Maze Generation"
pixel = 8

class Maze:
    def __init__(self, mazeLayer, screen_width, screen_height, width, height):
        self.mazeArray = []
        self.state = 'create'
        self.mLayer = mazeLayer
        self.width = width
        self.height = height
        self.mLayer.fill((0, 0, 0, 0))

        for y in range(self.height):
            #Draw vertical grid
            pygame.draw.line(self.mLayer, (0, 0, 0, 255), (0, y * pixel), (screen_width, y * pixel))
            for x in range(self.width):
                self.mazeArray.append(0)
                if (y == 0):
                    #Draw horizontal grid
                    pygame.draw.line(self.mLayer, (0, 0, 0, 255), (x * pixel, 0), (x * pixel, screen_height))

        self.totalCells = self.width * self.height
        self.currentCell = random.randint(0, self.totalCells - 1)
        self.visitedCells = 1
        self.cellStack = []
        #West, South, East, North
        self.compass = [(-1, 0), (0, 1), (1, 0), (0, -1)]


    def update(self):
        if self.state == 'create':
            if self.visitedCells >= self.totalCells:
                self.currentCell = 0
                self.cellStack = []
                self.state = 'solve'
                print("Finished")
                return

            moved = False

            while(moved == False):
                #Compute actual grid coordinates
                x = self.currentCell % self.width
                y = self.currentCell // self.width

                #Find all neighbors of CurrentCell with all walls intact
                neighbors = []
                for i in range(len(self.compass)):
                    #Neighbor coordinates
                    neighbor_x = x + self.compass[i][0]
                    neighbor_y = y + self.compass[i][1]

                    #Check the borders
                    if ((neighbor_x >= 0) and (neighbor_y >= 0) and
                        (neighbor_x < self.width) and (neighbor_y < self.height)):
                        #Has it been visited
                        #0x000F = 15 (upperbound), if equal to this => cell is visited
                        #either all cell tried this or it has been visited
                        if (self.mazeArray[(neighbor_y * self.width + neighbor_x)] & 0x000F) == 0:
                            neighbor_index = neighbor_y * self.width + neighbor_x
                            #Append value (in array index) of coordinates + value after shifting bits by 0, 1, 2, or 3
                            neighbors.append((neighbor_index, 1 << i))

                if len(neighbors) > 0:
                    #Choose neighbor at random
                    current_neighbor = random.randint(0, len(neighbors) - 1)
                    current_neighbor_loc , direction = neighbors[current_neighbor]

                    #Get grid's top left coordinates
                    grid_x = x * pixel
                    grid_y = y * pixel

                    #if direction is West
                    if direction & 1:
                        #Knock down East
                        self.mazeArray[current_neighbor_loc] |= (4)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (grid_x, grid_y + 1),
                                         (grid_x, grid_y + pixel - 1))
                    #if direction is South
                    elif direction & 2:
                        #Knock down North
                        self.mazeArray[current_neighbor_loc] |= (8)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (grid_x + 1, grid_y + pixel),
                                         (grid_x + pixel - 1, grid_y + pixel))
                    #if direction is East
                    elif direction & 4:
                        #Knock down West
                        self.mazeArray[current_neighbor_loc] |= (1)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (grid_x + pixel, grid_y + 1),
                                         (grid_x + pixel, grid_y + pixel - 1))
                    #if direction is North
                    elif direction & 8:
                        #Knock down South
                        self.mazeArray[current_neighbor_loc] |= (2)
                        pygame.draw.line(self.mLayer, (0, 0, 0, 0), (grid_x + 1, grid_y),
                                         (grid_x + pixel - 1, grid_y))

                    self.mazeArray[self.currentCell] |= direction

                    #Push currentCell location to the cellStack
                    self.cellStack.append(self.currentCell)

                    # Set currentCell to neighbor
                    self.currentCell = current_neighbor_loc

                    #Add 1 to visitiedCells
                    self.visitedCells += 1
                    moved = True

                else:
                    self.currentCell = self.cellStack.pop()

    def draw(self, screen):
        screen.blit(self.mLayer, (0, 0))

def main():
    #Init
    pygame.init()

    height = int(input("Rows: "))
    width = int(input("Columns: "))

    screen_width = width * pixel
    screen_height = height * pixel

    #Create screen + set display ratio + set caption + set mouse
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(screen_caption)
    pygame.mouse.set_visible(0)

    #Create background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    #mazeLayer
    mazeLayer = pygame.Surface(screen.get_size())
    mazeLayer = mazeLayer.convert_alpha()
    mazeLayer.fill((0, 0, 0, 0, ))

    #Init Maze
    newMaze = Maze(mazeLayer, screen_width, screen_height, width, height)

    #Blit background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                print(event.type)
                if event.type == K_ESCAPE:
                    print("Pressed")
                    return

        newMaze.update()

        screen.blit(background, (0, 0))
        newMaze.draw(screen)
        pygame.display.flip()

    return

if __name__ == '__main__':main()
