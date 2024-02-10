import pygame, sys, random, math
class GameManager():
    def __init__(self, enemy_kills):
        self.enemy_kills = enemy_kills

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, health, manager):
        super(Entity, self).__init__()
        self.manager = manager
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = pos)
        self.pos = self.rect.center
        self.velocity = pygame.Vector2(0,0)
        self.health = health

        #this is a dumb solution but i need to finish this and it works soooooo
        self.enemy_kills = 100

        self.pos = pos

    def take_damage(self,damage):
        self.health -= damage
        if(self.health < 0):
            entities.remove(self)
            self.kill()
            self.manager.enemy_kills -= 1

    def move(self):
        self.pos += self.velocity
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

class Player(Entity):
    def __init__(self, pos, health, manager):
        super(Entity, self).__init__()
        self.manager = manager

        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.original_image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.cannon_base = pygame.image.load("Cannon/cannonbasesprite.png").convert_alpha()

        self.shoot_files = ["Cannon/basiccannontop-frame1.png", "Cannon/basiccannontop-frame1.png","Cannon/basiccannontop-frame1.png"]
        self.shoot_images = [pygame.image.load(filename).convert_alpha() for filename in self.shoot_files]
        self.index = 0
        
        self.pics = [[self.shoot_images[0]],[img for img in self.shoot_images]]
        self.image = self.pics[0][0]
        self.original_image = self.pics[0][0]
  
        self.rect = self.image.get_rect(center = pos)
        self.pos = pos
        self.velocity = pygame.Vector2(0,0)
        self.health = health
        self.enemy_kills = 100
        self.bullets = pygame.sprite.Group()
        self.base_pos = pygame.Vector2(self.pos.x-15,self.pos.y-15)
    
    def shoot(self):
        self.bullets.add(Bullet(self.rect.center,10))


    def point_to_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x/screen_scale_factor - self.rect.centerx, mouse_y/screen_scale_factor - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle)-90)
        self.rect = self.image.get_rect(center=self.pos)


