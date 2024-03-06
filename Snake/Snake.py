import math
import random
import pygame


class Cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(0, 255, 0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))

        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0  # x direction
        self.dirny = 1  # y direction

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # border checking, if the snake hits any of the walls, it appears on the other side of the screen
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)

                else:
                    c.move(c.dirnx, c.dirny)  # if you haven't hit anything, just keep going

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0

    for i in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        # Draw two lines for every loop
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))  # Draws vertical line, moves horizontally
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))  # Draws horizontal line, moves vertically

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            # Gets a filtered list, filters by position of snake, this ensures that snack cannot spawn on snake body
            continue
        else:
            break
    return x, y


def messageBox(subject, content, score):
    font = pygame.font.Font(None, 36)
    score = "Score: " + str(score)
    text = font.render(score, True, (0,0,0))

    box_width = 300
    box_height = 100
    box_rect = pygame.Rect((size - box_width) // 2, (size - box_height) // 2, box_width, box_height)

    pygame.draw.rect(win, (255,255,255), box_rect)  # Draw a black rectangle
    win.blit(text,
             (box_rect.x + (box_width - text.get_width()) // 2, box_rect.y + (box_height - text.get_height()) // 2))
    pygame.display.flip()

    button_rect = pygame.Rect((size - 150) // 2, box_rect.bottom + 10, 150, 40)
    pygame.draw.rect(win, (0, 128, 255), button_rect)  # Draw a blue button
    button_text = font.render(content, True, (0,0,0))
    win.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                           button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    pygame.display.update()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting_for_key = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    waiting_for_key = False

    pygame.display.update()


def drawSurface(window: object):
    pygame.display.set_caption("Snake by Alec")

    window.fill((0, 0, 0))

    snake.draw(window)

    snack.draw(window)

    drawGrid(size, rows, window)

    pygame.display.flip()


def main():
    global win, size, rows, snake, snack
    size = 500
    rows = 20
    pygame.init()  # Initialize Pygame
    win = pygame.display.set_mode((size, size))
    snake = Snake((0, 255, 0), (10, 10))
    clock = pygame.time.Clock()
    snack = Cube(randomSnack(rows, snake), color=(255, 0, 0))
    # game loop
    flag = True
    while flag:
        pygame.time.delay(50)
        clock.tick(10)

        snake.move()

        if snake.body[0].pos == snack.pos:
            snake.addCube()
            snack = Cube(randomSnack(rows, snake), color=(255, 0, 0))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print("Score: ", len(snake.body))
                messageBox("You lost!", "Play again?", len(snake.body))
                snake.reset((10, 10))
                break

        drawSurface(win)

        # for loop through the event queue
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == pygame.QUIT:
                flag = False


if __name__ == "__main__":
    main()
