import pygame
from util.constants import ACCEPTED


class TextBox(object):
    def __init__(self, rect, **kwargs):
        self.rect: pygame.Rect = pygame.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)
        self.active = False

    def process_kwargs(self, kwargs):
        defaults = {
            "id": None,
            "command": None,
            "track_arg": None,
            "active": True,
            "color": pygame.Color("white"),
            "font_color": pygame.Color("black"),
            "outline_color": pygame.Color("black"),
            "outline_width": 2,
            "active_color": pygame.Color("blue"),
            "font": pygame.font.Font(None, self.rect.height + 4),
            "clear_on_enter": False,
            "inactive_on_enter": True,
        }
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in ACCEPTED:
                self.buffer.append(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def execute(self):
        if self.command:
            self.command(self.id, self.final, self.track_arg)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(
                x=self.rect.x + 2, centery=self.rect.centery
            )
            if self.render_rect.width > self.rect.width - 6:
                offset = self.render_rect.width - (self.rect.width - 6)
                self.render_area = pygame.Rect(
                    offset, 0, self.rect.width - 6, self.render_rect.height
                )
            else:
                self.render_area = self.rendered.get_rect(topleft=(0, 0))
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def draw(self, surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width * 2, self.outline_width * 2)
        surface.fill(outline_color, outline)
        surface.fill(self.color, self.rect)
        if self.rendered:
            surface.blit(self.rendered, self.render_rect, self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color, (curse.right + 1, curse.y, 2, curse.h))