class Bullet(Entity):
    def __init__(self, pos, speed):
        super(Entity, self).__init__()
        self.image = pygame.image.load("Cannon/cannonbullet.png").convert_alpha()

        self.rect = self.image.get_rect(center = pos)
        self.velocity = pygame.Vector2(0,0)
        self.speed = speed
        self.pos = pos
        self.aim()

    def aim(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x/screen_scale_factor - self.rect.x, mouse_y/screen_scale_factor - self.rect.y
        self.velocity = pygame.Vector2(rel_x,rel_y).normalize() * self.speed

        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        self.rect = self.image.get_rect(center=self.pos)

class Enemy(Entity):
    def __init__(self, health, player, manager):
        super(Entity, self).__init__()
        self.manager = manager
        self.image = pygame.Surface((50,50), pygame.SRCALPHA, 32)
        self.anim_length = 20
        self.move_files = ["Enemy/octopusenemy-frame1.png", "Enemy/octopusenemy-frame2.png"]
        self.move_images = [pygame.image.load(filename).convert_alpha() for filename in self.move_files]
        self.index = 0
        
        self.pics = [[self.move_images[0]],[]]
        frame_count = 0
        for img in self.move_images:
            for i in range(frame_count,frame_count + self.anim_length):
                self.pics[1].append(img)
                #print("I appended an img")
            frame_count+=self.anim_length

        self.image = self.pics[0][0]
        self.pos = pygame.Vector2(0,0)
        spawn_wall = random.randint(0,4)
        if(spawn_wall == 0):
            self.pos.x = random.randint(0,400)
            self.pos.y = 0
        elif(spawn_wall == 1):
            self.pos.y = random.randint(0,400)
            self.pos.x = 0
        elif(spawn_wall == 2):
            self.pos.x = random.randint(0,400)
            self.pos.y = 400
        else:
            self.pos.y = random.randint(0,400)
            self.pos.x = 400

        self.rect = self.image.get_rect(center = self.pos)
        self.velocity = pygame.Vector2(0,0)
        self.health = health
        self.player = player
        self.enemy_kills = None
        self.speed = 1

        self.point_to_player()

    def point_to_player(self):
        player_x = player.pos.x-20
        player_y = player.pos.y-20
        rel_x, rel_y = player_x - self.rect.x, player_y - self.rect.y
        self.velocity = pygame.Vector2(rel_x,rel_y).normalize() * self.speed

    def collision_detector(self):
        gets_hit = pygame.sprite.spritecollide(self, player.bullets, True)
        if(gets_hit):
            self.take_damage(1)
        if(pygame.Rect.colliderect(self.rect,self.player.rect)):
            player.take_damage(1)
            self.kill()
    
    def move(self):
        self.pos += self.velocity
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        
        if(self.index+1) < len(self.pics[1]):
            self.index = (self.index +1)
        else:
            self.index = 0
        self.image = self.pics[1][self.index]
            

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 800
screen_scale_factor = 2
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
display = pygame.Surface((screen_width/screen_scale_factor,screen_height/screen_scale_factor))
display.fill((156,219,67))
pygame.display.set_caption("Top Down Shooter")
font = pygame.font.Font('edit-undo.brk.ttf', 40)
small_font = pygame.font.Font('edit-undo.brk.ttf', 24)
tiny_font = pygame.font.Font('edit-undo.brk.ttf', 16)

enemy_amount = 1
enemy_spawn_progression = 500
time_between_enemies = 5000
current_time_between_enemies = time_between_enemies
# Create clock to later control frame rate
clock = pygame.time.Clock()

pause = True
start_screen =True
manager = GameManager(50)

entities = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player(pygame.Vector2(200,200),3, manager)
entities.add(player)

for i in range(0,enemy_amount):
    enemies.add(Enemy(0,player,manager))

entities.add(enemies)

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot()
            
    if(start_screen == True):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            start_screen = False
            pause = False

        start_text = small_font.render("Press Enter to start", False, (0,0,0))
        help_text = tiny_font.render("Shoot enemies to win, don't let enemies reach you", False, (0,0,0))
        help_text2 = tiny_font.render("art made by me", False, (0,0,0))


        display.blit(start_text, (80,180))
        display.blit(help_text, (15,210))
        display.blit(help_text2, (135,230))

    if(pause == False):
        if(pygame.time.get_ticks()>current_time_between_enemies):
            if(time_between_enemies - enemy_spawn_progression) < 100:
                time_between_enemies -= enemy_spawn_progression
            current_time_between_enemies += time_between_enemies
            if(enemy_amount< 10):
                enemy_amount += 1
            print(str(current_time_between_enemies))
            for i in range(0,enemy_amount):
                enemies.add(Enemy(0,player,manager))
                print("spawn enemy")
            entities.add(enemies)

        display.fill((156,219,67))
        display.blit(player.cannon_base,player.base_pos)
        player.bullets.draw(display)
        entities.draw(display)
        
        for enemy in enemies:
            enemy.move()
            enemy.collision_detector()
        
        player.point_to_mouse()
        for bullet in player.bullets:
            bullet.move()

    if(player.health <= 0):
        lose_text = font.render("You Lose", False, (0,0,0))
        display.blit(lose_text, (120,120))
        pause = True
    else:
        health_text = small_font.render("Health: " + str(player.health), False, (0,0,0))
        display.blit(health_text, (5,0))
    if(manager.enemy_kills <= 0):
        win_text = font.render("You Win", False, (255,255,255))
        display.blit(win_text, (120,120))
        pause = True
    else:
        enemy_text = small_font.render("Enemies Left: " + str(manager.enemy_kills), False, (0,0,0))
        display.blit(enemy_text, (210,0))

    # Update the display
    screen.blit(pygame.transform.scale(display,screen.get_size()),(0,0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
