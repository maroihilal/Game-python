import pygame
import math
import random

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.current_color = color
        self.hover = False
        self.clicked = False
        self.animation_timer = 0
        self.scale = 1.0
        self.glow_alpha = 0
        
    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.hover else self.color
        self.animation_timer += 1
        
        if self.hover:
            self.scale = 1.0 + math.sin(self.animation_timer * 0.05) * 0.02
            self.glow_alpha = min(255, self.glow_alpha + 5)
        else:
            self.scale = max(1.0, self.scale - 0.01)
            self.glow_alpha = max(0, self.glow_alpha - 5)
    
    def draw(self, screen, font):
        if self.glow_alpha > 0:
            glow_surf = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.hover_color[:3], min(50, self.glow_alpha//5)), 
                           (10, 10, self.rect.width, self.rect.height), border_radius=20)
            screen.blit(glow_surf, (self.rect.x - 10, self.rect.y - 10))
        
        scaled_rect = pygame.Rect(
            self.rect.x + (self.rect.width - self.rect.width * self.scale) / 2,
            self.rect.y + (self.rect.height - self.rect.height * self.scale) / 2,
            self.rect.width * self.scale,
            self.rect.height * self.scale
        )
        pygame.draw.rect(screen, self.current_color, scaled_rect, border_radius=20)
        
        if self.hover:
            pygame.draw.rect(screen, (255, 255, 255), scaled_rect, 3, border_radius=20)
        
        if self.text:
            text_surf = font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=scaled_rect.center)
            screen.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hover:
                self.clicked = True
                return True
        return False

