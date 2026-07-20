import pygame
import random
import json
import os
import math
from player import Player
from road import Road
from obstacle import ObstacleManager
from coin import CoinManager
from ui import HUD, PauseMenu, GameOverScreen, MainMenu, ShopUI
from audio_manager import AudioManager
from save import SettingsManager

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.running = True
        
        # Audio
        self.audio = AudioManager()
        
        # Settings
        self.settings = SettingsManager()
        
        # Load save
        self.load_save()
        
        # Initialize road first
        self.road = Road()
        
        # Initialize game objects with road reference
        self.player = Player(600, 550)
        self.obstacle_manager = ObstacleManager(self.road)
        self.coin_manager = CoinManager(self.road)
        
        # Game variables
        self.score = 0
        self.coins = self.save_data.get("total_coins", 0)
        self.high_score = self.save_data.get("high_score", 0)
        self.distance = 0
        self.speed = 8
        self.max_speed = 20
        self.difficulty = 1
        self.multiplier = 1
        self.combo = 0
        
        # Lane system
        self.lanes = self.road.lane_positions  # Get lane positions from road
        self.current_lane = 1  # Center
        self.target_lane = 1
        
        # Effects
        self.screen_shake = 0
        self.particles = []
        self.dust_particles = []
        
        # UI
        self.main_menu = MainMenu(screen, self)
        self.hud = HUD(screen, self)
        self.pause_menu = PauseMenu(screen, self)
        self.game_over_screen = GameOverScreen(screen, self)
        self.shop_ui = ShopUI(screen, self)
        
        # Background objects
        self.buildings = self.create_buildings()
        self.street_lights = self.create_street_lights()
        self.neon_signs = self.create_neon_signs()
        
        # Play menu music
        self.audio.play_menu_music()
    
    def load_save(self):
        try:
            os.makedirs("save", exist_ok=True)
            with open("save/save_data.json", "r") as f:
                self.save_data = json.load(f)
        except:
            self.save_data = {
                "high_score": 0,
                "total_coins": 0,
                "unlocked_outfits": [0],
                "current_outfit": 0
            }
    
    def save_game(self):
        self.save_data["high_score"] = max(self.save_data.get("high_score", 0), self.high_score)
        self.save_data["total_coins"] = self.coins
        self.save_data["unlocked_outfits"] = self.save_data.get("unlocked_outfits", [0])
        self.save_data["current_outfit"] = self.player.current_outfit
        with open("save/save_data.json", "w") as f:
            json.dump(self.save_data, f)
    
    def create_buildings(self):
        buildings = []
        for i in range(25):
            x = random.randint(-200, 1400)
            y = random.randint(-400, -50)
            width = random.randint(60, 150)
            height = random.randint(150, 400)
            color = random.choice([
                (15, 15, 40), (20, 10, 45), (25, 15, 50),
                (10, 20, 40), (20, 20, 45), (30, 15, 50)
            ])
            windows = []
            for w in range(width // 20):
                for h in range(height // 25):
                    if random.random() > 0.3:
                        windows.append({
                            "x": x + 10 + w * 20,
                            "y": y + 10 + h * 25,
                            "on": random.random() > 0.5
                        })
            buildings.append({
                "x": x, "y": y, "width": width, "height": height,
                "color": color, "windows": windows, "scroll_x": 0
            })
        return buildings
    
    def create_street_lights(self):
        lights = []
        for i in range(20):
            x = random.choice([-80, 1280])
            y = random.randint(-100, 700)
            lights.append({
                "x": x, "y": y,
                "color": (255, 200, 100),
                "glow": random.randint(50, 150)
            })
        return lights
    
    def create_neon_signs(self):
        signs = []
        colors = [(255, 100, 200), (200, 50, 255), (0, 255, 200), (255, 200, 0)]
        texts = [
            "PINK NEON",
            "CYBER QUEEN",
            "NEON DREAM",
            "STAR GIRL",
            "MOONLIGHT",
            "ELECTRIC PINK",
            "GALAXY",
            "AURORA",
            "COSMIC",
            "SHINE ON",
            "LUMINA",
            "NOVA",
            "GLOW UP",
            "RADIANT",
            "STARDUST",
            "PRISM"
        ]   
        for i in range(12):
            x = random.randint(50, 1150)
            y = random.randint(-200, 100)
            signs.append({
                "x": x, "y": y,
                "color": random.choice(colors),
                "text": random.choice(texts),
                "pulse": random.uniform(0, 3.14)
            })
        return signs
    
    def handle_events(self, events):
        if self.state == "playing":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.move_lane(-1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.move_lane(1)
                    elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        if self.player.jump():
                            self.audio.play_jump()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.slide()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "pause"
                        self.audio.play_pause()
                        self.audio.pause_music()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if pause button clicked
                    x, y = event.pos
                    if (x - 50) ** 2 + (y - 50) ** 2 <= 25 ** 2:
                        self.state = "pause"
                        self.audio.play_pause()
                        self.audio.pause_music()
        
        elif self.state == "menu":
            self.main_menu.handle_events(events)
        
        elif self.state == "pause":
            self.pause_menu.handle_events(events)
        
        elif self.state == "game_over":
            self.game_over_screen.handle_events(events)
        
        elif self.state == "shop":
            self.shop_ui.handle_events(events)
        
        elif self.state == "settings":
            # Handle settings events
            pass
    
    def move_lane(self, direction):
        new_lane = self.current_lane + direction
        if 0 <= new_lane < self.road.lane_count:
            self.current_lane = new_lane
            self.target_lane = new_lane
    
    def update(self):
        if self.state == "playing":
            # Update player
            self.player.update()
            
            # Smooth lane switching
            target_x = self.road.lane_positions[self.current_lane]
            self.player.x += (target_x - self.player.x) / 8
            
            # Update difficulty
            self.distance += self.speed * 0.016
            self.difficulty = 1 + self.distance / 2000
            self.speed = min(8 + self.distance / 500, self.max_speed)
            self.score = int(self.distance * self.multiplier)
            
            # Update road
            self.road.update(self.speed)
            
            # Update obstacles
            obstacle_hit = self.obstacle_manager.update(
                self.speed, self.difficulty, self.player.x, self.player.y,
                self.player.sliding
            )
            
            if obstacle_hit:
                self.game_over()
            
            # Update coins
            coins_collected = self.coin_manager.update(
                self.speed, self.difficulty, self.player.x, self.player.y
            )
            if coins_collected:
                self.coins += coins_collected
                self.combo += 1
                self.multiplier = 1 + self.combo // 5
                self.audio.play_coin()
                
                # Add coin particles
                for _ in range(10):
                    self.particles.append({
                        "x": self.player.x,
                        "y": 550,
                        "vx": random.uniform(-3, 3),
                        "vy": random.uniform(-5, -2),
                        "life": 30,
                        "max_life": 30
                    })
            
            # Update background
            self.update_background()
            
            # Update particles
            self.update_particles()
            
            # Update screen shake
            if self.screen_shake > 0:
                self.screen_shake *= 0.9
                if self.screen_shake < 0.1:
                    self.screen_shake = 0
    
    def update_background(self):
        # Scroll buildings
        for building in self.buildings:
            building["scroll_x"] += self.speed * 0.15
            if building["scroll_x"] > 1400 + building["width"]:
                building["scroll_x"] = -building["width"] - 200
                building["x"] = random.randint(-200, 1400)
                building["y"] = random.randint(-400, -50)
        
        # Update neon signs
        for sign in self.neon_signs:
            sign["pulse"] += 0.05
            if sign["pulse"] > 3.14 * 2:
                sign["pulse"] = 0
            sign["y"] += self.speed * 0.05
            if sign["y"] > 700:
                sign["y"] = random.randint(-200, 100)
                sign["x"] = random.randint(50, 1150)
    
    def update_particles(self):
        # Dust particles from running
        if self.player.grounded and not self.player.sliding and random.random() < 0.3:
            self.dust_particles.append({
                "x": self.player.x + random.randint(-15, 15),
                "y": 550 + random.randint(-5, 5),
                "vx": random.uniform(-1, -0.3),
                "vy": random.uniform(-0.5, 0),
                "size": random.randint(2, 5),
                "life": 20,
                "max_life": 20,
                "color": (150, 100, 200)
            })
        
        # Update dust particles
        for particle in self.dust_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.dust_particles.remove(particle)
        
        # Update coin particles
        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # Gravity
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.particles.remove(particle)
    
    def game_over(self):
        self.state = "game_over"
        self.audio.play_game_over()
        self.audio.stop_music()
        self.screen_shake = 15
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_game()
    
    def start_game(self):
        self.state = "playing"
        self.score = 0
        self.distance = 0
        self.speed = 8
        self.difficulty = 1
        self.multiplier = 1
        self.combo = 0
        self.screen_shake = 0
        self.current_lane = 1
        self.target_lane = 1
        self.player.reset()
        self.player.x = self.road.lane_positions[1]
        self.obstacle_manager.reset()
        self.coin_manager.reset()
        self.particles = []
        self.dust_particles = []
        self.audio.play_gameplay_music()
    
    def draw(self):
        # Clear screen
        self.screen.fill((5, 5, 20))
        
        # Apply screen shake
        shake_offset = (0, 0)
        if self.screen_shake > 0:
            shake_offset = (
                random.randint(-int(self.screen_shake), int(self.screen_shake)),
                random.randint(-int(self.screen_shake), int(self.screen_shake))
            )
        
        # Create a surface for shaking
        if shake_offset != (0, 0):
            temp_surface = pygame.Surface((1200, 700))
            temp_surface.blit(self.screen, (0, 0))
            self.screen.blit(temp_surface, shake_offset)
        
        if self.state == "menu":
            self.main_menu.draw()
            return
        
        # Draw background (buildings and sky)
        self.draw_background()
        
        # Draw road
        self.road.draw(self.screen)
        
        # Draw obstacles
        self.obstacle_manager.draw(self.screen)
        
        # Draw coins
        self.coin_manager.draw(self.screen)
        
        # Draw player
        self.draw_player()
        
        # Draw dust particles
        for particle in self.dust_particles:
            alpha = int(255 * (particle["life"] / particle["max_life"]))
            color = (*particle["color"], alpha)
            pygame.draw.circle(self.screen, color[:3], 
                             (int(particle["x"]), int(particle["y"])), 
                             particle["size"])
        
        # Draw coin particles (gold sparks)
        for particle in self.particles:
            alpha = int(255 * (particle["life"] / particle["max_life"]))
            color = (255, 215, 0, alpha)
            pygame.draw.circle(self.screen, color[:3], 
                             (int(particle["x"]), int(particle["y"])), 3)
        
        # Draw HUD
        self.hud.draw()
        
        # Draw pause button
        if self.state == "playing":
            self.draw_pause_button()
        
        # Draw pause menu overlay
        if self.state == "pause":
            self.pause_menu.draw()
        
        # Draw game over
        if self.state == "game_over":
            self.game_over_screen.draw()
        
        # Draw shop
        if self.state == "shop":
            self.shop_ui.draw()
    
    def draw_background(self):
        # Sky gradient (darker at top)
        for i in range(350):
            color = (5, 5, 20 + i // 10)
            pygame.draw.line(self.screen, color, (0, i), (1200, i))
        
        # Stars
        for i in range(50):
            x = (i * 137 + 50) % 1200
            y = (i * 97 + 30) % 300
            brightness = 50 + (i % 100)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness + 50), (x, y), 1)
        
        # Draw buildings with parallax
        for building in self.buildings:
            x = building["x"] - building["scroll_x"]
            if x < -building["width"] - 200:
                x += 1600 + building["width"]
            elif x > 1400:
                x -= 1600 + building["width"]
            
            # Building body
            pygame.draw.rect(self.screen, building["color"], 
                           (x, building["y"], building["width"], building["height"]))
            
            # Windows
            for window in building["windows"]:
                if window["on"]:
                    color = (255, 200, 100) if random.random() > 0.95 else (200, 150, 50)
                    window_x = window["x"] - building["scroll_x"]
                    if -building["width"] < window_x < 1400:
                        pygame.draw.rect(self.screen, color, 
                                       (window_x, window["y"], 8, 10))
        
        # Draw neon signs
        for sign in self.neon_signs:
            pulse = abs(math.sin(sign["pulse"]))
            alpha = int(100 + 155 * pulse)
            color = (*sign["color"], alpha)
            # Glow
            glow_surf = pygame.Surface((120, 40), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*sign["color"], 30), (0, 0, 120, 40), border_radius=5)
            self.screen.blit(glow_surf, (sign["x"] - 60, sign["y"] - 20))
            # Text
            font = pygame.font.Font(None, 28)
            text = font.render(sign["text"], True, color[:3])
            text_rect = text.get_rect(center=(sign["x"], sign["y"]))
            self.screen.blit(text, text_rect)
    
    def draw_player(self):
        # Perspective scaling (closer = bigger)
        scale = 1.2
        player_height = 80 * scale
        player_width = 40 * scale
        
        # Calculate perspective position (feet at bottom)
        perspective_y = 700 - (700 - self.player.y) * 0.8
        
        # Draw player shadow
        shadow_surf = pygame.Surface((player_width, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 100), (0, 0, player_width, 8))
        self.screen.blit(shadow_surf, (self.player.x - player_width//2, perspective_y + 5))
        
        # Get player sprite
        sprite = self.player.get_current_sprite()
        if sprite:
            # Scale sprite
            scaled_sprite = pygame.transform.scale(sprite, (int(player_width), int(player_height)))
            self.screen.blit(scaled_sprite, (self.player.x - player_width//2, perspective_y - player_height))
        else:
            # Fallback: Draw a simple character if no sprite
            pygame.draw.rect(self.screen, (200, 100, 255), 
                           (self.player.x - player_width//2, perspective_y - player_height, 
                            player_width, player_height), border_radius=10)
            pygame.draw.circle(self.screen, (255, 200, 200), 
                             (self.player.x, perspective_y - player_height + 20), 15)
        
        # Draw glow effect
        glow_surf = pygame.Surface((player_width + 40, player_height + 40), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (255, 100, 200, 20), (0, 0, player_width + 40, player_height + 40))
        self.screen.blit(glow_surf, (self.player.x - (player_width + 40)//2, perspective_y - player_height - 20))
    
    def draw_pause_button(self):
        # Pause button with glow
        pygame.draw.circle(self.screen, (200, 50, 150), (50, 50), 28)
        pygame.draw.circle(self.screen, (255, 100, 200), (50, 50), 25)
        pygame.draw.circle(self.screen, (255, 255, 255), (50, 50), 25, 2)
        # Pause icon
        pygame.draw.rect(self.screen, (255, 255, 255), (40, 40, 5, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (55, 40, 5, 20))