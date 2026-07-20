import pygame
import math
import random

class PowerUp:
    def __init__(self, x, y, powerup_type=None):
        self.x = x
        self.y = y
        self.radius = 20
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.type = powerup_type if powerup_type else random.choice(["invincible", "speed", "magnet", "double_coins"])
        self.rotation = 0
        self.collectable = True
        self.pulse = 0

        if self.type == "invincible":
            self.color = (255, 215, 0)
            self.glow_color = (255, 220, 50)
            self.duration = 300  
        elif self.type == "speed":
            self.color = (0, 255, 255)
            self.glow_color = (50, 255, 255)
            self.duration = 180  
        elif self.type == "magnet":
            self.color = (255, 0, 255)
            self.glow_color = (255, 50, 255)
            self.duration = 240  
        elif self.type == "double_coins":
            self.color = (255, 200, 0)
            self.glow_color = (255, 220, 50)
            self.duration = 180  
        
    def update(self, speed):
        self.x -= speed
        self.rect.x = self.x
        self.rotation += 0.05
        self.pulse += 0.05
        
        self.y += math.sin(self.pulse) * 0.15
        self.rect.y = self.y - self.radius
        
        if self.x < -50:
            self.collectable = False
    
    def draw(self, screen):
        glow_surf = pygame.Surface((self.radius * 8, self.radius * 8), pygame.SRCALPHA)
        for i in range(5, 0, -1):
            alpha = 15 * i
            radius = self.radius * (1 + i * 0.6)
            pygame.draw.circle(glow_surf, (*self.glow_color[:3], alpha), 
                             (self.radius * 4, self.radius * 4), radius)
        screen.blit(glow_surf, (self.x - self.radius * 4, self.y - self.radius * 4))

        scale_x = abs(math.cos(self.rotation))
        if scale_x > 0.1:
            pygame.draw.ellipse(screen, self.color, 
                               (self.x - self.radius * scale_x, 
                                self.y - self.radius,
                                self.radius * 2 * scale_x, 
                                self.radius * 2), 3)
            inner_radius = self.radius * 0.6
            pygame.draw.circle(screen, self.color, 
                             (int(self.x), int(self.y)), inner_radius)

            self.draw_icon(screen)
    
    def draw_icon(self, screen):

        if self.type == "invincible":
            points = []
            for i in range(5):
                angle = -math.pi / 2 + i * 2 * math.pi / 5
                r = self.radius * 0.5
                points.append((self.x + math.cos(angle) * r, 
                              self.y + math.sin(angle) * r))
            pygame.draw.polygon(screen, (255, 255, 255), points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
            
        elif self.type == "speed":
            points = [
                (self.x, self.y - self.radius * 0.5),
                (self.x - self.radius * 0.3, self.y),
                (self.x + self.radius * 0.2, self.y),
                (self.x, self.y + self.radius * 0.5)
            ]
            pygame.draw.polygon(screen, (255, 255, 255), points)
            
        elif self.type == "magnet":
            pygame.draw.arc(screen, (255, 255, 255), 
                           (self.x - self.radius * 0.4, self.y - self.radius * 0.3,
                            self.radius * 0.8, self.radius * 0.6), 
                           0, math.pi, 3)
            pygame.draw.arc(screen, (255, 255, 255), 
                           (self.x - self.radius * 0.4, self.y - self.radius * 0.1,
                            self.radius * 0.8, self.radius * 0.6), 
                           0, math.pi, 3)
            
        elif self.type == "double_coins":
            for i in range(2):
                pygame.draw.circle(screen, (255, 215, 0), 
                                 (int(self.x - 8 + i * 16), int(self.y)), 
                                 self.radius * 0.25)