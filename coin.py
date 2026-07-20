import pygame
import math
import random

class CoinManager:
    def __init__(self, road):
        self.road = road
        self.coins = []
        self.spawn_timer = 0
    def reset(self):
        self.coins = []
        self.spawn_timer = 0
    def update(self, speed, difficulty, player_x, player_y):
        """Update coins and check collection"""
        self.spawn_timer += 1
        spawn_rate = max(20, 50 - difficulty * 3)
        if self.spawn_timer >= spawn_rate:
            self.spawn_timer = 0
            if random.random() < 0.5:
                self.spawn_coins(difficulty)
        coins_collected = 0
        for coin in self.coins[:]:
            coin["y"] += speed * 2
            coin["rotation"] += 0.08
            if self.check_collection(coin, player_x, player_y):
                self.coins.remove(coin)
                coins_collected += 1
                continue
            if coin["y"] > self.road.end_y + 50:
                self.coins.remove(coin)
        return coins_collected

    def spawn_coins(self, difficulty):
        patterns = ["line", "zigzag", "arc", "lane_switch"]
        pattern = random.choice(patterns)
        start_lane = random.randint(0, self.road.lane_count - 1)
        count = random.randint(3, 6 + int(difficulty // 2))
        start_y = -50 - random.randint(0, 100)
        if pattern == "line":
            for i in range(count):
                self.coins.append({
                    "lane": start_lane,
                    "x": self.road.get_lane_x(start_lane, start_y + i * 60),
                    "y": start_y + i * 60,
                    "rotation": random.uniform(0, math.pi * 2),
                    "value": 1})
        
        elif pattern == "zigzag":
            for i in range(count):
                lane = (start_lane + (i % 2)) % self.road.lane_count
                y_pos = start_y + i * 55
                self.coins.append({
                    "lane": lane,
                    "x": self.road.get_lane_x(lane, y_pos),
                    "y": y_pos,
                    "rotation": random.uniform(0, math.pi * 2),
                    "value": 1
                })

        elif pattern == "arc":
            for i in range(count):
                progress = i / count
                angle = progress * math.pi
                offset = math.sin(angle) * 80
                lane = start_lane
                y_pos = start_y + i * 50
                x_pos = self.road.get_lane_x(lane, y_pos) + offset
                left_bound, right_bound = self.road.get_road_bounds(y_pos)
                x_pos = max(left_bound + 20, min(right_bound - 20, x_pos))
                
                self.coins.append({
                    "lane": lane,
                    "x": x_pos,
                    "y": y_pos,
                    "rotation": random.uniform(0, math.pi * 2),
                    "value": 1
                })
        elif pattern == "lane_switch":
            for i in range(count):
                lane = start_lane if i < count // 2 else (start_lane + 1) % self.road.lane_count
                y_pos = start_y + i * 50
                self.coins.append({
                    "lane": lane,
                    "x": self.road.get_lane_x(lane, y_pos),
                    "y": y_pos,
                    "rotation": random.uniform(0, math.pi * 2),
                    "value": 1
                })
    def check_collection(self, coin, player_x, player_y):
        y = coin["y"]

        if y < self.road.start_y or y > self.road.end_y:
            return False
        progress = (y - self.road.start_y) / (self.road.end_y - self.road.start_y)
        scale = 0.5 + progress * 0.5

        x = coin["x"]
        coin_radius = 15 * scale

        player_scale = 1.0
        player_width = 40 * player_scale
        player_height = 80 * player_scale
        
        player_y_pos = 700 - (700 - player_y) * 0.8
        player_x_pos = player_x

        distance = math.sqrt((player_x_pos - x)**2 + (player_y_pos - y)**2)
        return distance < (30 + coin_radius)
    
    def draw(self, screen):

        for coin in self.coins:
            y = coin["y"]

            if y < self.road.start_y - 20 or y > self.road.end_y + 20:
                continue
            
            progress = (y - self.road.start_y) / (self.road.end_y - self.road.start_y)
            progress = max(0, min(1, progress))
            scale = 0.5 + progress * 0.5
            x = coin["x"]
            radius = 15 * scale
            rotation = coin["rotation"]
            glow_surf = pygame.Surface((radius * 6, radius * 6), pygame.SRCALPHA)
            for i in range(3, 0, -1):
                alpha = 20 * i
                r = radius * (1 + i * 0.5)
                pygame.draw.circle(glow_surf, (255, 215, 0, alpha), 
                                 (radius * 3, radius * 3), r)
            screen.blit(glow_surf, (x - radius * 3, y - radius * 3))
            
            scale_x = abs(math.cos(rotation))
            if scale_x > 0.1:
                
                pygame.draw.ellipse(screen, (255, 215, 0),
                                   (x - radius * scale_x, y - radius,
                                    radius * 2 * scale_x, radius * 2), 2)
                
                inner_radius = radius * 0.6
                pygame.draw.circle(screen, (255, 215, 0), (int(x), int(y)), int(inner_radius))
                
                pygame.draw.circle(screen, (255, 255, 200), 
                                 (int(x), int(y)), int(inner_radius * 0.7))
                
                sparkle_x = x + radius * 0.4 * math.cos(rotation * 2)
                sparkle_y = y + radius * 0.4 * math.sin(rotation * 2)
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (int(sparkle_x), int(sparkle_y)), int(radius * 0.15))

                font = pygame.font.Font(None, int(radius * 1.2))
                text = font.render("1", True, (255, 215, 0))
                text_rect = text.get_rect(center=(int(x), int(y)))
                screen.blit(text, text_rect)