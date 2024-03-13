import math
import random
import sys
import os
import neat
import pygame
pygame.font.init()

WIN_WIDTH = 1150
WIN_HEIGHT = 670

BORDER_COLOR = (0,0,0,0)

CAR_IMG = pygame.transform.scale_by(pygame.image.load(os.path.join("imgs", "car.png")), 0.25)
CAR_IMG = pygame.transform.flip(CAR_IMG, True, False)
TRACK_IMGS = [pygame.image.load(os.path.join("imgs", "oval_track.png")),
               pygame.transform.scale_by(pygame.image.load(os.path.join("imgs", "oval_track_valid.png")), 1)]


FONT = pygame.font.SysFont("Arial", 20)

GEN = 0

class Car:
    MAX_STEERING_ANGLE = math.pi / 6
    STEERING_STEPS = 30
    FRICTION = 0.9
    DRAG = 0.001
    HORSEPOWER = 60

    def __init__(self, x=550, y=150):
        self.x = x
        self.y = y
        self.pos = [x, y]
        self.angle = 0
        self.image = CAR_IMG
        self.speed = -5
        self.radars = []
        self.img_x = CAR_IMG.get_width()
        self.img_y = CAR_IMG.get_height()
        self.center = [self.x + self.img_x / 2, self.y + self.img_y / 2]
        self.steering_angle = 0
        self.alive = True
        self.distance = 0
        self.time = 0
        self.corners = []

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def get_speed(self):
        return self.speed

    def set_speed(self, num):
        self.speed = num

    def get_position(self):
        return self.pos

    def set_position(self, x, y):
        self.pos = (x,y)

    def get_angle(self):
        return self.angle

    def get_steering_angle(self) -> float:
        return self.steering_angle

    def turn_left(self) -> None:
        #self.set_steering_angle(self.get_steering_angle() - 2 * self.MAX_STEERING_ANGLE / self.STEERING_STEPS)
        self.angle -= 10
    def turn_right(self) -> None:
        #self.set_steering_angle(self.get_steering_angle() + 2 * self.MAX_STEERING_ANGLE / self.STEERING_STEPS)
        self.angle += 10
    def press_gas(self):
        self.speed -= 1

    def reduce_speed(self):
        if self.speed <= -1:
            self.set_speed(1)
        else:
            self.speed += 1

    def draw(self, window) -> None:
        window.blit(self.image, self.pos)
        self.draw_radar(window)

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)


    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 1000 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 1000:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            if i > 4:
                break
            return_values[i] = int(radar[1] / 30)
        return return_values

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    def get_reward(self):
        return self.distance / (self.img_x / 2)

    def update(self, window, line_number):
        #if self.speed == 0:
            #self.speed = -5

        raw_num = line_number % 4
        if raw_num == 0:

            pygame.draw.line(TRACK_IMGS[1], (255, 0, 0), (300, 300), (300, 50), 2)
        elif raw_num == 1:
            pygame.draw.line(TRACK_IMGS[1], (255, 0, 0), (300, 600), (300, 350), 2)
        elif raw_num == 2:
            pygame.draw.line(TRACK_IMGS[1], (255, 0, 0), (850, 300), (850, 50), 2)
        elif raw_num == 3:
            pygame.draw.line(TRACK_IMGS[1], (255, 0, 0), (850, 600), (850, 350), 2)



        self.image = self.rotate_center(CAR_IMG, self.angle)
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[0] = max(self.pos[0], 20)
        self.pos[0] = min(self.pos[0], WIN_WIDTH - 50)

        self.distance += self.speed
        self.time += 1

        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.pos[1] = max(self.pos[1], 20)
        self.pos[1] = min(self.pos[1], WIN_WIDTH - 50)

        self.center = [int(self.pos[0]) + self.img_x / 2, int(self.pos[1]) + self.img_y / 2]

        length = 0.5 * self.img_x
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.check_collision(TRACK_IMGS[1])
        self.radars.clear()

        self.draw(window)

        angle_delta = [180, -90, 90, 135, -135]
        for angle in angle_delta:
            self.check_radar(angle, TRACK_IMGS[1])

    def check_collision(self, game_map):
        for point in self.corners:
            # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                return False
        return True

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rotated_image.get_rect()
        rotated_rectangle.center = rotated_image.get_rect().center
        #rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

    def get_distance(self):
        return self.distance

    def checkpoint(self, surface):
        if surface.get_at((int(self.center[0]), int(self.center[1]))) == (255,0,0):
            return True
        return False


def deg_to_radian(num):
    return math.pi * num / 180

def draw_window(window, cars):
    window.blit(TRACK_IMGS[1], (0,0))
    window.blit(TRACK_IMGS[0], (0,0))

    text = FONT.render("Still Alive: " + str(len(cars)), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (650, 300)
    window.blit(text, text_rect)

    text = FONT.render("Generation: " + str(GEN), True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (500, 300)
    window.blit(text, text_rect)

    for car in cars:
        car.draw(window)


    pygame.display.update()
def main(genomes, config):
    ge = []
    cars = []
    nets = []
    alive = True
    line_number = 0
    # distances = [0,0,0,0,0]
    for _, genome in genomes:  # genome is a tuple, with ID as its first element, (1,genome object)
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car())
        ge.append(genome)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    run = True

    clock = pygame.time.Clock()


    global GEN
    GEN += 1

    counter = 0

    while run:
        clock.tick(60)  # 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())  # add get data
            choice = output.index(max(output))
            #if choice == 0: # disabling the ability to change speed momentarily
                #car.press_gas()
            if choice == 1:
                car.turn_left()
            elif choice == 2:
                car.turn_right()
            elif choice == 3:
                car.turn_right()
            else:
                car.turn_left()


        for i, car in enumerate(cars):
            if car.check_collision(TRACK_IMGS[1]):
                car.update(win, line_number)
                ge[i].fitness += .02
            else:
                ge[i].fitness -= 1
                ge.pop(i)
                cars.remove(car)
                nets.pop(i)

        for i, car in enumerate(cars):
            HIT = car.checkpoint(TRACK_IMGS[1])
            if HIT:
                line_number += 1
                ge[i].fitness += 3


        if len(cars) == 0:
            break

        counter += 1
        if counter == 30 * 40:  # Stop After About 20 Seconds
            break

        draw_window(win, cars)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)  # load config file
    p = neat.Population(config)  # set population

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,100)

    print('\nBest genome:\n{!s}'.format(winner))



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)