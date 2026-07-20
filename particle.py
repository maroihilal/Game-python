import pygame
import random
import math

class Particle:
    def __init__(self, x, y, color=None, particle_type="sparkle"):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, 2)
        self.size = random.uniform(2, 6)
        self.initial_size = self.size
        if color:
            self.color = color
        else:
            self.color = (random.randint(200, 255), 
                         random.randint(100, 200), 
                         random.randint(200, 255))
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.gravity = 0.1
        self.rotation = random.uniform(0, math.pi * 2)
        self.rotation_speed = random.uniform(-0.1, 0.1)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.99  # Friction
        self.life -= 1
        self.size *= 0.98
        self.rotation += self.rotation_speed
        return self.life > 0 and self.size > 0.5
    
    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        
        if self.particle_type == "sparkle":

            points = []
            for i in range(4):
                angle = self.rotation + i * math.pi / 2
                r = self.size * (1 + math.sin(self.rotation + i))
                points.append((self.x + math.cos(angle) * r,
                              self.y + math.sin(angle) * r))
            pygame.draw.polygon(screen, (*self.color, alpha), points)
            
        elif self.particle_type == "circle":
            surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), 
                             (int(self.size), int(self.size)), int(self.size))
            screen.blit(surf, (self.x - self.size, self.y - self.size))
            
        elif self.particle_type == "trail":
            surf = pygame.Surface((int(self.size * 3), int(self.size)), pygame.SRCALPHA)
            pygame.draw.line(surf, (*self.color, alpha), 
                           (0, int(self.size/2)), 
                           (int(self.size * 3), int(self.size/2)), 
                           int(self.size))
            screen.blit(surf, (self.x - self.size * 1.5, self.y - self.size/2))
            
        elif self.particle_type == "star":
            points = []
            for i in range(5):
                angle = self.rotation + i * 2 * math.pi / 5
                r = self.size if i % 2 == 0 else self.size * 0.5
                points.append((self.x + math.cos(angle) * r,
                              self.y + math.sin(angle) * r))
            pygame.draw.polygon(screen, (*self.color, alpha), points)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit(self, x, y, count, particle_type="sparkle", color=None, spread=2):
        for _ in range(count):
            particle = Particle(
                x + random.uniform(-spread, spread),
                y + random.uniform(-spread, spread),
                color,
                particle_type
            )
            self.particles.append(particle)
    
    def emit_trail(self, x, y, color=None, count=1):
        for _ in range(count):
            particle = Particle(x, y, color, "trail")
            particle.vx = random.uniform(-1, 1)
            particle.vy = random.uniform(-1, 1)
            particle.size = random.uniform(1, 3)
            particle.life = random.randint(10, 20)
            self.particles.append(particle)
    
    def update(self):
        for particle in self.particles[:]:
            if not particle.update():
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        self.particles.clear()