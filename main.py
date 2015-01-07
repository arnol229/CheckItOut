import pygame
import pymunk.pygame_util as pygame_util
import pymunk # for later
import sys
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

buttons = {   
          'left': joystick.get_button(7), 
          'right' : joystick.get_button(5),
          'up' : joystick.get_button(4), 
          'down': joystick.get_button(6),
          'square' : joystick.get_button(15),
          'x' : joystick.get_button(14),
          'circle' : joystick.get_button(13),
          'triangle' : joystick.get_button(12),
          'r1' : joystick.get_button(11),
          'r2' : joystick.get_button(9),
          'l1' : joystick.get_button(10),
          'l2' : joystick.get_button(8),
          'select' : joystick.get_button(0),
          'start' : joystick.get_button(3),
          'l3' : joystick.get_button(1),
          'r3' : joystick.get_button(2),
          'ps' : joystick.get_button(16),
        }

clock = pygame.time.Clock()

windowSize = (800, 600)
screen = pygame.display.set_mode(windowSize)

running = True

space = pymunk.Space()
space.gravity = (0.0, -900.0)
rad = 14
ball_elasticity = 0.8
friction = 0.8
circles = []

def create_circle(position):
    '''
    Creates a circle at a given position
    '''
    mass = 1
    # inertia = pymunk.moment_for_circle(mass, 0, rad)
    inertia = pymunk.inf
    body = pymunk.Body(mass, inertia)
    body.position = position
    # body.position = position
    shape = pymunk.Circle(body, rad)
    shape.elasticity = ball_elasticity
    shape.friction = friction
    space.add(body, shape)
    return shape

def create_line():
    body = pymunk.Body()
    body.position = (400, 600)
    line_shape = pymunk.Segment(body, (-400, -500), (400, -500), 15)
    line_shape.elasticity = 0.5
    line_shape.friction = 0.8
    space.add(line_shape)
    return line_shape

line = create_line()
line.color = (60, 255, 0)

font = pygame.font.SysFont(None, 48)

newCircle = None
# bkg_music = pygame.mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=8192)
pygame.mixer.music.load('sounds/Baldur\'s Gate II Main Theme.mp3')
pygame.mixer.music.play()
snd_bringo = pygame.mixer.Sound('sounds/bringo.wav')
time.sleep(3)
pygame.mixer.music.set_volume(.4)

# bringo_music = pygame.mixer
# bringo_music.init(frequency=44100, size=-16, channels=2, buffer=8192)
# bringo_music.music.load('C:/Users/Bo/Downloads/bringo.mp3')

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(14):
              snd_bringo.play()
              if not newCircle:
                newCircle = create_circle((400,300))
                circles.append(newCircle)
                print(len(circles))
            elif joystick.get_button(5) and newCircle:
                newCircle.body.apply_impulse((100,0),(0,14))
    screen.fill((0, 0, 0))

    # for circle in circles:
        # circlePosition = int(circle.body.position.x), 600 - int(circle.body.position.y)
        # pygame.draw.circle(screen, (255, 0, 0), circlePosition, int(circle.radius), 0)
    pymunk.pygame_util.draw(screen, circles)
    pygame_util.draw(screen, line)

    circleCount = font.render(str(len(circles)), 1, (255, 0, 0))
    screen.blit(circleCount, (10, 10))

    pygame.display.flip()
    space.step(1/60.0)

sys.exit()