import pygame
from random import *

pygame.init()

f_settings = open('settings.txt')
arg_array = []
for i in range (13):                     # lines in txt
    arg_array.append( int( f_settings.read(6) ) )       # import args from file
    f_settings.read(1)
print(arg_array)
f_settings.close()

speed_of_update_game = arg_array[0]     # game speed

display_width = arg_array[1]
display_height = arg_array[2]     # display settings

array_quan = arg_array[3]
clouds_quan = arg_array[4]
props_quan = arg_array[5]         # quantity of objects

height_of_jump = arg_array[6]     # not in pixels, just a number
clouds_speed = arg_array[7]       # speed of the clouds

def str_to_bool(x):
    x = str(x)
    return x.lower() in ("1")
TEST = str_to_bool(arg_array[8])        # developer mode

points_to_spawn_pterodactyl = arg_array[9]      # distance after that pterodactyls begin to spawn
pterodactyls_quan = arg_array[10]       # quantity of pterodactyls
chance_to_spawn_pterodactyl = arg_array[11]

height_of_game = arg_array[12]          # indent from down of the screen

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

max_height_of_cloud = int( display_height - display_height/3 )
min_height_of_cloud = 50

prop_width = 7
prop_height = 7         # as a standart, then it will change


icon = pygame.image.load('logo32.png')
pygame.display.set_icon(icon)               # import icon

dino =[  pygame.image.load('dino\dino.png'),
    pygame.image.load('dino\dino_run_1.png'),
    pygame.image.load('dino\dino_run_2.png'),
    pygame.image.load('dino\dino_die.png'),
    pygame.image.load('dino\dino_sit_1.png'),
    pygame.image.load('dino\dino_sit_2.png')  ]     #   import dino textures
dino_options = [ [60, 60], [82,32] ]                #   width * height

cactus_img = [  pygame.image.load('cactus\cactus_1_1.png'),
    pygame.image.load('cactus\cactus_1_2.png'),
    pygame.image.load('cactus\cactus_1_3.png'),
    pygame.image.load('cactus\cactus_2_1.png'),
    pygame.image.load('cactus\cactus_2_2.png'),
    pygame.image.load('cactus\cactus_3_1.png')  ]           #   import cactus textures

cactus_options = [ [20,70], [25,60], [25,45], [60,70], [60,70], [60,50] ]        #   width * height
cactus_quan = len(cactus_img)

cloud_img = [pygame.image.load('other_props\cloud.png'),
    pygame.image.load('other_props\cloud_2.png')]           #   import clouds textures

cloud_options = [ [100,100], [100,100] ]            #   width * height

other_props = [ pygame.image.load( r'other_props\UFO.png'),
pygame.image.load(r'other_props\pterodactyl_1.png'),
pygame.image.load(r'other_props\pterodactyl_2.png') ]              #   import other textures

other_props_options = [ [100,100], [100,70], [100,70] ]            #   width * height

pterodactyl_height = [  display_height - height_of_game - 75,
                        display_height - height_of_game - 110,
                        display_height- height_of_game - 150 ]     #   height of pterodactyls

jump_sound = pygame.mixer.Sound('sound\jump_8bit.wav')

def play_collect_sound():
    pygame.mixer.music.load('sound\collect_8bit.mp3')
    pygame.mixer.music.play()