import pygame
from pygame import *
import time
import sys


def get_asset_path(asset):
	return "assets/" + asset

# Initialize Pygame
pygame.init()

# Create the starting window
window_width, window_height = (1280, 720) #screen.get_size()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Carrot Game") #pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

# Consts
white = (255, 255, 255)
button_color = (50, 150, 255)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (128, 64, 64)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LBLUE = (0, 255, 255)

# Sprites
main_menu = pygame.sprite.Sprite()
main_menu.image = pygame.image.load(get_asset_path('menu/main_screen.png'))
main_menu.rect = main_menu.image.get_rect()
main_menu.rect.center = (window_width / 2, window_height / 2)
new_button = pygame.sprite.Sprite()
new_button.image = pygame.image.load(get_asset_path('menu/newgame_button.png'))
new_button.rect = new_button.image.get_rect()
new_button.rect.center = ((window_width / 2)+16, (window_height / 2)+70)
exit_button = pygame.sprite.Sprite()
exit_button.image = pygame.image.load(get_asset_path('menu/exit_button.png'))
exit_button.rect = exit_button.image.get_rect()
exit_button.rect.center = ((window_width / 2)+16, (window_height / 2) + 200)
load_button = pygame.sprite.Sprite()
load_button.image = pygame.image.load(get_asset_path('menu/load_button.png'))
load_button.rect = load_button.image.get_rect()
load_button.rect.center = ((window_width / 2)+16, (window_height / 2) - 52)




key_cooldown = 10
font = pygame.font.Font(None, 18)


# To be moved

grow_time = 10

width, height = (1280, 720) #(1920, 1080) screen.get_size()
playerspeed = 3