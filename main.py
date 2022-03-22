import pygame
import math

pygame.init()

# window size and name
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving planet simulator")

# planet color
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GRAY = (80, 78, 81)

class Planet:
    # Constans values
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU #1AU = 100 pixel
    TIMESTEP = 3600*24 # 1 day

    def __init__ (self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distane_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        """
        Drawing the planet in scales
        win - parameters of window
        """
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x,y), self.radius)

    def attraction (self, other):

        """
        algoritm to creating moving planets force
        other - planets coordinates
        """
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass /distance**2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):

        """
        updating planet move xy coordinates in time
        planets - list of planets
        """

        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    # Objects created from Planet class
    sun = Planet(0, 0 , 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23 )
    mars.y_vel = 24.007 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 0.33 * 10**23)
    mercury.y_vel = 47.4 *1000

    venus = Planet( 0.723 * Planet. AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 *1000

#    jupiter = Planet(5.203 * Planet.AU, 0, 20, DARK_GRAY, 1.9 * 10**27)
#    jupiter.y_vel = 13.07 * 1000

    # list of planets drawing in model
    planets = [sun, earth, mars, mercury, venus,]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # Loop drawing and updating model
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    pygame.quit()

main()
