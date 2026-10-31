
import pygame
import random
import math

pygame.init()

catch_sound = pygame.mixer.Sound("assets/catch.mp3")
hurt_sound = pygame.mixer.Sound("assets/hurt.mp3")
gameover_sound = pygame.mixer.Sound("assets/gameover.mp3")

window = pygame.display.set_mode((800,600))
pygame.display.set_caption("PieGame-🥧")
player = pygame.image.load("assets/basket.png").convert_alpha()
player = pygame.transform.scale(player, (75,75))

player_x = 350
player_y = 515
player_vel_x = 0
player_vel_y = 0

object = pygame.image.load("assets/pie.png").convert_alpha()
object = pygame.transform.scale(object, (75,75))

object_x = 400
object_y = 0
object_vel_x = 0
object_vel_y = 1

shake = 0

blast = pygame.image.load("assets/blast.png").convert_alpha()
blast = pygame.transform.scale(blast, (65,65))

blast_x = random.randint(0,735)
blast_y = -300
blast_vel_y = 1

score = 0
lives = 3
game_state = 1

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None,70)

def collision_detection(x1,y1,w1,h1,x2,y2,w2,h2):
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_vel_x = -5
            elif event.key == pygame.K_RIGHT:
                player_vel_x = 5

            if event.key == pygame.K_r and game_state == 2:
                score = 0
                lives = 3
                game_state = 1
                player_x = 350
                object_x = random.randint(0,725)
                object_y = -75
                teddy_x = random.randint(0,735)
                teddy_y = -300
                player_vel_x = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_vel_x = 0

    if object_y > window.get_height():
        object_y = -75
        object_x = random.randint(0,725)

    window.fill((245,220,180))

    if game_state == 1:
        player_x += player_vel_x
        player_y += player_vel_y
        player_x = max(0,min(725,player_x))

        object_x += object_vel_x
        object_y += object_vel_y
        blast_y += blast_vel_y

        shake += 0.03
        sway = math.sin(shake) * 12
        pie_x = object_x + sway

        if collision_detection(player_x,player_y,75,75,
                               pie_x,object_y,75,75):
            score += 1
            catch_sound.play()
            object_y = -75
            object_x = random.randint(0,725)

        if collision_detection(player_x,player_y,75,75,
                               blast_x,blast_y,65,65):
            lives -= 1
            hurt_sound.play()           
            blast_y = -300
            blast_x = random.randint(0,735)

        if object_y > window.get_height():
            object_y = -75
            object_x = random.randint(0,725)

        if blast_y > window.get_height():
            blast_y = -300
            blast_x = random.randint(0,735)

        if lives <= 0:
            game_state = 2
            gameover_sound.play()

        if game_state == 1:
            window.blit(player, (player_x, player_y))
            window.blit(object, (pie_x,object_y))
            window.blit(blast, (blast_x,blast_y))

        score_text = font.render("Score: " + str(score), True, (100,55,30))
        lives_text = font.render("Lives: " + str(lives), True,(100,55,30))

        window.blit(score_text,(20,20))
        window.blit(lives_text,(650,20))

    if game_state == 2:
        game_over = big_font.render("GAME OVER", True,(120,50,40))
        final_score = font.render("Score: " + str(score), True,(100,55,30))
        restart = font.render("Press R to restart",True,(100,55,30))

        window.blit(game_over, (230,200))
        window.blit(final_score,(340,290))
        window.blit(restart,(275,350))

    pygame.display.flip()