class HUD:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def draw(self):

        self.draw_score()
        self.draw_coins()
        self.draw_multiplier()
        self.draw_high_score()
        self.draw_speed()
        self.draw_combo()
    
    def draw_score(self):

        score_text = self.font_large.render(f"{self.game.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(600, 30))
        self.screen.blit(score_text, score_rect)
        
        label = self.font_small.render("SCORE", True, (200, 200, 200))
        label_rect = label.get_rect(center=(600, 60))
        self.screen.blit(label, label_rect)
    
    def draw_coins(self):

        coin_text = self.font_medium.render(f"💰 {self.game.coins}", True, (255, 215, 0))
        coin_rect = coin_text.get_rect(center=(600, 90))
        self.screen.blit(coin_text, coin_rect)
    
    def draw_multiplier(self):

        if self.game.multiplier > 1:
            mult_text = self.font_medium.render(f"x{self.game.multiplier}", True, (255, 100, 200))
            mult_rect = mult_text.get_rect(center=(600, 120))
            self.screen.blit(mult_text, mult_rect)
    
    def draw_high_score(self):

        high_text = self.font_medium.render(f"🏆 {self.game.high_score}", True, (255, 200, 100))
        high_rect = high_text.get_rect(topright=(1180, 20))
        self.screen.blit(high_text, high_rect)
        
        label = self.font_small.render("HIGH SCORE", True, (200, 200, 200))
        label_rect = label.get_rect(topright=(1180, 50))
        self.screen.blit(label, label_rect)
    
    def draw_speed(self):

        speed_text = self.font_small.render(f"SPEED: {int(self.game.speed)}", True, (100, 200, 255))
        speed_rect = speed_text.get_rect(topright=(1180, 80))
        self.screen.blit(speed_text, speed_rect)
    
    def draw_combo(self):

        if self.game.combo > 0:
            combo_text = self.font_medium.render(f"COMBO x{self.game.combo}", True, (255, 200, 0))
            combo_rect = combo_text.get_rect(center=(600, 150))
            self.screen.blit(combo_text, combo_rect)

class MainMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_large = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        

        button_width = 280
        button_height = 60
        center_x = 600
        
        self.play_button = Button(center_x - button_width//2, 320, button_width, button_height, 
                                 "PLAY", (200, 50, 150), (255, 100, 200))
        self.shop_button = Button(center_x - button_width//2, 400, button_width, button_height,
                                 "SHOP", (150, 50, 200), (200, 100, 255))
        self.settings_button = Button(center_x - button_width//2, 480, button_width, button_height,
                                     "SETTINGS", (100, 50, 200), (150, 100, 255))
        self.exit_button = Button(center_x - button_width//2, 560, button_width, button_height,
                                 "EXIT", (200, 50, 50), (255, 100, 100))
        
        self.title_y = 150
        self.particles = []
        self.create_particles()
        
    def create_particles(self):
        for _ in range(50):
            self.particles.append({
                "x": random.randint(0, 1200),
                "y": random.randint(0, 700),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.5, -0.2),
                "size": random.randint(2, 5),
                "alpha": random.randint(50, 200)
            })
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        self.play_button.update(mouse_pos)
        self.shop_button.update(mouse_pos)
        self.settings_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.hover:
                    self.game.start_game()
                elif self.shop_button.hover:
                    self.game.state = "shop"
                elif self.settings_button.hover:
                    self.game.state = "settings"
                elif self.exit_button.hover:
                    pygame.quit()
                    exit()
    
    def draw(self):

        for i in range(700):
            color = (5, 5, 20 + i // 5)
            pygame.draw.line(self.screen, color, (0, i), (1200, i))
        

        for particle in self.particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            if particle["y"] < 0:
                particle["y"] = 700
                particle["x"] = random.randint(0, 1200)
            color = (255, 100, 200, particle["alpha"])
            pygame.draw.circle(self.screen, color[:3], 
                             (int(particle["x"]), int(particle["y"])), 
                             particle["size"])
        

        title_y = 150 + math.sin(pygame.time.get_ticks() * 0.001) * 10
        title = self.font_large.render("NEON CITY", True, (255, 100, 200))
        title_rect = title.get_rect(center=(600, title_y))
        

        for i in range(5, 0, -1):
            glow = self.font_large.render("NEON CITY", True, (255, 100, 200))
            glow_rect = glow.get_rect(center=(600 + i*2, title_y + i*2))
            glow.set_alpha(50 - i * 10)
            self.screen.blit(glow, glow_rect)
        
        self.screen.blit(title, title_rect)
        

        subtitle = self.font_small.render("RUNNER", True, (200, 150, 255))
        subtitle_rect = subtitle.get_rect(center=(600, title_y + 50))
        self.screen.blit(subtitle, subtitle_rect)

        self.play_button.draw(self.screen, self.font_medium)
        self.shop_button.draw(self.screen, self.font_medium)
        self.settings_button.draw(self.screen, self.font_medium)
        self.exit_button.draw(self.screen, self.font_medium)

class PauseMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        

        button_width = 280
        button_height = 55
        center_x = 600
        
        self.resume_button = Button(center_x - button_width//2, 300, button_width, button_height,
                                   "RESUME", (50, 150, 50), (100, 200, 100))
        self.restart_button = Button(center_x - button_width//2, 375, button_width, button_height,
                                    "RESTART", (200, 100, 50), (255, 150, 100))
        self.menu_button = Button(center_x - button_width//2, 450, button_width, button_height,
                                 "MAIN MENU", (100, 50, 200), (150, 100, 255))
        self.quit_button = Button(center_x - button_width//2, 525, button_width, button_height,
                                 "QUIT", (200, 50, 50), (255, 100, 100))
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        self.resume_button.update(mouse_pos)
        self.restart_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.resume_button.hover:
                    self.game.state = "playing"
                    self.game.audio.play_resume()
                    self.game.audio.unpause_music()
                elif self.restart_button.hover:
                    self.game.start_game()
                elif self.menu_button.hover:
                    self.game.state = "menu"
                    self.game.audio.play_menu_music()
                elif self.quit_button.hover:
                    pygame.quit()
                    exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.state = "playing"
                    self.game.audio.play_resume()
                    self.game.audio.unpause_music()
    
    def draw(self):
        # Overlay
        overlay = pygame.Surface((1200, 700))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        

        pulse = abs(math.sin(pygame.time.get_ticks() * 0.003))
        scale = 1.0 + pulse * 0.05
        title = self.font_large.render("PAUSED", True, (255, 100, 200))
        scaled_title = pygame.transform.scale(title, 
                                             (int(title.get_width() * scale),
                                              int(title.get_height() * scale)))
        title_rect = scaled_title.get_rect(center=(600, 200))
        self.screen.blit(scaled_title, title_rect)
        

        self.resume_button.draw(self.screen, self.font_medium)
        self.restart_button.draw(self.screen, self.font_medium)
        self.menu_button.draw(self.screen, self.font_medium)
        self.quit_button.draw(self.screen, self.font_medium)

class GameOverScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        

        button_width = 280
        button_height = 55
        center_x = 600
        
        self.restart_button = Button(center_x - button_width//2, 420, button_width, button_height,
                                    "RESTART", (200, 50, 150), (255, 100, 200))
        self.menu_button = Button(center_x - button_width//2, 495, button_width, button_height,
                                 "MAIN MENU", (100, 50, 200), (150, 100, 255))
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        self.restart_button.update(mouse_pos)
        self.menu_button.update(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.hover:
                    self.game.start_game()
                elif self.menu_button.hover:
                    self.game.state = "menu"
                    self.game.audio.play_menu_music()
    
    def draw(self):

        overlay = pygame.Surface((1200, 700))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))
        

        title = self.font_large.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(600, 150))
        

        for i in range(3, 0, -1):
            glow = self.font_large.render("GAME OVER", True, (255, 50, 50))
            glow_rect = glow.get_rect(center=(600 + i*3, 150 + i*3))
            glow.set_alpha(100 - i * 30)
            self.screen.blit(glow, glow_rect)
        
        self.screen.blit(title, title_rect)
        

        stats = [
            f"Score: {self.game.score}",
            f"High Score: {self.game.high_score}",
            f"Coins: {self.game.coins}",
            f"Distance: {int(self.game.distance)}m"
        ]
        y = 250
        for stat in stats:
            surf = self.font_medium.render(stat, True, (255, 255, 255))
            rect = surf.get_rect(center=(600, y))
            self.screen.blit(surf, rect)
            y += 45
        

        if self.game.score >= self.game.high_score and self.game.score > 0:
            new_record = self.font_medium.render("🏆 NEW HIGH SCORE!", True, (255, 215, 0))
            new_record_rect = new_record.get_rect(center=(600, y + 10))
            self.screen.blit(new_record, new_record_rect)
        

        self.restart_button.draw(self.screen, self.font_medium)
        self.menu_button.draw(self.screen, self.font_medium)

class ShopUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.selected_item = 0

        self.items = [
            {"id": 0, "name": "Classic", "price": 0, "color": "Pink", "unlocked": True},
            {"id": 1, "name": "Hoodie", "price": 100, "color": "Dark Pink", "unlocked": False},
            {"id": 2, "name": "Jacket", "price": 200, "color": "Blue", "unlocked": False},
            {"id": 3, "name": "Sportswear", "price": 300, "color": "Green", "unlocked": False},
            {"id": 4, "name": "Dress", "price": 400, "color": "Purple", "unlocked": False},
        ]
        
        self.update_items()
        
        self.back_button = Button(50, 600, 120, 50, "BACK", (200, 50, 150), (255, 100, 200))
    
    def update_items(self):
        unlocked = self.game.save_data.get("unlocked_outfits", [0])
        for item in self.items:
            item["unlocked"] = item["id"] in unlocked
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                y = 180
                for i, item in enumerate(self.items):
                    rect = pygame.Rect(200, y + i * 90, 800, 70)
                    if rect.collidepoint(event.pos):
                        if item["unlocked"]:
                            # Equip item
                            self.game.player.set_outfit(item["id"])
                            self.game.save_data["current_outfit"] = item["id"]
                            self.game.save_game()
                            self.game.audio.play_click()
                        else:
                            if self.game.coins >= item["price"]:
                                self.game.coins -= item["price"]
                                self.game.save_data["unlocked_outfits"].append(item["id"])
                                self.game.save_game()
                                item["unlocked"] = True
                                self.game.audio.play_click()
                    y += 90
                

                if self.back_button.hover:
                    self.game.state = "menu"
                    self.game.audio.play_click()
    
    def draw(self):

        self.screen.fill((10, 10, 30))
        

        title = self.font_large.render("SHOP", True, (255, 100, 200))
        title_rect = title.get_rect(center=(600, 60))
        self.screen.blit(title, title_rect)
        

        coins_text = self.font_medium.render(f"💰 {self.game.coins}", True, (255, 215, 0))
        coins_rect = coins_text.get_rect(center=(600, 120))
        self.screen.blit(coins_text, coins_rect)

        y = 180
        current_outfit = self.game.player.current_outfit
        for i, item in enumerate(self.items):

            if i == current_outfit:
                color = (50, 150, 50)  # Equipped
            elif item["unlocked"]:
                color = (50, 80, 50)   # Unlocked
            else:
                color = (50, 50, 80)   # Locked
            
            rect = pygame.Rect(200, y, 800, 70)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            

            name = self.font_small.render(item["name"], True, (255, 255, 255))
            self.screen.blit(name, (230, y + 10))
            

            color_text = self.font_small.render(f"Color: {item['color']}", True, (200, 200, 200))
            self.screen.blit(color_text, (230, y + 35))
            
            if i == current_outfit:
                status = "✅ EQUIPPED"
                status_color = (0, 255, 0)
            elif item["unlocked"]:
                status = "EQUIP"
                status_color = (100, 200, 255)
            else:
                status = f"💰 {item['price']}"
                status_color = (255, 215, 0)
            
            status_text = self.font_medium.render(status, True, status_color)
            status_rect = status_text.get_rect(center=(900, y + 35))
            self.screen.blit(status_text, status_rect)
            
            y += 90
        self.back_button.draw(self.screen, self.font_medium)

class ToggleButton:
    def __init__(self, x, y, width, height, label, initial_state=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.state = initial_state
        self.animation_pos = 0 if initial_state else 1
        self.hover = False
        
    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        target = 1 if self.state else 0
        self.animation_pos += (target - self.animation_pos) * 0.1
    
    def toggle(self):
        self.state = not self.state
        return self.state
    
    def draw(self, screen, font):
        color = (50, 150, 50) if self.state else (100, 50, 50)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        circle_x = self.rect.x + 5 + self.animation_pos * (self.rect.width - 30)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(circle_x), self.rect.centery), 12)
        
        label_surf = font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surf, (self.rect.x + self.rect.width + 15, 
                                self.rect.centery - label_surf.get_height() // 2))

class Slider:
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value
        self.dragging = False
        self.handle_radius = 10
        
    def update(self, mouse_pos):
        if self.dragging:
            relative_x = max(0, min(mouse_pos[0] - self.rect.x, self.rect.width))
            self.value = relative_x / self.rect.width
    
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 80), self.rect, border_radius=5)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, 
                                self.rect.width * self.value, self.rect.height)
        pygame.draw.rect(screen, (200, 50, 150), fill_rect, border_radius=5)
        
        handle_x = self.rect.x + self.rect.width * self.value
        pygame.draw.circle(screen, (255, 100, 200), 
                          (int(handle_x), self.rect.centery), 
                          self.handle_radius)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(handle_x), self.rect.centery), 
                          self.handle_radius, 2)