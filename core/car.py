import math
from typing import override

import pygame

from util.constants import (
    ACCELERATION,
    MAX_SPEED,
    REVERSE_ACCELERATION,
    REVERSE_MAX_SPEED,
)


class Car(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.degrees: float = 0
        self.speed: float = 0
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)

        self.image_original: pygame.Surface = pygame.Surface([40, 20])
        self.image_original.set_colorkey("green")
        _ = self.image_original.fill("red")
        self.image: pygame.Surface = self.image_original.copy()
        self.image.set_colorkey("green")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center=(x, y)
        self.reversing: bool = False

    # Sets the position to the new position
    def set_position(self, x: float, y: float) -> None:
        self.position = pygame.Vector2(x, y)

    # Handles turning
    def turn(self, angle: float) -> None:
        if self.speed == 0 and self.velocity == pygame.Vector2(0,0):
            return

        dir = -1 if self.reversing else 1
        self.degrees = (self.degrees + angle * dir)

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_original, -self.degrees)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    # Handles speed change
    def change_speed(self, dt: float, dir: int, accelerating: bool = False) -> None:
        self.reversing = True if self.speed < 0 else False
        if self.speed >= MAX_SPEED and accelerating:
            self.speed = MAX_SPEED
            return
        elif self.speed <= REVERSE_MAX_SPEED and accelerating:
            self.speed = REVERSE_MAX_SPEED
            return

        if accelerating:
            if dir > 0:
                accel = ACCELERATION
            elif self.speed > 0:
                accel = -ACCELERATION
            else:
                accel = REVERSE_ACCELERATION
        else:
            if self.speed > 0:
                accel = -ACCELERATION
            elif self.speed < 0:
                accel = -REVERSE_ACCELERATION
            else:
                accel = 0

        self.speed += accel * dt


        if abs(self.speed) < 0.1:
            self.speed = 0

    @override
    def update(self) -> None:
        self.velocity.from_polar((self.speed, math.degrees(math.radians(self.degrees))))
        self.position += self.velocity
        self.rect.center = int(self.position.x), int(self.position.y)



class CameraGroup(pygame.sprite.GroupSingle):
    def __init__(self, sprite: pygame.sprite.Sprite | None = None) -> None:
        super().__init__(sprite)

    def draw(self, surface: pygame.Surface, camera: pygame.Rect) -> None:
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, (spr.rect.x - camera.x, spr.rect.y - camera.y))
        self.lostsprites = []
