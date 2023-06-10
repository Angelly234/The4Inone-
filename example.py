
# Import necessary modules:
import pygame
from sys import exit
from random import randint, choice

# Define the Player class
class Player(pygame.sprite.Sprite):
  def init(self): # initialize
    super().init()  
    # Load player animation frames and jumping image
    player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
    player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
    self.player_walk = [player_walk_1, player_walk_2]
    self.player_index = 0
    self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

    self.image = self.player_walk[self.player_index]
    self.rect = self.image.get_rect(topleft=(80, 500)) # Set initial position of the player
    self.is_jumping = False
    self.gravity = 0

    # Load and set volume for the jump sound effect
    self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
    self.jump_sound.set_volume(1)

  # Handle player input
  def player_input(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
      self.gravity = -20
      self.jump_sound.play()
      self.is_jumping = True

  # Apply gravity to the player character
  def apply_gravity(self):
    self.gravity += 0.85
    self.rect.y += self.gravity
    if self.rect.bottom >= 500:
      self.rect.bottom = 500
      self.is_jumping = False
      
  # Update the player animation state
  def animation_state(self):
    if self.rect.bottom < 500:
      self.image = self.player_jump
    else:
      self.player_index += 0.1
      if self.player_index >= len(self.player_walk):
        self.player_index = 0
      self.image = self.player_walk[int(self.player_index)]

  # Update the player
  def update(self):
    self.player_input()
    self.apply_gravity()
    self.animation_state()

# Define the Trash class
class Trash(pygame.sprite.Sprite):
  def init(self, type):
    super().init()

    # Load trash image based on the type
    if type == 'trash_can':
      trash_can = pygame.image.load('graphics/trash/can-trash.png').convert_alpha()
      self.image = trash_can
      self.frames = [self.image]
      self.y_pos = 370
    elif type == 'trash_paper':
      trash_paper = pygame.image.load('graphics/trash/paper-trash.png').convert_alpha()
      self.image = trash_paper
      self.frames = [self.image]
      self.y_pos = 370

    self.animation_index = 0
    self.rect = self.image.get_rect(midbottom=(randint(1400, 1500), self.y_pos))

  # Update the trash animation state
  def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames):
      self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

  # Update the trash
  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()

  # Destroy the trash if it goes off-screen
  def destroy(self):
    if self.rect.x <= -100:
      self.kill()

# Define the Obstacle class
class Obstacle(pygame.sprite.Sprite):
  def init(self, type):
    super().init()

     # Load obstacle image based on the type
    if type == 'tree':
      tree = pygame.image.load('graphics/big-tree.png').convert_alpha()
      self.image = tree
      self.frames = [self.image]
      self.y_pos = 500

      self.animation_index = 0
      self.rect = self.image.get_rect(midbottom=(randint(1400, 1700), self.y_pos))

  # Update the obstacle animation state
  def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames):
      self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

  # Update the obstacle
  def update(self):
    self.animation_state()
    self.rect.x -= 6
    self.destroy()

  # Destroy the obstacle if it goes off-screen
  def destroy(self):
    if self.rect.x <= -100:
      self.kill()


# Display the current score on the screen
def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surf = test_font.render(f'Score: {current_score}', False, (64, 64, 64))
  score_rect = score_surf.get_rect(center=(500, 50))
  screen.blit(score_surf, score_rect)

# Check collision between the player and obstacles
def collision_sprite():
  if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
    return True
  else:
    return False

# Check collection of trash by the player
def collection_sprite():
  global current_score
  trash_collected = pygame.sprite.spritecollide(player.sprite, trash_group, True)
  if trash_collected:
    current_score += len(trash_collected)

# Initialize pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
current_score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)

# Create player sprite group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Create obstacle and trash sprite groups
obstacle_group = pygame.sprite.Group()
trash_group = pygame.sprite.Group()

# Load background images
sky_surface = pygame.image.load('graphics/Sky1.png').convert()
ground_surface = pygame.image.load('graphics/ground1.png').convert()

# Load intro screen and game messages
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(500, 300))

game_name = test_font.render('Alien Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(500, 180))
game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(500, 430))

# Set up timer for spawning obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if game_active:
      if event.type == obstacle_timer:
        obstacle_group.add(Obstacle(choice(['tree'])))
        trash_group.add(Trash(choice(['trash_can', 'trash_paper'])))

      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        player.sprite.gravity = 0

    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        start_time = int(pygame.time.get_ticks() / 1000)
        current_score = 0
        player.sprite.rect.midbottom = (80, 300)
        obstacle_group.empty()
        trash_group.empty()

  if game_active:
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 500))
    display_score()

    player.draw(screen)
    player.update()

    obstacle_group.draw(screen)
    obstacle_group.update()

    trash_group.draw(screen)
    trash_group.update()

    if collision_sprite():
      game_active = False

    collection_sprite()

  else:
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)

    score_message = test_font.render(f'Your score: {current_score}', False, (111, 196, 169))
    score_message_rect = score_message.get_rect(center=(500, 430))
    screen.blit(game_name, game_name_rect)

    if current_score == 0:
      screen.blit(game_message, game_message_rect)
    else:
      screen.blit(score_message, score_message_rect)

  pygame.display.update()
  clock.tick(60)

pygame.quit()