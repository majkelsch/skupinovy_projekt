import pygame

# Button
class Button:
    def __init__(self, rect, color, text, font, text_color=(0, 0, 0), align="center", border_color=(0, 0, 0), border_width=2):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color
        self.align = align  # "left", "center", or "right"
        self.border_color = border_color
        self.border_width = border_width

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect()
        if self.align == "center":
            text_rect.center = self.rect.center
        elif self.align == "right":
            text_rect.midright = self.rect.midright
        else:  # default to left
            text_rect.midleft = self.rect.midleft
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Label:
    def __init__(self, pos, text, font, color=(0, 0, 0), align="left"):
        self.pos = pos
        self.text = text
        self.font = font
        self.color = color
        self.align = align  # "left", "center", or "right"

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        text_rect = text_surf.get_rect()
        x, y = self.pos

        if self.align == "center":
            text_rect.center = (x, y)
        elif self.align == "right":
            text_rect.topright = (x, y)
        else:  # default to left
            text_rect.topleft = (x, y)

        surface.blit(text_surf, text_rect)


class HealthSlider:
    def __init__(self, pos, size, min_value, max_value, value, bar_color=(0, 200, 0), bg_color=(200, 200, 200), border_color=(0, 0, 0)):
        self.x, self.y = pos
        self.width, self.height = size
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.bar_color = bar_color
        self.bg_color = bg_color
        self.border_color = border_color

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))

    def draw(self, surface):
        # Draw background
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.bg_color, bg_rect)
        # Draw health bar
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        bar_width = int(self.width * ratio)
        bar_rect = pygame.Rect(self.x, self.y, bar_width, self.height)
        pygame.draw.rect(surface, self.bar_color, bar_rect)
        # Draw border
        pygame.draw.rect(surface, self.border_color, bg_rect, 2)

class Image:
    def __init__(self, pos, image_path):
        self.x, self.y = pos
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def set_position(self, pos):
        self.x, self.y = pos
        self.rect.topleft = (self.x, self.y)

class EnemyImage:
    def __init__(self, pos, enemy, max_size=(100, 100), align="left"):
        self.x, self.y = pos
        self.enemy = enemy
        self.image_original = pygame.image.load(enemy.image_path).convert_alpha()
        self.image = self._scale_image(self.image_original, max_size)
        self.align = align  # "left", "center", or "right"
        self._update_rect()

    def _scale_image(self, image, max_size):
        max_w, max_h = max_size
        img_w, img_h = image.get_size()
        scale = min(max_w / img_w, max_h / img_h, 1)
        new_size = (int(img_w * scale), int(img_h * scale))
        return pygame.transform.smoothscale(image, new_size)

    def _update_rect(self):
        img_w, img_h = self.image.get_size()
        x, y = self.x, self.y
        if self.align == "center":
            self.rect = self.image.get_rect(center=(x, y))
        elif self.align == "right":
            self.rect = self.image.get_rect(topright=(x, y))
        else:  # default to left
            self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_position(self, pos):
        self.x, self.y = pos
        self._update_rect()

    def set_align(self, align):
        self.align = align
        self._update_rect()