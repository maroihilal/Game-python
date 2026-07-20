
import pygame
import math
import os

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        
        
        self.sprites = self.load_sprites()
        self.current_sprite = 0  # 0: idle, 1: run1, 2: run2
        self.image = self.sprites[0] if self.sprites else None
        
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -12
        self.grounded = True
        
        
        self.jumping = False
        self.sliding = False
        self.slide_timer = 0
        self.falling = False
    
        self.animation_timer = 0
        self.animation_speed = 8
        self.current_outfit = 0
        self.outfits = [
            {"name": "Classic", "color": (255, 100, 200)},
            {"name": "Hoodie", "color": (200, 50, 150)},
            {"name": "Jacket", "color": (50, 100, 200)},
            {"name": "Sportswear", "color": (50, 200, 100)},
            {"name": "Dress", "color": (200, 50, 200)}]
        self.rect = pygame.Rect(x - 20, y - 80, 40, 80)
    
    def load_sprites(self):
        sprites = []
        
        sprite_folder = "assets/images/characters/"
        sprite_files = ["idle.png", "run1.png", "run2.png"]
        possible_paths = [
            "assets/images/characters/",
            "assets/characters/",
            "images/characters/",
            "sprites/",
            ""]
        for filename in sprite_files:
            loaded = False
            for folder in possible_paths:
                path = os.path.join(folder, filename)
                try:
                    if os.path.exists(path):
                        print(f"✅ Loading sprite: {path}")
                        sprite = pygame.image.load(path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, (self.width, self.height))
                        sprites.append(sprite)
                        loaded = True
                        break
                except Exception as e:
                    print(f"⚠️ Error loading {path}: {e}")
            if not loaded:
                print(f"⚠️ Sprite not found: {filename}, using placeholder")
                sprites.append(self.create_placeholder_sprite(filename))
        while len(sprites) < 3:
            sprites.append(self.create_placeholder_sprite(f"sprite_{len(sprites)}"))
        
        return sprites
    
    def create_placeholder_sprite(self, name):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 100, 255), (10, 20, 30, 45), border_radius=5)
        pygame.draw.circle(surf, (255, 200, 200), (25, 15), 12)
        pygame.draw.rect(surf, (50, 50, 50), (5, 15, 5, 20))
        pygame.draw.rect(surf, (50, 50, 50), (35, 15, 5, 20))
        pygame.draw.rect(surf, (200, 100, 255), (12, 65, 8, 15))
        pygame.draw.rect(surf, (200, 100, 255), (25, 65, 8, 15))
        pygame.draw.rect(surf, (100, 100, 100), (10, 78, 12, 5))
        pygame.draw.rect(surf, (100, 100, 100), (23, 78, 12, 5))
        return surf
    
    def set_outfit(self, outfit_id):
        if 0 <= outfit_id < len(self.outfits):
            self.current_outfit = outfit_id
            self.apply_outfit()
    
    def apply_outfit(self):
        if self.sprites and self.current_sprite < len(self.sprites):
            base_sprite = self.sprites[self.current_sprite]
            if base_sprite:
                colored_sprite = base_sprite.copy()
                outfit = self.outfits[self.current_outfit]
                color_surf = pygame.Surface(colored_sprite.get_size(), pygame.SRCALPHA)
                color_surf.fill((*outfit["color"], 80))  # Semi-transparent overlay
                colored_sprite.blit(color_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = colored_sprite
    
    def get_current_sprite(self):
        if self.sprites and self.current_sprite < len(self.sprites):
            # Get base sprite
            base_sprite = self.sprites[self.current_sprite]
            if base_sprite:
                # Apply outfit if needed
                outfit = self.outfits[self.current_outfit]
                colored_sprite = base_sprite.copy()
                color_surf = pygame.Surface(colored_sprite.get_size(), pygame.SRCALPHA)
                color_surf.fill((*outfit["color"], 80))
                colored_sprite.blit(color_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                return colored_sprite
        return None
    
    def jump(self):
        if self.grounded and not self.sliding:
            self.vel_y = self.jump_power
            self.grounded = False
            self.jumping = True
            return True
        return False
    
    def slide(self):
        if self.grounded and not self.sliding:
            self.sliding = True
            self.slide_timer = 30
            return True
        return False
    
    def reset(self):
        self.y = 550
        self.vel_y = 0
        self.grounded = True
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.current_sprite = 0
        self.animation_timer = 0
    
    def update(self):
        self.vel_y += self.gravity
        self.y += self.vel_y
        if self.y >= 550:
            self.y = 550
            self.vel_y = 0
            self.grounded = True
            self.jumping = False
            if self.falling:
                self.falling = False
        if self.sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.sliding = False
        if self.grounded and not self.sliding:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                if self.current_sprite == 1:
                    self.current_sprite = 2
                else:
                    self.current_sprite = 1
        else:
            self.current_sprite = 0
            self.animation_timer = 0
        if self.sliding:
            self.rect = pygame.Rect(self.x - 20, self.y - 40, 40, 40)
        else:
            self.rect = pygame.Rect(self.x - 20, self.y - 80, 40, 80)
    
    def check_collision(self, obstacle_x, obstacle_y, obstacle_width, obstacle_height):
        player_rect = self.rect
        obstacle_rect = pygame.Rect(obstacle_x - obstacle_width//2, obstacle_y - obstacle_height, 
                                    obstacle_width, obstacle_height)
        hitbox = player_rect.inflate(-10, -10)
        return hitbox.colliderect(obstacle_rect)