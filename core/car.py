from constants import *

import pygame
import math


class Car(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.degrees = 0
        self.speed = 0
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.image_original = pygame.Surface([40, 20])
        self.image_original.set_colorkey("green")
        self.image_original.fill("red")
        self.image = self.image_original.copy()
        self.image.set_colorkey("green")
        self.rect = self.image.get_rect()
        self.rect.center=(x, y) 
        self.reversing = False


    def set_position(self, x, y):
        self.position = pygame.Vector2(x, y)
        

    def turn(self, angle):
        if self.speed == 0 and self.velocity == pygame.Vector2(0,0):
            return
        dir = -1 if self.reversing else 1
        self.degrees = (self.degrees + angle * dir)

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_original, -self.degrees)
        self.rect = self.image.get_rect()
        self.rect.center = old_center


    def change_speed(self, dt, dir, accelerating=False):
        self.reversing = True if self.speed < 0 else False
        if self.speed >= MAX_SPEED and accelerating:
            self.speed = MAX_SPEED
            return
        elif self.speed <= REVERSE_MAX_SPEED and accelerating:
            self.speed = REVERSE_MAX_SPEED
            return
        
        if accelerating:
            if dir > 0:
                self.speed += ACCELERATION * dt
                return
            
            if self.speed > 0:
                self.speed -= ACCELERATION * dt
            else:
                self.speed += REVERSE_ACCELERATION * dt

            return

        if self.speed < 0:
            acceleration = REVERSE_ACCELERATION
        elif self.speed > 0:
            acceleration = ACCELERATION
        else:
            acceleration = 0 
        
        self.speed += (-acceleration * dt)
        if abs(self.speed) < 0.1:
            self.speed = 0


    def update(self):
        self.velocity.from_polar((self.speed, math.degrees(math.radians(self.degrees))))
        self.position += self.velocity
        self.rect.center = self.position

    
    def offset(self, camera):
        self.position.x -= camera.x
        self.position.y -= camera.y
        self.rect.center = self.position



class CameraGroup(pygame.sprite.GroupSingle):

    def draw(self, surface, camera):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            self.spritedict[spr] = surface_blit(spr.image, (spr.rect.x - camera.x, spr.rect.y - camera.y))
        self.lostsprites = []