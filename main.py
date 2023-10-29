import pygame
import math
import random
import time


# TO DO: Make timer and drawing method for elon crying about crash.
pygame.init()

SCREEN_SIZE = 1600, 1000

win = pygame.display.set_mode(SCREEN_SIZE)

pygame.display.set_caption("Slingshot")



    # S E T T I N G S

global BUDGET
BUDGET = 5000000000

SHIP_MASS = 20
G = 50
FPS = 60
PLANET1_SIZE = 50
PLANET1_MASS = 2000
PLANET1_X, PLANET1_Y = 600, 400
PLANET1 = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET1_SIZE * 2, PLANET1_SIZE * 2))

font_budget = pygame.font.SysFont("Bauhaus 93", 50)

OBJ_SIZE = 5
VEL_SCALE = 100


crash_time = 0
current_time = 0


BG = pygame.transform.scale(pygame.image.load("background.jpg"), (1600, 1200))

ELON = []
ELON.append(pygame.transform.scale(pygame.image.load("elo1.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo2.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo3.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo4.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo5.jpeg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo6.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo7.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo8.jpg"), (800, 500)))
ELON.append(pygame.transform.scale(pygame.image.load("elo9.jpg"), (800, 500)))



WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(PLANET1, (self.x - PLANET1_SIZE, self.y - PLANET1_SIZE))



class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)
        force = (G * self.mass * planet.mass) / distance ** 2
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)
        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)
        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x // 10
        self.y += self.vel_y // 10
    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)


#def success():
#    if level_won:
#        text = (("SUCCESS!), font_budget, WHITE, 25, 25)
#        win.blit(text, (400, 400))
#        time.sleep(3)

def create_ship(location, mouse):
     t_x, t_y = location
     m_x, m_y = mouse
     vel_x = m_x - t_x
     vel_y = m_y - t_y
     obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
     return obj

def draw_budget(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    win.blit(img, (x, y))

def crash_cost():
    global BUDGET
    BUDGET -= int(200000000 + random.random() * 100000000)



def crash_display():
    global crash_time
    x = int(random.random() * 9)
    if current_time - crash_time > 2000:
        win.blit(ELON[x], ((x * 80, x * 80)))



def main():
    running = True
    clock = pygame.time.Clock()

    objects = []
    temp_obj_pos = None
    planet = Planet(PLANET1_X, PLANET1_Y, PLANET1_MASS)

    while running == True:
        clock.tick(FPS / 2)
        global current_time
        current_time = pygame.time.get_ticks()



        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None

                else:
                    temp_obj_pos = mouse_pos
                    
        win.blit(BG, (0,0))
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > 1600 or obj.y < 0 or obj.y > 1000
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET1_SIZE
            if off_screen:
                objects.remove(obj)
            if collided:
                objects.remove(obj)
                crash_cost()
                random_pic = random.random()
                if BUDGET < 4000000000 and BUDGET > 1500000000:# and random_pic < 0.2:
                    crash_time = pygame.time.get_ticks()
                    crash_display()
                if BUDGET < 1500000000 and random_pic < 0.5:
                    crash_time = pygame.time.get_ticks()
                    crash_display()



        draw_budget("Budget: $" + str(BUDGET), font_budget, WHITE, 25, 25)

        planet.draw()
        pygame.display.update()




    pygame.quit()


if __name__ == "__main__":
    main()

