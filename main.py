
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
            self.kill()

    def move(self):
        self.pos += self.velocity
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

class Player(Entity):
    def __init__(self, pos, health):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.original_image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.shoot_files = ["Cannon/basiccannontop-frame1.png", "Cannon/basiccannontop-frame2.png","Cannon/basiccannontop-frame3.png"]
        self.shoot_images = [pygame.image.load(filename).convert_alpha() for filename in self.shoot_files]
        self.index = 0
        
        self.pics = [[self.shoot_images[0]],[img for img in self.shoot_images]]
        self.image = self.pics[0][0]
        self.original_image = self.pics[0][0]
  
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
        self.image = pygame.transform.rotate(self.original_image, int(angle) - 90)
        self.rect = self.image.get_rect(center=self.pos)

class Bullet(Entity):
    def __init__(self, pos, speed):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,25), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        self.image.fill((0,255,0))
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

class Enemy(Entity):
    def __init__(self, health, player):
        super(Entity, self).__init__()
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.original_image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.original_image.convert_alpha()
        self.image.fill((255,0,0))
        self.original_image.fill((0,255,0))

        self.pos = pygame.Vector2(0,0)
        spawn_wall = random.randint(0,4)
        if(spawn_wall == 0):
            self.pos.x = random.randint(0,800)
            self.pos.y = 800
        elif(spawn_wall == 1):
            self.pos.y = random.randint(-800,0)
            self.pos.x = -800
        elif(spawn_wall == 2):
            self.pos.x = random.randint(0,800)
            self.pos.y = -800
        else:
            self.pos.y = random.randint(-800,0)
            self.pos.x = 800

        self.rect = self.image.get_rect(center = self.pos)
        self.velocity = pygame.Vector2(0,0)
        self.health = health
        self.player = player
        self.speed = 3

        self.point_to_player()

    def point_to_player(self):
        player_x = player.pos.x
        player_y = player.pos.y
        rel_x, rel_y = player_x - self.rect.x, player_y - self.rect.y
        self.velocity = pygame.Vector2(rel_x,rel_y).normalize() * self.speed

    def collision_detector(self):
        gets_hit = pygame.sprite.spritecollide(self, player.bullets, True)
        if(gets_hit):
            self.take_damage(1)
        if(pygame.Rect.colliderect(self.rect,self.player.rect)):
            self.kill()
            

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)

screen.fill((156,219,67))
pygame.display.set_caption("Top Down Shooter")

# Create clock to later control frame rate
clock = pygame.time.Clock()

entities = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player(pygame.Vector2(400,400),1000)
entities.add(player)

for i in range(0,5):
    enemies.add(Enemy(1,player))

entities.add(enemies)
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
    screen.fill((156,219,67))

    for enemy in enemies:
        enemy.move()
        enemy.collision_detector()

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
