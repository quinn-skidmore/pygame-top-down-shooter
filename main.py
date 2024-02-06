
import pygame, sys, random, math

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, health):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = pos)
        self.pos = self.rect.center
        self.velocity = pygame.Vector2(0,0)
        self.health = health
        self.pos = pos

    def take_damage(self,damage):
        self.health -= damage
        if(self.health < 0):
            entities.remove(self)

    def move(self):
        self.pos += self.velocity

class Player(Entity):
    def __init__(self, pos, health):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.original_image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.original_image.convert_alpha()
        self.image.fill((0,255,0))
        self.original_image.fill((0,255,0))
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.velocity = pygame.Vector2(0,0)
        self.health = health
        self.bullets = pygame.sprite.Group()
    
    def shoot(self):
        self.bullets.add(Bullet(self.rect.center,10))

    def point_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.rect = self.image.get_rect(center=self.pos)

class Bullet(Entity):
    def __init__(self, pos, speed):
        super(Entity, self).__init__()
        self.image = pygame.Surface((25,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = pos)
        self.velocity = pygame.Vector2(0,0)
        self.speed = speed
        self.pos = pos
        self.aim()

    def aim(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        self.velocity = pygame.Vector2(rel_x,rel_y).normalize() * self.speed

        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        self.rect = self.image.get_rect(center=self.pos)
# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Top Down Shooter")

# Create clock to later control frame rate
clock = pygame.time.Clock()

entities = pygame.sprite.Group()
player = Player((400,400),1000)
entities.add(player)
# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot()
            print("Shoot")
    screen.fill((0,0,0))

        # Get the state of all keys
    # Update rectangle position based on key presses
    # if keys[pygame.K_LEFT]:
    #     sq.rect.x -= 2
    # if keys[pygame.K_RIGHT]:
    #     sq.rect.x += 2
    # if keys[pygame.K_UP]:
    #     sq.rect.y -= 2
    # if keys[pygame.K_DOWN]:
    #     sq.rect.y += 2

    for entity in entities:
        entity.take_damage(1)
    entities.draw(screen)
    player.point_to_mouse()
    for bullet in player.bullets:
        bullet.move()
    player.bullets.draw(screen)
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
