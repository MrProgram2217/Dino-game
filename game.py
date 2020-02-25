import pygame
import sys
from random import randint,choice
from config import *

pygame.init()

game_over = False
ufo_fly = False
dino_sit = False
jump_sound_played = False

pterodactyls_count = 0

make_jump = False
jump_counter = height_of_jump       # for make jump

way = 1                     # distance that u have run

array_long_x = 0            # for change location of cactuses (put them in the end of the array)

usr_x = display_width // 4
usr_y = display_height - dino_options[0][1] - height_of_game       # user position

display = pygame.display.set_mode( (display_width, display_height) )
pygame.display.set_caption( 'run' )

game_speed = 4              # speed of the game
max_game_speed = 15         # don't put more than 24
points_speed = 4            # =game_speed

step_for_anim = 0           # to improve stability into animations
dino_anim_step = 0          # to save last frame in dino animation
pterodactyl_anim_step = 0   # to save last frame in pterodactyl animation

clock = pygame.time.Clock()

draw_way = 1        # points in game
max_draw_way = 0
num_for_sound = 1

try:
    f_score = open('max_score.txt', 'r')
    max_score_from_file = int( f_score.read()[:-2] )
    f_score.close()
except:
    max_score_from_file = 0

draw_to_file = False

ufo_in_game = None

cactus_array = []
clouds_array = []
props_array = []

class Cloud:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
    
    def move_clouds(self):
        if self.x >= -self.width:
            display.blit(self.image, ((self.x), (self.y)))
            self.x -= clouds_speed
        else:
            self.x = display_width + self.width
            self.y = randint(min_height_of_cloud, max_height_of_cloud)

class Ufo(Cloud):
    def move(self):
        global ufo_fly
        if (self.x >= -self.width) and (self.x <= display_width + self.width) and ufo_fly:
            display.blit( self.image, ( self.x, self.y ) )
            self.x += clouds_speed*3
        else:
            self.x = -self.width
            ufo_fly = False

    def draw_position(self):
        print( self.x, '  ', self.y )

class Prop:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
    
    def move_props(self):
        if self.x >= -self.width:
            pygame.draw.rect(  display, self.color, ( self.x, self.y, self.width, self.height )  )
            self.x -= game_speed
        else:
            self.x = display_width
            self.y = randint( display_height - 105, display_height )
            self.width = randint(5,8)
            self.height = randint(5,8)

class Cactus:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def move(self):
        if self.x >= -self.width:
            display.blit( self.image, (self.x, self.y ) )
            self.x -= game_speed
        else:
            self.x = array_long_x + 100

class Pterodactyl(Cactus):
    def draw_animation(self, anim_step):
        global pterodactyl_anim_step
        anim_speed = 40

        if int(anim_step) % anim_speed == 0:
            pterodactyl_anim_step = 1
        elif (int(anim_step) + anim_speed/2) % anim_speed == 0:
            pterodactyl_anim_step = 2
        display.blit( other_props[pterodactyl_anim_step], ( self.x, self.y ) )              # draw pterodactyl
    
    def move_pterodactyl(self):
        if self.x >= -self.width:
            self.x -= game_speed
        else:
            self.x = array_long_x + 100
            self.y = choice(pterodactyl_height)


def run_game():
    global make_jump, game_speed, step_for_anim, myfont, max_draw_way, draw_way, ufo_fly, points_speed, dino_sit, TEST, num_for_sound

    game = True

    create_cactus_arr(cactus_array)
    create_clouds_arr(clouds_array)
    create_props_arr(props_array)

    spawn_ufo()

    while game:
        global way
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        check_collision(cactus_array, max_draw_way)
        check_game_over()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            make_jump = True

        if keys[pygame.K_LSHIFT]:             # STOP
            game = False

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dino_sit = True
        else:
            dino_sit = False
        
        if make_jump == True:
            jump()

        if int(draw_way) % 100 == 0 and draw_way > 80 and num_for_sound > 0:
            play_collect_sound()
            num_for_sound = 0
        
        display.fill((15,15,15))

        pygame.draw.rect(display, (164, 144, 62), (0, display_height - 100 , display_width, 100))                 # floor

        if way % 1000 == 0 and game_speed < max_game_speed:
            game_speed += 1
        
        if int(draw_way + 1) % 1500 == 0:
            ufo_fly = True

        ufo_in_game.move()
        draw_clouds_arr(clouds_array)
        draw_props_arr(props_array)
        draw_cactus_arr(cactus_array, step_for_anim)

        insert_pterodactyl(draw_way)

        step_for_anim += 1
        draw_dino_anim(step_for_anim)                                                          # player

        way += game_speed/4
        try:
            draw_way = round( way/(points_speed*2), 0 )
            max_draw_way = draw_way
        except:
            draw_way = max_draw_way

        textsurface = myfont.render('points= ' + str(draw_way) + '      speed= ' + str(int(game_speed)) + '      '+ str(clock)[7:-2] +
        '              record= ' + str(max_score_from_file), False, (255, 255, 255) )   # draw stats
        display.blit(textsurface,(0,0))

        if game_over:
            myfont_game_over = pygame.font.SysFont('Tomorrow', 120)
            textsurface = myfont_game_over.render('GAME OVER', False, (255, 255, 255))                            # draw stats
            display.blit(textsurface,(330,300))

        pygame.display.update()
        clock.tick( speed_of_update_game )


