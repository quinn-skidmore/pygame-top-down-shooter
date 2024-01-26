
import pygame, sys, random

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, health):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = pos)
        self.velocity = pygame.Vector2(0,0)
        self.health = health

    def take_damage(self,damage):
        self.health -= damage
        if(self.health < 0):
            entities.remove(self)

class Player(Entity):
    def __init__(self, pos, health):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(center = pos)
        self.velocity = pygame.Vector2(0,0)
        self.health = health
    def move(self):
        pass

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Top Down Shooter")

# Create clock to later control frame rate
clock = pygame.time.Clock()

entities = pygame.sprite.Group()
player = Player((100,100),1000)
entities.add(player)
# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))

        # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Update rectangle position based on key presses
    # if keys[pygame.K_LEFT]:
    #     sq.rect.x -= 2
    # if keys[pygame.K_RIGHT]:
    #     sq.rect.x += 2
    # if keys[pygame.K_UP]:
    #     sq.rect.y -= 2
    # if keys[pygame.K_DOWN]:
    #     sq.rect.y += 2
    
    if keys[pygame.K_LEFT]:
        player.move(-2,0)
    if keys[pygame.K_RIGHT]:
        player.move(2,0)
    if keys[pygame.K_UP]:
        player.move(0,-2)
    if keys[pygame.K_DOWN]:
        player.move(0,2)
    
    for entity in entities:
        entity.take_damage(1)
    entities.draw(screen)
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
