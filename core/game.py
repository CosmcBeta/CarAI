import util.constants as constants
from core.track import Track
from core.car import Car, CameraGroup
from ui.button import Button
from ui.textbox import TextBox

import pygame

class Game:
    def __init__(self) -> None:
        self.seed_changed: bool = False

        _ = pygame.init()
        self.total_display: pygame.Surface = pygame.display.set_mode(constants.TOTAL_SIZE)
        self.screen: pygame.Surface = pygame.surface.Surface(constants.SCREEN_SIZE)
        self.bottom_bar: pygame.Surface = pygame.surface.Surface(constants.BOTTOM_BAR_SIZE)
        self.camera: pygame.Rect = self.screen.get_rect().copy()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.dt: float = 0
        self.font: pygame.font.Font = pygame.font.SysFont('Comic Sans MS', 30)

        self.track: Track = Track()
        self.track.create_track()

        self.starting_position: tuple[int, int] = self.track.final_points[0][0], self.track.final_points[0][1]
        self.player: Car = Car(self.starting_position[0], self.starting_position[1])
        self.player_sprite: CameraGroup = CameraGroup()
        self.player_sprite.add(self.player)


        self.player.mask = pygame.mask.from_threshold(self.player.image, pygame.Color("green"))

        button_style = {
            "font" : self.font,
            "hover_color" : pygame.Color(200,200,200),
            "clicked_color" : pygame.Color(0,0,0)
        }

        self.seed_textbox: TextBox = TextBox((0, 0, 200, 50), command=self.set_seed, track_arg=self.track, clear_on_enter=True, inactive_on_enter=True)
        self.seed_textbox.rect.center = ((constants.BB_WIDTH // 8) * 5, constants.S_HEIGHT + (constants.BB_HEIGHT // 2))

        self.randomize_seed_button: Button = Button((0,0,200,50), pygame.Color(0,0,0), self.randomize_seed, track=self.track, text="Randomize", **button_style)
        self.randomize_seed_button.rect.center = ((constants.BB_WIDTH // 8) * 3, constants.S_HEIGHT + (constants.BB_HEIGHT // 2))

        self.restart_button: Button = Button((0,0,200,50), pygame.Color(0,0,0), self.player.set_position, x_position=self.starting_position[0],
                                y_position=self.starting_position[1], text="Restart", **button_style)
        self.restart_button.rect.center = ((constants.BB_WIDTH // 8), constants.S_HEIGHT + (constants.BB_HEIGHT // 2))

        self.seed_button: Button = Button((0,0,200,50), pygame.Color(0,0,0), self.seed_textbox.execute, text="Set Seed", **button_style)
        self.seed_button.rect.center = ((constants.BB_WIDTH // 8) * 7, constants.S_HEIGHT + (constants.BB_HEIGHT // 2))


    def set_seed(self, id, seed: int, track: Track):
        if not seed:
            return
        track.set_seed(int(seed))
        track.clear_track()
        track.create_track()
        self.starting_position = track.final_points[0][0], track.final_points[0][1]
        self.seed_changed = True


    def randomize_seed(self, track: Track):
        track.randomize_seed()
        track.clear_track()
        track.create_track()
        self.starting_position = track.final_points[0][0], track.final_points[0][1]
        self.seed_changed = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.randomize_seed_button.check_event(event)
                self.restart_button.check_event(event)
                self.seed_button.check_event(event)
                self.seed_textbox.get_event(event)

            if self.seed_changed:
                self.player.set_position(self.starting_position[0], self.starting_position[1])
                self.seed_changed = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.change_speed(self.dt, 1, True)
            if keys[pygame.K_s]:
                self.player.change_speed(self.dt, -1, True)
            if not keys[pygame.K_w] and not keys[pygame.K_s]:
                self.player.change_speed(self.dt, 0, False)
            if keys[pygame.K_a]:
                self.player.turn(-2)
            if keys[pygame.K_d]:
                self.player.turn(2)

            self.player_sprite.update()
            self.seed_textbox.update()
            self.restart_button.update_starting_pos(self.starting_position[0], self.starting_position[1])

            velocity_surface = self.font.render("{:.2f}".format(self.player.speed), False, (0,0,0))
            position_text = "{:.2f}".format(self.player.position.x) + ", " + "{:.2f}".format(self.player.position.y)
            position_surface = self.font.render(position_text, False, (0,0,0))
            seed = self.track.get_seed()
            seed_surface = self.font.render(str(seed), False, (0,0,0))

            self.camera.center = self.player.rect.center
            _ = self.screen.fill("green")
            self.track.draw(self.screen, self.camera)
            _ = self.player_sprite.draw(self.screen, self.camera)

            _ = self.screen.blit(velocity_surface, (3,0))
            _ = self.screen.blit(position_surface, (3, velocity_surface.get_height()))
            _ = self.screen.blit(seed_surface, (3, velocity_surface.get_height() + position_surface.get_height()))

            _ = self.bottom_bar.fill("green")
            _ = self.total_display.blit(self.bottom_bar, (0, constants.S_HEIGHT))

            self.randomize_seed_button.update(self.total_display)
            self.restart_button.update(self.total_display)
            self.seed_button.update(self.total_display)


            _ = self.total_display.blit(self.screen, (0,0))
            self.seed_textbox.draw(self.total_display)

            pygame.display.flip()

            self.dt = self.clock.tick(60) / 1000