def jump ():
    global usr_y, make_jump, jump_counter, jump_sound_played, jump_sound, num_for_sound

    if jump_counter >= -height_of_jump and not game_over:
        usr_y -= jump_counter / 2.6         # 2.6 to improve gravity
        jump_counter -= 1
        if not jump_sound_played:
            jump_sound.play()
        jump_sound_played = True
    else:
        jump_counter = height_of_jump
        make_jump = False
        jump_sound_played = False
        num_for_sound = 1

def draw_dino_anim(step):
    global dino_anim_step, usr_y
    
    if game_over:
        dino_anim_step = 3

    elif make_jump:
        dino_anim_step = 0

    elif step % int(25 - game_speed) == 0:
        if dino_sit:
            dino_anim_step = 4
            usr_y = display_height - dino_options[1][1] - height_of_game
        else:
            dino_anim_step = 1
            usr_y = display_height - dino_options[0][1] - height_of_game

    elif (step + int( (25 - game_speed)/2 )) % (25 - game_speed) == 0:
        if dino_sit:
            dino_anim_step = 5
            usr_y = display_height - dino_options[1][1] - height_of_game
        else:
            dino_anim_step = 2
            usr_y = display_height - dino_options[0][1] - height_of_game

    display.blit(dino[dino_anim_step], (usr_x, int(usr_y) ) )

def create_cactus_arr(array):
    global array_long_x

    last_cactus_x = 0

    for i in range (array_quan):
        x = randint(250,500)

        cactus_id = randint(0,cactus_quan-1)
        cactus = cactus_img[cactus_id]

        cactus_width = cactus_options[cactus_id][0]
        cactus_height = cactus_options[cactus_id][1]
        cactus_x = int((display_width - display_width/4)*i + x + 200)

        array.append(Cactus( cactus_x,
        display_height - cactus_height - height_of_game,
        cactus_width,
        cactus_height,
        cactus ))

        array_long_x += cactus_x - last_cactus_x 
        last_cactus_x = cactus_x

def draw_cactus_arr(array, step):
    for enemy in array:
        try:
            enemy.draw_animation(step)
            enemy.move_pterodactyl()
        except:
            enemy.move()

def create_clouds_arr(array):
    for i in range (clouds_quan):
        x = i * randint(290,310)
        y = randint(min_height_of_cloud, max_height_of_cloud)

        cloud_id = randint(0,1)

        array.append(  Cloud( x, y, cloud_options[cloud_id][0], cloud_options[cloud_id][1] , cloud_img[cloud_id] )  )

def draw_clouds_arr(array):
    for cloud in array:
        cloud.move_clouds()

def create_props_arr(array):
    for i in range (props_quan):
        x = randint( 0,display_width )
        y = randint( display_height - 105, display_height )

        color_red = randint(120,140)
        color_green = randint(105,115)
        color_blue = randint(35,45)

        color_rgb = (color_red, color_green, color_blue)
        array.append(  Prop( x, y, prop_width, prop_height, color_rgb )  )

def draw_props_arr(array):
    for prop in array:
        prop.move_props()

def check_collision(enemys, score):
    global game_over
    if dino_sit:
        dino_width = dino_options[1][0]
        dino_height = dino_options[1][1]
    else:
        dino_width = dino_options[0][0]
        dino_height = dino_options[0][1]

    for enemy in enemys:
        if (( enemy.y <= usr_y <= (enemy.y + enemy.height) ) or ( enemy.y <= ( usr_y + dino_height) <= (enemy.y + enemy.height) ) or (enemy.y >= usr_y and (enemy.y + enemy.height) <= (usr_y + dino_height) )) and score > 25.0 and not TEST:
            if (enemy.x <= usr_x <= enemy.x + enemy.width) or (enemy.x <= usr_x + dino_width <= enemy.x + enemy.width):
                game_over = True

def check_game_over():
    global game_speed

    if game_over:
        game_speed = 0

        textsurface = myfont.render('GAME OVER', False, (255, 255, 255))
        display.blit(textsurface,(0,0))

        if not draw_to_file:
            draw_max_score_to_file(max_draw_way)

def draw_max_score_to_file(score):
    global draw_to_file

    if draw_way > max_score_from_file:
        if max_draw_way > max_score_from_file:
            score_write = score
        else:
            score_write = max_score_from_file

        f_score = open('max_score.txt', 'w')
        f_score.write( str(score_write) )
        f_score.close
        draw_to_file = True

def spawn_ufo():
    global ufo_in_game

    ufo_in_game = Ufo( -other_props_options[0][0],
    randint(min_height_of_cloud, max_height_of_cloud),
    other_props_options[0][0], other_props_options[0][1],
    other_props[0] )

def insert_pterodactyl(points):
    global cactus_array, pterodactyls_count

    if ( points > points_to_spawn_pterodactyl ) and ( pterodactyls_count <= pterodactyls_quan ) and ( randint(0,99) >= (100 - chance_to_spawn_pterodactyl) ):
        element = randint(0, int(array_quan/2))
        x_pos = cactus_array[element].x

        cactus_array.pop( element )
        pterodactyls_count += 1

        cactus_array.insert(element, Pterodactyl( x_pos,
                                                  choice(pterodactyl_height),
                                                  other_props_options[1][0],
                                                  other_props_options[1][1],
                                                  other_props[1] ))


run_game()