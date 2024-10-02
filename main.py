from constants import *
from track import Track
from car import Car, CameraGroup
from button import Button
from textbox import TextBox

import pygame

STARTING_X_POSITION, STARTING_Y_POSITION = 0, 0
SEED_CHANGED = False

def set_seed(id, seed, track):
    global STARTING_X_POSITION, STARTING_Y_POSITION, SEED_CHANGED
    if not seed:
        return
    track.set_seed(int(seed))
    track.clear_track()
    track.create_track()
    STARTING_X_POSITION, STARTING_Y_POSITION = track.final_points[0][0], track.final_points[0][1]
    SEED_CHANGED = True


def randomize_seed(track):
    global STARTING_X_POSITION, STARTING_Y_POSITION, SEED_CHANGED
    track.randomize_seed()
    track.clear_track()
    track.create_track()
    STARTING_X_POSITION, STARTING_Y_POSITION = track.final_points[0][0], track.final_points[0][1]
    SEED_CHANGED = True


def main():
    pygame.init()
    total_display = pygame.display.set_mode(TOTAL_SIZE)
    screen = pygame.surface.Surface(SCREEN_SIZE)
    bottom_bar = pygame.surface.Surface(BOTTOM_BAR_SIZE)
    camera = screen.get_rect().copy()
    clock = pygame.time.Clock()
    running = True
    dt = 0
    font = pygame.font.SysFont('Comic Sans MS', 30)

    tr = Track()
    tr.create_track()
    #print(tr.final_points[0])
    global STARTING_X_POSITION, STARTING_Y_POSITION, SEED_CHANGED
    STARTING_X_POSITION, STARTING_Y_POSITION = tr.final_points[0][0], tr.final_points[0][1]
    player = Car(STARTING_X_POSITION, STARTING_Y_POSITION)
    player_sprite = CameraGroup()
    player_sprite.add(player)

    #sprite.mask = pygame.mask.from_threshold(sprite.image, pygame.Color('yellow'), (1, 1, 1, 255))
    player.mask = pygame.mask.from_threshold(player.image, pygame.Color("green"))

    button_style = {"font" : font,
                    "hover_color" : pygame.Color(200,200,200),
                    "clicked_color" : pygame.Color(0,0,0)}

    seed_textbox = TextBox((0, 0, 200, 50), command=set_seed, track_arg=tr, clear_on_enter=True, inactive_on_enter=True)
    seed_textbox.rect.center = ((BB_WIDTH // 8) * 5, S_HEIGHT + (BB_HEIGHT // 2))

    randomize_seed_button = Button((0,0,200,50), pygame.Color(0,0,0), randomize_seed, track=tr, text="Randomize", **button_style)
    randomize_seed_button.rect.center = ((BB_WIDTH // 8) * 3, S_HEIGHT + (BB_HEIGHT // 2))

    restart_button = Button((0,0,200,50), pygame.Color(0,0,0), player.set_position, x_position=STARTING_X_POSITION,
                            y_position=STARTING_Y_POSITION, text="Restart", **button_style)
    restart_button.rect.center = ((BB_WIDTH // 8), S_HEIGHT + (BB_HEIGHT // 2))

    seed_button = Button((0,0,200,50), pygame.Color(0,0,0), seed_textbox.execute, text="Set Seed", **button_style)
    seed_button.rect.center = ((BB_WIDTH // 8) * 7, S_HEIGHT + (BB_HEIGHT // 2))



    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            randomize_seed_button.check_event(event)
            restart_button.check_event(event)
            seed_button.check_event(event)
            seed_textbox.get_event(event)
        
        if SEED_CHANGED:
            player.set_position(STARTING_X_POSITION, STARTING_Y_POSITION)
            SEED_CHANGED = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.change_speed(dt, 1, True)
        if keys[pygame.K_s]:
            player.change_speed(dt, -1, True)
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            player.change_speed(dt, 0, False)
        if keys[pygame.K_a]:
            player.turn(-2)
        if keys[pygame.K_d]:
            player.turn(2)
            
        player_sprite.update()
        #if pygame.sprite.spritecollideany(player, objects, pygame.sprite.collide_mask):
        seed_textbox.update()
        restart_button.update_starting_pos(STARTING_X_POSITION, STARTING_Y_POSITION)

        velocity_surface = font.render("{:.2f}".format(player.speed), False, (0,0,0))
        position_text = "{:.2f}".format(player.position.x) + ", " + "{:.2f}".format(player.position.y)
        position_surface = font.render(position_text, False, (0,0,0))
        seed = tr.get_seed()
        seed_surface = font.render(str(seed), False, (0,0,0))

        camera.center = player.rect.center
        screen.fill("green")
        tr.draw(screen, camera)
        player_sprite.draw(screen, camera)

        screen.blit(velocity_surface, (3,0))
        screen.blit(position_surface, (3,velocity_surface.get_height()))
        screen.blit(seed_surface, (3,velocity_surface.get_height() + position_surface.get_height()))

        bottom_bar.fill("green")
        total_display.blit(bottom_bar, (0,S_HEIGHT))
        
        randomize_seed_button.update(total_display)
        restart_button.update(total_display)
        seed_button.update(total_display)


        total_display.blit(screen, (0,0))
        seed_textbox.draw(total_display)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()

#
# TO-DO LIST
#
# Collision
# Create the distance to wall vectors
# Create the AI
# Train the AI
# Test the AI



# Fuck that list
# Create Collision
# Create distance to wall vectors
# Everything related to the AI
# interpolation
# maybe clean code up