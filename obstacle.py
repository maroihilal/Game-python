import pygame
import random
import math

class ObstacleManager:
    def __init__(self, road):
        self.road = road
        self.obstacles = []
        self.spawn_timer = 0
        self.min_spacing = 200  
        self.obstacle_types = [
            {"name": "crate", "width": 40, "height": 40, "color": (139, 69, 19)},
            {"name": "barrier", "width": 60, "height": 30, "color": (200, 50, 50)},
            {"name": "cone", "width": 30, "height": 40, "color": (255, 150, 0)},
            {"name": "car", "width": 80, "height": 45, "color": (50, 50, 200)},
        ]
        
    def reset(self):
        self.obstacles = []
        self.spawn_timer = 0
    
    def update(self, speed, difficulty, player_x, player_y, player_sliding):
        self.spawn_timer += 1
        spawn_rate = max(30, 80 - difficulty * 5)
        if self.spawn_timer >= spawn_rate:
            self.spawn_timer = 0
            if random.random() < 0.4 + difficulty * 0.05:
                self.spawn_obstacle(difficulty)
        for obstacle in self.obstacles[:]:
            obstacle["y"] += speed * 2
            if obstacle["y"] > self.road.end_y + 100:
                self.obstacles.remove(obstacle)
                continue
            if self.check_collision(obstacle, player_x, player_y, player_sliding):
                return True
        return False
    
    def spawn_obstacle(self, difficulty):
        lane = random.randint(0, self.road.lane_count - 1)
        for obs in self.obstacles:
            if obs["lane"] == lane and obs["y"] < 300:
                return  
        available_types = self.obstacle_types[:min(3 + int(difficulty // 2), len(self.obstacle_types))]
        obstacle_type = random.choice(available_types)

        y = -50 - random.randint(0, 50)

        x = self.road.get_lane_x(lane, y)
        
        self.obstacles.append({
            "x": x,
            "y": y,
            "lane": lane,
            "type": obstacle_type,
            "width": obstacle_type["width"],
            "height": obstacle_type["height"],
            "color": obstacle_type["color"],
            "rotation": 0,
            "scale": 1.0
        })
    
    def check_collision(self, obstacle, player_x, player_y, player_sliding):
        y = obstacle["y"]

        if y < self.road.start_y or y > self.road.end_y:
            return False
        
        lane = obstacle["lane"]
        obs_x = self.road.get_lane_x(lane, y)
        
        progress = (y - self.road.start_y) / (self.road.end_y - self.road.start_y)
        scale = 0.5 + progress * 0.5
        
        obs_width = obstacle["width"] * scale
        obs_height = obstacle["height"] * scale

        player_scale = 1.0
        player_width = 40 * player_scale
        player_height = 80 * player_scale if not player_sliding else 40 * player_scale
        

        player_y_pos = 700 - (700 - player_y) * 0.8
        player_x_pos = player_x

        obs_rect = pygame.Rect(
            obs_x - obs_width // 2,
            y - obs_height // 2,
            obs_width,
            obs_height
        )
        
        player_rect = pygame.Rect(
            player_x_pos - player_width // 2,
            player_y_pos - player_height,
            player_width,
            player_height
        )
        obs_rect.inflate_ip(-10, -10)
        player_rect.inflate_ip(-10, -10)
        
        return obs_rect.colliderect(player_rect)
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            y = obstacle["y"]

            if y < self.road.start_y - 50 or y > self.road.end_y + 50:
                continue
            

            progress = (y - self.road.start_y) / (self.road.end_y - self.road.start_y)
            progress = max(0, min(1, progress))
            scale = 0.5 + progress * 0.5
            
            lane = obstacle["lane"]
            x = self.road.get_lane_x(lane, y)
            

            width = obstacle["width"] * scale
            height = obstacle["height"] * scale
            color = obstacle["color"]
            

            shadow_surf = pygame.Surface((width, 10), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surf, (0, 0, 0, 80), (0, 0, width, 10))
            screen.blit(shadow_surf, (x - width//2, y + height//2))
            
            glow_surf = pygame.Surface((width + 30, height + 30), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*color[:3], 30), (15, 15, width, height), border_radius=10)
            screen.blit(glow_surf, (x - width//2 - 15, y - height//2 - 15))
            
            pygame.draw.rect(screen, color, 
                           (x - width//2, y - height//2, width, height), 
                           border_radius=5)
            
            pygame.draw.rect(screen, (255, 100, 200), 
                           (x - width//2, y - height//2, width, height), 
                           2, border_radius=5)
            if obstacle["type"]["name"] == "crate":

                pygame.draw.line(screen, (100, 50, 20), 
                               (x - width//2 + 5, y), 
                               (x + width//2 - 5, y), 2)
                pygame.draw.line(screen, (100, 50, 20), 
                               (x, y - height//2 + 5), 
                               (x, y + height//2 - 5), 2)
            
            elif obstacle["type"]["name"] == "cone":

                stripe_y1 = y - height//4
                stripe_y2 = y + height//4
                pygame.draw.rect(screen, (255, 255, 255), 
                               (x - width//4, stripe_y1, width//2, 5))
                pygame.draw.rect(screen, (255, 255, 255), 
                               (x - width//3, stripe_y2, width//1.5, 5))
            
            elif obstacle["type"]["name"] == "car":
                pygame.draw.rect(screen, (150, 200, 255), 
                               (x - width//4, y - height//3, width//3, height//3))

                pygame.draw.circle(screen, (30, 30, 30), 
                                 (int(x - width//3), int(y + height//3)), int(width//8))
                pygame.draw.circle(screen, (30, 30, 30), 
                                 (int(x + width//3), int(y + height//3)), int(width//8))